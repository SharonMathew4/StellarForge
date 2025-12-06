#include <glad/glad.h>
#include "Platform/CrossPlatform/GlfwWIndow.hpp"
#include "../../Utility/Memory.hpp"
#include "Window.hpp"
#include <print>
#include <Macro.hpp>

#define GET_GLFW_USER_POINTER() *(GlfwUserPointer *)glfwGetWindowUserPointer(window)

namespace Unknown
{
	Window* Window::Create(const WindowProperty& properties)
	{
		return new GlfwWindow(properties);
	}

	void closeCallback(GLFWwindow* window)
	{
		GlfwUserPointer& mUserPointer = GET_GLFW_USER_POINTER();
		mUserPointer.property->closed = true;
	}

	void windowMinimizedCallback(GLFWwindow* window, int minimized)
	{
		GlfwUserPointer& mUserPointer = GET_GLFW_USER_POINTER();
		mUserPointer.property->minimized = minimized;
	}

	void windowMaximizedCallback(GLFWwindow* window, int maximized)
	{
		GlfwUserPointer& mUserPointer = GET_GLFW_USER_POINTER();
		mUserPointer.property->maximized = maximized;

		int width, height;
		glfwGetWindowSize(window, &width, &height);
		mUserPointer.property->size = { width, height };
	}

	void windowFocusedCallback(GLFWwindow* window, int focused)
	{
		GlfwUserPointer& mUserPointer = GET_GLFW_USER_POINTER();
		mUserPointer.property->focused = focused;
	}

	void cursorPositionCallback(GLFWwindow* window, double x, double y)
	{
		GlfwUserPointer& mUserPointer = GET_GLFW_USER_POINTER();
		mUserPointer.input->mouse.offset = mUserPointer.input->mouse.position;
		mUserPointer.input->mouse.position = { x, y };
		mUserPointer.input->mouse.offset = mUserPointer.input->mouse.position - mUserPointer.input->mouse.offset;
	}

	void cursorEnterCallback(GLFWwindow* window, int entered)
	{
		GlfwUserPointer& mUserPointer = GET_GLFW_USER_POINTER();
		mUserPointer.input->mouse.windowEntered = entered;
	}

	void mouseButtonCallback(GLFWwindow* window, int button, int action, int mods)
	{
		GlfwUserPointer& mUserPointer = GET_GLFW_USER_POINTER();
		if (button == GLFW_MOUSE_BUTTON_LEFT)
		{
			mUserPointer.input->mouse.leftPress = (action == GLFW_PRESS);
		}
		if (button == GLFW_MOUSE_BUTTON_MIDDLE)
		{
			mUserPointer.input->mouse.middlePress = (action == GLFW_PRESS);
		}
		if (button == GLFW_MOUSE_BUTTON_RIGHT)
		{
			mUserPointer.input->mouse.rightPress = (action == GLFW_PRESS);
		}
	}

	void scrollCallback(GLFWwindow* window, double xoffset, double yoffset)
	{
		GlfwUserPointer& mUserPointer = GET_GLFW_USER_POINTER();
		mUserPointer.input->mouse.scroll = {xoffset, yoffset};
	}

