#pragma once
#include <string>
#include <Renderer/Types.hpp>

namespace Unknown
{
	struct ShaderSource
	{
		std::string vertex;
		std::string fragment;
		std::string geometry;
		std::string tessellation;
		std::string compute;
	};



	class Shader
	{
	public:
		virtual void Bind() = 0;
		virtual void UnBind() = 0;
		virtual void SetUniform(ShaderType type, const char* name, void* data) = 0;
		virtual void ResetUniformCache() = 0;


		static Shader* Create(const ShaderSource& source);
	};
}