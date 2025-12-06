#pragma once
#include <chrono>
#include <string>

#define UNK_SCOPE_PROFILER() Unknown::ScopeProfiler __scope_profiler__(__FUNCTION__)

namespace Unknown
{
	class Timer
	{
	public:
		void Start();
		float End();
		float GetDuration() const;
		float GetElapsedTime() const;

	private:
		decltype(std::chrono::high_resolution_clock::now()) mStart;
		std::chrono::duration<float> mDuration;
		bool mRunning = false;
	};

	class ScopeProfiler
	{
	public:
		ScopeProfiler(const std::string &name);
		~ScopeProfiler();

	private:
		Timer mTimer;
		std::string mName;
	};
} // namespace Unknown
