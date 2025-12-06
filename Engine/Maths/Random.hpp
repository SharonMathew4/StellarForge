#pragma once
#include <cstdlib>
#include <glm/glm.hpp>

namespace Unknown
{
	class Maths
	{
	public:
		static float RandomUnitFloat();
		static glm::vec2 RandomUnitVec2();
		static glm::vec3 RandomUnitVec3();
		static glm::vec4 RandomUnitVec4();
		static float RandomFloat();
		static glm::vec2 RandomVec2();
		static glm::vec3 RandomVec3();
		static glm::vec4 RandomVec4();
		static int RandomInt();
		static glm::ivec2 RandomIVec2();
		static glm::ivec3 RandomIVec3();
		static glm::ivec4 RandomIVec4();

		static glm::vec3 RGB(int r, int g, int b);
		static glm::vec4 RGBA(int r, int g, int b, int a);
		static glm::vec3 HexRGB(int hex);
		static glm::vec4 HexRGBA(int hex);
	};
}