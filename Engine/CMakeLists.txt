cmake_minimum_required(VERSION 3.20.0)

project(Engine)

file(GLOB sources
	"${PROJECT_SOURCE_DIR}/Core/*.cpp"
	"${PROJECT_SOURCE_DIR}/Platform/CrossPlatform/*.cpp"
	"${PROJECT_SOURCE_DIR}/Renderer/Opengl/*.cpp"
	"${PROJECT_SOURCE_DIR}/Renderer/*.cpp"
	"${PROJECT_SOURCE_DIR}/Event/*.cpp"	
	"${PROJECT_SOURCE_DIR}/Assets/*.cpp"
	"${PROJECT_SOURCE_DIR}/Maths/*.cpp"
	"${PROJECT_SOURCE_DIR}/Utility/*.cpp"

	"${PROJECT_SOURCE_DIR}/Core/*.hpp"
	"${PROJECT_SOURCE_DIR}/Platform/CrossPlatform/*.hpp"
	"${PROJECT_SOURCE_DIR}/Renderer/Opengl/*.hpp"
	"${PROJECT_SOURCE_DIR}/Renderer/*.hpp"
	"${PROJECT_SOURCE_DIR}/Event/*.hpp"
	"${PROJECT_SOURCE_DIR}/Assets/*.hpp"
	"${PROJECT_SOURCE_DIR}/Maths/*.hpp"
	"${PROJECT_SOURCE_DIR}/Utility/*.hpp"

)

add_subdirectory(ThirdParty)

add_library(Engine ${sources})
target_link_libraries(Engine glfw)
target_link_libraries(Engine glad)
target_link_libraries(Engine stb_image)
target_include_directories(Engine PUBLIC ${PROJECT_SOURCE_DIR}/Core)