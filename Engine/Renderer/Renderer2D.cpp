#include "Renderer2D.hpp"
#include <Core/Macro.hpp>
#include <sstream>

namespace Unknown
{

const char *quadrilateralVertexShader = R"(
	#version 450 core
	
	layout(location = 0) in vec3 aPos;
	layout(location = 1) in vec4 aColor;

	out vec4 color;

	uniform mat4 view;
	uniform mat4 projection;

	void main()
	{
		gl_Position = projection * view * vec4(aPos, 1.0);
		color = aColor;
	}
	)";

const char *quadrilateralFragmentShader = R"(
	#version 450 core
	
	out vec4 outputColor;

	in vec4 color;

	void main()
	{
		outputColor = color;
	}
	)";

const char *circleVertexShader = R"(
	#version 450 core
	
	layout(location = 0) in vec3 aPos;
	layout(location = 1) in vec4 aColor;
	layout(location = 2) in vec2 aUv;

	out vec4 color;
	out vec2 uv;

	uniform mat4 view;
	uniform mat4 projection;

	

	void main()
	{
		uv = aUv;
		gl_Position = projection * view * vec4(aPos, 1.0);
		color = aColor;
	}
	)";

const char *circleFragmentShader = R"(
	#version 450 core
	
	out vec4 outputColor;

	in vec4 color;
	in vec2 uv;

	void main()
	{

		outputColor = color; 		
		if(distance(vec2(0.5), uv) > 0.5)
			discard;
	}
	)";

const char *spriteVertexShader = R"(
	#version 450 core
	
	layout(location = 0) in vec3 aPos;
	layout(location = 1) in vec2 aUv;
	layout(location = 2) in vec2 aSpriteOffset;
	layout(location = 3) in ivec2 aSpriteIndex;
	layout(location = 4) in int aTextureSlot;

	out vec2 uv;
	flat out int slot; 

	uniform mat4 view;
	uniform mat4 projection;

	

	void main()
	{
		gl_Position = projection * view * vec4(aPos, 1.0);
		slot = aTextureSlot;
		uv = (aUv * aSpriteOffset) + vec2((aSpriteOffset * vec2(aSpriteIndex)));
	}
	)";

const char *spriteFragmentShader = R"(
	#version 450 core
	
	out vec4 outputColor;

	uniform sampler2D textures[32];

	in vec2 uv;
	flat in int slot; 

	void main()
	{
		outputColor = texture(textures[slot], uv);
	}
	)";

void Renderer2D::Initialize()
{
    mRenderCommand.reset(RenderCommand::Create());
    mQuadrilateralShader.reset(Shader::Create({quadrilateralVertexShader, quadrilateralFragmentShader}));
    mCircleShader.reset(Shader::Create({circleVertexShader, circleFragmentShader}));
    mSpriteShader.reset(Shader::Create({spriteVertexShader, spriteFragmentShader}));

    CameraProperty property;
    property.size.x = float(mViewport.size.x) / float(mViewport.size.y);
    property.size.y = float(mViewport.size.y) / float(mViewport.size.y); // = 1.f
    property.projectionType = CameraProjectionType::Orthographic;

    mCamera.SetProperty(property);
}

void Renderer2D::Terminate()
{
}

void Renderer2D::BeginFrame()
{
    mRenderCommand->ClearColorBuffer();
    CameraProperty property;
    property.size.x = float(mViewport.size.x) / float(mViewport.size.y);
    property.size.y = float(mViewport.size.y) / float(mViewport.size.y); // = 1.f
    property.projectionType = CameraProjectionType::Orthographic;

    mRenderCommand->SetViewport(mViewport.size, mViewport.position);

    mCamera.SetProperty(property);

    mCamera.Calculate();
}

void Renderer2D::EndFrame()
{
    Flush();
}

