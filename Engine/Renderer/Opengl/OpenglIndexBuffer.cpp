#include "OpenglIndexBuffer.hpp"
#include <glad/glad.h>
#include <cassert>


namespace Unknown
{
	IndexBuffer* IndexBuffer::Create(size_t size, void* data)
	{
		return new OpenglIndexBuffer(size, data);
	}
	void OpenglIndexBuffer::SetData(size_t size, void* data)
	{
		Bind();
		glBufferData(GL_ELEMENT_ARRAY_BUFFER, size, data, GL_DYNAMIC_DRAW);
	}

	void OpenglIndexBuffer::Bind()
	{
		assert(mId != 0);
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mId);
	}

	void OpenglIndexBuffer::UnBind()
	{
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0);
	}

	void OpenglIndexBuffer::SubData(size_t size, void* data, size_t offset /*= 0*/)
	{
		glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mId);
		glBufferSubData(GL_ELEMENT_ARRAY_BUFFER, offset, size, data);
	}

	OpenglIndexBuffer::OpenglIndexBuffer(size_t size, void* data)
	{
		assert(mId == 0);
		glCreateBuffers(1, &mId);
		if (size != 0) SetData(size, data);
	}

	OpenglIndexBuffer::~OpenglIndexBuffer()
	{
		assert(mId != 0);
		glDeleteBuffers(1, &mId);
		mId = 0;
	}
}
