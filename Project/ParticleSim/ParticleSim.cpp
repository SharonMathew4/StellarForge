#include <print>
#include "ParticleSim.hpp"

using namespace glm;
using namespace Unknown;

vec3 ParticleSim::GetMouseWorldPosition(const CameraProperty& property)
{
    float aspectRatio = float(GetWindow()->GetSize().x) / float(GetWindow()->GetSize().y);
    vec2 pos = -((vec2(GetInput().mouse.position) / vec2(GetWindow()->GetSize()) * 2.f) - 1.f);
    pos.x *= aspectRatio;
    pos *= property.zoom;
    pos += vec2(property.position);
    return vec3(pos, 0.f);
}

void ParticleSim::OnStart()
{
    int count = 10000;
    for (int i = 0; i < count; i++) 
    {
        float p = float(i) / float(count);
        Particle particle;
        particle.SetPosition(vec3(Maths::RandomUnitVec2(), 0.f));
        particle.SetColor(Maths::RandomUnitVec3());
        particles.push_back(particle);
    }
}

void ParticleSim::OnUpdate()
{
    ProcessInput();
    UpdatePositions();
    Render();

    std::println("scroll {} {}", GetInput().mouse.scroll.x, GetInput().mouse.scroll.y);
}

void ParticleSim::Render()
{
    Viewport viewport;
    viewport.position = vec2(0);
    viewport.size = GetWindow()->GetSize();
    GetRenderer2D()->BeginFrame();
    GetRenderer2D()->SetViewport(viewport);

    for (int i = 0; i < particles.size(); i++) 
    {
        Circle circle;
        circle.transform.position = particles[i].GetPosition();
        circle.transform.scale = vec3(0.01f);


        vec3 gradiant1 = Maths::HexRGBA(0xdb376dff);
        vec3 gradiant2 = Maths::HexRGBA(0x1b4ca2ff);

        circle.color = vec4(particles[i].GetColor(), 1.f);

        std::println("test: {}", length(particles[i].GetVelocity()));

        GetRenderer2D()->PushCircle(circle);
    }

    GetRenderer2D()->EndFrame();
}



void ParticleSim::UpdatePositions() 
{
    for (Particle& particle : particles) 
    {
        if(GetInput().mouse.leftPress)
        {
            float d = distance(GetMouseWorldPosition(GetRenderer2D()->GetCamera().GetProperty()), particle.GetPosition());
            vec3 force = normalize(GetMouseWorldPosition(GetRenderer2D()->GetCamera().GetProperty()) - particle.GetPosition());
            force.z = 0;
            particle.AddForce(((force * 0.01f)) * GetTime().deltaTime);
        }
        if(GetInput().mouse.rightPress)
        {
            vec3 force = normalize(particle.GetPosition() - GetMouseWorldPosition(GetRenderer2D()->GetCamera().GetProperty()));
            force.z = 0;
            particle.AddForce(force * 0.01f * GetTime().deltaTime);
        }
        particle.UpdatePosition();
    }    
}

void ParticleSim::ProcessInput() 
{
	ProcessMouseInput();
    ProcessKeyboardInput();
}

void ParticleSim::ProcessMouseInput() 
{
    Camera camera = GetRenderer2D()->GetCamera();
    CameraProperty property = camera.GetProperty();
	MouseInput mouse = GetInput().mouse;


    property.zoom += mouse.scroll.y;
    if(property.zoom >= -1.f)
        property.zoom = -1.f;

    if(mouse.middlePress)
    {
        property.position.x += mouse.offset.x * 0.01f * GetRenderer2D()->GetCamera().GetProperty().zoom;
        property.position.y += mouse.offset.y * 0.01f * GetRenderer2D()->GetCamera().GetProperty().zoom;
    }

    camera.SetProperty(property);
    GetRenderer2D()->SetCamera(camera);
    
}

void ParticleSim::ProcessKeyboardInput() 
{
    KeyboardInput keyboard = GetInput().keyboard;
	if(keyboard.keyK)
    {
        for (Particle& particle : particles) 
        {
            particle.SetVelocity(vec3(0));            
        }
    }
}

void ParticleSim::OnEnd()
{
}

CREATE_APPLICATION(ParticleSim)
