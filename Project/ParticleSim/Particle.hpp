#pragma once 
#include "Engine.hpp"

class Particle
{

public:
	void SetPosition(const glm::vec3 &positon);
	void SetVelocity(const glm::vec3 &velocity);
	void SetAcceleration(const glm::vec3 &acceleration);
	void SetForce(const glm::vec3 &force);
	void SetColor(const glm::vec3 &color);

	void AddForce(const glm::vec3 &force);

	glm::vec3 GetPosition();
	glm::vec3 GetVelocity();
	glm::vec3 GetAcceleration();
	glm::vec3 GetForce();
	glm::vec3 GetColor();

	void UpdatePosition();

private:
	glm::vec3 mPositon = glm::vec3(0);
	glm::vec3 mVelocity = glm::vec3(0);
	glm::vec3 mAcceleration = glm::vec3(0);
	glm::vec3 mForce = glm::vec3(0);
	glm::vec3 mColor = glm::vec3(1);
};