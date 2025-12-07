#include "cuda_kernels.h"
#include <cstdio>

namespace stellarforge {
namespace cuda {

// Direct N-body gravity calculation (O(N^2) but highly parallel)
__global__ void compute_gravity_kernel(
    const float3* positions,
    const float* masses,
    float3* accelerations,
    int num_particles,
    float G,
    float softening
) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= num_particles) return;
    
    float3 acc = make_float3(0.0f, 0.0f, 0.0f);
    float3 pos_i = positions[i];
    
    // Compute acceleration from all other particles
    for (int j = 0; j < num_particles; ++j) {
        if (i == j) continue;
        
        float3 pos_j = positions[j];
        float dx = pos_j.x - pos_i.x;
        float dy = pos_j.y - pos_i.y;
        float dz = pos_j.z - pos_i.z;
        
        float dist2 = dx*dx + dy*dy + dz*dz + softening*softening;
        float dist = sqrtf(dist2);
        float dist3 = dist2 * dist;
        
        // a = G * m / r^2, direction = (pos_j - pos_i) / r
        float factor = G * masses[j] / dist3;
        
        acc.x += factor * dx;
        acc.y += factor * dy;
        acc.z += factor * dz;
    }
    
    accelerations[i] = acc;
}

// Optimized version using shared memory for better performance
__global__ void compute_gravity_shared_kernel(
    const float3* positions,
    const float* masses,
    float3* accelerations,
    int num_particles,
    float G,
    float softening
) {
    extern __shared__ float3 shared_pos[];
    __shared__ float shared_mass[256];  // Adjust based on block size
    
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    float3 acc = make_float3(0.0f, 0.0f, 0.0f);
    
    if (i < num_particles) {
        float3 pos_i = positions[i];
        
        // Process particles in tiles
        for (int tile = 0; tile < (num_particles + blockDim.x - 1) / blockDim.x; ++tile) {
            int j = tile * blockDim.x + threadIdx.x;
            
            // Load tile into shared memory
            if (j < num_particles) {
                shared_pos[threadIdx.x] = positions[j];
                shared_mass[threadIdx.x] = masses[j];
            }
            __syncthreads();
            
            // Compute interactions with particles in this tile
            int tile_size = min(blockDim.x, num_particles - tile * blockDim.x);
            for (int k = 0; k < tile_size; ++k) {
                int j_global = tile * blockDim.x + k;
                if (i == j_global) continue;
                
                float dx = shared_pos[k].x - pos_i.x;
                float dy = shared_pos[k].y - pos_i.y;
                float dz = shared_pos[k].z - pos_i.z;
                
                float dist2 = dx*dx + dy*dy + dz*dz + softening*softening;
                float dist = sqrtf(dist2);
                float dist3 = dist2 * dist;
                
                float factor = G * shared_mass[k] / dist3;
                
                acc.x += factor * dx;
                acc.y += factor * dy;
                acc.z += factor * dz;
            }
            __syncthreads();
        }
        
        accelerations[i] = acc;
    }
}

// Verlet integration on GPU
__global__ void verlet_integrate_kernel(
    float3* positions,
    float3* velocities,
    const float3* accelerations,
    int num_particles,
    float dt
) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= num_particles) return;
    
    float dt2 = dt * dt;
    
    // Verlet: x(t+dt) = x(t) + v(t)*dt + 0.5*a(t)*dt^2
    positions[i].x += velocities[i].x * dt + 0.5f * accelerations[i].x * dt2;
    positions[i].y += velocities[i].y * dt + 0.5f * accelerations[i].y * dt2;
    positions[i].z += velocities[i].z * dt + 0.5f * accelerations[i].z * dt2;
    
    // Update velocity: v(t+dt) = v(t) + a(t)*dt
    velocities[i].x += accelerations[i].x * dt;
    velocities[i].y += accelerations[i].y * dt;
    velocities[i].z += accelerations[i].z * dt;
}

// Collision detection using spatial hashing (simplified)
__global__ void detect_collisions_kernel(
    const float3* positions,
    const float3* velocities,
    const float* masses,
    int* collision_pairs,
    int* num_collisions,
    int num_particles,
    float collision_radius
) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= num_particles) return;
    
    float3 pos_i = positions[i];
    float radius2 = collision_radius * collision_radius;
    
    for (int j = i + 1; j < num_particles; ++j) {
        float3 pos_j = positions[j];
        
        float dx = pos_j.x - pos_i.x;
        float dy = pos_j.y - pos_i.y;
        float dz = pos_j.z - pos_i.z;
        float dist2 = dx*dx + dy*dy + dz*dz;
        
        if (dist2 < radius2) {
            // Collision detected - store pair
            int idx = atomicAdd(num_collisions, 1);
            if (idx < num_particles) {  // Prevent overflow
                collision_pairs[idx * 2] = i;
                collision_pairs[idx * 2 + 1] = j;
            }
        }
    }
}

// Host functions to launch kernels
void launch_gravity_direct(
    const float* d_positions,
    const float* d_masses,
    float* d_accelerations,
    int num_particles,
    float G,
    float softening
) {
    int block_size = 256;
    int num_blocks = (num_particles + block_size - 1) / block_size;
    
    // Use shared memory version for better performance
    size_t shared_mem_size = block_size * (sizeof(float3) + sizeof(float));
    
    compute_gravity_shared_kernel<<<num_blocks, block_size, shared_mem_size>>>(
        reinterpret_cast<const float3*>(d_positions),
        d_masses,
        reinterpret_cast<float3*>(d_accelerations),
        num_particles,
        G,
        softening
    );
    
    CUDA_CHECK(cudaGetLastError());
}

void launch_verlet_integration(
    float* d_positions,
    float* d_velocities,
    const float* d_accelerations,
    int num_particles,
    float dt
) {
    int block_size = 256;
    int num_blocks = (num_particles + block_size - 1) / block_size;
    
    verlet_integrate_kernel<<<num_blocks, block_size>>>(
        reinterpret_cast<float3*>(d_positions),
        reinterpret_cast<float3*>(d_velocities),
        reinterpret_cast<const float3*>(d_accelerations),
        num_particles,
        dt
    );
    
    CUDA_CHECK(cudaGetLastError());
}

} // namespace cuda
} // namespace stellarforge
