#include <Core/Application.hpp>
#include <Core/EntryPoint.hpp>

int main(int argv, char** argc)
{
	Unknown::Application* application = Unknown::CreateApplication(argv, argc);
	application->Run();
	delete application;
	return 0;
}