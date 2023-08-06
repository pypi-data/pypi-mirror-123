
<p align="center">
  <img width="40%" src="./assets/ltlogo.png" />
</p>

# LieTorch

This project provides a python package that expands the functionality of the PyTorch framework,
the goals of this project are twofold:
1) Introduce Lie-group based geometrical tools to PyTorch in order to experiment with advanced geometrical machine learning.
2) Bring the capabilities of the Mathematica package [LieAnalysis](https://www.lieanalysis.nl) to python/pytorch.


#### The name

The name LieTorch is a reference to the Norwegian mathematician [Sophus Lie](https://infogalactic.com/info/Sophus_Lie), whose contributions to geometry are extensively used in this project. The name is pronounced */li:/* (as in *Lee*) and not */ˈlī/* (as in *lie*).

## Milestones

- 0.1 : B-Spline based 𝕄₂ G-CNNs (2D roto-translation equivariant), see [B-Spline CNNs on Lie Groups (arXiv)](https://arxiv.org/abs/1909.12057).
- 0.2 : 𝕄₂ PDE-NNs, see [PDE-based Group Equivariant Convolutional Neural Networks (arXiv)](https://arxiv.org/abs/2001.09046).
- 0.3 : ℝ² PDE-NNs 


## Neural network modules

Modules are grouped according to the manifold they operate on. Most modules have a functional equivalant in the `lietorch.nn.functional` namespace.

### Euclidean Space ℝ² 

Basic operators:

| Module | Functional | C++/CUDA backend  |
| --- | --- | :---: |
| `MorphologicalConvolutionR2` | `morphological_convolution_r2` | ✓ |
| `FractionalDilationR2` | `fractional_dilation_r2` | ✓ |
| `FractionalErosionR2` | `fractional_erosion_r2` | ✓ |
| `ConvectionR2` | `convection_r2` | ⏳ |
| `DiffusionR2` | `diffusion_r2` | ⏳ |
| `LinearR2` | `linear_r2` | ✓ |

### Position and Orientation Space 𝕄₂

Basic operators:

| Module | Functional | C++/CUDA backend  |
| --- | --- | :---: |
| `LiftM2Cartesian` | `lift_m2_cartesian` | - |
| `ReflectionPadM2` | `reflection_pad_m2` | - |
| `ConvM2Cartesian` | `conv_m2_cartesian`  | - |
| `MaxProjectM2`    |  `max_project_m2` | - | 
| `AnisotropicDilatedProjectM2` | `anisotropic_dilated_project_m2` | ✓ |
| `MorphologicalConvolutionM2` | `morphological_convolution_m2` | ✓ |
| `ConvectionM2` | `convection_m2` | ✓ |
| `DiffusionM2` | `diffusion_m2` | ⏳ |
| `FractionalDilationM2` | `fractional_dilation_m2` | ✓ |
| `FractionalErosionM2` | `fractional_erosion_m2` | ✓ |
| `LinearM2` | `linear_m2` | ✓ |


High-level modules for implementing PDE-based networks:

| Module | Description/PDE  |
| --- | :--- |
| `ConvectionDilationPdeM2` | $`u_t=-\mathbf{c}u + \lVert \nabla u \rVert^{2 \alpha}_{\mathcal{G}}`$ |
| `ConvectionErosionPdeM2` | $`u_t=-\mathbf{c}u - \lVert \nabla u \rVert^{2 \alpha}_{\mathcal{G}}`$ |
| `CDEPdeLayerM2` | $`u_t=-\mathbf{c}u + \lVert \nabla u \rVert^{2 \alpha}_{\mathcal{G}_1} - \lVert \nabla u \rVert^{2 \alpha}_{\mathcal{G}_2}`$ <br>  with batch normalization and linear combinations |


### Loss functions

Additional loss functions.

| Module | Functional | Description |
| ------ | ---------- | :---------: |
| `lietorch.nn.loss.DiceLoss` | `lietorch.nn.functional.dice_loss` | Binary DICE loss |


### Generic 

The modules in the generic category do not fit into any previous category and include operators that serve as C++/CUDA implementation examples.

| Module | Functional | C++/CUDA backend  |
| --- | --- | :---: |
| `GrayscaleDilation2D` | `grayscale_dilation_2d` | ✓ |
| `GrayscaleErosion2D` | `grayscale_erosion_2d` | ✓ |



## Dependencies

The `lietorch` python package has the following dependencies.
- python 3.7+
- pytorch 1.6+
- torchvision 0.7+
 
 The included experiments additionally depend on the following packages.
 - scikit-learn
 - tqdm
 - numpy
 - sty (PIP)
 - mlflow (PIP)
 - libtiff (PIP)

 ## Structure

- `/lietorch` contains the main python package.
- `/experiments` contains various experiments, including those used in publications.
- `/tests` contains unit tests.
- `/backend` contains the source code of the C++/CUDA backend,
    - see [./backend/README.md](./backend/README.md) if you wish to compile the extension yourself.
- `/assets` various files used in tests and documentation.



## Cite

If you use this code in your own work please cite our paper:

Smets, B.M.N., Portegies, J., Bekkers, E.J., & Duits, R. (2021). PDE-based Group Equivariant Convolutional Neural Networks. arXiv preprint arXiv:2001.09046. Retrieved 10 August 2021, from <https://arxiv.org/abs/2001.09046>

```
@article{smets2021pde,
  title={PDE-based Group Equivariant Convolutional Neural Networks},
  author={Smets, Bart and Portegies, Jim and Bekkers, Erik and Duits, Remco},
  journal={arXiv preprint arXiv:2001.09046},
  year={2020}
}
```