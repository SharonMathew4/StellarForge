#include "Types.hpp"
#include <glm/gtc/matrix_transform.hpp>

namespace Unknown
{
	glm::mat4 Transform::GetMatrix() const
	{
		glm::mat4 model = glm::mat4(1.f);
		model = glm::translate(model, position);
		model = glm::rotate(model, glm::radians(rotation.x), glm::vec3(1, 0, 0));
		model = glm::rotate(model, glm::radians(rotation.y), glm::vec3(0, 1, 0));
		model = glm::rotate(model, glm::radians(rotation.z), glm::vec3(0, 0, 1));
		model = glm::scale(model, scale);
		return model;
	}

}
