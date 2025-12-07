#pragma once

#include <vector>
#include <array>
#include <memory>

namespace stellarforge {

// Particle data structure (Structure of Arrays for performance)
struct ParticleSystem {
    std::vector<std::array<float, 3>> positions;   // x, y, z
    std::vector<std::array<float, 3>> velocities;  // vx, vy, vz
    std::vector<std::array<float, 3>> accelerations; // ax, ay, az
    std::vector<float> masses;
    std::vector<int> types;  // 0=star, 1=planet, 2=black_hole
    
    size_t size() const { return positions.size(); }
    
    void resize(size_t n) {
        positions.resize(n);
        velocities.resize(n);
        accelerations.resize(n);
        masses.resize(n);
        types.resize(n);
    }
    
    void clear() {
        positions.clear();
        velocities.clear();
        accelerations.clear();
        masses.clear();
        types.clear();
    }
};

// Octree node for Barnes-Hut algorithm
struct OctreeNode {
    std::array<float, 3> center;
    float size;
    std::array<float, 3> center_of_mass;
    float total_mass;
    int particle_index;  // -1 if internal node
    std::unique_ptr<OctreeNode> children[8];
    
    OctreeNode(const std::array<float, 3>& c, float s)
        : center(c), size(s), total_mass(0.0f), particle_index(-1) {
        center_of_mass = {0.0f, 0.0f, 0.0f};
    }
    
    bool is_leaf() const { return particle_index >= 0; }
    bool is_empty() const { return particle_index < 0 && total_mass == 0.0f; }
};

// Backend enumeration
enum class ComputeBackend {
    CPU_SINGLE_THREAD,
    CPU_OPENMP,
    CUDA,
    OPENGL_COMPUTE
};

// Main physics engine class
class PhysicsEngine {
public:
    PhysicsEngine();
    ~PhysicsEngine();
    
    // Initialization
    void initialize(size_t particle_count, ComputeBackend backend = ComputeBackend::CPU_OPENMP);
    void set_backend(ComputeBackend backend);
    ComputeBackend get_backend() const { return current_backend_; }
    
    // Particle management
    void set_positions(const float* positions, size_t count);
    void set_velocities(const float* velocities, size_t count);
    void set_masses(const float* masses, size_t count);
    void set_types(const int* types, size_t count);
    
    void get_positions(float* out_positions) const;
    void get_velocities(float* out_velocities) const;
    void get_masses(float* out_masses) const;
    void get_types(int* out_types) const;
    
    size_t get_particle_count() const { return particles_.size(); }
    
    // Add/remove particles
    void add_particle(const std::array<float, 3>& pos,
                     const std::array<float, 3>& vel,
                     float mass, int type);
    void remove_particle(size_t index);
    
    // Simulation step
    void step(float dt);
    void reset();
    
    // Physics parameters
    void set_gravitational_constant(float G) { G_ = G; }
    void set_softening_length(float epsilon) { softening_ = epsilon; }
    void set_theta(float theta) { theta_ = theta; }  // Barnes-Hut opening angle
    void enable_collisions(bool enable) { collisions_enabled_ = enable; }
    
    // Performance metrics
    double get_last_step_time_ms() const { return last_step_time_ms_; }
    
private:
    ParticleSystem particles_;
    ComputeBackend current_backend_;
    
    // Physics parameters
    float G_;            // Gravitational constant
    float softening_;    // Softening length for close encounters
    float theta_;        // Barnes-Hut theta parameter
    bool collisions_enabled_;
    
    // Performance tracking
    double last_step_time_ms_;
    
    // Backend-specific methods
    void step_cpu_single_thread(float dt);
    void step_cpu_openmp(float dt);
    void step_cuda(float dt);
    void step_opengl_compute(float dt);
    
    // Physics subroutines
    void compute_accelerations_barnes_hut();
    void compute_accelerations_direct();
    void integrate_verlet(float dt);
    void handle_collisions();
    
    // Barnes-Hut tree
    std::unique_ptr<OctreeNode> build_octree();
    void insert_particle_into_tree(OctreeNode* node, size_t particle_idx);
    void compute_node_mass_distribution(OctreeNode* node);
    void compute_acceleration_from_tree(size_t particle_idx, const OctreeNode* node,
                                       std::array<float, 3>& acceleration);
};

} // namespace stellarforge
