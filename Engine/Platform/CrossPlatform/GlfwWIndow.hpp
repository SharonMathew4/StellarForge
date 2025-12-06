#pragma once
#include <Core/Window.hpp>
#include <GLFW/glfw3.h>
#include <Event/EventHandler.hpp>

namespace Unknown
{
	struct GlfwUserPointer
	{
		WindowInput* input;
		WindowProperty* property;
	};

	class GlfwWindow : public Window
	{
	public:
		void SetProperty(const WindowProperty& properties) override;
		WindowProperty GetProperty() const override;
		void* GetNativeWindow() override;
		WindowInput GetInput() override;
		void ProcessInput() override;
		void SwapBuffer() override;
		glm::ivec2 GetSize() override;


		GlfwWindow(const WindowProperty& properties);
		~GlfwWindow();

	private:
		GLFWwindow* mWindow = nullptr;
		WindowProperty mProperty;
		WindowInput mInput;
		GlfwUserPointer mUserPointer;

		static bool mGlfwInitialized;
	private:
		void ProcessKeyboard();

		// Inherited via Window
		std::shared_ptr<FrameBuffer> GetFrameBuffer() override;
	};
}