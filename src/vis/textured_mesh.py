"""
Custom textured mesh visual for VisPy with proper UV mapping.
"""

import numpy as np
from vispy import gloo
from vispy.visuals.visual import Visual
from vispy.scene.visuals import create_visual_node

# Vertex shader with UV coordinates
VERT_SHADER = """
attribute vec3 a_position;
attribute vec2 a_texcoord;
attribute vec3 a_normal;

varying vec2 v_texcoord;
varying vec3 v_normal;
varying vec3 v_position;

void main() {
    v_texcoord = a_texcoord;
    v_normal = a_normal;
    v_position = a_position;
    gl_Position = $transform(vec4(a_position, 1.0));
}
"""

# Fragment shader with texture sampling
FRAG_SHADER = """
uniform sampler2D u_texture;
uniform bool u_has_texture;
uniform vec4 u_base_color;

varying vec2 v_texcoord;
varying vec3 v_normal;
varying vec3 v_position;

void main() {
    if (u_has_texture) {
        vec4 tex_color = texture2D(u_texture, v_texcoord);
        // Simple lighting
        vec3 light_dir = normalize(vec3(1.0, 1.0, 1.0));
        float diffuse = max(dot(normalize(v_normal), light_dir), 0.3);
        gl_FragColor = vec4(tex_color.rgb * diffuse, tex_color.a);
    } else {
        // Fallback color
        vec3 light_dir = normalize(vec3(1.0, 1.0, 1.0));
        float diffuse = max(dot(normalize(v_normal), light_dir), 0.3);
        gl_FragColor = vec4(u_base_color.rgb * diffuse, u_base_color.a);
    }
}
"""


class TexturedMeshVisual(Visual):
    """
    Visual for rendering textured 3D meshes with proper UV mapping.
    """
    
    def __init__(self, vertices=None, faces=None, texture=None, uvs=None, 
                 vertex_colors=None, **kwargs):
        """
        Parameters
        ----------
        vertices : ndarray (N, 3)
            Vertex positions
        faces : ndarray (M, 3)
            Triangle face indices
        texture : ndarray (H, W, 3) or (H, W, 4)
            Texture image
        uvs : ndarray (N, 2)
            UV coordinates for each vertex
        vertex_colors : ndarray (N, 3) or (N, 4)
            Fallback vertex colors if no texture
        """
        Visual.__init__(self, vcode=VERT_SHADER, fcode=FRAG_SHADER)
        
        self._vertices = None
        self._faces = None
        self._texture = None
        self._uvs = None
        self._vertex_colors = vertex_colors
        self._has_texture = False
        
        # Create buffers
        self._vbo = gloo.VertexBuffer()
        self._uv_vbo = gloo.VertexBuffer()
        self._normal_vbo = gloo.VertexBuffer()
        self._index_buffer = gloo.IndexBuffer()
        
        # Create texture
        self._texture_obj = gloo.Texture2D(shape=(1, 1, 3), internalformat='rgb')
        
        # Set initial data
        if vertices is not None:
            self.set_data(vertices, faces, texture, uvs, vertex_colors)
        
        self.set_gl_state('translucent', depth_test=True, cull_face=False, blend=True)
        self._draw_mode = 'triangles'
    
    def set_data(self, vertices=None, faces=None, texture=None, uvs=None, vertex_colors=None):
        """Update mesh data."""
        if vertices is not None:
            self._vertices = np.asarray(vertices, dtype=np.float32)
            self._vbo.set_data(self._vertices)
        
        if faces is not None:
            self._faces = np.asarray(faces, dtype=np.uint32).ravel()
            self._index_buffer.set_data(self._faces)
        
        if uvs is not None and len(uvs) == len(self._vertices):
            self._uvs = np.asarray(uvs, dtype=np.float32)
            # Ensure UVs are in [0, 1]
            self._uvs = np.clip(self._uvs, 0.0, 1.0)
            self._uv_vbo.set_data(self._uvs)
        else:
            # Default UVs if none provided
            self._uvs = np.zeros((len(self._vertices), 2), dtype=np.float32)
            self._uv_vbo.set_data(self._uvs)
        
        if texture is not None:
            # Ensure texture is correct format
            texture = np.asarray(texture, dtype=np.float32)
            if texture.ndim == 2:
                texture = texture[:, :, np.newaxis].repeat(3, axis=2)
            if texture.shape[2] == 4:
                # RGBA -> RGB
                texture = texture[:, :, :3]
            
            # Ensure values in [0, 1]
            if texture.max() > 1.0:
                texture = texture / 255.0
            
            self._texture = texture
            self._texture_obj.set_data(texture)
            self._has_texture = True
        else:
            self._has_texture = False
        
        # Compute normals
        self._compute_normals()
        
        self.update()
    
    def _compute_normals(self):
        """Compute vertex normals from face data."""
        if self._vertices is None or self._faces is None:
            return
        
        # Initialize normals
        normals = np.zeros_like(self._vertices)
        
        # Reshape faces
        faces = self._faces.reshape(-1, 3)
        
        # Compute face normals and accumulate
        for face in faces:
            v0, v1, v2 = self._vertices[face]
            # Compute face normal
            normal = np.cross(v1 - v0, v2 - v0)
            norm_length = np.linalg.norm(normal)
            if norm_length > 0:
                normal = normal / norm_length
                # Accumulate to vertices
                normals[face[0]] += normal
                normals[face[1]] += normal
                normals[face[2]] += normal
        
        # Normalize vertex normals
        norms = np.linalg.norm(normals, axis=1, keepdims=True)
        norms[norms == 0] = 1  # Avoid division by zero
        normals = normals / norms
        
        self._normals = normals.astype(np.float32)
        self._normal_vbo.set_data(self._normals)
    
    def _prepare_draw(self, view=None):
        """Prepare for drawing."""
        if self._vertices is None or view is None:
            return False
        
        # Set attributes
        self.shared_program.vert['a_position'] = self._vbo
        self.shared_program.vert['a_texcoord'] = self._uv_vbo
        self.shared_program.vert['a_normal'] = self._normal_vbo
        
        # Set uniforms
        self.shared_program.frag['u_texture'] = self._texture_obj
        self.shared_program.frag['u_has_texture'] = self._has_texture
        
        # Base color fallback
        if self._vertex_colors is not None and len(self._vertex_colors) > 0:
            base_color = np.mean(self._vertex_colors[:10], axis=0)
            if len(base_color) == 3:
                base_color = np.append(base_color, 1.0)
        else:
            base_color = np.array([0.5, 0.5, 0.5, 1.0])
        
        self.shared_program.frag['u_base_color'] = base_color
    
    def _draw(self, view=None):
        """Draw the mesh."""
        if self._vertices is None:
            return
        
        gloo.draw_elements(gloo.gl.GL_TRIANGLES, self._index_buffer)


# Create scene visual node for easy use in scene graph
TexturedMesh = create_visual_node(TexturedMeshVisual)
