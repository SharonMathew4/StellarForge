#pragma once
#include <Renderer/FrameBuffer.hpp>

namespace Unknown
{
	class OpenglFrameBuffer : public FrameBuffer
	{
	public:
		void Bind() override;
		void UnBind() override;
		std::shared_ptr<Texture> GetTexture() override;
		OpenglFrameBuffer(const FrameBufferProperty& property);
		FrameBufferProperty GetProperty() override;

	private:
		uint32_t mId = 0;
		std::shared_ptr<Texture> mTexture;
		FrameBufferProperty mProperty;

	};
}