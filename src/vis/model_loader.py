"""
Model loader for 3D assets (GLB/GLTF).
Uses trimesh to load geometry and materials.
"""

import trimesh
import numpy as np
from typing import Tuple, Optional
from core.error_logger import get_error_logger, ErrorSeverity

class ModelLoader:
    """Handles loading of 3D mesh files."""
    
    def __init__(self):
        self.logger = get_error_logger()

    def load_mesh(self, file_path: str, simplify: bool = True) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray]]:
        """
        Load a mesh from file with texture extraction and optimization.
        
        Args:
            file_path: Path to the .glb or .gltf file
            simplify: Reduce vertex count for large meshes (Saturn rings, etc.)
            
        Returns:
            Tuple of (vertices, faces, colors, texture, uvs)
        """
        try:
            # Load with all metadata
            scene = trimesh.load(file_path, force='scene', process=False)
            
            # Merge all meshes in scene
            if isinstance(scene, trimesh.Scene):
                if len(scene.geometry) == 0:
                    raise ValueError("Scene contains no geometry")
                mesh = scene.dump(concatenate=True)
            else:
                mesh = scene

            # Simplify very large meshes (e.g., Saturn with rings has 202k vertices)
            if simplify and len(mesh.vertices) > 50000:
                target_count = 20000
                self.logger.log_error(
                    f"Simplifying mesh {file_path}: {len(mesh.vertices)} -> {target_count} vertices",
                    component="MODEL_LOADER",
                    severity=ErrorSeverity.INFO
                )
                mesh = mesh.simplify_mesh(target_count=target_count, aggressiveness=7.0)

            vertices = np.array(mesh.vertices, dtype=np.float32)
            faces = np.array(mesh.faces, dtype=np.int32)
            
            # Extract vertex colors
            colors = None
            if hasattr(mesh.visual, 'vertex_colors'):
                colors = np.array(mesh.visual.vertex_colors, dtype=np.float32) / 255.0
            
            # Extract texture from material
            texture = None
            uvs = None
            
            try:
                # Try to get texture from material
                if hasattr(mesh, 'visual') and hasattr(mesh.visual, 'material'):
                    material = mesh.visual.material
                    
                    # Check for image in material
                    if hasattr(material, 'image') and material.image is not None:
                        from PIL import Image
                        img = material.image
                        
                        # Convert to numpy array
                        if isinstance(img, Image.Image):
                            texture = np.array(img, dtype=np.float32)
                            if texture.max() > 1.0:
                                texture = texture / 255.0
                    
                    # Extract UV coordinates
                    if hasattr(mesh.visual, 'uv'):
                        uvs = np.array(mesh.visual.uv, dtype=np.float32)
            except Exception as texture_error:
                self.logger.log_error(
                    f"Could not extract texture from {file_path}: {str(texture_error)}",
                    component="MODEL_LOADER",
                    severity=ErrorSeverity.DEBUG
                )

            self.logger.log_error(
                f"Loaded mesh {file_path}: {len(vertices)} vertices, Texture: {texture is not None}",
                component="MODEL_LOADER",
                severity=ErrorSeverity.INFO
            )
            
            return vertices, faces, colors, texture, uvs

        except Exception as e:
            self.logger.log_exception(
                e,
                component="MODEL_LOADER",
                severity=ErrorSeverity.ERROR,
                context={'file': file_path}
            )
            return (np.zeros((0, 3), dtype=np.float32), 
                    np.zeros((0, 3), dtype=np.int32), 
                    None, None, None)
