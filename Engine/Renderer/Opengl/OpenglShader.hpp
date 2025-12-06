#pragma once 
#include "Renderer/Shader.hpp"
#include <cstdint>
#include <unordered_map>

namespace Unknown
{
	class OpenglShader : public  Shader
	{
	public:
		virtual void Bind() override;
		virtual void UnBind() override;
		virtual void SetUniform(ShaderType type, const char* name, void* data) override;
		virtual void ResetUniformCache() override;


		OpenglShader(const ShaderSource& source);
		~OpenglShader();
	private:
		int32_t GetUniformLocation(const char* name);
		std::unordered_map<std::string, int32_t> mUniformCache;
		uint32_t mId = 0;
	};
}