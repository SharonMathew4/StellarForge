#pragma once
#include <functional>

namespace Unknown
{
	class EventListener
	{
	public:
		std::function<void(void* data)> callback;
	};
}