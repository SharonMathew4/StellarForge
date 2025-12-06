cmake_minimum_required(VERSION 3.20.0)

project(stb_image)

add_library(stb_image STATIC "stb_image.cpp" "stb_image.h" "stb_image_write.cpp" "stb_image_write.h")
