from manim import *
import numpy as np

class RocketAnalysisOverview(Scene):
    def construct(self):
        # 1. Intro
        title = Text("Rocket Flight Analysis", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))

        # 2. Setup Axes for Altitude
        ax = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 100, 20],
            axis_config={"include_numbers": True},
            x_length=6,
            y_length=4
        ).to_edge(LEFT, buff=0.5)
        
        labels = ax.get_axis_labels(x_label="t (s)", y_label="h (m)")
        self.play(Create(ax), Create(labels))

        # 3. Raw Data (Noisy)
        # Function: y = 30*t - 4.9*t^2 (approx)
        # Peak at ~3 sec, height ~ 45m.
        # Add noise
        t_raw = np.linspace(0, 6, 15)
        y_raw = 30*t_raw - 4.9*t_raw**2 + np.random.normal(0, 2, len(t_raw))
        y_raw = np.maximum(y_raw, 0) # No negative altitude

        data_dots = VGroup()
        for t, y in zip(t_raw, y_raw):
            data_dots.add(Dot(ax.c2p(t, y), color=YELLOW, radius=0.06))
        
        data_label = Text("Raw Altimeter Data", font_size=20, color=YELLOW).next_to(ax, UP)
        self.play(FadeIn(data_dots), Write(data_label))
        self.wait(1)

        # 4. Interpolation
        # Smooth spline
        interp_curve = ax.plot(
            lambda t: 30*t - 4.9*t**2, 
            color=BLUE, 
            x_range=[0, 6.1]
        )
        interp_label = Text("Spline Interpolation", font_size=20, color=BLUE).next_to(data_label, DOWN)
        
        self.play(Create(interp_curve), Write(interp_label))
        self.wait(1)
        self.play(FadeOut(data_dots), FadeOut(data_label)) # Clean up view

        # 5. Numerical Differentiation (Velocity)
        # Create second axes for velocity
        ax_v = Axes(
            x_range=[0, 10, 1],
            y_range=[-40, 40, 20], 
            axis_config={"include_numbers": True},
            x_length=6,
            y_length=3
        ).to_edge(RIGHT, buff=0.5) # Overlap? Maybe shift left one up and right one down?
        # Let's arrange them side by side? 6+6=12 > 14 (screen width ~14). It fits.
        # Scale down.
        
        self.play(
            Group(ax, labels, interp_curve, interp_label).animate.scale(0.7).to_edge(LEFT, buff=1)
        )
        
        ax_v.scale(0.7).next_to(ax, RIGHT, buff=1.5)
        v_labels = ax_v.get_axis_labels(x_label="t", y_label="v (m/s)")
        
        self.play(Create(ax_v), Create(v_labels))
        
        # Velocity curve v = 30 - 9.8*t
        vel_curve = ax_v.plot(
            lambda t: 30 - 9.8*t,
            color=RED,
            x_range=[0, 6.1]
        )
        vel_text = Text("Derived Velocity", font_size=20, color=RED).next_to(ax_v, UP)
        
        self.play(ReplacementTransform(interp_curve.copy(), vel_curve), Write(vel_text))
        self.wait(1)
        
        # 6. Drag Model Fitting
        # Focus back on Altitude
        self.play(FadeOut(vel_curve), FadeOut(ax_v), FadeOut(v_labels), FadeOut(vel_text))
        self.play(Group(ax, labels, interp_curve, interp_label).animate.scale(1.42).move_to(ORIGIN)) # Restore size
        
        model_title = Text("Model Fitting: Drag Coefficient k", font_size=24).to_corner(UL)
        self.play(Write(model_title))
        
        # Function with drag: y'' = -g - (k/m) v |v|
        # Visual approx: Higher k -> Lower peak, faster descent
        # k=0 -> Parabola (Ideal)
        # k=High -> Squashed
        
        # Let's animate a curve changing with a parameter k
        # Base parabola: 30t - 4.9t^2
        # With drag: lower peak
        
        def get_drag_curve(k_factor):
            # Visually approximate drag effect
            # Peak height reduces by k_factor * constant
            # t-intercepts shift
            return ax.plot(
                lambda t: (30 * t - 4.9 * t**2) * (1 - k_factor * t/10), 
                # Pure hack for visual "squashing" down-range
                color=GREEN,
                x_range=[0, 6.1]
            )

        # k=0 (No Drag - Overshoots data? Maybe data has drag, so ideal overshoots)
        # Let's say Data (BLUE) includes drag.
        # Initial guess k=0 (Ideal physics) -> Should be higher than data
        ideal_curve = ax.plot(
            lambda t: 32 * t - 4.9 * t**2, # Slightly higher initial v or less loss
            color=GREEN,
            x_range=[0, 6.5]
        )
        
        k_tracker = ValueTracker(0.0)
        k_label = DecimalNumber(0.00, num_decimal_places=2).next_to(model_title, RIGHT)
        k_text = Text("k = ", font_size=24).next_to(k_label, LEFT)
        
        self.play(Create(ideal_curve), FadeIn(k_text), FadeIn(k_label))
        
        self.play(k_tracker.animate.set_value(0.5), run_time=2)
        
        # In a real update loop we'd compute the curve, but for simple animation:
        # We'll just transform the curve to the "Best Fit"
        
        best_fit_curve = interp_curve.copy().set_color(GREEN) # The data IS the target
        
        self.play(
            Transform(ideal_curve, best_fit_curve),
            k_tracker.animate.set_value(0.15), # Optimal k
            UpdateFromFunc(k_label, lambda m: m.set_value(k_tracker.get_value())),
            run_time=3
        )
        
        match_text = Text("Match Found!", color=GREEN, font_size=30).next_to(ideal_curve, RIGHT, buff=0.1)
        self.play(Write(match_text))
        self.wait(2)
        
        # 7. Conclusion
        final_group = VGroup(ax, labels, interp_curve, ideal_curve, k_text, k_label, match_text, model_title)
        self.play(final_group.animate.scale(0.8))
        
        results = Tex(
            r"Apogee: 45.2 m \\",
            r"Max Vel: 30.1 m/s \\",
            r"Drag Coeff: 0.15 kg/m",
            font_size=30
        ).next_to(final_group, DOWN)
        
        self.play(Write(results))
        self.wait(2)
