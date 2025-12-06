#pragma once
#include "Renderer/RenderCommand.hpp"
#include <glm/glm.hpp>


namespace Unknown
{
	class OpenglRenderCommand : public RenderCommand
	{
	public:
		void SetClearColor(const glm::vec4& color) override;
		void ClearColorBuffer() override;
		void ClearDepthBuffer() override;
		void DrawIndexed(int count, DrawPrimitive primitive = Triangle) override;
		void DrawArrays(int count, DrawPrimitive primitive = Triangle) override;
		void SetViewport(const glm::vec2& size, const glm::vec2& offset = glm::vec2(0, 0)) override;

		void EnableBlending() override;
		void EnableDepthTest() override;
		void EnableCulling() override;
		void EnableWireframe() override;

		void DisableBlending() override;
		void DisableDepthTest() override;
		void DisableCulling() override;
		void DisableWireframe() override;


		OpenglRenderCommand();
	};
}