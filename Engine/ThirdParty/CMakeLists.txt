cmake_minimum_required(VERSION 3.20.0)

message("file: " ${CMAKE_BINARY_DIR})

project(ThirdParty)

set(MSDFGEN_USE_VCPKG OFF)
set(MSDFGEN_USE_SKIA OFF)
set(MSDFGEN_USE_TINYXML2 OFF)
set(MSDFGEN_DISABLE_SVG ON)
set(MSDFGEN_BUILD_STANDALONE OFF)
#set(MSDFGEN_DISABLE_PNG ON)

if(UNIX)
	add_compile_definitions(HAVE_UNISTD_H)
	add_compile_definitions(HAVE_FCNTL_H)
endif ()

add_subdirectory(freetype)

set(ZLIB_BUILD_TESTING OFF)
set(ZLIB_BUILD_SHARED  OFF)

set(ZLIB_LIBRARY ${CMAKE_BINARY_DIR}/Engine/zlib)
set(ZLIB_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/zlib)



include_directories(${PROJECT_SOURCE_DIR}/zlib)


include_directories(${PROJECT_SOURCE_DIR}/libpng)
include_directories(${CMAKE_BINARY_DIR}/Engine/ThirdParty/libpng)

add_subdirectory(glfw)
add_subdirectory(glad)
add_subdirectory(stb)

