from manim import *
import numpy as np

class CubicSplineInterpolation(Scene):
    def construct(self):
        # 1. Intro
        title = Text("Cubic Spline Interpolation", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 2. Setup Axes
        ax = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 5, 1],
            axis_config={"include_numbers": True},
        )
        labels = ax.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(ax), Create(labels))

        # 3. Data Points
        points_data = [
            (0.5, 1.0),
            (2.0, 3.5),
            (3.5, 2.0),
            (5.0, 4.0)
        ]
        
        dots = VGroup()
        for x, y in points_data:
            dots.add(Dot(ax.c2p(x, y), color=YELLOW))
            
        self.play(FadeIn(dots))
        self.wait(1)

        # 4. Naive Linear Interpolation (Connect the dots)
        lines = VGroup()
        for i in range(len(points_data) - 1):
            p1 = ax.c2p(*points_data[i])
            p2 = ax.c2p(*points_data[i+1])
            lines.add(Line(p1, p2, color=GRAY, stroke_opacity=0.5))
            
        linear_text = Text("Linear Interpolation?", font_size=24, color=GRAY).to_corner(UR)
        self.play(Create(lines), Write(linear_text))
        self.wait(1)
        self.play(FadeOut(lines), FadeOut(linear_text))

        # 5. Cubic Spline
        # Concept: A cubic polynomial S_i(x) between each pair of points
        # Constraints: 
        # - S_i(x_i) = y_i
        # - S_i(x_{i+1}) = y_{i+1}
        # - S'_i(x_{i+1}) = S'_{i+1}(x_{i+1})  (Smooth slope)
        # - S''_i(x_{i+1}) = S''_{i+1}(x_{i+1}) (Smooth curvature)
        
        spline_text = Text("Cubic Spline (Smooth C2)", font_size=24, color=BLUE).to_corner(UR)
        self.play(Write(spline_text))

        # Hardcoded cubic fits for these points (approximate for visual)
        # Or I can use scipy if available, but let's just draw a smooth curve
        # passing through them.
        # Catmull-Rom or similar is fine for visual if explicit math isn't key
        # But Manim has smooth plotting.
        
        # Let's use a standard interpolation for the graph
        # Manim's 'CubicBezier' or just plot a fitted poly?
        # A high degree poly might oscillate.
        # Let's manually define control handles for visual smoothness
        
        # Visualizing the curve piece by piece
        
        # Piece 1: 0.5 to 2.0
        # Start slope > 0.
        

        # Better:
        path = VMobject(color=BLUE)
        path.set_points_smoothly([ax.c2p(*p) for p in points_data])
        
        self.play(Create(path))
        self.wait(1)
        
        # Highlight logic - Zoom in on a joint?
        # Let's highlight the joint at (2.0, 3.5)
        joint_circle = Circle(radius=0.3, color=RED).move_to(ax.c2p(2.0, 3.5))
        self.play(Create(joint_circle))
        
        note1 = Text("Continuous Position", font_size=16).next_to(joint_circle, UP)
        self.play(Write(note1))
        self.wait(1)
        
        note2 = Text("Continuous Slope (1st Deriv)", font_size=16).next_to(note1, DOWN)
        self.play(Transform(note1, note2))
        self.wait(1)

        note3 = Text("Continuous Curvature (2nd Deriv)", font_size=16).next_to(note1, DOWN)
        self.play(Transform(note1, note3))
        self.wait(2)
        
        self.play(FadeOut(joint_circle), FadeOut(note1), FadeOut(spline_text))
        
        # 6. Natural Spline Condition
        # Endpoints have 2nd derivative = 0 (Linear approach at ends)
        # Visual: Show straight-ish ends
        
        conclusion = Text("Essential for smooth derivatives!", font_size=30).to_edge(DOWN)
        self.play(Write(conclusion))
        self.wait(2)
