#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include "physics_engine.h"

namespace py = pybind11;

namespace stellarforge {

// Wrapper class to handle NumPy array interfacing
class PhysicsEnginePython {
public:
    PhysicsEnginePython() : engine_() {}
    
    void initialize(size_t particle_count, const std::string& backend = "openmp") {
        ComputeBackend backend_enum;
        if (backend == "single") {
            backend_enum = ComputeBackend::CPU_SINGLE_THREAD;
        } else if (backend == "openmp") {
            backend_enum = ComputeBackend::CPU_OPENMP;
        } else if (backend == "cuda") {
            backend_enum = ComputeBackend::CUDA;
        } else if (backend == "opengl") {
            backend_enum = ComputeBackend::OPENGL_COMPUTE;
        } else {
            throw std::runtime_error("Unknown backend: " + backend);
        }
        
        engine_.initialize(particle_count, backend_enum);
    }
    
    void set_positions(py::array_t<float> positions) {
        auto buf = positions.request();
        if (buf.ndim != 2 || buf.shape[1] != 3) {
            throw std::runtime_error("Positions must be (N, 3) array");
        }
        
        size_t count = buf.shape[0];
        float* ptr = static_cast<float*>(buf.ptr);
        engine_.set_positions(ptr, count);
    }
    
    void set_velocities(py::array_t<float> velocities) {
        auto buf = velocities.request();
        if (buf.ndim != 2 || buf.shape[1] != 3) {
            throw std::runtime_error("Velocities must be (N, 3) array");
        }
        
        size_t count = buf.shape[0];
        float* ptr = static_cast<float*>(buf.ptr);
        engine_.set_velocities(ptr, count);
    }
    
    void set_masses(py::array_t<float> masses) {
        auto buf = masses.request();
        if (buf.ndim != 1) {
            throw std::runtime_error("Masses must be (N,) array");
        }
        
        size_t count = buf.shape[0];
        float* ptr = static_cast<float*>(buf.ptr);
        engine_.set_masses(ptr, count);
    }
    
    void set_types(py::array_t<int> types) {
        auto buf = types.request();
        if (buf.ndim != 1) {
            throw std::runtime_error("Types must be (N,) array");
        }
        
        size_t count = buf.shape[0];
        int* ptr = static_cast<int*>(buf.ptr);
        engine_.set_types(ptr, count);
    }
    
    py::array_t<float> get_positions() {
        size_t count = engine_.get_particle_count();
        auto result = py::array_t<float>(std::vector<py::ssize_t>{static_cast<py::ssize_t>(count), 3});
        auto buf = result.request();
        float* ptr = static_cast<float*>(buf.ptr);
        engine_.get_positions(ptr);
        return result;
    }
    
    py::array_t<float> get_velocities() {
        size_t count = engine_.get_particle_count();
        auto result = py::array_t<float>(std::vector<py::ssize_t>{static_cast<py::ssize_t>(count), 3});
        auto buf = result.request();
        float* ptr = static_cast<float*>(buf.ptr);
        engine_.get_velocities(ptr);
        return result;
    }
    
    py::array_t<float> get_masses() {
        size_t count = engine_.get_particle_count();
        auto result = py::array_t<float>(count);
        auto buf = result.request();
        float* ptr = static_cast<float*>(buf.ptr);
        engine_.get_masses(ptr);
        return result;
    }
    
    py::array_t<int> get_types() {
        size_t count = engine_.get_particle_count();
        auto result = py::array_t<int>(count);
        auto buf = result.request();
        int* ptr = static_cast<int*>(buf.ptr);
        engine_.get_types(ptr);
        return result;
    }
    
    size_t get_particle_count() const {
        return engine_.get_particle_count();
    }
    
    void add_particle(py::array_t<float> pos, py::array_t<float> vel, float mass, int type) {
        auto pos_buf = pos.request();
        auto vel_buf = vel.request();
        
        if (pos_buf.size != 3 || vel_buf.size != 3) {
            throw std::runtime_error("Position and velocity must be size 3");
        }
        
        float* pos_ptr = static_cast<float*>(pos_buf.ptr);
        float* vel_ptr = static_cast<float*>(vel_buf.ptr);
        
        std::array<float, 3> pos_arr = {pos_ptr[0], pos_ptr[1], pos_ptr[2]};
        std::array<float, 3> vel_arr = {vel_ptr[0], vel_ptr[1], vel_ptr[2]};
        
        engine_.add_particle(pos_arr, vel_arr, mass, type);
    }
    
    void remove_particle(size_t index) {
        engine_.remove_particle(index);
    }
    
    void step(float dt) {
        engine_.step(dt);
    }
    
