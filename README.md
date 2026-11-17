# Autostereogram-OpenGL-Python

## Goals
Implement a rendering system capable of loading three-dimensional objects, extracting a real-time depth map from the rendered scene, and synthesizing an autostereogram based on the generated camera view.

To achieve this, the project defines the following core milestones:
- Set up a 3D rendering environment to load and display external 3D models.
- Implement interactive camera movement and view transformations.
- Extract and visualize the scene's depth map (Z-buffer).
- Develop the stereogram synthesis algorithm to generate autostereograms from the depth data.

## Design Decisions
- **Target Domain:** 3D Computer Graphics & Stereoscopic Rendering
- **Application Chapter:** Depth Map

The target domain chosen was **3D Computer Graphics** under the **Depth Map** chapter, leveraging Modern OpenGL pipelines in Python. The architecture separates standard 3D scene rendering from post-processing depth extraction, allowing dynamic camera navigation so users can inspect 3D geometry from multiple angles before converting the spatial depth information into single-image random-dot or textured autostereograms.

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
