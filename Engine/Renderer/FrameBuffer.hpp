#pragma once
#include <memory>
#include <Renderer/Texture.hpp>

namespace Unknown
{
	struct FrameBufferProperty
	{
		glm::uvec2 size = glm::uvec2(0);
	};

	class FrameBuffer
	{
	public:
		virtual void Bind() = 0;
		virtual void UnBind() = 0;
		virtual std::shared_ptr<Texture> GetTexture() = 0;
		virtual FrameBufferProperty GetProperty() = 0;

		static FrameBuffer* Create(const FrameBufferProperty& property);
	};
}