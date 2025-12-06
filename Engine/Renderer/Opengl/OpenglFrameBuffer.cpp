#include <glad/glad.h>
#include "OpenglFrameBuffer.hpp"
#include <stdio.h>

namespace Unknown
{
	FrameBuffer* FrameBuffer::Create(const FrameBufferProperty& property)
	{
		return new OpenglFrameBuffer(property);
	}

	void OpenglFrameBuffer::UnBind()
	{
		glBindFramebuffer(GL_FRAMEBUFFER, 0);
	}

	void OpenglFrameBuffer::Bind()
	{
		glBindFramebuffer(GL_FRAMEBUFFER, mId);
	}

	std::shared_ptr<Texture> OpenglFrameBuffer::GetTexture()
	{
		return mTexture;
	}

	OpenglFrameBuffer::OpenglFrameBuffer(const FrameBufferProperty& property)
	{
		mProperty = property;
		glGenFramebuffers(1, &mId);
		glBindFramebuffer(GL_FRAMEBUFFER, mId);
		TextureProperty textureProperty;
		textureProperty.image.size = mProperty.size;

		mTexture.reset(Texture::Create(textureProperty));

		glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, mTexture->GetId(), 0);

		printf("Texture id: %d\n", mTexture->GetId());

		if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE)
		{
			printf("Framebuffer not complete\n");
		}
		glBindFramebuffer(GL_FRAMEBUFFER, 0);
	}

	FrameBufferProperty OpenglFrameBuffer::GetProperty()
	{
		return mProperty;
	}
}
