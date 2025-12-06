#pragma once 
#include <glm/glm.hpp>

namespace Unknown
{
	enum ImageFormat
	{
		RED,
		RG,
		RGB,
		RGBA
	};
	struct Image
	{
		unsigned char* data = nullptr;
		glm::uvec2 size = { 0,0 };
		ImageFormat format;
		Image(): data(nullptr), size{0,0}, format(RED)
		{
		}
		Image(const Image& image)
		{
			data = image.data;
			size = image.size;
			format = image.format;
		}
		Image(Image&& image) noexcept
		{
			data = image.data;
			size = image.size;
			format = image.format;

			image.data = nullptr;
			image.size = { 0,0 };
			image.format = RED;
		}
		~Image()
		{

		}
		void operator=(Image image)
		{
			data = image.data;
			size = image.size;
			format = image.format;
		}
		void Load(const char* filename, ImageFormat desiredFormat = RGBA);
		void Write(const char* filename);
	};
}
