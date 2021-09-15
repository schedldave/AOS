# CMakeList.txt : CMake project for LFR_CMake, include source and define
# project specific logic here.
#
cmake_minimum_required (VERSION 3.8)





#SET(CMAKE_CONFIGURATION_TYPES ${CMAKE_BUILD_TYPE} CACHE STRING "" FORCE)
project (main)

#set(CMAKE_BUILD_TYPE Release)

# find packages using vcpkg
# make sure you set the DCMAKE_TOOLCHAIN_FILE to vcpkg
# e.g., cmake  --build .. "-DCMAKE_TOOLCHAIN_FILE=C:\dev\vcpkg\scripts\buildsystems\vcpkg.cmake"
find_package(assimp CONFIG REQUIRED)
find_package(glfw3 CONFIG REQUIRED)
find_package(CLI11 CONFIG REQUIRED)
find_package(glad CONFIG REQUIRED)
find_package(glm CONFIG REQUIRED)
find_package(nlohmann_json CONFIG REQUIRED)
find_package(imgui CONFIG REQUIRED)
find_path(STB_INCLUDE_DIRS "stb.h")


file(GLOB LFR_SRC
     "./src/*.cpp"
) # see https://stackoverflow.com/questions/3201154/automatically-add-all-files-in-a-folder-to-a-target-using-cmake

# Add source to this project's executable.
add_executable (main  ${LFR_SRC})

target_include_directories(main PRIVATE "./include/" )
target_include_directories(main PRIVATE ${STB_INCLUDE_DIRS})

target_link_libraries(main PRIVATE assimp::assimp)
target_link_libraries(main PRIVATE glfw)
target_link_libraries(main PRIVATE CLI11::CLI11)
target_link_libraries(main PRIVATE glad::glad)
target_link_libraries(main PRIVATE glm::glm)
target_link_libraries(main PRIVATE nlohmann_json nlohmann_json::nlohmann_json)
target_link_libraries(main PRIVATE imgui::imgui)

set_target_properties(
    main
    PROPERTIES 
        OUTPUT_NAME "LFR" # override output name
)

# TODO: Add tests and install targets if needed.
install(  TARGETS main 
          CONFIGURATIONS Release
          RUNTIME DESTINATION ${PROJECT_SOURCE_DIR}/bin)

# copy the dlls (only needed on windows)
install(DIRECTORY ${PROJECT_BINARY_DIR}/$<CONFIG>/ DESTINATION ${PROJECT_SOURCE_DIR}/bin FILES_MATCHING PATTERN "*.dll" )
