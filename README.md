# Autostereogram-OpenGL-Python

## Goals
Implement a rendering system capable of loading three-dimensional objects, extracting a real-time depth map from the rendered scene, and synthesizing an autostereogram based on the generated camera view.

To achieve this, the project defines the following core milestones:
- Set up a 3D rendering environment to load and display external 3D models.
- Implement interactive camera movement.
- Extract and visualize the scene's depth map (Z-buffer).
- Develop the stereogram synthesis algorithm to generate autostereograms from the depth map.

## Design Decisions
- **Target Domain:** Archetypes Depth Map
- **Application Chapter:** Depth Map & Stereo

The core domain of this project focuses on **Archetypes Depth Map**, placing special emphasis on the **Depth Map** and **Stereo** chapters. The project is structured into two main sections:

1. **3D Environment & Depth Map Generation:** The first section implements a rendering environment to load 3D objects and extract depth maps from the active camera view. **PyOpenGL** was selected for this stage due to the extensive availability of documentation and tutorials (primarily guided by AtiByte’s YouTube channel). For simplicity, the loaded 3D model remains static while camera movement handles perspective shifts.
2. **Autostereogram Synthesis:** The second section focuses on generating the autostereogram. This approach builds upon concepts covered in the **Stereo** chapter, creating a 3D illusion without requiring two simultaneous views. Instead, it utilizes a single image combined with the repetition of a simple (or random) pattern. *Note: This section is currently under development; therefore, definitive design decisions for this module have not yet been finalized.*

## Outcomes and Future Work
- **Outcomes:** Successfully established the OpenGL rendering environment and achieved proper loading and visualization of 3D models. Core scene setup is functional, setting the foundation for the remaining pipeline stages.
- **Future Work:** 
  - **Depth Map Extraction:** Implement framebuffer capture and linearization of the Z-buffer to generate an accurate grayscale depth map from the active camera perspective.
  - **Autostereogram Synthesis:** Build the image-processing module to map pixel disparity from the extracted depth map and render the final autostereogram output.

## References
- De Vries, J. (n.d.). *Learn OpenGL: Extensive tutorial resource for learning Modern OpenGL*. LearnOpenGL. https://learnopengl.com
- Toth, A. (n.d.). *Learn-OpenGL-in-python: All the source codes from my YouTube tutorial series called “OpenGL in Python”* [Source code]. GitHub.
- AtiByte. (n.d.). *AtiByte* [YouTube channel]. YouTube. https://www.youtube.com/channel/UC4L3JyeL7TXQM1f3yD6iVQQ
- Blend Swap. (n.d.). *Free 3D models and assets*. BlendSwap. https://blendswap.com
