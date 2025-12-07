// Verlet Integration Compute Shader
// verlet_compute.glsl

#version 430 core

layout (local_size_x = 256) in;

struct Particle {
    vec4 position;  // xyz + mass
    vec4 velocity;  // xyz + type
    vec4 acceleration; // xyz + padding
};

layout(std430, binding = 0) buffer ParticleBuffer {
    Particle particles[];
};

uniform float dt;
uniform int numParticles;

void main() {
    uint i = gl_GlobalInvocationID.x;
    if (i >= numParticles) return;
    
    vec3 pos = particles[i].position.xyz;
    vec3 vel = particles[i].velocity.xyz;
    vec3 acc = particles[i].acceleration.xyz;
    
    // Verlet integration
    pos += vel * dt + 0.5 * acc * dt * dt;
    vel += acc * dt;
    
    particles[i].position.xyz = pos;
    particles[i].velocity.xyz = vel;
}
