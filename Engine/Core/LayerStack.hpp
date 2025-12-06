#pragma once
#include "Layer.hpp"
#include <vector>
#include <memory>

namespace Unknown
{
	class LayerStack
	{
	public:
		template<typename T>
		T* AddLayer()
		{
			static_assert(std::is_base_of<Layer, T>::value, "T must derive from Layer");
			mLayers.push_back(std::make_unique<T>());
			return (T*)mLayers[mLayers.size() - 1].get();
		}

		void RunOnStart();
		void RunOnUpdate();
		void RunOnEnd();
	private:
		std::vector<std::unique_ptr<Layer>> mLayers;
	};
}