#include "physics_engine.h"
#include <cmath>
#include <limits>
#include <algorithm>

namespace stellarforge {

// Helper function to determine which octant a point belongs to
static int get_octant(const std::array<float, 3>& point, const std::array<float, 3>& center) {
    int octant = 0;
    if (point[0] >= center[0]) octant |= 4;
    if (point[1] >= center[1]) octant |= 2;
    if (point[2] >= center[2]) octant |= 1;
    return octant;
}

// Get center of child octant
static std::array<float, 3> get_octant_center(const std::array<float, 3>& parent_center,
                                               float parent_size, int octant) {
    float half_size = parent_size * 0.25f;
    return {
        parent_center[0] + ((octant & 4) ? half_size : -half_size),
        parent_center[1] + ((octant & 2) ? half_size : -half_size),
        parent_center[2] + ((octant & 1) ? half_size : -half_size)
    };
}

std::unique_ptr<OctreeNode> PhysicsEngine::build_octree() {
    if (particles_.size() == 0) return nullptr;
    
    // Find bounding box
    std::array<float, 3> min_bounds = {
        std::numeric_limits<float>::max(),
        std::numeric_limits<float>::max(),
        std::numeric_limits<float>::max()
    };
    std::array<float, 3> max_bounds = {
        std::numeric_limits<float>::lowest(),
        std::numeric_limits<float>::lowest(),
        std::numeric_limits<float>::lowest()
    };
    
    for (const auto& pos : particles_.positions) {
        for (int i = 0; i < 3; ++i) {
            min_bounds[i] = std::min(min_bounds[i], pos[i]);
            max_bounds[i] = std::max(max_bounds[i], pos[i]);
        }
    }
    
    // Calculate center and size of root node
    std::array<float, 3> center;
    float size = 0.0f;
    for (int i = 0; i < 3; ++i) {
        center[i] = (min_bounds[i] + max_bounds[i]) * 0.5f;
        size = std::max(size, max_bounds[i] - min_bounds[i]);
    }
    size *= 1.1f;  // Add 10% padding
    
    // Create root node
    auto root = std::make_unique<OctreeNode>(center, size);
    
    // Insert all particles
    for (size_t i = 0; i < particles_.size(); ++i) {
        insert_particle_into_tree(root.get(), i);
    }
    
    return root;
}

void PhysicsEngine::insert_particle_into_tree(OctreeNode* node, size_t particle_idx) {
    // If node is empty, make it a leaf with this particle
    if (node->is_empty()) {
        node->particle_index = particle_idx;
        return;
    }
    
    // If node is a leaf with one particle, subdivide
    if (node->is_leaf()) {
        int old_particle_idx = node->particle_index;
        node->particle_index = -1;  // Convert to internal node
        
        // Create children and reinsert old particle
        int octant = get_octant(particles_.positions[old_particle_idx], node->center);
        if (!node->children[octant]) {
            node->children[octant] = std::make_unique<OctreeNode>(
                get_octant_center(node->center, node->size, octant),
                node->size * 0.5f
            );
        }
        insert_particle_into_tree(node->children[octant].get(), old_particle_idx);
    }
    
    // Insert new particle into appropriate child
    int octant = get_octant(particles_.positions[particle_idx], node->center);
    if (!node->children[octant]) {
        node->children[octant] = std::make_unique<OctreeNode>(
            get_octant_center(node->center, node->size, octant),
            node->size * 0.5f
        );
    }
    insert_particle_into_tree(node->children[octant].get(), particle_idx);
}

void PhysicsEngine::compute_node_mass_distribution(OctreeNode* node) {
    if (!node) return;
    
    if (node->is_leaf()) {
        // Leaf node: use particle's mass and position
        int idx = node->particle_index;
        node->total_mass = particles_.masses[idx];
        node->center_of_mass = particles_.positions[idx];
    } else {
        // Internal node: sum of children
        node->total_mass = 0.0f;
        std::array<float, 3> weighted_sum = {0.0f, 0.0f, 0.0f};
        
        for (int i = 0; i < 8; ++i) {
            if (node->children[i]) {
                compute_node_mass_distribution(node->children[i].get());
                
                float child_mass = node->children[i]->total_mass;
                node->total_mass += child_mass;
                
                for (int j = 0; j < 3; ++j) {
                    weighted_sum[j] += node->children[i]->center_of_mass[j] * child_mass;
                }
            }
        }
        
        if (node->total_mass > 0.0f) {
            for (int j = 0; j < 3; ++j) {
                node->center_of_mass[j] = weighted_sum[j] / node->total_mass;
            }
        }
    }
}

void PhysicsEngine::compute_acceleration_from_tree(size_t particle_idx,
                                                   const OctreeNode* node,
                                                   std::array<float, 3>& acceleration) {
    if (!node || node->is_empty()) return;
    
    // Calculate distance to node's center of mass
    float dx = node->center_of_mass[0] - particles_.positions[particle_idx][0];
    float dy = node->center_of_mass[1] - particles_.positions[particle_idx][1];
    float dz = node->center_of_mass[2] - particles_.positions[particle_idx][2];
    float dist2 = dx*dx + dy*dy + dz*dz + softening_ * softening_;
    float dist = std::sqrt(dist2);
    
    // Barnes-Hut criterion: s/d < theta
    float s = node->size;
    if (node->is_leaf() || (s / dist < theta_)) {
        // Node is far enough or is a leaf: use as single mass
        if (node->is_leaf() && node->particle_index == static_cast<int>(particle_idx)) {
            // Don't compute self-interaction
            return;
        }
        
        // F = G * m1 * m2 / r^2, a = F / m1 = G * m2 / r^2
        float factor = G_ * node->total_mass / (dist2 * dist);  // div by dist^3 for direction
        
        acceleration[0] += factor * dx;
        acceleration[1] += factor * dy;
        acceleration[2] += factor * dz;
    } else {
        // Node is too close: recurse into children
        for (int i = 0; i < 8; ++i) {
            if (node->children[i]) {
                compute_acceleration_from_tree(particle_idx, node->children[i].get(), acceleration);
            }
        }
    }
}

} // namespace stellarforge
