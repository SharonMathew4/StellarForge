#pragma once
#include <glm/glm.hpp>

namespace Unknown
{
	enum DrawPrimitive
	{
		Triangle,
		Triangle_Strip,
		Triangle_Fan,
		Line,
		Line_Strip,
		Point
	};

	class RenderCommand
	{
	public:
		virtual void SetClearColor(const glm::vec4& color) = 0;
		virtual void SetViewport(const glm::vec2& size, const glm::vec2& offset = glm::vec2(0, 0)) = 0;

		virtual void ClearColorBuffer() = 0;
		virtual void ClearDepthBuffer() = 0;

		virtual void DrawIndexed(int count, DrawPrimitive primitive = Triangle) = 0;
		virtual void DrawArrays(int count, DrawPrimitive primitive = Triangle) = 0;


		virtual void EnableBlending() = 0;
		virtual void EnableDepthTest() = 0;
		virtual void EnableCulling() = 0;
		virtual void EnableWireframe() = 0;

		virtual void DisableBlending() = 0;
		virtual void DisableDepthTest() = 0;
		virtual void DisableCulling() = 0;
		virtual void DisableWireframe() = 0;
		static RenderCommand* Create();
	};
}