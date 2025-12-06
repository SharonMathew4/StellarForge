#include "OpenglRenderCommand.hpp"
#include <glad/glad.h>

namespace Unknown
{
	static GLenum openglPrimitives[] =
	{
		GL_TRIANGLES,
		GL_TRIANGLE_STRIP,
		GL_TRIANGLE_FAN,
		GL_LINE,
		GL_LINE_STRIP,
		GL_POINT
	};

	RenderCommand* RenderCommand::Create()
	{
		return new OpenglRenderCommand();
	}


	void OpenglRenderCommand::SetClearColor(const glm::vec4& color)
	{
		glClearColor(color.r, color.g, color.b, color.a);
	}

	void OpenglRenderCommand::ClearColorBuffer()
	{
		glClear(GL_COLOR_BUFFER_BIT);
	}

	void OpenglRenderCommand::ClearDepthBuffer()
	{
		glClear(GL_DEPTH_BUFFER_BIT);
	}

	void OpenglRenderCommand::DrawIndexed(int count, DrawPrimitive primitive)
	{
		glDrawElements(openglPrimitives[primitive], count, GL_UNSIGNED_INT, nullptr);
	}

	void OpenglRenderCommand::DrawArrays(int count, DrawPrimitive primitive)
	{
		glDrawArrays(openglPrimitives[primitive], 0, count);
	}


	void OpenglRenderCommand::SetViewport(const glm::vec2& size, const glm::vec2& offset /*= glm::vec2(0, 0)*/)
	{
		glViewport(offset.x, offset.y, size.x, size.y);
	}

	void OpenglRenderCommand::EnableBlending()
	{
		glEnable(GL_BLEND);
		glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
	}

	void OpenglRenderCommand::EnableDepthTest()
	{
		glEnable(GL_DEPTH_TEST);
	}

	void OpenglRenderCommand::EnableCulling()
	{
		glEnable(GL_CULL_FACE);
	}

	void OpenglRenderCommand::EnableWireframe()
	{
		glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
	}

	void OpenglRenderCommand::DisableBlending()
	{
		glDisable(GL_BLEND);
	}

	void OpenglRenderCommand::DisableDepthTest()
	{
		glDisable(GL_DEPTH_TEST);

	}

	void OpenglRenderCommand::DisableCulling()
	{
		glDisable(GL_CULL_FACE);
	}

	void OpenglRenderCommand::DisableWireframe()
	{
		glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
	}

	OpenglRenderCommand::OpenglRenderCommand()
	{

	}

}
