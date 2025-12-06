#pragma once
#include <unordered_map>
#include <string>
#include <Utility/Memory.hpp>

namespace Unknown
{
	template<typename T>
	class StorageLibrary
	{
	public:
		virtual Ref<T> Load(const char* filename) {}
		virtual Ref<T> Create(const char* filename) {}
		virtual Ref<T> Reload(const char* filename) {}
		virtual Ref<T> Recreate(const char* filename) {}
		virtual void Destroy(const char* filename) {}

		Ref<T>& operator[](const char* filename) { return Get(filename); }
		Ref<T> operator[](const char* filename) const { return Get(filename); }
		Ref<T>& Get(const char* filename) { return mMap[filename]; }
		Ref<T> Get(const char* filename) const { return mMap.at(filename); }

	protected:
		std::unordered_map<std::string, Ref<T>> mMap;
	};
}