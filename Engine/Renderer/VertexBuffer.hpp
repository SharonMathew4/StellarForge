#pragma once
#include <Renderer/Types.hpp>

namespace Unknown
{
	class VertexBuffer
	{
	public:
		virtual void SetData(size_t size, void* data) = 0;
		virtual void Bind() = 0;
		virtual void UnBind() = 0;
		virtual void AddLayout(ShaderType type) = 0;
		virtual void SubData(size_t size, void* data, size_t offset = 0) = 0;

		static VertexBuffer* Create(size_t size, void* data);
	};
}
