#pragma once
#include "EventListener.hpp"
#include <vector>

namespace Unknown
{
	class EventDispatcher
	{
	public:
		void Subscribe(EventListener& listener);
		void UnSubscribe(EventListener& listener);

		void dispatch(void* data);
	private:
		std::vector<EventListener*> mListener;
	};
}