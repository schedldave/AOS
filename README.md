# AOS-LFR: A light-field renderer for airborne light fields.

A light-field renderer for airborne light fields.
This repository contains updates and improvements for the LFR module of [JKU's AOS](https://github.com/JKU-ICG/AOS) repository. 
Note that the original [JKU's AOS](https://github.com/JKU-ICG/AOS) repository contains several modules, whereas this repo just focuses on light-field rendering. 
The algorithms are implemented with C++ and Python code.

🐛🐞 This repository also contains experimental features and thus might be buggy or broken. If you are looking for something stable, use [JKU's AOS](https://github.com/JKU-ICG/AOS)!

🆕 For a list of updates see the [changelog](LFR/README#changelog).

## AOS: Airborne Optical Sectioning

Airborne Optical Sectioning (AOS) is a wide synthetic-aperture imaging technique that employs manned or unmanned aircraft, to sample images within large (synthetic aperture) areas from above occluded volumes, such as forests. Based on the poses of the aircraft during capturing, these images are computationally combined to integral images by light-field technology. These integral images suppress strong occlusion and reveal targets that remain hidden in single recordings.

Single Images         |  Airborne Optical Sectioning
:-------------------------:|:-------------------------:
![single-images](./img/Nature_single-images.gif) | ![AOS](./img/Nature_aos.gif)

> Source: [Video on YouTube](https://www.youtube.com/watch?v=kyKVQYG-j7U) | [FLIR](https://www.flir.com/discover/cores-components/researchers-develop-search-and-rescue-technology-that-sees-through-forest-with-thermal-imaging/)
 

## Related-Publications

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

## Installation
 
For installation instructions refer to the [README in LFR](LFR/README.md).

## License
* Code Modules: You are free to modify and use the software non-commercially; For commercial usage refer to the [original LICENSE](https://github.com/JKU-ICG/AOS/blob/stable_release/LICENSE.txt).