void Renderer2D::PushQuadrilateral(const Quadrilateral &quadrilateral)
{
    QuadrilateralVertex vertices[4];

    vertices[0].position = glm::vec3(0.5, 0.5, 0.0);
    vertices[1].position = glm::vec3(0.5, -0.5, 0.0);
    vertices[2].position = glm::vec3(-0.5, -0.5, 0.0);
    vertices[3].position = glm::vec3(-0.5, 0.5, 0.0);

    glm::mat4 transformMatrix = quadrilateral.transform.GetMatrix();

    for (int i = 0; i < sizeof(vertices) / sizeof(QuadrilateralVertex); i++)
    {

        vertices[i].position = glm::vec3(transformMatrix * glm::vec4(vertices[i].position, 1.0));
        vertices[i].color = quadrilateral.color;

        mQuadrilateralVertices.push_back(vertices[i]);
    }

    uint32_t quadrilateralCount = mQuadrilateralIndices.size() / 6;
    uint32_t indices[] = {0, 1, 2, 2, 3, 0};

    for (int i = 0; i < sizeof(indices) / sizeof(uint32_t); i++)
    {

        indices[i] = indices[i] + (quadrilateralCount * 4);
        mQuadrilateralIndices.push_back(indices[i]);
    }
}

void Renderer2D::PushCircle(const Circle &circle)
{
    CircleVertex vertices[4];

    vertices[0].position = glm::vec3(0.5, 0.5, 0.0);
    vertices[1].position = glm::vec3(0.5, -0.5, 0.0);
    vertices[2].position = glm::vec3(-0.5, -0.5, 0.0);
    vertices[3].position = glm::vec3(-0.5, 0.5, 0.0);

    vertices[0].uv = glm::vec2(1, 1);
    vertices[1].uv = glm::vec2(1, 0);
    vertices[2].uv = glm::vec2(0, 0);
    vertices[3].uv = glm::vec2(0, 1);

    glm::mat4 transformMatrix = circle.transform.GetMatrix();

    for (int i = 0; i < sizeof(vertices) / sizeof(CircleVertex); i++)
    {

        vertices[i].position = glm::vec3(transformMatrix * glm::vec4(vertices[i].position, 1.0));
        vertices[i].color = circle.color;

        mCircleVertices.push_back(vertices[i]);
    }

    uint32_t circleCount = mCircleIndices.size() / 6;
    uint32_t indices[] = {0, 1, 2, 2, 3, 0};

    for (int i = 0; i < sizeof(indices) / sizeof(uint32_t); i++)
    {

        indices[i] = indices[i] + (circleCount * 4);
        mCircleIndices.push_back(indices[i]);
    }
}

void Renderer2D::PushSprite(const Sprite &sprite)
{
    SpriteVertex vertices[4];

    vertices[0].position = glm::vec3(0.5, 0.5, 0.0);
    vertices[1].position = glm::vec3(0.5, -0.5, 0.0);
    vertices[2].position = glm::vec3(-0.5, -0.5, 0.0);
    vertices[3].position = glm::vec3(-0.5, 0.5, 0.0);

    vertices[0].uv = glm::vec2(1, 0);
    vertices[1].uv = glm::vec2(1, 1);
    vertices[2].uv = glm::vec2(0, 1);
    vertices[3].uv = glm::vec2(0, 0);

    vertices[0].spriteOffset = glm::vec2(1.f / sprite.spriteCount.x, 1.f / sprite.spriteCount.y);
    vertices[1].spriteOffset = glm::vec2(1.f / sprite.spriteCount.x, 1.f / sprite.spriteCount.y);
    vertices[2].spriteOffset = glm::vec2(1.f / sprite.spriteCount.x, 1.f / sprite.spriteCount.y);
    vertices[3].spriteOffset = glm::vec2(1.f / sprite.spriteCount.x, 1.f / sprite.spriteCount.y);

    vertices[0].spriteIndex = sprite.spriteIndex;
    vertices[1].spriteIndex = sprite.spriteIndex;
    vertices[2].spriteIndex = sprite.spriteIndex;
    vertices[3].spriteIndex = sprite.spriteIndex;

    vertices[0].textureSlot = mTextures.size();
    vertices[1].textureSlot = mTextures.size();
    vertices[2].textureSlot = mTextures.size();
    vertices[3].textureSlot = mTextures.size();

    mTextures.push_back(sprite.texture);

    glm::mat4 transformMatrix = sprite.transform.GetMatrix();

    for (int i = 0; i < sizeof(vertices) / sizeof(SpriteVertex); i++)
    {
        vertices[i].position = glm::vec3(transformMatrix * glm::vec4(vertices[i].position, 1.0));
        mSpriteVertices.push_back(vertices[i]);
    }

    uint32_t spriteCount = mSpriteIndices.size() / 6;
    uint32_t indices[] = {0, 1, 2, 2, 3, 0};

    for (int i = 0; i < sizeof(indices) / sizeof(uint32_t); i++)
    {
        indices[i] = indices[i] + (spriteCount * 4);
        mSpriteIndices.push_back(indices[i]);
    }

    if (mTextures.size() >= 32)
        FlushSprite();
}

