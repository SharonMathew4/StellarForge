#include "Random.hpp"


namespace Unknown
{
	float Maths::RandomUnitFloat()
	{
		return float(rand()) / RAND_MAX;
	}

	glm::vec2 Maths::RandomUnitVec2()
	{
		return { RandomUnitFloat(), RandomUnitFloat() };
	}

	glm::vec3 Maths::RandomUnitVec3()
	{
		return { RandomUnitFloat(), RandomUnitFloat(), RandomUnitFloat() };
	}

	glm::vec4 Maths::RandomUnitVec4()
	{
		return { RandomUnitFloat(), RandomUnitFloat(), RandomUnitFloat(), RandomUnitFloat() };
	}

	float Maths::RandomFloat()
	{
		return float(rand()) / float(rand());
	}

	glm::vec2 Maths::RandomVec2()
	{
		return { RandomFloat(), RandomFloat() };
	}

	glm::vec3 Maths::RandomVec3()
	{
		return { RandomFloat(), RandomFloat(), RandomFloat() };
	}

	glm::vec4 Maths::RandomVec4()
	{
		return { RandomFloat(), RandomFloat(), RandomFloat(), RandomFloat() };
	}

	int Maths::RandomInt()
	{
		return int(rand());
	}

	glm::ivec2 Maths::RandomIVec2()
	{
		return { RandomInt(), RandomInt() };
	}

	glm::ivec3 Maths::RandomIVec3()
	{
		return { RandomInt(), RandomInt(), RandomInt() };
	}

	glm::ivec4 Maths::RandomIVec4()
	{
		return { RandomInt(), RandomInt(), RandomInt(), RandomInt() };
	}


	glm::vec3 Maths::RGB(int r, int g, int b)
	{
		return { float(r) / 255.f, float(g) / 255.f, float(b) / 255.f };
	}


	glm::vec4 Maths::RGBA(int r, int g, int b, int a)
	{
		return { float(r) / 255.f, float(g) / 255.f, float(b) / 255.f, float(a) / 255.f };
	}

	glm::vec3 Maths::HexRGB(int hex)
	{
		float r = (hex & 0xff0000) >> 16;
		float g = (hex & 0x00ff00) >> 8;
		float b = (hex & 0x0000ff);
		return glm::vec3(r, g, b) / glm::vec3(255.f);
	}

	glm::vec4 Maths::HexRGBA(int hex)
	{
		float r = (hex & 0xff000000) >> 24;
		float g = (hex & 0x00ff0000) >> 16;
		float b = (hex & 0x0000ff00) >> 8;
		float a = (hex & 0x000000ff);
		return glm::vec4(r, g, b, a) / glm::vec4(255.f);
	}
}
