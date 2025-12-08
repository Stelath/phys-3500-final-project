from manim import *
import numpy as np
from scipy.interpolate import interp1d

class RootFinding(Scene):
    def construct(self):
        # --- 1. Physics & Data Setup (Copied from differentiation.py) ---
        t_data = np.linspace(0, 25, 200)
        
        def rocket_altitude(t):
            g = 9.8
            thrust_accel = 50.3
            burn_time = 1.8
            v0 = 0.0
            
            if t <= burn_time:
                alt = v0 * t + 0.5 * thrust_accel * t**2
            else:
                v_burnout = v0 + thrust_accel * burn_time
                h_burnout = v0 * burn_time + 0.5 * thrust_accel * burn_time**2
                dt = t - burn_time
                alt = h_burnout + v_burnout * dt - 0.5 * g * dt**2
            return max(0, alt)
        
        y_raw = np.array([rocket_altitude(t) for t in t_data])
        
        # Noise and Smoothing
        np.random.seed(42)
        noise = np.cumsum(np.random.normal(0, 0.5, len(t_data)))
        kernel_size = 15
        noise_smooth = np.convolve(noise, np.ones(kernel_size)/kernel_size, mode='same')
        y_smooth_data = np.clip(y_raw + noise_smooth, 0, None)
        
        # Interpolation Functions
        alt_func = interp1d(t_data, y_smooth_data, kind='cubic', fill_value="extrapolate")
        
        # Calculate Velocity numerically
        ts = np.linspace(0, 25, 200)
        dt = ts[1] - ts[0]
        ys = alt_func(ts)
        vs = np.zeros_like(ys)
        vs[1:-1] = (ys[2:] - ys[:-2]) / (2*dt)
        vs[0] = (ys[1] - ys[0]) / dt
        vs[-1] = (ys[-1] - ys[-2]) / dt
        
        vel_func = interp1d(ts, vs, kind='linear', fill_value="extrapolate")

        # --- 2. Scene Setup ---
        # Left: Altitude (Green), Right: Velocity (Red)
        conf_alt = {"x_range": [0, 25, 5], "y_range": [0, 600, 100], "x_length": 6, "y_length": 4}
        conf_vel = {"x_range": [0, 25, 5], "y_range": [-100, 100, 50], "x_length": 6, "y_length": 4}
        
        ax_alt = Axes(**conf_alt, axis_config={"include_numbers": True, "font_size": 20}).to_edge(LEFT, buff=0.5)
        ax_vel = Axes(**conf_vel, axis_config={"include_numbers": True, "font_size": 20}).to_edge(RIGHT, buff=0.5)
        
        lbl_alt = Text("Altitude (m)", font_size=24, color=GREEN).next_to(ax_alt, UP)
        lbl_vel = Text("Velocity (m/s)", font_size=24, color=RED).next_to(ax_vel, UP)
        
        c_alt = ax_alt.plot(lambda t: alt_func(t), color=GREEN, x_range=[0, 25])
        c_vel = ax_vel.plot(lambda t: vel_func(t), color=RED, x_range=[0, 25])
        
        # Zero line for velocity
        v_zero_line = ax_vel.get_horizontal_line(ax_vel.c2p(25, 0), color=WHITE, stroke_width=1)

        self.play(
            Create(ax_alt), Write(lbl_alt), Create(c_alt),
            Create(ax_vel), Write(lbl_vel), Create(c_vel),
            Create(v_zero_line)
        )
        self.wait(1)

        # --- 3. Bisection Method Visualization ---
        
        # Intro Text
        intro = Text("Root Finding - Bisection Method", font_size=32).to_edge(UP)
        self.play(Write(intro))
        
        # Initial Interval
        a, b = 2.0, 20.0
        
        # Visual Elements for Brackets
        # We'll use vertical lines on the Velocity graph to show the bounds
        line_a = Line(ax_vel.c2p(a, -100), ax_vel.c2p(a, 100), color=BLUE, stroke_opacity=0.5)
        line_b = Line(ax_vel.c2p(b, -100), ax_vel.c2p(b, 100), color=BLUE, stroke_opacity=0.5)
        
        label_a = MathTex("a", color=BLUE).next_to(line_a, DOWN)
        label_b = MathTex("b", color=BLUE).next_to(line_b, DOWN)
        
        self.play(Create(line_a), Create(line_b), Write(label_a), Write(label_b))
        
        # Iteration Loop
        max_iter = 6
        
        midpoint_dot_vel = Dot(color=YELLOW)
        midpoint_dot_alt = Dot(color=YELLOW)
        
        # Status Text to show calculations
        status_box = VGroup()
        
        for i in range(max_iter):
            # Calculate midpoint
            m = (a + b) / 2.0
            vm = vel_func(m)
            ym = alt_func(m)
            
            # Update visuals for midpoint
            p_vel = ax_vel.c2p(m, vm)
            p_alt = ax_alt.c2p(m, ym)
            p_axis = ax_vel.c2p(m, 0)
            
            # Animate finding the midpoint
            midpoint_dot_vel.move_to(p_vel)
            midpoint_dot_alt.move_to(p_alt)
            
            # Create dashed line dynamically for this frame
            midpoint_line_vel = DashedLine(start=p_axis, end=p_vel, color=YELLOW)
            
            iter_text = Text(f"Iter {i+1}", font_size=24, color=YELLOW).to_corner(UL)
            val_text = MathTex(f"v({m:.2f}) = {vm:.2f}", font_size=24).next_to(iter_text, DOWN, aligned_edge=LEFT)
            
            self.play(
                FadeIn(iter_text), FadeIn(val_text),
                FadeIn(midpoint_dot_vel), Create(midpoint_line_vel)
            )
            
            # Show corresponding point on Altitude graph (Pinning logic)
            # Draw a line from V-axis midpoint to Altitude graph? Or just show the dot?
            # User request: "pinning that point on the altitude graph"
            # Let's flash the dot on altitude
            self.play(TransformFromCopy(midpoint_dot_vel, midpoint_dot_alt))
            self.play(Indicate(midpoint_dot_alt, scale_factor=1.5))
            
            # Logic check
            va = vel_func(a)
            # If sign change between a and m, new b = m
            # If sign change between m and b, new a = m
            
            # We assume f(a) > 0 and f(b) < 0 for this rocket case
            # (Velocity starts positive, ends negative)
            
            if va * vm < 0:
                # Root is in [a, m]
                # b becomes m
                target_b = ax_vel.c2p(m, -100) # Keep same y-levels for lines roughly or just fixed x
                line_b_new = Line(ax_vel.c2p(m, -100), ax_vel.c2p(m, 100), color=BLUE, stroke_opacity=0.5)
                self.play(
                    Transform(line_b, line_b_new),
                    label_b.animate.next_to(line_b_new, DOWN)
                )
                b = m
            else:
                # Root is in [m, b]
                # a becomes m
                line_a_new = Line(ax_vel.c2p(m, -100), ax_vel.c2p(m, 100), color=BLUE, stroke_opacity=0.5)
                self.play(
                    Transform(line_a, line_a_new),
                    label_a.animate.next_to(line_a_new, DOWN)
                )
                a = m
            
            self.play(
                FadeOut(iter_text), FadeOut(val_text),
                FadeOut(midpoint_line_vel), FadeOut(midpoint_dot_vel), FadeOut(midpoint_dot_alt)
            )
            
        # Final Result
        final_t = (a + b) / 2.0
        final_h = alt_func(final_t)
        
        result_dot = Dot(ax_alt.c2p(final_t, final_h), color=PURE_RED, radius=0.1)
        result_lbl = MathTex(f"Max H \\approx {final_h:.1f} m", color=PURE_RED).next_to(result_dot, UP)
        
        self.play(Create(result_dot), Write(result_lbl))
        self.wait(3)
