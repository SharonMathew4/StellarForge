#include "OpenglShader.hpp"
#include <cstdint>
#include <Renderer/Shader.hpp>
#include <glad/glad.h>
#include <cassert>
#include <stdio.h>
#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>

namespace Unknown
{
	Shader* Shader::Create(const ShaderSource& source)
	{
		return new OpenglShader(source);
	}

	void OpenglShader::Bind()
	{
		assert(mId != 0);

		glUseProgram(mId);
	}

	void OpenglShader::UnBind()
	{
		glUseProgram(0);
	}

	void OpenglShader::SetUniform(ShaderType type, const char* name, void* data)
	{
		assert(mId != 0);
		int32_t location = GetUniformLocation(name);

		switch (type)
		{
		case Float:
			glUniform1f(location, *(float*)(data));
			break;
		case Int:
			glUniform1i(location, *(int32_t*)(data));
			break;
		case Double:
			glUniform1d(location, *(double*)(data));
			break;
		case UInt:
			glUniform1ui(location, *(uint32_t*)(data));
			break;

		case Vec2:
			glUniform2fv(location, 1, (float*)(data));
			break;
		case IVec2:
			glUniform2iv(location, 1, (int32_t*)(data));
			break;
		case DVec2:
			glUniform2dv(location, 1, (double*)(data));
			break;
		case UIVec2:
			glUniform2uiv(location, 1, (uint32_t*)(data));
			break;

		case Vec3:
			glUniform3fv(location, 1, (float*)(data));
			break;
		case IVec3:
			glUniform3iv(location, 1, (int32_t*)(data));
			break;
		case DVec3:
			glUniform3dv(location, 1, (double*)(data));
			break;
		case UIVec3:
			glUniform3uiv(location, 1, (uint32_t*)(data));
			break;

		case Vec4:
			glUniform4fv(location, 1, (float*)(data));
			break;
		case IVec4:
			glUniform4iv(location, 1, (int32_t*)(data));
			break;
		case DVec4:
			glUniform4dv(location, 1, (double*)(data));
			break;
		case UIVec4:
			glUniform4uiv(location, 1, (uint32_t*)(data));
			break;

		case Mat2:
			glUniformMatrix2fv(location, 1, GL_FALSE, glm::value_ptr(*(glm::mat2*)(data)));
			break;
		case Mat3:
			glUniformMatrix3fv(location, 1, GL_FALSE, glm::value_ptr(*(glm::mat3*)(data)));
			break;
		case Mat4:
			glUniformMatrix4fv(location, 1, GL_FALSE, glm::value_ptr(*(glm::mat4*)(data)));
			break;
		}
	}

	void OpenglShader::ResetUniformCache()
	{
		mUniformCache.clear();
	}

	OpenglShader::OpenglShader(const ShaderSource& source)
	{
		assert(mId == 0);

		const char* vertexCode = source.vertex.c_str();
		const char* fragmentCode = source.fragment.c_str();

		uint32_t vertexShader = glCreateShader(GL_VERTEX_SHADER);
		glShaderSource(vertexShader, 1, &vertexCode, nullptr);
		glCompileShader(vertexShader);

		uint32_t fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
		glShaderSource(fragmentShader, 1, &fragmentCode, nullptr);
		glCompileShader(fragmentShader);

		mId = glCreateProgram();
		glAttachShader(mId, vertexShader);
		glAttachShader(mId, fragmentShader);
		glLinkProgram(mId);

		int success = 0;
		glGetProgramiv(mId, GL_LINK_STATUS, &success);
		if (!success)
		{
			char infoLog[512];
			glGetShaderInfoLog(vertexShader, 512, nullptr, infoLog);
			printf("Vertex shader error: %s\n", infoLog);
			glGetShaderInfoLog(fragmentShader, 512, nullptr, infoLog);
			printf("Fragment shader error: %s\n", infoLog);
			glGetProgramInfoLog(mId, 512, nullptr, infoLog);
			printf("Program error: %s\n", infoLog);
		}
	}

	OpenglShader::~OpenglShader()
	{
		assert(mId != 0);

		glDeleteProgram(mId);
		mId = 0;
	}

	int32_t OpenglShader::GetUniformLocation(const char* name)
	{
		if (mUniformCache.find(name) == mUniformCache.end())
		{
			int32_t location = glGetUniformLocation(mId, name);
			mUniformCache.insert({ name, location });
			if (location < 0)
			{
				printf("Uniform Error: Failed to find uniform [%s]\n", name);
			}
			return location;
		}
		else
		{
			return mUniformCache[name];
		}
	}

}
