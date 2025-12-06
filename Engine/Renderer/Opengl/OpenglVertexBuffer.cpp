#include "OpenglVertexBuffer.hpp"
#include <glad/glad.h>
#include <cassert>

namespace Unknown
{
	static size_t shaderTypeSize[] =
	{
		sizeof(float), sizeof(int), sizeof(double), sizeof(uint32_t), // sizeof Float Int Double UInt
		sizeof(float) * 2, sizeof(int) * 2, sizeof(double) * 2, sizeof(uint32_t) * 2, // sizeof Vec2 IVec2 DVec2 UIVec2
		sizeof(float) * 3, sizeof(int) * 3, sizeof(double) * 3, sizeof(uint32_t) * 3, // sizeof Vec3 IVec3 DVec3 UIVec3
		sizeof(float) * 4, sizeof(int) * 4, sizeof(double) * 4, sizeof(uint32_t) * 4, // sizeof Vec4 IVec4 DVec4 UIVec4
		sizeof(float) * 4, sizeof(float) * 9, sizeof(float) * 16 // sizeof Mat2 Mat3 Mat4
	};

	static uint32_t shaderTypeElement[] =
	{
		1,1,1,1, // number of elements Float Int Double UInt
		2,2,2,2, // number of elements Vec2 IVec2 DVec2 UIVec2
		3,3,3,3, // number of elements Vec3 IVec3 DVec3 UIVec3
		4,4,4,4, // number of elements Vec4 IVec4 DVec4 UIVec4
		4,9,16	 // number of elements Mat2 Mat3 Mat4
	};

	static GLenum openglShaderType[] =
	{
		GL_FLOAT, GL_INT, GL_DOUBLE, GL_UNSIGNED_INT, // corresponding opengl type of Float Int Double UInt
		GL_FLOAT, GL_INT, GL_DOUBLE, GL_UNSIGNED_INT, // corresponding opengl type of Vec2 IVec2 DVec2 UIVec2
		GL_FLOAT, GL_INT, GL_DOUBLE, GL_UNSIGNED_INT, // corresponding opengl type of Vec3 IVec3 DVec3 UIVec3
		GL_FLOAT, GL_INT, GL_DOUBLE, GL_UNSIGNED_INT, // corresponding opengl type of Vec4 IVec4 DVec4 UIVec4
		GL_FLOAT, GL_FLOAT, GL_FLOAT				  // corresponding opengl type of Mat2 Mat3 Mat4
	};

	VertexBuffer* VertexBuffer::Create(size_t size, void* data)
	{
		return new OpenglVertexBuffer(size, data);
	}

	void OpenglVertexBuffer::SetData(size_t size, void* data)
	{
		BindBuffer();
		glBufferData(GL_ARRAY_BUFFER, size, data, GL_DYNAMIC_DRAW);
	}

	void OpenglVertexBuffer::Bind()
	{
		assert(mId != 0);
		assert(mVaoId != 0);

		BindBuffer();

		size_t offset = 0;
		for (size_t i = 0; i < mLayout.size(); i++)
		{
			ShaderType type = mLayout[i];
			glEnableVertexAttribArray(i);

			if (openglShaderType[type] == GL_INT || openglShaderType[type] == GL_UNSIGNED_INT)
				glVertexAttribIPointer(i, shaderTypeElement[type], openglShaderType[type], mStride, (void*)offset);
			else
				glVertexAttribPointer(i, shaderTypeElement[type], openglShaderType[type], GL_FALSE, mStride, (void*)offset);

			offset += shaderTypeSize[type];
		}
	}

	void OpenglVertexBuffer::UnBind()
	{
		glBindBuffer(GL_ARRAY_BUFFER, 0);
		glBindVertexArray(0);
	}

	void OpenglVertexBuffer::AddLayout(ShaderType type)
	{
		mLayout.push_back(type);
		mStride += shaderTypeSize[type];
	}

	void OpenglVertexBuffer::SubData(size_t size, void* data, size_t offset /*= 0*/)
	{
		BindBuffer();
		glBufferSubData(GL_ARRAY_BUFFER, offset, size, data);
	}

	OpenglVertexBuffer::OpenglVertexBuffer(size_t size, void* data)
	{
		glCreateVertexArrays(1, &mVaoId);
		glBindVertexArray(mVaoId);

		glCreateBuffers(1, &mId);
		glBindBuffer(GL_ARRAY_BUFFER, mId);

		if (size != 0) SetData(size, data);
	}

	OpenglVertexBuffer::~OpenglVertexBuffer()
	{
		assert(mId != 0);
		assert(mVaoId != 0);


		glDeleteBuffers(1, &mId);
		glDeleteVertexArrays(1, &mVaoId);
		mId = 0;
		mVaoId = 0;
	}

	void OpenglVertexBuffer::BindBuffer()
	{
		glBindVertexArray(mVaoId);
		glBindBuffer(GL_ARRAY_BUFFER, mId);
	}
}
