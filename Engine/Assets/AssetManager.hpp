#pragma once
#include <Utility/StorageLibrary.hpp>
#include <Renderer/Texture.hpp>

namespace Unknown
{

	class TextureLibrary : public StorageLibrary<Texture>
	{
	public:

		Ref<Texture> Load(const char* filename) override;
		Ref<Texture> Create(const char* filename) override;
		Ref<Texture> Reload(const char* filename) override;
		Ref<Texture> Recreate(const char* filename) override;
		void Destroy(const char* filename) override;


	private:

	};
	class AssetManager
	{

	};
}