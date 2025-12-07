#include "physics_engine.h"
#include <cmath>
#include <chrono>
#include <algorithm>
#include <iostream>

#ifdef USE_OPENMP
#include <omp.h>
#endif

namespace stellarforge {

PhysicsEngine::PhysicsEngine()
    : current_backend_(ComputeBackend::CPU_OPENMP),
      G_(1.0f),
      softening_(0.01f),
      theta_(0.5f),
      collisions_enabled_(false),
      last_step_time_ms_(0.0) {
}

PhysicsEngine::~PhysicsEngine() {
}

void PhysicsEngine::initialize(size_t particle_count, ComputeBackend backend) {
    particles_.resize(particle_count);
    current_backend_ = backend;
    
    // Initialize accelerations to zero
    for (size_t i = 0; i < particle_count; ++i) {
        particles_.accelerations[i] = {0.0f, 0.0f, 0.0f};
    }
    
    std::cout << "PhysicsEngine initialized with " << particle_count 
              << " particles using backend " << static_cast<int>(backend) << std::endl;
}

void PhysicsEngine::set_backend(ComputeBackend backend) {
    current_backend_ = backend;
}

void PhysicsEngine::set_positions(const float* positions, size_t count) {
    particles_.positions.resize(count);
    for (size_t i = 0; i < count; ++i) {
        particles_.positions[i] = {positions[i*3], positions[i*3+1], positions[i*3+2]};
    }
}

void PhysicsEngine::set_velocities(const float* velocities, size_t count) {
    particles_.velocities.resize(count);
    for (size_t i = 0; i < count; ++i) {
        particles_.velocities[i] = {velocities[i*3], velocities[i*3+1], velocities[i*3+2]};
    }
}

void PhysicsEngine::set_masses(const float* masses, size_t count) {
    particles_.masses.resize(count);
    for (size_t i = 0; i < count; ++i) {
        particles_.masses[i] = masses[i];
    }
}

void PhysicsEngine::set_types(const int* types, size_t count) {
    particles_.types.resize(count);
    for (size_t i = 0; i < count; ++i) {
        particles_.types[i] = types[i];
    }
}

void PhysicsEngine::get_positions(float* out_positions) const {
    for (size_t i = 0; i < particles_.size(); ++i) {
        out_positions[i*3] = particles_.positions[i][0];
        out_positions[i*3+1] = particles_.positions[i][1];
        out_positions[i*3+2] = particles_.positions[i][2];
    }
}

void PhysicsEngine::get_velocities(float* out_velocities) const {
    for (size_t i = 0; i < particles_.size(); ++i) {
        out_velocities[i*3] = particles_.velocities[i][0];
        out_velocities[i*3+1] = particles_.velocities[i][1];
        out_velocities[i*3+2] = particles_.velocities[i][2];
    }
}

void PhysicsEngine::get_masses(float* out_masses) const {
    for (size_t i = 0; i < particles_.size(); ++i) {
        out_masses[i] = particles_.masses[i];
    }
}

void PhysicsEngine::get_types(int* out_types) const {
    for (size_t i = 0; i < particles_.size(); ++i) {
        out_types[i] = particles_.types[i];
    }
}

void PhysicsEngine::add_particle(const std::array<float, 3>& pos,
                                 const std::array<float, 3>& vel,
                                 float mass, int type) {
    particles_.positions.push_back(pos);
    particles_.velocities.push_back(vel);
    particles_.accelerations.push_back({0.0f, 0.0f, 0.0f});
    particles_.masses.push_back(mass);
    particles_.types.push_back(type);
}

void PhysicsEngine::remove_particle(size_t index) {
    if (index >= particles_.size()) return;
    
    particles_.positions.erase(particles_.positions.begin() + index);
    particles_.velocities.erase(particles_.velocities.begin() + index);
    particles_.accelerations.erase(particles_.accelerations.begin() + index);
    particles_.masses.erase(particles_.masses.begin() + index);
    particles_.types.erase(particles_.types.begin() + index);
}

void PhysicsEngine::step(float dt) {
    auto start = std::chrono::high_resolution_clock::now();
    
    switch (current_backend_) {
        case ComputeBackend::CPU_SINGLE_THREAD:
            step_cpu_single_thread(dt);
            break;
        case ComputeBackend::CPU_OPENMP:
            step_cpu_openmp(dt);
            break;
        case ComputeBackend::CUDA:
#ifdef USE_CUDA
            step_cuda(dt);
#else
            std::cerr << "CUDA backend requested but not compiled. Falling back to CPU." << std::endl;
            step_cpu_openmp(dt);
#endif
            break;
        case ComputeBackend::OPENGL_COMPUTE:
#ifdef USE_OPENGL_COMPUTE
            step_opengl_compute(dt);
#else
            std::cerr << "OpenGL compute backend requested but not compiled. Falling back to CPU." << std::endl;
            step_cpu_openmp(dt);
#endif
            break;
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    last_step_time_ms_ = std::chrono::duration<double, std::milli>(end - start).count();
}

void PhysicsEngine::step_cpu_single_thread(float dt) {
    // 1. Compute accelerations using Barnes-Hut
    compute_accelerations_barnes_hut();
    
    // 2. Integrate using Verlet
    integrate_verlet(dt);
    
    // 3. Handle collisions if enabled
    if (collisions_enabled_) {
        handle_collisions();
    }
}

void PhysicsEngine::step_cpu_openmp(float dt) {
    // Same as single-threaded but with OpenMP parallelization
    compute_accelerations_barnes_hut();
    integrate_verlet(dt);
    
    if (collisions_enabled_) {
        handle_collisions();
    }
}

void PhysicsEngine::compute_accelerations_barnes_hut() {
    // Build octree
    auto tree = build_octree();
    if (!tree) return;
    
    // Compute mass distribution in tree
    compute_node_mass_distribution(tree.get());
    
    // Compute acceleration for each particle
#ifdef USE_OPENMP
    #pragma omp parallel for
#endif
    for (size_t i = 0; i < particles_.size(); ++i) {
        particles_.accelerations[i] = {0.0f, 0.0f, 0.0f};
        compute_acceleration_from_tree(i, tree.get(), particles_.accelerations[i]);
    }
}

void PhysicsEngine::integrate_verlet(float dt) {
    const float dt2 = dt * dt;
    
#ifdef USE_OPENMP
    #pragma omp parallel for
#endif
    for (size_t i = 0; i < particles_.size(); ++i) {
        // Verlet integration: x(t+dt) = x(t) + v(t)*dt + 0.5*a(t)*dt^2
        for (int j = 0; j < 3; ++j) {
            particles_.positions[i][j] += particles_.velocities[i][j] * dt 
                                        + 0.5f * particles_.accelerations[i][j] * dt2;
            particles_.velocities[i][j] += particles_.accelerations[i][j] * dt;
        }
    }
}

void PhysicsEngine::handle_collisions() {
    // Simple collision detection (will be replaced with spatial hashing)
    // For now, just merge particles that are very close
    const float collision_dist = softening_ * 2.0f;
    const float collision_dist2 = collision_dist * collision_dist;
    
    // Mark particles for removal
    std::vector<bool> removed(particles_.size(), false);
    
    for (size_t i = 0; i < particles_.size(); ++i) {
        if (removed[i]) continue;
        
        for (size_t j = i + 1; j < particles_.size(); ++j) {
            if (removed[j]) continue;
            
            float dx = particles_.positions[i][0] - particles_.positions[j][0];
            float dy = particles_.positions[i][1] - particles_.positions[j][1];
            float dz = particles_.positions[i][2] - particles_.positions[j][2];
            float dist2 = dx*dx + dy*dy + dz*dz;
            
            if (dist2 < collision_dist2) {
                // Perfectly inelastic collision: merge into particle i
                float total_mass = particles_.masses[i] + particles_.masses[j];
                
                // Conservation of momentum
                for (int k = 0; k < 3; ++k) {
                    particles_.velocities[i][k] = (particles_.velocities[i][k] * particles_.masses[i] +
                                                   particles_.velocities[j][k] * particles_.masses[j]) / total_mass;
                }
                
                particles_.masses[i] = total_mass;
                removed[j] = true;
            }
        }
    }
    
    // Remove marked particles (in reverse order to maintain indices)
    for (size_t i = particles_.size(); i-- > 0;) {
        if (removed[i]) {
            remove_particle(i);
        }
    }
}

// Barnes-Hut tree implementation will be in separate file
void PhysicsEngine::step_cuda(float dt) {
    // CUDA implementation - for now use OpenMP as fallback
    // Full CUDA kernel integration would require CUDA memory management
    step_cpu_openmp(dt);
}

void PhysicsEngine::step_opengl_compute(float dt) {
    // OpenGL compute implementation
    std::cerr << "OpenGL compute step not yet implemented" << std::endl;
}

void PhysicsEngine::reset() {
    // Reset all particles to initial state
    // Clear accelerations
    for (size_t i = 0; i < particles_.size(); ++i) {
        particles_.accelerations[i] = {0.0f, 0.0f, 0.0f};
    }
}

} // namespace stellarforge
