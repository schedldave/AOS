# CMakeList.txt : CMake project for LFR_CMake, include source and define
# project specific logic here.
#
cmake_minimum_required (VERSION 3.8)





#SET(CMAKE_CONFIGURATION_TYPES ${CMAKE_BUILD_TYPE} CACHE STRING "" FORCE)
project (LFR)

#set(CMAKE_BUILD_TYPE Release)

# find packages using vcpkg
# make sure you set the DCMAKE_TOOLCHAIN_FILE to vcpkg
# e.g., cmake  --build .. "-DCMAKE_TOOLCHAIN_FILE=C:\dev\vcpkg\scripts\buildsystems\vcpkg.cmake"
find_package(assimp CONFIG REQUIRED)
find_package(glfw3 CONFIG REQUIRED)



file(GLOB LFR_SRC
     "./src/*.cpp"
     "./src/glad.c" 
     "./include/imgui/*.cpp"
) # see https://stackoverflow.com/questions/3201154/automatically-add-all-files-in-a-folder-to-a-target-using-cmake

# Add source to this project's executable.
add_executable (main  ${LFR_SRC})

target_include_directories(main PUBLIC "./include/" )

# assimp
target_link_libraries(main PUBLIC assimp::assimp)

# GLFW3
target_link_libraries(main PUBLIC glfw)

# TODO: Add tests and install targets if needed.
install(  TARGETS main 
          CONFIGURATIONS Release
          RUNTIME DESTINATION ${PROJECT_SOURCE_DIR}/bin)
#install(IMPORTED_RUNTIME_ARTIFACTS main DESTINATION ${PROJECT_SOURCE_DIR}/bin)
#install(RUNTIME_DEPENDENCY_SET main DESTINATION ${PROJECT_SOURCE_DIR}/bin)
# copy the dlls (only needed on windows)
install(DIRECTORY ${PROJECT_BINARY_DIR}/$<CONFIG>/ DESTINATION ${PROJECT_SOURCE_DIR}/bin FILES_MATCHING PATTERN "*.dll" )
