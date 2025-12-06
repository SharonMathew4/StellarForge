#include "OpenglTexture.hpp"
#include <glad/glad.h>

namespace Unknown
{
	static GLenum textureFilter[]{ GL_LINEAR, GL_NEAREST };

	static GLenum textureWrap[]{
		GL_REPEAT,
		GL_MIRRORED_REPEAT,
	};

	static GLenum format[]{
		GL_RED,
		GL_RG,
		GL_RGB,
		GL_RGBA,
	};

	Texture* Texture::Create(const TextureProperty& property)
	{
		return new OpenglTexture(property);
	}

	void OpenglTexture::SetProperty(const TextureProperty& property)
	{
		mProperty = property;
	}

	TextureProperty OpenglTexture::GetProperty() const
	{
		return mProperty;
	}

	void OpenglTexture::Bind() const
	{
		assert(mId != 0);
		glActiveTexture(GL_TEXTURE0 + mProperty.slot);
		glBindTexture(GL_TEXTURE_2D, mId);
	}

	void OpenglTexture::Bind(uint32_t slot)
	{
		assert(mId != 0);
		mProperty.slot = slot;
		glActiveTexture(GL_TEXTURE0 + mProperty.slot);
		glBindTexture(GL_TEXTURE_2D, mId);
	}

	OpenglTexture::OpenglTexture(const TextureProperty& property)
	{
		mProperty = property;
		glActiveTexture(GL_TEXTURE0 + property.slot);
		glCreateTextures(GL_TEXTURE_2D, 1, &mId);
		glBindTexture(GL_TEXTURE_2D, mId);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, textureWrap[mProperty.wrapS]);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, textureWrap[mProperty.wrapT]);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, textureFilter[mProperty.magFilter]);
		glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, textureFilter[mProperty.minFilter]);

		glPixelStorei(GL_UNPACK_ALIGNMENT, 1);

		glTexImage2D(GL_TEXTURE_2D, 0, format[mProperty.image.format], mProperty.image.size.x, mProperty.image.size.y, 0, format[mProperty.image.format], GL_UNSIGNED_BYTE, mProperty.image.data);

		if (mProperty.generateMipmaps)
			glGenerateMipmap(GL_TEXTURE_2D);
	}

	OpenglTexture::~OpenglTexture()
	{
	}

	uint32_t OpenglTexture::GetId()
	{
		return mId;
	}

	void OpenglTexture::SubData(const Image& image, const glm::ivec2& offset)
	{
		glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
		glBindTexture(GL_TEXTURE_2D, mId);
		glTexSubImage2D(GL_TEXTURE_2D, 0, offset.x, offset.y, image.size.x, image.size.y, mProperty.image.format, GL_UNSIGNED_BYTE, image.data);
	}
}
