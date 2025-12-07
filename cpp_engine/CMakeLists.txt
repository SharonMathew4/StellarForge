cmake_minimum_required(VERSION 3.18)
project(StellarForgeEngine LANGUAGES CXX)

# C++17 required for modern features
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Options for optional features
option(USE_CUDA "Build with CUDA support" ON)
option(USE_OPENGL_COMPUTE "Build with OpenGL compute shader support" OFF)
option(USE_OPENMP "Build with OpenMP multi-threading" ON)

# Find required packages
find_package(Python3 COMPONENTS Interpreter Development NumPy REQUIRED)

# pybind11 (try find_package first, fallback to submodule)
find_package(pybind11 CONFIG)
if(NOT pybind11_FOUND)
    message(STATUS "pybind11 not found, using bundled version")
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../external/pybind11 pybind11)
endif()

# OpenMP support
if(USE_OPENMP)
    find_package(OpenMP)
    if(OpenMP_CXX_FOUND)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
        add_definitions(-DUSE_OPENMP)
    endif()
endif()

# CUDA support
if(USE_CUDA)
    include(CheckLanguage)
    check_language(CUDA)
    if(CMAKE_CUDA_COMPILER)
        enable_language(CUDA)
        set(CMAKE_CUDA_STANDARD 14)
        set(CMAKE_CUDA_STANDARD_REQUIRED ON)
        add_definitions(-DUSE_CUDA)
        
        # CUDA architecture for RTX 3050/4050 (Ampere/Ada Lovelace)
        set(CMAKE_CUDA_ARCHITECTURES 86 89)
    else()
        message(WARNING "CUDA requested but not found, building without CUDA")
        set(USE_CUDA OFF)
    endif()
endif()

# OpenGL support
if(USE_OPENGL_COMPUTE)
    find_package(OpenGL REQUIRED)
    find_package(GLEW REQUIRED)
    add_definitions(-DUSE_OPENGL_COMPUTE)
endif()

# Source files
set(CORE_SOURCES
    src/physics_engine.cpp
    src/barnes_hut_tree.cpp
    src/verlet_integrator.cpp
    src/collision_system.cpp
    src/particle_system.cpp
)

set(CUDA_SOURCES
    cuda/gravity_kernel.cu
    cuda/collision_kernel.cu
)

set(OPENGL_SOURCES
    src/gl_compute_backend.cpp
)

# Create the core library
add_library(stellarforge_core STATIC ${CORE_SOURCES})
target_include_directories(stellarforge_core PUBLIC include)
target_include_directories(stellarforge_core PRIVATE ${Python3_INCLUDE_DIRS})
target_include_directories(stellarforge_core PRIVATE ${Python3_NumPy_INCLUDE_DIRS})
set_target_properties(stellarforge_core PROPERTIES POSITION_INDEPENDENT_CODE ON)

# Link OpenMP
if(OpenMP_CXX_FOUND)
    target_link_libraries(stellarforge_core PUBLIC OpenMP::OpenMP_CXX)
endif()

# Add CUDA library if enabled
if(USE_CUDA)
    add_library(stellarforge_cuda STATIC ${CUDA_SOURCES})
    target_include_directories(stellarforge_cuda PUBLIC include)
    set_target_properties(stellarforge_cuda PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
    target_link_libraries(stellarforge_core PUBLIC stellarforge_cuda)
endif()

# Add OpenGL compute library if enabled
if(USE_OPENGL_COMPUTE)
    add_library(stellarforge_gl STATIC ${OPENGL_SOURCES})
    target_include_directories(stellarforge_gl PUBLIC include)
    target_link_libraries(stellarforge_gl PUBLIC OpenGL::GL GLEW::GLEW)
    target_link_libraries(stellarforge_core PUBLIC stellarforge_gl)
endif()

# Python module using pybind11
pybind11_add_module(stellarforge_cpp_engine src/python_bindings.cpp)
target_link_libraries(stellarforge_cpp_engine PRIVATE stellarforge_core)
target_include_directories(stellarforge_cpp_engine PRIVATE include)

# Installation
install(TARGETS stellarforge_cpp_engine
    LIBRARY DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/../src/engine_bridge
)
