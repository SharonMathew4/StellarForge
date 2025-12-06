#pragma once
#include <glm/glm.hpp>
#include <Assets/Image.hpp>

namespace Unknown
{
	enum TextureFilter
	{
		LINEAR,
		NEAREST
	};

	enum TextureWrap
	{
		REPEAT,
		MIRROR_REPEAT
	};

	struct TextureProperty
	{
		int slot = 0;
		Image image;
		TextureFilter minFilter = NEAREST;
		TextureFilter magFilter = NEAREST;
		TextureWrap wrapS = REPEAT;
		TextureWrap wrapT = REPEAT;
		bool generateMipmaps = true;
	};

	class Texture
	{
	public:
		virtual void SetProperty(const TextureProperty& property) = 0;
		virtual TextureProperty GetProperty() const = 0;
		virtual void Bind() const = 0;
		virtual void Bind(uint32_t slot) = 0;
		virtual uint32_t GetId() = 0;
		virtual void SubData(const Image& image, const glm::ivec2& offset) = 0;

		static Texture* Create(const TextureProperty& property);
	};
}