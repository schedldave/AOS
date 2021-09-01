
# AOS/LFR: A Light-Field Renderer for Airborne Light Fields

This is a C++ implementation of the Light-Field Renderer for Airborne Optical Sectioning. 
It is based on OpenGL, uses [Dear ImGui](https://github.com/ocornut/imgui) and [GLFW](https://www.glfw.org/) for a basic user interface, and uses [Assimp](https://www.assimp.org/) to load a digital terrain.

## Changelog 🆕

- [x] Command line arguments and help with CLI11: you don't need to modify the main.cpp to load your own data.
- [x] CMakefile for building with vcpkg (tested under Windows).
- [x] Shaders are included as strings now. The 'shader' folder is not required anymore after compilation.

![alt text](../img/LFR.gif)

## [Python bindings](/LFR/python/)
We provide Python bindings, which make it easy to use the renderer in Python projects. To compile them follow the steps described in [`/LFR/python/README`](./python/README.md).

## Install
To compile the renderer with the GUI in native C++ follow the steps below:
### vcpkg and CMake:

Make sure that [vcpkg](https://github.com/microsoft/vcpkg) is installed and define an `VCPKG_ROOT` environment variable (it also works without the environment variable; just adjust the paths accordingly). 
Install `assimp` and `glfw3` via vcpkg.
To build the module, make [LFR](/LFR) the current directory and run the following Powershell commands:
```pwsh
mkdir build 
cd build
cmake .. "-DCMAKE_TOOLCHAIN_FILE=$env:VCPKG_ROOT\scripts\buildsystems\vcpkg.cmake"
cmake --build . --config=Release
cmake --install .
cd ../bin
```
The `bin` folder now contains an executable application `main`.

### Linux Make: 
Install [GLFW](https://www.glfw.org/) and compile [Assimp](https://www.assimp.org/) first. 
To build, make [LFR](/LFR) the current directory and run `make `.
After that, change the dir to `LFR/bin` and run `./main`. 

## Detailed usage and Parameters

You can use `-h` or `--help` to get details about the command line options.
```
 ./main -h
 > Options:
 > -h,--help                   Print this help message and exit
 > --fov FLOAT                 Field of view of the cameras in degrees.
 > --dem TEXT                  The path to the digital elevation model (DEM).
 > --pose TEXT                 The path to the poses in a json format.
 > --img TEXT                  The path to the images in POSES.
 > -r,--replaceTiff BOOLEAN    Replace .tiff with .png in the POSES file.
 > -z,--ztranslDEM FLOAT       Translate the DEM on the z axis.
 > -v,--view INT               view index for startup
``` 

Running `./bin/main` starts the application with the default parameters (i.e., the scene in `/AOS/data/F0`).


For further details take a look at  the C++ code [`/LFR/src/main.cpp`](/LFR/src/main.cpp).

## Dependencies
Our software builds on the following code/libraries/tools from:
- [Dear ImGui](https://github.com/ocornut/imgui) for the user interface
- [GLFW](https://www.glfw.org/) for opengl window creation
- [Assimp](https://www.assimp.org/) for digital terrain loading
- [Glad](https://glad.dav1d.de/) for opengl loading
- [learnopengl.com](https://learnopengl.com/) for handling shaders and meshes
- [GLM](https://github.com/g-truc/glm) for matrix/vector calculations
- [nlohmann/json](https://github.com/nlohmann/json) for reading and writing JSON files
- [stb_image](https://github.com/nothings/stb) for reading images


## ToDos/Wishlist

Some of the features that will be nice to have or are on our agenda for implementation:

- [ ] consider window size and aspect ratio for rendering (right now we use a default size e.g., 512x512 px)
- [ ] support for masking / alpha channels (e.g., to remove FLIR/DJI watermarks or text)
- [ ] render with RGB (3 channel) images. So far only grayscale has been tested.
- [ ] show a wireframe of the digital elevation model
- [ ] check if float32 ifdef is working on LINUX and older hardware
- [ ] Image loading: stb_image does not support TIFF so consider switching to FreeImage, SDL, or OpenCV
- [ ] Unittests in C++: https://cmake.org/cmake/help/latest/module/CTest.html  
- [ ] Disable the OpenGL Window when using the python binding: https://www.glfw.org/docs/latest/context.html#context_offscreen or https://github.com/glfw/glfw/issues/648
- [ ] Optimize min/max computation (used for displaying)
- [ ] Heatmap visualization
- [x] command line arguments: https://github.com/CLIUtils/CLI11#install 


## Ideas / Low priority

- [ ] OBJ loading: switch to a more lightweight loader (e.g., https://github.com/tinyobjloader/tinyobjloader) or keep Assimp
- [ ] optionally display a satelite image on the ground



