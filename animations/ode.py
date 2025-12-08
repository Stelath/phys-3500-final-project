from manim import *
import numpy as np
from scipy.interpolate import interp1d

class RocketODE(Scene):
    def construct(self):
        # ========================================================================
        # PHASE 1: Visualize Runge-Kutta 4 Method Steps
        # ========================================================================
        
        title_rk = Text("4th Order Runge-Kutta Method", font_size=36).to_edge(UP)
        self.play(Write(title_rk))
        
        # Show the ODE we're solving
        ode_eq = MathTex(
            r"\frac{dv}{dt} = -g - \frac{k}{m} v |v|",
            font_size=32
        ).next_to(title_rk, DOWN)
        self.play(Write(ode_eq))
        self.wait(1)
        
        # Create a simple graph to illustrate RK4 steps
        ax_rk = Axes(
            x_range=[0, 2, 0.5], y_range=[0, 50, 10],
            x_length=8, y_length=5,
            axis_config={"include_numbers": True, "font_size": 18}
        ).shift(DOWN*0.5)
        
        ax_labels = ax_rk.get_axis_labels(x_label="t", y_label="v(t)")
        self.play(Create(ax_rk), Write(ax_labels))
        
        # Define a simple slope function for illustration
        # v' = f(t, v) = 30 - 0.5*v (simplified drag-like)
        def slope_func(t, v):
            return 30 - 0.5 * v
        
        # Starting point
        t0, v0 = 0.5, 20.0
        h = 0.8  # Step size (large for visibility)
        
        # Calculate RK4 components
        k1 = slope_func(t0, v0)
        k2 = slope_func(t0 + h/2, v0 + k1*h/2)
        k3 = slope_func(t0 + h/2, v0 + k2*h/2)
        k4 = slope_func(t0 + h, v0 + k3*h)
        v_next = v0 + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
        
        # Draw starting point
        p0 = ax_rk.c2p(t0, v0)
        dot0 = Dot(p0, color=YELLOW)
        lbl0 = MathTex("(t_n, v_n)", font_size=20).next_to(dot0, LEFT)
        self.play(FadeIn(dot0), Write(lbl0))
        
        # --- k1: Slope at current point ---
        k1_line = Line(
            ax_rk.c2p(t0, v0),
            ax_rk.c2p(t0 + h, v0 + k1*h),
            color=BLUE
        )
        k1_label = MathTex("k_1", color=BLUE, font_size=24).next_to(k1_line, UP)
        self.play(Create(k1_line), Write(k1_label))
        self.wait(0.5)
        
        # --- k2: Slope at midpoint using k1 ---
        mid_pt_k2 = ax_rk.c2p(t0 + h/2, v0 + k1*h/2)
        dot_k2 = Dot(mid_pt_k2, color=BLUE, radius=0.06)
        k2_line = Line(
            ax_rk.c2p(t0, v0),
            ax_rk.c2p(t0 + h, v0 + k2*h),
            color=GREEN
        )
        k2_label = MathTex("k_2", color=GREEN, font_size=24).next_to(k2_line.get_end(), RIGHT)
        self.play(FadeIn(dot_k2), Create(k2_line), Write(k2_label))
        self.wait(0.5)
        
        # --- k3: Slope at midpoint using k2 ---
        mid_pt_k3 = ax_rk.c2p(t0 + h/2, v0 + k2*h/2)
        dot_k3 = Dot(mid_pt_k3, color=GREEN, radius=0.06)
        k3_line = Line(
            ax_rk.c2p(t0, v0),
            ax_rk.c2p(t0 + h, v0 + k3*h),
            color=ORANGE
        )
        k3_label = MathTex("k_3", color=ORANGE, font_size=24).next_to(k3_line.get_end(), UR)
        self.play(FadeIn(dot_k3), Create(k3_line), Write(k3_label))
        self.wait(0.5)
        
        # --- k4: Slope at endpoint using k3 ---
        end_pt_k4 = ax_rk.c2p(t0 + h, v0 + k3*h)
        dot_k4 = Dot(end_pt_k4, color=ORANGE, radius=0.06)
        k4_line = Line(
            ax_rk.c2p(t0, v0),
            ax_rk.c2p(t0 + h, v0 + k4*h),
            color=RED
        )
        k4_label = MathTex("k_4", color=RED, font_size=24).next_to(k4_line.get_end(), DR)
        self.play(FadeIn(dot_k4), Create(k4_line), Write(k4_label))
        self.wait(0.5)
        
        # --- Weighted average (final step) ---
        p_next = ax_rk.c2p(t0 + h, v_next)
        dot_next = Dot(p_next, color=YELLOW)
        lbl_next = MathTex("(t_{n+1}, v_{n+1})", font_size=20).next_to(dot_next, RIGHT)
        
        weighted_formula = MathTex(
            r"v_{n+1} = v_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)",
            font_size=28
        ).to_edge(DOWN)
        
        self.play(Write(weighted_formula))
        self.play(FadeIn(dot_next), Write(lbl_next))
        self.wait(2)
        
        # Fade out Phase 1
        phase1_group = VGroup(
            title_rk, ode_eq, ax_rk, ax_labels,
            dot0, lbl0, k1_line, k1_label, dot_k2, k2_line, k2_label,
            dot_k3, k3_line, k3_label, dot_k4, k4_line, k4_label,
            dot_next, lbl_next, weighted_formula
        )
        self.play(FadeOut(phase1_group))
        
        # ========================================================================
        # PHASE 2: Show Altitude Curve from differentiation.py
        # ========================================================================
        
        title_fit = Text("Fitting Quadratic Drag to Flight Data", font_size=36).to_edge(UP)
        self.play(Write(title_fit))
        
        # Replicate altitude data from differentiation.py
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
        
        y_smooth_data = np.array([rocket_altitude(t) for t in t_data])
        
        # Add noise
        np.random.seed(42)
        noise = np.cumsum(np.random.normal(0, 0.5, len(t_data)))
        kernel_size = 15
        noise_smooth = np.convolve(noise, np.ones(kernel_size)/kernel_size, mode='same')
        y_smooth_data = y_smooth_data + noise_smooth
        y_smooth_data = np.clip(y_smooth_data, 0, None)
        
        alt_func = interp1d(t_data, y_smooth_data, kind='cubic', fill_value="extrapolate")
        
        # Create Axes for Altitude
        ax_alt = Axes(
            x_range=[0, 25, 5], y_range=[0, 600, 100],
            x_length=10, y_length=5.5,
            axis_config={"include_numbers": True, "font_size": 18}
        ).shift(DOWN*0.3)
        
        alt_labels = ax_alt.get_axis_labels(x_label="Time (s)", y_label="Altitude (m)")
        
        # Plot the "observed" altitude curve
        curve_alt = ax_alt.plot(lambda t: alt_func(t), color=GREEN, x_range=[0, 25])
        lbl_data = Text("Observed Flight Data", font_size=20, color=GREEN).next_to(ax_alt, UR).shift(LEFT*2 + DOWN*0.5)
        
        self.play(Create(ax_alt), Write(alt_labels))
        self.play(Create(curve_alt, run_time=2), Write(lbl_data))
        self.wait(1)
        
        # ========================================================================
        # PHASE 3: Fitting Loop - Try Different k Values
        # ========================================================================
        
        # RK4 Solver for altitude
        g = 9.8
        mass = 50.0
        
        # Initial conditions at burnout (t=1.8s)
        t_burn = 1.8
        burn_idx = np.searchsorted(t_data, t_burn)
        y0_fit = y_smooth_data[burn_idx]
        
        # Estimate initial velocity from data
        v0_fit = (y_smooth_data[burn_idx + 1] - y_smooth_data[burn_idx - 1]) / (t_data[burn_idx + 1] - t_data[burn_idx - 1])
        
        t_fit = t_data[burn_idx:]
        y_obs = y_smooth_data[burn_idx:]
        
        def rk4_solve(k_val, t_array, y0, v0):
            y_out = [y0]
            v_out = [v0]
            
            curr_y, curr_v = y0, v0
            
            for i in range(len(t_array) - 1):
                h = t_array[i+1] - t_array[i]
                
                # k1
                vy_k1 = curr_v
                vv_k1 = -g - (k_val/mass)*curr_v*abs(curr_v)
                
                # k2
                v_mid1 = curr_v + vv_k1*h/2
                vy_k2 = v_mid1
                vv_k2 = -g - (k_val/mass)*v_mid1*abs(v_mid1)
                
                # k3
                v_mid2 = curr_v + vv_k2*h/2
                vy_k3 = v_mid2
                vv_k3 = -g - (k_val/mass)*v_mid2*abs(v_mid2)
                
                # k4
                v_end = curr_v + vv_k3*h
                vy_k4 = v_end
                vv_k4 = -g - (k_val/mass)*v_end*abs(v_end)
                
                # Update
                curr_y = curr_y + (h/6)*(vy_k1 + 2*vy_k2 + 2*vy_k3 + vy_k4)
                curr_v = curr_v + (h/6)*(vv_k1 + 2*vv_k2 + 2*vv_k3 + vv_k4)
                
                if curr_y < 0:
                    curr_y = 0
                    curr_v = 0
                
                y_out.append(curr_y)
                v_out.append(curr_v)
            
            return np.array(y_out)
        
        def calc_rmse(y_model, y_data):
            return np.sqrt(np.mean((y_model - y_data)**2))
        
        # Info display
        k_text = MathTex(r"k = ?", color=RED, font_size=28).to_corner(UL).shift(RIGHT*0.5 + DOWN*0.5)
        rmse_text = MathTex(r"RMSE = ?", color=RED, font_size=28).next_to(k_text, DOWN, aligned_edge=LEFT)
        self.play(Write(k_text), Write(rmse_text))
        
        # Trials
        trials = [0.001, 0.30, 0.05, 0.005]  # Bad -> Bad -> Better -> Best
        
        model_curve = None
        
        for k_val in trials:
            y_model = rk4_solve(k_val, t_fit, y0_fit, v0_fit)
            rmse = calc_rmse(y_model, y_obs)
            
            # Build curve
            points = [ax_alt.c2p(t, y) for t, y in zip(t_fit, y_model)]
            new_curve = VMobject(color=RED)
            new_curve.set_points_smoothly(points)
            
            # Color based on RMSE
            color = GREEN if rmse < 15 else ORANGE if rmse < 50 else RED
            new_curve.set_color(color)
            
            # Update text
            new_k = MathTex(rf"k = {k_val:.3f}", font_size=28).move_to(k_text, aligned_edge=LEFT)
            new_rmse = MathTex(rf"RMSE = {rmse:.1f}", font_size=28).move_to(rmse_text, aligned_edge=LEFT)
            new_rmse.set_color(color)
            new_k.set_color(color)
            
            if model_curve is None:
                model_curve = new_curve
                self.play(
                    Create(model_curve, run_time=1.5),
                    Transform(k_text, new_k),
                    Transform(rmse_text, new_rmse)
                )
            else:
                self.play(
                    Transform(model_curve, new_curve, run_time=1),
                    Transform(k_text, new_k),
                    Transform(rmse_text, new_rmse)
                )
            
            self.wait(1)
        
        # Highlight best fit
        best_box = SurroundingRectangle(VGroup(k_text, rmse_text), color=GREEN, buff=0.2)
        lbl_best = Text("Best Fit!", color=GREEN, font_size=24).next_to(best_box, RIGHT)
        self.play(Create(best_box), Write(lbl_best))
        
        self.wait(3)
