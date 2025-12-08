from manim import *
import numpy as np

class InterpolationAndSmoothing(Scene):
    def construct(self):
        # 1. Setup Graph
        # Center the graph and move it up slightly to make room for X-axis label
        ax = Axes(
            x_range=[0, 25, 5],      # 0 to 25 seconds
            y_range=[0, 600, 100],   # 0 to 500m (using 600 for headroom)
            axis_config={"include_numbers": True},
            x_length=10,             # Wider
            y_length=6
        ).move_to(ORIGIN).shift(UP * 0.15) 
        
        # Manual Labels
        y_label = Text("Altitude (m)", font_size=24).rotate(PI/2).next_to(ax.y_axis, LEFT, buff=0.5)
        x_label = Text("Time (s)", font_size=24).next_to(ax.x_axis, DOWN, buff=0.25)
        
        self.play(Create(ax), Write(y_label), Write(x_label))
        
        # 2. Plotting Data Points (Realistic Parabola for 25s flight)
        # Flight time ~25s, Peak ~500m
        # y = -a(t - 12.5)^2 + 500
        # Roots at t=0, t=25 => 0 = -a(-12.5)^2 + 500 => 500 = a*156.25 => a = 3.2
        
        t_vals = np.linspace(0.5, 24.5, 40) # More points for wider range
        true_func = lambda t: -3.2 * (t - 12.5)**2 + 500
        
        np.random.seed(42)
        noise_amp = 40 # Scaled up noise for 500m scale
        y_vals = [max(0, true_func(t) + np.random.normal(0, noise_amp/2)) for t in t_vals]
        
        points = VGroup()
        for t, y in zip(t_vals, y_vals):
            points.add(Dot(ax.c2p(t, y), color=YELLOW, radius=0.06))
            
        self.play(FadeIn(points))
        self.wait(0.5)
        
        # 3. Cubic Spline Interpolation
        text_spline = Text("Cubic Spline Interpolation", font_size=36, color=BLUE).to_edge(UP)
        self.play(Write(text_spline))
        
        # Create the wiggly spline
        spline_curve = VMobject().set_color(BLUE)
        spline_points = [ax.c2p(t, y) for t, y in zip(t_vals, y_vals)]
        spline_curve.set_points_smoothly(spline_points)
        
        self.play(Create(spline_curve), run_time=6.0) 
        self.wait(1.5)
        
        # 4. Gaussian Filter Smoothing
        text_gaussian = Text("Gaussian Filter Smoothing", font_size=36, color=GREEN).to_edge(UP)
        
        # Highlighted Rectangle (Filter Window)
        window_width = 3.0 # Wider window for 25s scale
        window = Rectangle(
            width=window_width, 
            height=9.75, 
            color=GREEN, 
            fill_opacity=0.3, 
            stroke_opacity=0
        )
        # Convert window width in data units to plot units?
        # Manim Rectangle width is in scene units. 
        # ax.c2p(3,0)[0] - ax.c2p(0,0)[0] gives scale.
        data_scale_x = (ax.c2p(1,0)[0] - ax.c2p(0,0)[0])
        scene_window_width = window_width * data_scale_x 
        # Actually just setting width visually is fine, but let's make it correspond to ~3 seconds
        window.width = 4 * data_scale_x # 4 second window
        
        window.move_to(ax.c2p(0, 260)) # Start at t=0, centered y=300
        
        # Calculate REAL Smoothed Data
        def gaussian_kernel(size, sigma=1):
            x = np.linspace(-size//2, size//2, size)
            k = np.exp(-0.5 * (x/sigma)**2)
            return k / k.sum()

        kernel = gaussian_kernel(size=9, sigma=3) 
        y_smooth_vals = np.convolve(y_vals, kernel, mode='same')
        
        # Fix ends
        y_smooth_vals[:4] = y_vals[:4]
        y_smooth_vals[-4:] = y_vals[-4:]
        
        smooth_curve = VMobject().set_color(GREEN)
        smooth_points = [ax.c2p(t, y) for t, y in zip(t_vals, y_smooth_vals)]
        smooth_curve.set_points_smoothly(smooth_points)
        
        self.play(
            ReplacementTransform(text_spline, text_gaussian),
            FadeIn(window)
        )
        
        self.play(
            window.animate.move_to(ax.c2p(25, 260)),
            Create(smooth_curve),
            rate_func=linear,
            run_time=6.0
        )
        
        self.play(FadeOut(window), FadeOut(points), FadeOut(spline_curve))
        self.wait(2)
