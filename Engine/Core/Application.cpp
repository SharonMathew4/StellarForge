#include <Core/Application.hpp>
#include <Utility/Timer.hpp>
#include "Macro.hpp"

namespace Unknown
{
	void Application::Initialize()
	{
		UNK_CORE_ASSERT("Application not created", mInstance != nullptr);
		OnInitialize();
		InitializeSystems();
		OnStart();
		mLayerStack->RunOnStart();
	}

	void Application::Run()
	{
		mTime.applicationTimer.Start();
		Initialize();
		MainLoop();
		Terminate();
	}

	void Application::MainLoop()
	{
		Timer deltaTimer;
		while (mRunning)
		{
			deltaTimer.Start();
			ProcessEvent();
			mRunning = !mWindow->GetProperty().closed;
			
			mTime.deltaTime = deltaTimer.GetDuration();
			OnUpdate();

			mLayerStack->RunOnUpdate();
			mWindow->SwapBuffer();
			deltaTimer.End();
		}
	}

	void Application::Terminate()
	{
		OnEnd();
		mLayerStack->RunOnEnd();
	}

	void Application::Close()
	{
		mRunning = false;
	}

	Application::Application()
	{
		UNK_CORE_ASSERT("Application already created", mInstance == nullptr);
		mInstance = this;
	}

	Application::~Application()
	{

	}

	void Application::ProcessEvent()
	{
		mWindow->ProcessInput();
	}

	void Application::InitializeSystems()
	{
		mWindow.reset(Window::Create(mProperty.windowProperty));
		mRenderer2D.reset(new Renderer2D());
		mRenderer2D->Initialize();
		mLayerStack.reset(new LayerStack);
	}

	Application* Application::mInstance = nullptr;
}