# UROP: Making maths more inclusive

This is the official repository for two mathematical visualisations by Louis Sun and Suleyman Ansari of the Mechanical Engineering (ME) department at Imperial. The UROP aims to make the ME1 maths lecture notes more inclusive by producing additional learning resources including TikZ figures, animations, and an interactive web app.

## TikZ: Slope fields
For the differential equations chapter, we produced example slope fields to visualise the gradient defined by a given differential equation at sample points on a 2D plane. On the slope fields, example particular solutions are also drawn. Below are screenshots of example renders.

### Slope field of $\frac{\mathrm{d}w}{\mathrm{d}t}=3-0.08w$
[Example 1 of examples.tex](./assets/slopefield-example1.png)
### Slope field of $\frac{\mathrm{d}y}{\mathrm{d}x}=k(2x+1)$
[Example 2 of examples.tex](./assets/slopefield-example2.png)
### Slope field of $\frac{\mathrm{d}y}{\mathrm{d}x}=-\frac{2x+y+1}{x+2y+1}$
[Example 3 of examples.tex](./assets/slopefield-example3.png)

There is also an additional [Desmos slope field generator](https://www.desmos.com/calculator/v2x5tqxdfa) for trying out custom differential equations.

## Manim: 3D integration visualised in animation
In order to help ME1 students make sense of multidimensional integrals, animations were produced to visualise the sequential steps of integrating through a 3D domain. The [Manim](https://github.com/ManimCommunity/manim/tree/main) animation library was used, originally developed by [3Blue1Brown](https://www.youtube.com/@3blue1brown).

## Three.js/React: [Interactive 3D integration](https://imperialcollegelondon.github.io/3d-domain-visualiser/)
As a supplementary resource to the 3D integration animations, a web app was created for playing around with integral limits to build various volumes. Additionally, the user can drag and drop the infinitesimals to reorder the integration.
