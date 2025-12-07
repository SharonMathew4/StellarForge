// OpenGL Compute Shader Physics (GLSL 4.3+)
// gravity_compute.glsl

#version 430 core

layout (local_size_x = 256) in;

// Particle data structures
struct Particle {
    vec4 position;  // xyz + mass
    vec4 velocity;  // xyz + type
    vec4 acceleration; // xyz + padding
};

// Shader storage buffer objects (SSBOs)
layout(std430, binding = 0) buffer ParticleBuffer {
    Particle particles[];
};

// Uniforms
uniform float G;            // Gravitational constant
uniform float softening;    // Softening length
uniform float dt;           // Time step
uniform int numParticles;

// Compute gravity acceleration for each particle
void main() {
    uint i = gl_GlobalInvocationID.x;
    if (i >= numParticles) return;
    
    vec3 pos_i = particles[i].position.xyz;
    float mass_i = particles[i].position.w;
    vec3 acc = vec3(0.0);
    
    // Compute acceleration from all other particles
    for (int j = 0; j < numParticles; j++) {
        if (i == j) continue;
        
        vec3 pos_j = particles[j].position.xyz;
        float mass_j = particles[j].position.w;
        
        vec3 r = pos_j - pos_i;
        float dist2 = dot(r, r) + softening * softening;
        float dist = sqrt(dist2);
        float dist3 = dist2 * dist;
        
        // a = G * m / r^2, direction = r / |r|
        acc += G * mass_j * r / dist3;
    }
    
    particles[i].acceleration.xyz = acc;
}
