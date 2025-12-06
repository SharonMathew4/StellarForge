#include "Layer.hpp"
#include "Application.hpp"

namespace Unknown
{
	bool Layer::isEnabled()
	{
		return mEnabled;
	}

	void Layer::enable()
	{
		mEnabled = true;
	}

	void Layer::disable()
	{
		mEnabled = false;
	}
}

