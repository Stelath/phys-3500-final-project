from manim import *
import numpy as np
from scipy.interpolate import interp1d

class RocketODE(Scene):
    def construct(self):
        # ========================================================================
        # PHASE 1: Visualize Runge-Kutta 4 Method Steps (Iterative)
        # ========================================================================
        
        title_rk = Text("4th Order Runge-Kutta Method", font_size=36).to_edge(UP)
        self.play(Write(title_rk))
        
        # Show the ODE we're solving (Quadratic Drag)
        ode_eq = MathTex(
            r"\frac{dv}{dt} = -g - \frac{k}{m} v |v|",
            font_size=32
        ).next_to(title_rk, DOWN)
        self.play(Write(ode_eq))
        
        # Create a simple graph to illustrate RK4 steps
        ax_rk = Axes(
            x_range=[0, 2.5, 0.5], y_range=[0, 30, 10], # Adjusted ranges
            x_length=8, y_length=5,
            axis_config={"include_numbers": True, "font_size": 18}
        ).shift(DOWN*0.5)
        
        # Match style from interpolation.py
        rk_ylabel = Text("Velocity", font_size=20).rotate(PI/2).next_to(ax_rk.y_axis, LEFT, buff=0.3)
        rk_xlabel = Text("Time", font_size=20).next_to(ax_rk.x_axis, DOWN, buff=0.2)
        
        self.play(Create(ax_rk), Write(rk_ylabel), Write(rk_xlabel))
        
        # v' = 30 - 1.5*v (Toy model for visual clarity, decays to 20)
        def slope_func(t, v):
             return 30 - 1.5 * v
        
        # Start
        curr_t, curr_v = 0.0, 5.0 # Start low go high
        h = 0.8
        
        # Loop for 3 iterations
        for i in range(3):
            # Calculate RK4 components
            k1 = slope_func(curr_t, curr_v)
            k2 = slope_func(curr_t + h/2, curr_v + k1*h/2)
            k3 = slope_func(curr_t + h/2, curr_v + k2*h/2)
            k4 = slope_func(curr_t + h, curr_v + k3*h)
            next_v = curr_v + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
            
            # Draw starting point
            p_start = ax_rk.c2p(curr_t, curr_v)
            dot_start = Dot(p_start, color=YELLOW)
            if i == 0:
                self.play(FadeIn(dot_start))
            
            # Visualize Slopes (only fully detail the first one)
            # Use arrows or lines
            
            # k1
            line_k1 = Line(p_start, ax_rk.c2p(curr_t + h, curr_v + k1*h), color=BLUE, stroke_opacity=0.6)
            
            # k2
            p_mid1 = ax_rk.c2p(curr_t + h/2, curr_v + k1*h/2)
            line_k2 = Line(p_start, ax_rk.c2p(curr_t + h, curr_v + k2*h), color=GREEN, stroke_opacity=0.6)
            
            # k3
            p_mid2 = ax_rk.c2p(curr_t + h/2, curr_v + k2*h/2)
            line_k3 = Line(p_start, ax_rk.c2p(curr_t + h, curr_v + k3*h), color=ORANGE, stroke_opacity=0.6)
            
            # k4
            p_end = ax_rk.c2p(curr_t + h, curr_v + k3*h)
            line_k4 = Line(p_start, ax_rk.c2p(curr_t + h, curr_v + k4*h), color=RED, stroke_opacity=0.6)
            
            # Show slopes
            lines = VGroup(line_k1, line_k2, line_k3, line_k4)
            self.play(Create(lines), run_time=1.0)
            
            # Resulting step
            p_next = ax_rk.c2p(curr_t + h, next_v)
            dot_next = Dot(p_next, color=YELLOW)
            step_curve = VMobject(color=YELLOW)
            step_curve.set_points_smoothly([p_start, p_next]) # Straight-ish connector
            
            self.play(FadeIn(dot_next), Create(step_curve))
            self.play(FadeOut(lines)) # Clean up construction lines
            
            curr_t += h
            curr_v = next_v
            
        self.wait(1)
        
        # Cleanup Phase 1
        self.play(
            FadeOut(title_rk), FadeOut(ode_eq), 
            FadeOut(ax_rk), FadeOut(rk_ylabel), FadeOut(rk_xlabel),
            FadeOut(dot_start), FadeOut(dot_next), FadeOut(step_curve) # Note: this only catches last ones, simplest to fade all mobjects
        )
        self.clear() # Nuclear option to ensure clean slate for Phase 2
        
        # ========================================================================
        # PHASE 2 & 3: Altitude Data & Fitting
        # ========================================================================
        
        # ========================================================================
        # PHASE 2 & 3: Altitude Data & Fitting
        # ========================================================================
        
        title_fit = Text("Fitting Quadratic Drag to Flight Data", font_size=36).to_edge(UP)
        self.add(title_fit) 
        self.play(Write(title_fit))
        
        # --- Data Generation (True Drag Physics) ---
        t_data = np.linspace(0, 25, 200)
        
        # Define Ground Truth Physics Parameters
        true_k = 0.05
        mass = 50.0
        g = 9.8
        thrust_force = mass * 75.0 # Increased thrust to hit 500m with drag
        burn_time = 1.8
        
        # Function to solve for THE WHOLE FLIGHT (Thrust + Coast) with Drag
        def solve_full_flight(k_val):
            dt = t_data[1] - t_data[0]
            y_arr = [0.0]
            v_arr = [0.0]
            
            curr_y, curr_v = 0.0, 0.0
            
            for i in range(len(t_data) - 1):
                t = t_data[i]
                
                # Thrust force active?
                F_thrust = thrust_force if t < burn_time else 0.0
                
                # v' = (F_thrust - F_drag - F_gravity) / m
                # F_drag = k * v * |v|
                
                # RK4 Step
                def get_accel(v):
                    drag = k_val * v * abs(v)
                    return (F_thrust - drag)/mass - g
                
                # k1
                v_k1 = curr_v
                a_k1 = get_accel(curr_v)
                
                # k2
                v_k2 = curr_v + a_k1 * dt/2
                a_k2 = get_accel(v_k2)
                
                # k3
                v_k3 = curr_v + a_k2 * dt/2
                a_k3 = get_accel(v_k3)
                
                # k4 
                v_k4 = curr_v + a_k3 * dt
                a_k4 = get_accel(v_k4)
                
                curr_y += (dt/6) * (v_k1 + 2*v_k2 + 2*v_k3 + v_k4)
                curr_v += (dt/6) * (a_k1 + 2*a_k2 + 2*a_k3 + a_k4)
                
                if curr_y < 0: curr_y, curr_v = 0, 0
                
                y_arr.append(curr_y)
                v_arr.append(curr_v)
            return np.array(y_arr), np.array(v_arr)
            
        # Generate Ground Truth
        y_true, v_true = solve_full_flight(true_k)
        
        # Add realistic noise
        np.random.seed(42)
        noise = np.cumsum(np.random.normal(0, 0.5, len(t_data)))
        kernel_size = 15
        noise_smooth = np.convolve(noise, np.ones(kernel_size)/kernel_size, mode='same')
        y_smooth_data = y_true + noise_smooth
        y_smooth_data = np.clip(y_smooth_data, 0, None)
        
        alt_func = interp1d(t_data, y_smooth_data, kind='cubic', fill_value="extrapolate")
        
        # --- Axis Setup (Matching interpolation.py style) ---
        ax_alt = Axes(
            x_range=[0, 25, 5], y_range=[0, 600, 100],
            x_length=10, y_length=6,
            axis_config={"include_numbers": True}
        ).move_to(ORIGIN).shift(UP * 0.15)
        
        y_label = Text("Altitude (m)", font_size=24).rotate(PI/2).next_to(ax_alt.y_axis, LEFT, buff=0.5)
        x_label = Text("Time (s)", font_size=24).next_to(ax_alt.x_axis, DOWN, buff=0.25)
        
        self.play(Create(ax_alt), Write(y_label), Write(x_label))
        
        # Plot Observed Data
        curve_alt = ax_alt.plot(lambda t: alt_func(t), color=GREEN, x_range=[0, 25])
        # Removed text "Observed Flight Data" as requested
        
        self.play(Create(curve_alt, run_time=2))
        self.wait(1)
        
        # --- Fitting Loop (Discrete Trials) ---
        
        # Initial fit Setup (at burnout)
        t_burn = 1.8
        burn_idx = np.searchsorted(t_data, t_burn)
        y0_fit = y_smooth_data[burn_idx]
        v0_fit = v_true[burn_idx] # Assume we can measure v reasonably well or derive it
        
        t_fit = t_data[burn_idx:]
        y_obs = y_smooth_data[burn_idx:]
        
        # RK4 Solver for just the Coast Phase (Fitting Model)
        def rk4_solve_coast(k_val, t_arr):
            # Solves v' = -g - (k/m)v|v|
            y_res = [y0_fit]
            v_res = [v0_fit]
            c_y, c_v = y0_fit, v0_fit
            
            for i in range(len(t_arr)-1):
                h = t_arr[i+1] - t_arr[i]
                
                def get_coast_accel(v):
                    return -g - (k_val/mass)*v*abs(v)
                
                # k1
                v_k1 = c_v
                a_k1 = get_coast_accel(c_v)
                # k2
                v_k2 = c_v + a_k1*h/2
                a_k2 = get_coast_accel(v_k2)
                # k3
                v_k3 = c_v + a_k2*h/2
                a_k3 = get_coast_accel(v_k3)
                # k4
                v_k4 = c_v + a_k3*h
                a_k4 = get_coast_accel(v_k4)
                
                c_y += (h/6)*(v_k1 + 2*v_k2 + 2*v_k3 + v_k4)
                c_v += (h/6)*(a_k1 + 2*a_k2 + 2*a_k3 + a_k4)
                
                if c_y < 0: c_y, c_v = 0, 0
                y_res.append(c_y)
                
            return np.array(y_res)
            
        def calc_rmse(y_mod, y_dat):
            L = min(len(y_mod), len(y_dat))
            return np.sqrt(np.mean((y_mod[:L] - y_dat[:L])**2))
            
        # Info Box (Top Right)
        k_text = MathTex(r"k = ?", color=RED, font_size=28).move_to(ax_alt.c2p(24, 520))
        rmse_text = MathTex(r"RMSE = ?", color=RED, font_size=28).next_to(k_text, DOWN, aligned_edge=RIGHT)
        self.play(Write(k_text), Write(rmse_text))
        
        # Trials
        trials = [0.001, 0.5, 0.1, 0.05]
        # 0.001 -> Low drag
        # 0.5 -> Very High drag
        # 0.1 -> Moderate drag
        # 0.05 -> Spot on (True Physics)
        
        model_curve = None
        
        for k_val in trials:
            y_model = rk4_solve_coast(k_val, t_fit)
            rmse = calc_rmse(y_model, y_obs)
            
            # Draw fitting curve
            if len(y_model) != len(t_fit):
                 min_len = min(len(y_model), len(t_fit))
                 t_plot = t_fit[:min_len]
                 y_plot = y_model[:min_len]
            else:
                 t_plot = t_fit
                 y_plot = y_model
            
            points = [ax_alt.c2p(t, y) for t, y in zip(t_plot, y_plot)]
            new_curve = VMobject(color=RED)
            new_curve.set_points_smoothly(points)
            
            # Color logic
            color = RED
            if k_val == 0.05: color = GREEN
            elif k_val == 0.1: color = ORANGE
            
            new_curve.set_color(color)
            
            new_k = MathTex(rf"k = {k_val:.3f}", font_size=28).move_to(k_text, aligned_edge=RIGHT)
            new_rmse = MathTex(rf"RMSE = {rmse:.1f}", font_size=28).move_to(rmse_text, aligned_edge=RIGHT)
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
            self.wait(0.8)
            
        # Highlight best
        best_box = SurroundingRectangle(VGroup(k_text, rmse_text), color=GREEN, buff=0.2)
        self.play(Create(best_box))
        
        self.wait(3)
