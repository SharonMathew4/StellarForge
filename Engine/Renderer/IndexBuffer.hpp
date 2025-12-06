#pragma once
#include <stddef.h>

namespace Unknown
{
	class IndexBuffer
	{
	public:
		virtual void SetData(size_t size, void* data) = 0;
		virtual void Bind() = 0;
		virtual void UnBind() = 0;
		virtual void SubData(size_t size, void* data, size_t offset = 0) = 0;

		static IndexBuffer* Create(size_t size, void* data);
	};
}