	GlfwWindow::GlfwWindow(const WindowProperty& property)
	{
		mProperty = property;

		if (!mGlfwInitialized)
			glfwInit();

		if (mProperty.graphicApi == Opengl)
		{
			glfwWindowHint(GLFW_CLIENT_API, GLFW_OPENGL_API);
			glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, mProperty.openglVersion.x);
			glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, mProperty.openglVersion.y);
			glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
			if (mProperty.multisample != 0)
				glfwWindowHint(GLFW_SAMPLES, mProperty.multisample);
		}
		else if (mProperty.graphicApi == Vulkan)
		{
			glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
		}

		mWindow = glfwCreateWindow(mProperty.size.x, mProperty.size.y, mProperty.title.c_str(), nullptr, nullptr);
		glfwSetWindowPos(mWindow, mProperty.position.x, mProperty.position.y);

		if (mProperty.graphicApi == Opengl)
		{
			glfwMakeContextCurrent(mWindow);
			if (gladLoadGLLoader((GLADloadproc)glfwGetProcAddress) == false)
			{
				std::println("error: failed to load glad");
			}
		}

		mUserPointer.property = &mProperty;
		mUserPointer.input = &mInput;

		glfwSetWindowUserPointer(mWindow, &mUserPointer);

		glfwSetWindowCloseCallback(mWindow, closeCallback);
		glfwSetWindowFocusCallback(mWindow, windowFocusedCallback);
		glfwSetWindowMaximizeCallback(mWindow, windowMaximizedCallback);
		glfwSetWindowIconifyCallback(mWindow, windowMinimizedCallback);
		glfwSetCursorPosCallback(mWindow, cursorPositionCallback);
		glfwSetCursorEnterCallback(mWindow, cursorEnterCallback);
		glfwSetMouseButtonCallback(mWindow, mouseButtonCallback);
		glfwSetScrollCallback(mWindow, scrollCallback);

		if (mProperty.fullscreen)
		{
			GLFWmonitor* monitor = glfwGetPrimaryMonitor();
			const GLFWvidmode* mode = glfwGetVideoMode(monitor);

			glfwSetWindowMonitor(mWindow, monitor, 0, 0, mode->width, mode->height, mode->refreshRate);
		}
	}

	GlfwWindow::~GlfwWindow()
	{
		glfwDestroyWindow(mWindow);
		mWindow = nullptr;
	}

	void GlfwWindow::SetProperty(const WindowProperty& properties)
	{
		if (mProperty.size != properties.size)
			glfwSetWindowSize(mWindow, properties.size.x, properties.size.y);
		if (mProperty.position != properties.position)
			glfwSetWindowPos(mWindow, properties.position.x, properties.position.y);
		if (mProperty.minimized != properties.minimized)
			glfwIconifyWindow(mWindow);
		if (mProperty.maximized != properties.maximized)
			glfwMaximizeWindow(mWindow);
		if (mProperty.title != properties.title)
			glfwSetWindowTitle(mWindow, properties.title.c_str());
		if (mProperty.focused != properties.focused)
			glfwFocusWindow(mWindow);

		mProperty = properties;
	}

	WindowProperty GlfwWindow::GetProperty() const
	{
		return mProperty;
	}

	void* GlfwWindow::GetNativeWindow()
	{
		return mWindow;
	}

	WindowInput GlfwWindow::GetInput()
	{
		return mInput;
	}


	void GlfwWindow::ProcessKeyboard()
	{
		mInput.keyboard = KeyboardInput();
		if (glfwGetKey(mWindow, GLFW_KEY_SPACE) == GLFW_PRESS)
			mUserPointer.input->keyboard.keySpace = true;
		if (glfwGetKey(mWindow, GLFW_KEY_APOSTROPHE) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyApostrophe = true;
		if (glfwGetKey(mWindow, GLFW_KEY_COMMA) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyComma = true;
		if (glfwGetKey(mWindow, GLFW_KEY_MINUS) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyMinus = true;
		if (glfwGetKey(mWindow, GLFW_KEY_PERIOD) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPeriod = true;
		if (glfwGetKey(mWindow, GLFW_KEY_SLASH) == GLFW_PRESS)
			mUserPointer.input->keyboard.keySlash = true;
		if (glfwGetKey(mWindow, GLFW_KEY_0) == GLFW_PRESS)
			mUserPointer.input->keyboard.key0 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_1) == GLFW_PRESS)
			mUserPointer.input->keyboard.key1 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_2) == GLFW_PRESS)
			mUserPointer.input->keyboard.key2 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_3) == GLFW_PRESS)
			mUserPointer.input->keyboard.key3 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_4) == GLFW_PRESS)
			mUserPointer.input->keyboard.key4 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_5) == GLFW_PRESS)
			mUserPointer.input->keyboard.key5 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_6) == GLFW_PRESS)
			mUserPointer.input->keyboard.key6 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_7) == GLFW_PRESS)
			mUserPointer.input->keyboard.key7 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_8) == GLFW_PRESS)
			mUserPointer.input->keyboard.key8 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_9) == GLFW_PRESS)
			mUserPointer.input->keyboard.key9 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_SEMICOLON) == GLFW_PRESS)
			mUserPointer.input->keyboard.keySemicolon = true;
		if (glfwGetKey(mWindow, GLFW_KEY_EQUAL) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyEqual = true;
		if (glfwGetKey(mWindow, GLFW_KEY_A) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyA = true;
		if (glfwGetKey(mWindow, GLFW_KEY_B) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyB = true;
		if (glfwGetKey(mWindow, GLFW_KEY_C) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyC = true;
		if (glfwGetKey(mWindow, GLFW_KEY_D) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyD = true;
		if (glfwGetKey(mWindow, GLFW_KEY_E) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyE = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF = true;
		if (glfwGetKey(mWindow, GLFW_KEY_G) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyG = true;
		if (glfwGetKey(mWindow, GLFW_KEY_H) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyH = true;
		if (glfwGetKey(mWindow, GLFW_KEY_I) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyI = true;
		if (glfwGetKey(mWindow, GLFW_KEY_J) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyJ = true;
		if (glfwGetKey(mWindow, GLFW_KEY_K) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyK = true;
		if (glfwGetKey(mWindow, GLFW_KEY_L) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyL = true;
		if (glfwGetKey(mWindow, GLFW_KEY_M) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyM = true;
		if (glfwGetKey(mWindow, GLFW_KEY_N) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyN = true;
		if (glfwGetKey(mWindow, GLFW_KEY_O) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyO = true;
		if (glfwGetKey(mWindow, GLFW_KEY_P) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyP = true;
		if (glfwGetKey(mWindow, GLFW_KEY_Q) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyQ = true;
		if (glfwGetKey(mWindow, GLFW_KEY_R) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyR = true;
		if (glfwGetKey(mWindow, GLFW_KEY_S) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyS = true;
		if (glfwGetKey(mWindow, GLFW_KEY_T) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyT = true;
		if (glfwGetKey(mWindow, GLFW_KEY_U) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyU = true;
		if (glfwGetKey(mWindow, GLFW_KEY_V) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyV = true;
		if (glfwGetKey(mWindow, GLFW_KEY_W) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyW = true;
		if (glfwGetKey(mWindow, GLFW_KEY_X) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyX = true;
		if (glfwGetKey(mWindow, GLFW_KEY_Y) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyY = true;
		if (glfwGetKey(mWindow, GLFW_KEY_Z) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyZ = true;
		if (glfwGetKey(mWindow, GLFW_KEY_LEFT_BRACKET) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyLeftBracket = true;
		if (glfwGetKey(mWindow, GLFW_KEY_BACKSLASH) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyBackslash = true;
		if (glfwGetKey(mWindow, GLFW_KEY_RIGHT_BRACKET) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyRightBracket = true;
		if (glfwGetKey(mWindow, GLFW_KEY_GRAVE_ACCENT) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyGraveAccent = true;
		if (glfwGetKey(mWindow, GLFW_KEY_ESCAPE) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyEscape = true;
		if (glfwGetKey(mWindow, GLFW_KEY_ENTER) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyEnter = true;
		if (glfwGetKey(mWindow, GLFW_KEY_TAB) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyTab = true;
		if (glfwGetKey(mWindow, GLFW_KEY_BACKSPACE) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyBackspace = true;
		if (glfwGetKey(mWindow, GLFW_KEY_INSERT) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyInsert = true;
		if (glfwGetKey(mWindow, GLFW_KEY_DELETE) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyDelete = true;
		if (glfwGetKey(mWindow, GLFW_KEY_RIGHT) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyRight = true;
		if (glfwGetKey(mWindow, GLFW_KEY_LEFT) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyLeft = true;
		if (glfwGetKey(mWindow, GLFW_KEY_DOWN) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyDown = true;
		if (glfwGetKey(mWindow, GLFW_KEY_UP) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyUp = true;
		if (glfwGetKey(mWindow, GLFW_KEY_PAGE_UP) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPageUp = true;
		if (glfwGetKey(mWindow, GLFW_KEY_PAGE_DOWN) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPageDown = true;
		if (glfwGetKey(mWindow, GLFW_KEY_HOME) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyHome = true;
		if (glfwGetKey(mWindow, GLFW_KEY_END) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyEnd = true;
		if (glfwGetKey(mWindow, GLFW_KEY_CAPS_LOCK) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyCapsLock = true;
		if (glfwGetKey(mWindow, GLFW_KEY_SCROLL_LOCK) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyScrollLock = true;
		if (glfwGetKey(mWindow, GLFW_KEY_NUM_LOCK) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyNumLock = true;
		if (glfwGetKey(mWindow, GLFW_KEY_PRINT_SCREEN) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPrintScreen = true;
		if (glfwGetKey(mWindow, GLFW_KEY_PAUSE) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPause = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F1) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF1 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F2) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF2 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F3) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF3 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F4) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF4 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F5) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF5 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F6) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF6 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F7) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF7 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F8) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF8 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F9) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF9 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F10) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF10 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F11) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF11 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F12) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF12 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F13) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF13 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F14) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF14 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F15) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF15 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F16) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF16 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F17) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF17 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F18) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF18 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F19) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF19 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F20) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF20 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F21) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF21 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F22) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF22 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F23) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF23 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F24) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF24 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_F25) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyF25 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_0) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPad0 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_1) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPad1 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_2) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPad2 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_3) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPad3 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_4) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPad4 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_5) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPad5 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_6) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPad6 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_7) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPad7 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_8) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPad8 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_9) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPad9 = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_DECIMAL) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPadDecimal = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_DIVIDE) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPadDivide = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_MULTIPLY) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPadMultiply = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_SUBTRACT) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPadSubtract = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_ADD) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPadAdd = true;
		if (glfwGetKey(mWindow, GLFW_KEY_KP_ENTER) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyPadEnter = true;
		if (glfwGetKey(mWindow, GLFW_KEY_LEFT_SHIFT) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyLeftShift = true;
		if (glfwGetKey(mWindow, GLFW_KEY_LEFT_CONTROL) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyLeftControl = true;
		if (glfwGetKey(mWindow, GLFW_KEY_LEFT_ALT) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyLeftAlt = true;
		if (glfwGetKey(mWindow, GLFW_KEY_LEFT_SUPER) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyLeftSuper = true;
		if (glfwGetKey(mWindow, GLFW_KEY_RIGHT_SHIFT) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyRightShift = true;
		if (glfwGetKey(mWindow, GLFW_KEY_RIGHT_CONTROL) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyRightControl = true;
		if (glfwGetKey(mWindow, GLFW_KEY_RIGHT_ALT) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyRightAlt = true;
		if (glfwGetKey(mWindow, GLFW_KEY_RIGHT_SUPER) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyRightSuper = true;
		if (glfwGetKey(mWindow, GLFW_KEY_MENU) == GLFW_PRESS)
			mUserPointer.input->keyboard.keyMenu = true;
	}

	Ref<FrameBuffer> GlfwWindow::GetFrameBuffer()
	{
		return Ref<FrameBuffer>();
	}

	void GlfwWindow::ProcessInput()
	{
		mInput.mouse.offset = { 0, 0 };
		mInput.mouse.scroll = { 0, 0 };
		glfwPollEvents();
		glfwGetWindowSize(mWindow, &mProperty.size.x, &mProperty.size.y);
		mProperty.aspectRatio = float(mProperty.size.x) / float(mProperty.size.y);
		glfwGetWindowPos(mWindow, &mProperty.position.x, &mProperty.position.y);
		ProcessKeyboard();
	}

	void GlfwWindow::SwapBuffer()
	{
		if (mProperty.graphicApi == Opengl)
			glfwSwapBuffers(mWindow);
	}

	glm::ivec2 GlfwWindow::GetSize()
	{
		return mProperty.size;
	}

	bool GlfwWindow::mGlfwInitialized = false;
}