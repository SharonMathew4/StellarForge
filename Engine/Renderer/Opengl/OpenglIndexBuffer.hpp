#pragma once
#include <Renderer/IndexBuffer.hpp>
#include <cstdint>

namespace Unknown
{
	class OpenglIndexBuffer : public IndexBuffer
	{
	public:
		OpenglIndexBuffer(size_t size, void* data);
		~OpenglIndexBuffer();
		void SetData(size_t size, void* data) override;
		void Bind() override;
		void UnBind() override;
		void SubData(size_t size, void* data, size_t offset = 0) override;
	private:
		uint32_t mId = 0;
	};
}