#pragma once
#include <glm/glm.hpp>
#include <string>
#include <vector>
#include "Core/CoreTypes.hpp"
#include <Event/EventListener.hpp>
#include <memory>
#include <Renderer/FrameBuffer.hpp>
#include <Core/Input.hpp>

namespace Unknown
{
	struct WindowInput
	{
		MouseInput mouse;
		KeyboardInput keyboard;
	};

	struct WindowProperty
	{
		glm::ivec2 size = glm::ivec2(800, 600);
		glm::ivec2 position = glm::ivec2(200, 200);
		std::string title = "Untitled";
		GraphicApi graphicApi = Opengl;
		glm::ivec3 openglVersion = glm::ivec3(4, 5, 0);
		glm::ivec3 vulkanVersion = glm::ivec3(1, 4, 0);
		bool resize = false;
		bool move = false;
		bool minimized = false;
		bool maximized = false;
		bool closed = false;
		bool focused = false;
		bool fullscreen = false;
		float aspectRatio = 1.33333; // default aspectRation = 800 / 600
		uint32_t multisample = 0;
	};

	class Window
	{
	public:
		virtual void SetProperty(const WindowProperty& properties) = 0;
		virtual WindowProperty GetProperty() const = 0;
		virtual void* GetNativeWindow() = 0;
		virtual void ProcessInput() = 0;
		virtual WindowInput GetInput() = 0;
		virtual void SwapBuffer() = 0;
		virtual std::shared_ptr<FrameBuffer> GetFrameBuffer() = 0;
		virtual glm::ivec2 GetSize() = 0;

		static Window* Create(const WindowProperty& properties);
	};
}
