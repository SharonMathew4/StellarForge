#include "EventHandler.hpp"
#include <cassert>

namespace Unknown
{
	void EventDispatcher::Subscribe(EventListener& listener)
	{
		mListener.push_back(&listener);
	}

	void EventDispatcher::UnSubscribe(EventListener& listener)
	{
		for (size_t i = 0; i < mListener.size(); i++)
		{
			if (mListener[i] == &listener)
			{
				mListener.erase(mListener.begin() + i);
				break;
			}
		}
		assert(false);
	}

	void EventDispatcher::dispatch(void* data)
	{
		for (size_t i = 0; i < mListener.size(); i++)
		{
			mListener[i]->callback(data);
		}
	}

}
