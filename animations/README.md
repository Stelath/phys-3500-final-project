# Physics Project Animations

This directory contains Manim animations explaining the numerical methods used in the final project.

## Requirements

You need [Manim Community](https://www.manim.community/) installed.
```bash
pip install manim
```

## Running the Animations

To render the animations, run the following commands from this directory:

### 1. Bisection Method
```bash
manim -pql bisection_method.py BisectionMethod
```

### 2. Runge-Kutta 4 Method
```bash
manim -pql runge_kutta.py RungeKuttaMethod
```

### 3. Cubic Spline Interpolation
```bash
manim -pql cubic_spline.py CubicSplineInterpolation
```

### 4. Rocket Analysis Overview
```bash
manim -pql rocket_analysis_overview.py RocketAnalysisOverview
```

**Note:** The `-pql` flag stands for Preview, Quality Low. For high quality production rendering, use `-pqh`.
