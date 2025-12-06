#include "Particle.hpp"

using namespace Unknown;
using namespace glm;

void Particle::UpdatePosition() 
{
    mAcceleration = mForce;
    mPositon += mVelocity;
    mVelocity += mAcceleration;
    mForce = vec3(0);
}
glm::vec3 Particle::GetColor()
{
	return mColor;
}
glm::vec3 Particle::GetForce()
{
	return mForce;
}
glm::vec3 Particle::GetAcceleration()
{
	return mAcceleration;
}
glm::vec3 Particle::GetVelocity()
{
	return mVelocity;
}
glm::vec3 Particle::GetPosition()
{
	return mPositon;
}
void Particle::AddForce(const glm::vec3 &force)
{
	mForce += force;
}
void Particle::SetColor(const glm::vec3 &color)
{
	mColor = color;
}
void Particle::SetForce(const glm::vec3 &force)
{
	mForce = force;
}
void Particle::SetAcceleration(const glm::vec3 &acceleration)
{
	mAcceleration = acceleration;
}
void Particle::SetVelocity(const glm::vec3 &velocity)
{
	mVelocity = velocity;
}
void Particle::SetPosition(const glm::vec3 &positon)
{
	mPositon = positon;
}
