# AOS-LFR: A light-field renderer for airborne light fields. 

A light-field renderer for airborne light fields as used in the [Airborne Optical Sectioning](#publications) technique.

This repository contains updates and improvements for the LFR module of the [JKU-ICG/AOS](https://github.com/JKU-ICG/AOS) repository. 
Note that the original [JKU-ICG/AOS](https://github.com/JKU-ICG/AOS) repository contains several modules, whereas this repo just focuses on light-field rendering. 
The algorithms are implemented with C++ and Python code.

This repository also contains new and experimental features and thus might not work with the original implementation at [JKU-ICG/AOS](https://github.com/JKU-ICG/AOS)! 

### Changelog | Recent Changes 

- [x] vcpkg based setup
- [x] RGB image loading works
- [x] Command line arguments and help with CLI11: you don't need to modify the main.cpp to load your own data.
- [x] CMakefile for building with vcpkg (tested under Windows).
- [x] Shaders are included as strings now. The 'shader' folder is not required anymore after compilation.
- [x] support for masking / alpha channels (e.g., to remove watermarks, timestamps or any other text)

### ToDos/Wishlist and Ideas for New Features

<details><summary><b>CLICK ME</b> to see new features that are on our agenda</summary>

- [ ] use gladUnload to recover if window has closed in python: https://github.com/Dav1dde/glad
- [ ] fallback to a simple plane if no DEM is loaded or DEM loading fails.
- [ ] verify installation on Linux (and MacOS).
- [ ] consider window size and aspect ratio for rendering (right now we use a default size e.g., 512x512 px)
- [ ] show a wireframe of the digital elevation model
- [ ] check if float32 ifdef is working on LINUX and older hardware
- [ ] Image loading: stb_image does not support TIFF so consider switching to SAIL, FreeImage, SDL, or OpenCV
- [ ] Unittests in C++: https://cmake.org/cmake/help/latest/module/CTest.html  
- [ ] Disable the OpenGL Window when using the python binding: https://www.glfw.org/docs/latest/context.html#context_offscreen or https://github.com/glfw/glfw/issues/648. DOES NOT WORK!
- [ ] Optimize min/max computation (used for displaying)
- [ ] Heatmap visualization for grayscale images
- [ ] OBJ loading: switch to a more lightweight loader with less dependencies (e.g., https://github.com/tinyobjloader/tinyobjloader) or keep Assimp
- [ ] optionally display a satellite image on the ground
</details>

# Installation
Building is based on the vcpkg package manager. Make sure that you have a compatible compiler installed (e.g. Visual Studio).

## Requirements
Then install [vcpkg](https://github.com/microsoft/vcpkg) and define an `VCPKG_ROOT` environment variable that points to your vcpkg installation. 
Then install all necessary dependencies/libraries by running: 
```pwsh
vcpkg install cli11 nlohmann-json stb glm imgui[core,glfw-binding,opengl3-binding] glfw3 glad assimp --triplet x64-windows       
```
Note that you might need to change the `triplet` parameter if you are on a different system. 
#### Dependencies
<details><summary><b>CLICK ME</b> to see why the dependencies are needed</summary>

- [Dear ImGui](https://github.com/ocornut/imgui) for the user interface
- [GLFW](https://www.glfw.org/) for opengl window creation
- [Assimp](https://www.assimp.org/) for digital terrain loading
- [Glad](https://glad.dav1d.de/) for opengl loading
- [learnopengl.com](https://learnopengl.com/) for handling shaders and meshes
- [GLM](https://github.com/g-truc/glm) for matrix/vector calculations
- [nlohmann/json](https://github.com/nlohmann/json) for reading and writing JSON files
- [stb](https://github.com/nothings/stb) for reading/writing images
- [CLI11](https://github.com/CLIUtils/CLI11) for parsing command line arguments
</details>

---
## LFR Application (C++)
To compile the renderer with the GUI in native C++ clone this repository and follow the steps below:
### Compile using vcpkg and CMake:

Make sure that you have a compiler, [vcpkg](https://github.com/microsoft/vcpkg) and the [required libraries](#installation) installed. 
To build the module, make [LFR](/LFR) the current directory and run the following Powershell commands:
```pwsh
mkdir build 
cd build
cmake .. "-DCMAKE_TOOLCHAIN_FILE=$env:VCPKG_ROOT\scripts\buildsystems\vcpkg.cmake"
cmake --build . --config=Release
cmake --install .
cd ../bin
```
The `bin` folder now contains an executable application `LFR`.
Running `./bin/LFR` starts the application with some default parameters (i.e., the example scene in `data`).

### Compile using Visual Studio

Integrate vcpkg into Visual Studio with:
```pwsh
vcpkg integrate install
```
All installed libraries should now be discoverable by IntelliSense and usable in code without additional configuration.
Just open the project or solution file in the `VS` folder and compile the `LFR` application.

### Detailed Usage and Parameters

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

For further details take a look at  the C++ code [`src/main.cpp`](./src/main.cpp).


---
## Python Bindings 

The python wrapper renders images in the `numpy` format that is also used by OpenCV. 
The build process is based on Phyton's setuptools and uses Cython. Make sure that vcpkg and [the C++ dependencies](#requirements), and the [Python dependencies](pyaos/requirements.txt) are installed.

Note that a GLFW3 window with an OpenGL context opens in the background every time the module runs. Therefore, this will most likely not work on headless systems (without monitors).

### Install using PIP

To install the python bindings as python package directly from Github run:
```pwsh
pip install git+https://github.com/schedldave/AOS
```


Optionally compile the Python bindings by cloning this repository and running the following command in the root folder:
```pwsh
pip install .
```
This has been tested on Windows and needs verification on Linux. 
Make sure that you close Visual Studio before running `pip install`.



### Quick tutorial
```py
import pyaos.lfr as LFR
r,w,fovDegrees = 512,512,50 # resolution and field of view

# initialize an OpenGL context and window
window = LFR.PyGlfwWindow( r, w, 'AOS' ) 

# init the light-field renderer
aos = LFR.PyAOS( r, w, fovDegrees )
# upload a digital terrain in an OBJ format
aos.loadDEM( "../data/plane.obj" )

# add (mutiple) single images (single image, pose, name)
aos.addView( img, pose, "01" )
# ...

# compute integral images at a virtual position
rimg = aos.render( vpose, fovDegrees )
```

### Detailed Usage

Please take a look at [`/pyaos/sample.py`](./pyaos/sample.py) file in the repository for a complex example.

The `./pyaos/LFR_utils.py` file provides additional auxiliary functions for initializing the light-field renderer, uploading poses and images, and for modifying poses (e.g., to virtual camera positions needed for integration).

`./pyaos/pyaos_test.py` is a unit test written in Python's `unittest` framework. To verify that the code compiled correctly, just run the unit test. Make sure that the working directory is set to `./pyaos/` so that the data is loaded correctly.



---
# Details about Airborne Optical Sectioning

Airborne Optical Sectioning (AOS) is a wide synthetic-aperture imaging technique that employs manned or unmanned aircraft, to sample images within large (synthetic aperture) areas from above occluded volumes, such as forests. Based on the poses of the aircraft during capturing, these images are computationally combined to integral images by light-field technology. These integral images suppress strong occlusion and reveal targets that remain hidden in single recordings.

Single Images         |  Airborne Optical Sectioning
:-------------------------:|:-------------------------:
![single-images](./img/Nature_single-images.gif) | ![AOS](./img/Nature_aos.gif)

> Source: [Video on YouTube](https://www.youtube.com/watch?v=kyKVQYG-j7U) | [FLIR](https://www.flir.com/discover/cores-components/researchers-develop-search-and-rescue-technology-that-sees-through-forest-with-thermal-imaging/)

## Publications
- David C. Schedl, Indrajit Kurmi, and Oliver Bimber, *Autonomous Drones for Search and Rescue in Forests*, Science Robotics, (2021)
- David C. Schedl, Indrajit Kurmi, and Oliver Bimber, *Search and rescue with airborne optical sectioning*, Nature Machine Intelligence, (2020)
- ...
<details><summary><b>CLICK ME</b> to see full details and more publications</summary>

- Indrajit Kurmi, David C. Schedl, and Oliver Bimber, Combined People Classification with Airborne Optical Sectioning, IEEE SENSORS JOURNAL (under review), (2021)
  - [arXiv (pre-print)](https://arxiv.org/abs/2106.10077)  
  - [Data: ](https://doi.org/10.5281/zenodo.5013640)[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5013640.svg)](https://doi.org/10.5281/zenodo.5013640)
- David C. Schedl, Indrajit Kurmi, and Oliver Bimber, Autonomous Drones for Search and Rescue in Forests, Science Robotics 6(55), eabg1188, https://doi.org/10.1126/scirobotics.abg1188, (2021)
  - [Science (final version)](https://robotics.sciencemag.org/content/6/55/eabg1188)
  - [arXiv (pre-print)](https://arxiv.org/pdf/2105.04328)  
  - [Data: ](https://doi.org/10.5281/zenodo.4349220) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4349220.svg)](https://doi.org/10.5281/zenodo.4349220)
  - [Video on YouTube](https://www.youtube.com/watch?v=ebk7GQH5ltk)
- David C. Schedl, Indrajit Kurmi, and Oliver Bimber, Search and rescue with airborne optical sectioning, Nature Machine Intelligence 2, 783-790, https://doi.org/10.1038/s42256-020-00261-3 (2020)
  - [Nature (final version)](https://www.nature.com/articles/s42256-020-00261-3) | [(view only version)](https://rdcu.be/cbcf2) 
  - [arXiv (pre-print)](https://arxiv.org/pdf/2009.08835.pdf)
  - [Data: ](https://doi.org/10.5281/zenodo.3894773) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3894773.svg)](https://doi.org/10.5281/zenodo.3894773)
  - [Video on YouTube](https://www.youtube.com/watch?v=kyKVQYG-j7U)
- Indrajit Kurmi, David C. Schedl, and Oliver Bimber, Pose Error Reduction for Focus Enhancement in Thermal Synthetic Aperture Visualization, IEEE Geoscience and Remote Sensing Letters, DOI: https://doi.org/10.1109/LGRS.2021.3051718 (2021).
  - [IEEE (final version)](https://ieeexplore.ieee.org/document/9340240) 
  - [arXiv (pre-print)](https://arxiv.org/abs/2012.08606)
- Indrajit Kurmi, David C. Schedl, and Oliver Bimber, Fast automatic visibility optimization for thermal synthetic aperture visualization, IEEE Geosci. Remote Sens. Lett. https://doi.org/10.1109/LGRS.2020.2987471 (2020).
  - [IEEE (final version)](https://ieeexplore.ieee.org/document/9086501) 
  - [arXiv (pre-print)](https://arxiv.org/abs/2005.04065)
  - [Video on YouTube](https://www.youtube.com/watch?v=39GU1BOCfWQ&ab_channel=JKUInstituteofComputerGraphics)
- David C. Schedl, Indrajit Kurmi, and Oliver Bimber, Airborne Optical Sectioning for Nesting Observation. Sci Rep 10, 7254, https://doi.org/10.1038/s41598-020-63317-9 (2020).
  - [Nature (open access and final version)](https://www.nature.com/articles/s41598-020-63317-9) 
  - [Video on YouTube](www.youtube.com/watch?v=81l-Y6rVznI)
- Indrajit Kurmi, David C. Schedl, and Oliver Bimber, Thermal airborne optical sectioning. Remote Sensing. 11, 1668, https://doi.org/10.3390/rs11141668, (2019).
  - [MDPI (open access and final version)](https://www.mdpi.com/2072-4292/11/14/1668) 
  - [Video on YouTube](https://www.youtube.com/watch?v=_t2GEwA_tus&ab_channel=JKUCG)
- Indrajit Kurmi, David C. Schedl, and Oliver Bimber, A statistical view on synthetic aperture imaging for occlusion removal. IEEE Sensors J. 19, 9374 – 9383 (2019).
  - [IEEE (final version)](https://ieeexplore.ieee.org/document/8736348)
  - [arXiv (pre-print)](https://arxiv.org/abs/1906.06600) 
- Oliver Bimber, Indrajit Kurmi, and David C. Schedl, Synthetic aperture imaging with drones. IEEE Computer Graphics and Applications. 39, 8 – 15 (2019).
  - [IEEE (open access and final version)](https://doi.ieeecomputersociety.org/10.1109/MCG.2019.2896024) 
- Indrajit Kurmi, David C. Schedl, and Oliver Bimber, Airborne optical sectioning. Journal of Imaging. 4, 102 (2018).
  - [MDPI (open access and final version)](https://www.mdpi.com/2313-433X/4/8/102)
  - [Video on YouTube](https://www.youtube.com/watch?v=ELnvBfafnRA&ab_channel=JKUCG) 

</details>

---
# License / Copyright

This code is based on the [JKU-ICG/AOS](https://github.com/JKU-ICG/AOS) repository that is published under a free for non-commercial use license (commerical use is restricted; see the original repository for details). I am making my changes publicly available to researchers. The implementation may be used for academic and research purposes, but not to be used for commercial purposes, nor should they appear in a product for sale without my permission. </br>
**Copyright: [Dr. David C. Schedl](mailto:david.schedl@fh-hagenberg.at)** </br>