void Renderer2D::Flush()
{
    FlushQuadrilateral();
    FlushCircle();
    FlushSprite();
}

void Renderer2D::FlushQuadrilateral()
{
    if (mQuadrilateralIndices.size() == 0)
        return;
    mQuadrilateralShader->Bind();
    mQuadrilateralVertexBuffer.reset(VertexBuffer::Create(mQuadrilateralVertices.size() * sizeof(QuadrilateralVertex), mQuadrilateralVertices.data()));
    mQuadrilateralIndexBuffer.reset(IndexBuffer::Create(mQuadrilateralIndices.size() * sizeof(uint32_t), mQuadrilateralIndices.data()));

    QuadrilateralVertex::SetVertexBufferLayout(mQuadrilateralVertexBuffer);

    mQuadrilateralVertexBuffer->Bind();
    mQuadrilateralIndexBuffer->Bind();
    glm::mat4 view = mCamera.GetViewMatrix();
    glm::mat4 projection = mCamera.GetProjectionMatrix();

    mQuadrilateralShader->SetUniform(Mat4, "view", &view);
    mQuadrilateralShader->SetUniform(Mat4, "projection", &projection);

    mRenderCommand->DrawIndexed(mQuadrilateralIndices.size());

    mQuadrilateralIndices.clear();
    mQuadrilateralVertices.clear();
}

void Renderer2D::FlushCircle()
{
    if (mCircleIndices.size() == 0)
        return;

    mCircleShader->Bind();
    mCircleVertexBuffer.reset(VertexBuffer::Create(mCircleVertices.size() * sizeof(CircleVertex), mCircleVertices.data()));
    mCircleIndexBuffer.reset(IndexBuffer::Create(mCircleIndices.size() * sizeof(uint32_t), mCircleIndices.data()));

    CircleVertex::SetVertexBufferLayout(mCircleVertexBuffer);

    mCircleVertexBuffer->Bind();
    mCircleIndexBuffer->Bind();

    glm::mat4 view = mCamera.GetViewMatrix();
    glm::mat4 projection = mCamera.GetProjectionMatrix();

    mCircleShader->SetUniform(Mat4, "view", &view);
    mCircleShader->SetUniform(Mat4, "projection", &projection);

    mRenderCommand->DrawIndexed(mCircleIndices.size());

    mCircleIndices.clear();
    mCircleVertices.clear();
}

void Renderer2D::FlushSprite()
{
    if (mSpriteIndices.size() == 0)
        return;

    mSpriteShader->Bind();
    mSpriteVertexBuffer.reset(VertexBuffer::Create(mSpriteVertices.size() * sizeof(SpriteVertex), mSpriteVertices.data()));
    mSpriteIndexBuffer.reset(IndexBuffer::Create(mSpriteIndices.size() * sizeof(uint32_t), mSpriteIndices.data()));

    SpriteVertex::SetVertexBufferLayout(mSpriteVertexBuffer);

    mSpriteVertexBuffer->Bind();
    mSpriteIndexBuffer->Bind();

    glm::mat4 view = mCamera.GetViewMatrix();
    glm::mat4 projection = mCamera.GetProjectionMatrix();

    mSpriteShader->SetUniform(Mat4, "view", &view);
    mSpriteShader->SetUniform(Mat4, "projection", &projection);

    for (int i = 0; i < mTextures.size(); i++)
    {
        mTextures[i]->Bind(i);
        std::ostringstream oss;
        oss << "textures[" << i << "]";

        mSpriteShader->SetUniform(Int, oss.str().c_str(), &i);
    }

    mRenderCommand->DrawIndexed(mSpriteIndices.size());

    mSpriteIndices.clear();
    mSpriteVertices.clear();
    mTextures.clear();
}

void Renderer2D::SetCamera(const Camera &camera)
{
    mCamera = camera;
}

const Camera &Renderer2D::GetCamera() const
{
    return mCamera;
}

void Renderer2D::SetViewport(const Viewport &viewport)
{
    mViewport = viewport;
}

const Viewport &Renderer2D::GetViewport() const
{
    return mViewport;
}

} // namespace Unknown
