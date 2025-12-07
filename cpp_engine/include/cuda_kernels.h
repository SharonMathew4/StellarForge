#pragma once

#ifdef USE_CUDA

#include <cuda_runtime.h>

namespace stellarforge {
namespace cuda {

// CUDA kernel for direct N-body gravity calculation
// This is simpler than Barnes-Hut but works well on GPU for moderate particle counts
__global__ void compute_gravity_kernel(
    const float3* positions,
    const float* masses,
    float3* accelerations,
    int num_particles,
    float G,
    float softening
);

// CUDA kernel for Barnes-Hut tree traversal (more complex, better for large N)
__global__ void compute_gravity_barnes_hut_kernel(
    const float3* positions,
    const float* masses,
    float3* accelerations,
    int num_particles,
    float G,
    float softening,
    float theta
);

// Collision detection using spatial hashing
__global__ void detect_collisions_kernel(
    const float3* positions,
    const float3* velocities,
    const float* masses,
    int* collision_pairs,
    int* num_collisions,
    int num_particles,
    float collision_radius
);

// Verlet integration kernel
__global__ void verlet_integrate_kernel(
    float3* positions,
    float3* velocities,
    const float3* accelerations,
    int num_particles,
    float dt
);

// Host functions to launch kernels
void launch_gravity_direct(
    const float* d_positions,
    const float* d_masses,
    float* d_accelerations,
    int num_particles,
    float G,
    float softening
);

void launch_verlet_integration(
    float* d_positions,
    float* d_velocities,
    const float* d_accelerations,
    int num_particles,
    float dt
);

// Helper to check CUDA errors
#define CUDA_CHECK(call) \
    do { \
        cudaError_t error = call; \
        if (error != cudaSuccess) { \
            fprintf(stderr, "CUDA error at %s:%d: %s\n", __FILE__, __LINE__, \
                    cudaGetErrorString(error)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

} // namespace cuda
} // namespace stellarforge

#endif // USE_CUDA
