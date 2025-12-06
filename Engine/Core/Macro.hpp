#include <print>
#include <filesystem>

#define UNK_ENABLE_PRINT_MACROS 1
#define UNK_ENABLE_ASSERT 1
#define UNK_ENABLE_FILE_CHECK 1

///////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////    LOGGING    ///////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////

#if UNK_ENABLE_PRINT_MACROS
#define UNK_CORE_LOG(...)\
        std::print("core log: ")\
        std::print(__VA_ARGS__)\
        std::print("\n");
#define UNK_CORE_WARN(...)\
        std::print("core warn: ");\
        std::print(__VA_ARGS__);\
        std::print("\n");
#define UNK_CORE_ERROR(...)\
        std::print("core error: ")\
        std::print(__VA_ARGS__);\
        std::print("\n");
#define UNK_CORE_FATAL(...)\
        std::print("core fatal: ")\
        std::print(f__VA_ARGS__);\
        std::print("\n");

#define UNK_CLIENT_LOG(...)\
        std::print("client log: ");\
        std::print(__VA_ARGS__);\
        std::print("\n");
#define UNK_CLIENT_WARN(...)\
        std::print("client warn: ");\
        std::print(__VA_ARGS__);\
        std::print("\n");
#define UNK_CLIENT_ERROR(...)\
        std::print("client error: ");\
        std::print(__VA_ARGS__);\
        std::print("\n");
#define UNK_CLIENT_FATAL(...)\
        std::print("client fatal: ");\
        std::print(__VA_ARGS__);\
        std::print("\n");
#else
#define UNK_CORE_LOG(...)
#define UNK_CORE_WARN(...)
#define UNK_CORE_ERROR(...)
#define UNK_CORE_FATAL(...)

#define UNK_CLIENT_LOG(...)
#define UNK_CLIENT_WARN(...)
#define UNK_CLIENT_ERROR(...)
#define UNK_CLIENT_FATAL(...)
#endif

///////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////    ASSERTION    /////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////

#if UNK_ENABLE_ASSERT
#define UNK_CORE_ASSERT(message, expression)\
        if ((expression) == false)\
        {\
            std::println("core assert: {} {}", message, #expression);\
            assert(expression);\
        }


#define UNK_CLIENT_ASSERT(message, expression)\
        if ((expression) == false)\
        {\
            std::println("client assert: {} {}", message, #expression);\
            assert(expression);\
        }
#else
#define UNK_CORE_ASSERT(message, expression)
#define UNK_CLIENT_ASSERT(message, expression)
#endif

///////////////////////////////////////////////////////////////////////////////////////////////
/////////////////////////////////    FILE CHECK    ////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////////

#if UNK_ENABLE_FILE_CHECK

#define UNK_CORE_CHECK_FILE_EXIST(filename) \
        if (!std::filesystem::exists(filename))\
        {\
	        std::println("core error: file not found {}", filename);\
        }

#define UNK_CLIENT_CHECK_FILE_EXIST(filename) \
        if (!std::filesystem::exists(filename))\
        {\
	        std::println("client error: file not found {}", filename);\
        }
#else
#define UNK_CORE_CHECK_FILE_EXIST(filename)
#define UNK_CLIENT_CHECK_FILE_EXIST(filename) 
#endif

// helpful for printing 

#define UNK_EXPAND_VEC2(vec) vec.x, vec.y
#define UNK_EXPAND_VEC3(vec) vec.x, vec.y, vec.z
#define UNK_EXPAND_VEC4(vec) vec.x, vec.y, vec.z, vec.w
