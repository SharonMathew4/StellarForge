#pragma once
#include <Renderer/VertexBuffer.hpp>
#include <cstdint>
#include <Renderer/Types.hpp>
#include <vector>

namespace Unknown
{
	class OpenglVertexBuffer : public VertexBuffer
	{
	public:
		void SetData(size_t size, void* data) override;
		void Bind() override;
		void UnBind() override;
		void AddLayout(ShaderType type) override;
		void SubData(size_t size, void* data, size_t offset = 0) override;


		OpenglVertexBuffer(size_t size, void* data);
		~OpenglVertexBuffer();
	private:
		void BindBuffer();
		uint32_t mId = 0;
		uint32_t mVaoId = 0;
		uint32_t mStride = 0;
		std::vector<ShaderType> mLayout = std::vector<ShaderType>();
	};
}