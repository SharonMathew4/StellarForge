#include "LayerStack.hpp"

namespace Unknown
{

	void LayerStack::RunOnStart()
	{
		for (int i = 0; i < mLayers.size(); i++)
		{
			if (mLayers[i]->isEnabled())
				mLayers[i]->OnStart();
		}
	}

	void LayerStack::RunOnUpdate()
	{
		for (int i = 0; i < mLayers.size(); i++)
		{
			if (mLayers[i]->isEnabled())
				mLayers[i]->OnUpdate();
		}
	}

	void LayerStack::RunOnEnd()
	{
		for (int i = 0; i < mLayers.size(); i++)
		{
			if (mLayers[i]->isEnabled())
				mLayers[i]->OnEnd();
		}
	}

}
