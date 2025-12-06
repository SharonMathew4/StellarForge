#pragma once
#include <Renderer/Texture.hpp>

namespace Unknown
{
	class OpenglTexture : public Texture
	{
	public:
		void SetProperty(const TextureProperty& property) override;
		TextureProperty GetProperty() const override;
		void Bind() const override;
		void Bind(uint32_t slot) override;
		uint32_t GetId() override;
		void SubData(const Image& image, const glm::ivec2& offset) override;

		OpenglTexture(const TextureProperty& property);
		~OpenglTexture();
	private:
		TextureProperty mProperty;
		uint32_t mId = 0;

		// Inherited via Texture
	};
}