#pragma once
#include <glm/glm.hpp>

namespace Unknown
{
enum class CameraType
{
    Orbital,
    FirstPerson
};
enum class CameraProjectionType
{
    Perspective,
    Orthographic
};

struct CameraProperty
{
    CameraType type = CameraType::FirstPerson;
    CameraProjectionType projectionType = CameraProjectionType::Perspective;
    float fov = 90.f;
    glm::vec2 size = {800.f, 600.f};
    float nearPlane = 0.01f;
    float farPlane = 100.f;
    glm::vec3 position = glm::vec3(0.f, 0.f, -1.f);
    glm::vec3 lookAt = glm::vec3(0.f, 0.f, 1.f);
    glm::vec3 up = glm::vec3(0.f, 1.f, 0.f);
    float zoom = 1.f;
};

class Camera
{
  public:
    CameraProperty GetProperty() const;
    glm::mat4 GetViewMatrix() const;
    glm::mat4 GetProjectionMatrix() const;

    void SetProperty(const CameraProperty &property);
    void SetViewMatrix(const glm::mat4 &view);
    void SetProjectionMatrix(const glm::mat4 &projection);

    void Calculate();

  private:
    glm::mat4 mProjectionMatrix = glm::mat4(1.f);
    glm::mat4 mViewMatrix = glm::mat4(1.f);
    CameraProperty mProperty;

  public:
    CameraProperty &GetPropertyRef();
};
} // namespace Unknown
