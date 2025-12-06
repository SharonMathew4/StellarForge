#pragma once
#include <glm/glm.hpp>
#include <memory>
#include <vector>


namespace Unknown
{
	enum ShaderType
	{
		Float, Int, Double, UInt,
		Vec2, IVec2, DVec2, UIVec2,
		Vec3, IVec3, DVec3, UIVec3,
		Vec4, IVec4, DVec4, UIVec4,
		Mat2, Mat3, Mat4
	};

	struct Transform
	{
		glm::vec3 position = glm::vec3(0);
		glm::vec3 rotation = glm::vec3(0);
		glm::vec3 scale = glm::vec3(1);
		glm::mat4 GetMatrix() const;
	};

	struct Vertex
	{
		glm::vec3 position = glm::vec3(0);
		glm::vec2 textureCoordinate = glm::vec2(0);
		glm::vec3 normal = glm::vec3(0);
	};

}
