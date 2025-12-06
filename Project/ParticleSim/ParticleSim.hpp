
#include <Engine.hpp>

class Particle
{

public:
	void SetPosition(const glm::vec3 &positon)
	{
		mPositon = positon;
	}
	void SetVelocity(const glm::vec3 &velocity)
	{
		mVelocity = velocity;
	}
	void SetAcceleration(const glm::vec3 &acceleration)
	{
		mAcceleration = acceleration;
	}
	void SetForce(const glm::vec3 &force)
	{
		mForce = force;
	}
	void SetColor(const glm::vec3 &color)
	{
		mColor = color;
	}

	void AddForce(const glm::vec3 &force)
	{
		mForce += force;
	}

	glm::vec3 GetPosition()
	{
		return mPositon;
	}
	glm::vec3 GetVelocity()
	{
		return mVelocity;
	}
	glm::vec3 GetAcceleration()
	{
		return mAcceleration;
	}
	glm::vec3 GetForce()
	{
		return mForce;
	}
	glm::vec3 GetColor()
	{
		return mColor;
	}

    void UpdatePosition();

private:
	glm::vec3 mPositon = glm::vec3(0);
	glm::vec3 mVelocity = glm::vec3(0);
	glm::vec3 mAcceleration = glm::vec3(0);
	glm::vec3 mForce = glm::vec3(0);
	glm::vec3 mColor = glm::vec3(1);
};

class ParticleSim : public Unknown::Application
{
	std::vector<Particle> particles;

	void OnStart() override;
	void OnUpdate() override;
	void OnEnd() override;

	void Render();
    void UpdatePositions();

    glm::vec3 GetMouseWorldPosition();
};
