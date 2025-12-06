#include <print>
#include "ParticleSim.hpp"

using namespace glm;
using namespace Unknown;

vec3 ParticleSim::GetMouseWorldPosition()
{
    float aspectRatio = float(GetWindow()->GetSize().x) / float(GetWindow()->GetSize().y);
    vec2 pos = -((vec2(GetInput().mouse.position) / vec2(GetWindow()->GetSize()) * 2.f) - 1.f);
    pos.x *= aspectRatio;
    return vec3(pos, 0.f);
}

void ParticleSim::OnStart()
{
    for (int i = 0; i < 1000; i++) 
    {
        Particle particle;
        particle.SetPosition(Maths::RandomUnitVec3() * 2.f - 1.f);
        particle.SetColor(Maths::RandomUnitVec3());
        particles.push_back(particle);
    }
}

void ParticleSim::OnUpdate()
{
    UpdatePositions();
    Render();
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
        circle.color = vec4(particles[i].GetColor(), 1.f);
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
            vec3 force = normalize(GetMouseWorldPosition() - particle.GetPosition());
            particle.AddForce(force * 0.01f * GetTime().deltaTime);
        }
        particle.UpdatePosition();
    }    
}

void ParticleSim::OnEnd()
{
}

CREATE_APPLICATION(ParticleSim)
