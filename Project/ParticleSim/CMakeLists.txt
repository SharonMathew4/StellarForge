
cmake_minimum_required(VERSION 3.20.0)

project(ParticleSim)

file(GLOB sources ${PROJECT_SOURCE_DIR}/*.cpp)

add_executable(ParticleSim ${sources})
target_link_libraries(ParticleSim Engine)
set_target_properties(ParticleSim PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${PROJECT_SOURCE_DIR}")
