#include <Assets/AssetManager.hpp>
#include <Utility/Memory.hpp>

namespace Unknown
{

	Ref<Texture> TextureLibrary::Load(const char* filename)
	{
		TextureProperty property;
		property.image.Load(filename);
		Ref<Texture> texture = Ref<Texture>(Texture::Create(property));
		mMap[filename] = texture;
		return texture;
	}

	Ref<Texture> TextureLibrary::Create(const char* filename)
	{
		return nullptr;
	}

	Ref<Texture> TextureLibrary::Reload(const char* filename)
	{
		return nullptr;
	}

	Ref<Texture> TextureLibrary::Recreate(const char* filename)
	{
		return nullptr;
	}

	void TextureLibrary::Destroy(const char* filename)
	{
	}

}