    void reset() {
        engine_.reset();
    }
    
    void set_gravitational_constant(float G) {
        engine_.set_gravitational_constant(G);
    }
    
    void set_softening_length(float epsilon) {
        engine_.set_softening_length(epsilon);
    }
    
    void set_theta(float theta) {
        engine_.set_theta(theta);
    }
    
    void enable_collisions(bool enable) {
        engine_.enable_collisions(enable);
    }
    
    std::string get_backend() const {
        switch (engine_.get_backend()) {
            case ComputeBackend::CPU_SINGLE_THREAD: return "single";
            case ComputeBackend::CPU_OPENMP: return "openmp";
            case ComputeBackend::CUDA: return "cuda";
            case ComputeBackend::OPENGL_COMPUTE: return "opengl";
            default: return "unknown";
        }
    }
    
    void set_backend(const std::string& backend) {
        ComputeBackend backend_enum;
        if (backend == "single") {
            backend_enum = ComputeBackend::CPU_SINGLE_THREAD;
        } else if (backend == "openmp") {
            backend_enum = ComputeBackend::CPU_OPENMP;
        } else if (backend == "cuda") {
            backend_enum = ComputeBackend::CUDA;
        } else if (backend == "opengl") {
            backend_enum = ComputeBackend::OPENGL_COMPUTE;
        } else {
            throw std::runtime_error("Unknown backend: " + backend);
        }
        engine_.set_backend(backend_enum);
    }
    
    double get_last_step_time_ms() const {
        return engine_.get_last_step_time_ms();
    }
    
private:
    PhysicsEngine engine_;
};

} // namespace stellarforge

PYBIND11_MODULE(stellarforge_cpp_engine, m) {
    m.doc() = "StellarForge C++ Physics Engine with CUDA and OpenGL compute support";
    
    py::class_<stellarforge::PhysicsEnginePython>(m, "PhysicsEngine")
        .def(py::init<>())
        .def("initialize", &stellarforge::PhysicsEnginePython::initialize,
             py::arg("particle_count"), py::arg("backend") = "openmp",
             "Initialize the physics engine with a given number of particles")
        .def("set_positions", &stellarforge::PhysicsEnginePython::set_positions,
             "Set particle positions (N, 3) array")
        .def("set_velocities", &stellarforge::PhysicsEnginePython::set_velocities,
             "Set particle velocities (N, 3) array")
        .def("set_masses", &stellarforge::PhysicsEnginePython::set_masses,
             "Set particle masses (N,) array")
        .def("set_types", &stellarforge::PhysicsEnginePython::set_types,
             "Set particle types (N,) array")
        .def("get_positions", &stellarforge::PhysicsEnginePython::get_positions,
             "Get particle positions as (N, 3) NumPy array")
        .def("get_velocities", &stellarforge::PhysicsEnginePython::get_velocities,
             "Get particle velocities as (N, 3) NumPy array")
        .def("get_masses", &stellarforge::PhysicsEnginePython::get_masses,
             "Get particle masses as (N,) NumPy array")
        .def("get_types", &stellarforge::PhysicsEnginePython::get_types,
             "Get particle types as (N,) NumPy array")
        .def("get_particle_count", &stellarforge::PhysicsEnginePython::get_particle_count,
             "Get the number of particles")
        .def("add_particle", &stellarforge::PhysicsEnginePython::add_particle,
             "Add a new particle")
        .def("remove_particle", &stellarforge::PhysicsEnginePython::remove_particle,
             "Remove a particle by index")
        .def("step", &stellarforge::PhysicsEnginePython::step,
             "Advance simulation by dt")
        .def("reset", &stellarforge::PhysicsEnginePython::reset,
             "Reset the simulation")
        .def("set_gravitational_constant", &stellarforge::PhysicsEnginePython::set_gravitational_constant,
             "Set gravitational constant")
        .def("set_softening_length", &stellarforge::PhysicsEnginePython::set_softening_length,
             "Set softening length for gravity calculation")
        .def("set_theta", &stellarforge::PhysicsEnginePython::set_theta,
             "Set Barnes-Hut theta parameter (lower = more accurate, slower)")
        .def("enable_collisions", &stellarforge::PhysicsEnginePython::enable_collisions,
             "Enable or disable collision detection")
        .def("get_backend", &stellarforge::PhysicsEnginePython::get_backend,
             "Get current compute backend")
        .def("set_backend", &stellarforge::PhysicsEnginePython::set_backend,
             "Set compute backend (single/openmp/cuda/opengl)")
        .def("get_last_step_time_ms", &stellarforge::PhysicsEnginePython::get_last_step_time_ms,
             "Get time taken for last simulation step in milliseconds");
}
