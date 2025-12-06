#include "Image.hpp"
#include <ThirdParty/stb/stb_image.h>
#include <Macro.hpp>
#include <stb/stb_image_write.h>


namespace Unknown
{
	
	void Image::Load(const char* filename, ImageFormat desiredFormat)
	{
		UNK_CORE_CHECK_FILE_EXIST(filename);

		int width, height, outputChannel;
		data = stbi_load(filename, &width, &height, &outputChannel, desiredFormat + 1);
		size = { width, height };
		format = desiredFormat;
	}

	void Image::Write(const char* filename)
	{
		stbi_write_png(filename, size.x, size.y, format + 1, data, size.x * (format + 1));
	}

}
