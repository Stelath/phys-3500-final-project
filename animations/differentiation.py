from manim import *
import numpy as np

class DifferentiationVisualization(Scene):
    def construct(self):
        # --- 1. Data Generation ---
        t_vals = np.linspace(0.5, 24.5, 100) # Higher res for smooth sliding
        true_func = lambda t: -3.2 * (t - 12.5)**2 + 500
        
        np.random.seed(42)
        noise_amp = 40
        # Generate noisy data on a coarser grid first to match interpolation feeling?
        # Actually let's just use the function + noise for generating the curve content
        # But we need the arrays for numerical diff
        
        # Consistent with interpolation.py:
        t_data = np.linspace(0.5, 24.5, 40)
        y_data = [max(0, true_func(t) + np.random.normal(0, noise_amp/2)) for t in t_data]
        
        # Smooth it
        def gaussian_kernel(size, sigma=1):
            x = np.linspace(-size//2, size//2, size)
            k = np.exp(-0.5 * (x/sigma)**2)
            return k / k.sum()
        kernel = gaussian_kernel(size=9, sigma=3)
        y_smooth_data = np.convolve(y_data, kernel, mode='same')
        y_smooth_data[:4] = y_data[:4]
        y_smooth_data[-4:] = y_data[-4:]
        
        # Create interpolation functions for continuous sampling in animation
        from scipy.interpolate import interp1d
        # Kind='cubic' to match the spline feeling
        alt_func = interp1d(t_data, y_smooth_data, kind='cubic', fill_value="extrapolate")
        
        # Calculate Derivatives numerically on the fine grid
        ts = np.linspace(0, 25, 200)
        dt = ts[1] - ts[0]
        ys = alt_func(ts)
        
        # Central difference for Velocity
        vs = np.zeros_like(ys)
        vs[1:-1] = (ys[2:] - ys[:-2]) / (2*dt)
        vs[0] = (ys[1] - ys[0]) / dt
        vs[-1] = (ys[-1] - ys[-2]) / dt
        
        vel_func = interp1d(ts, vs, kind='linear', fill_value="extrapolate")

        # Central difference for Acceleration
        as_ = np.zeros_like(vs)
        as_[1:-1] = (vs[2:] - vs[:-2]) / (2*dt)
        as_[0] = (vs[1] - vs[0]) / dt
        as_[-1] = (vs[-1] - vs[-2]) / dt
        
        acc_func = interp1d(ts, as_, kind='linear', fill_value="extrapolate")

        # --- 2. Setup Axes (Phase 1) ---
        # Left: Altitude (Green)
        # Right: Velocity (Red)
        
        # Define configuration
        config_alt = {
            "x_range": [0, 25, 5], "y_range": [0, 600, 100], 
            "x_length": 6, "y_length": 4, 
            "axis_config": {"include_numbers": True, "font_size": 20}
        }
        config_vel = {
            "x_range": [0, 25, 5], "y_range": [-100, 100, 50], 
            "x_length": 6, "y_length": 4, 
            "axis_config": {"include_numbers": True, "font_size": 20}
        }
        config_acc = {
            "x_range": [0, 25, 5], "y_range": [-20, 20, 5], 
            "x_length": 6, "y_length": 4, 
            "axis_config": {"include_numbers": True, "font_size": 20}
        }

        ax_alt = Axes(**config_alt).to_edge(LEFT, buff=0.5)
        ax_vel = Axes(**config_vel).to_edge(RIGHT, buff=0.5)
        
        # Labels
        lbl_alt = Text("Altitude (m)", font_size=20, color=GREEN).next_to(ax_alt, UP)
        lbl_vel = Text("Velocity (m/s)", font_size=20, color=RED).next_to(ax_vel, UP)
        
        # Curves
        curve_alt = ax_alt.plot(lambda t: alt_func(t), color=GREEN, x_range=[0, 25])
        curve_vel = ax_vel.plot(lambda t: vel_func(t), color=RED, x_range=[0, 25])
        
        # --- Animation Phase 1 : Alt -> Vel ---
        self.play(Create(ax_alt), Write(lbl_alt), Create(curve_alt))
        self.play(Create(ax_vel), Write(lbl_vel))
        
        # Sliding Tangent Updater
        t_tracker = ValueTracker(0.1) # Start slightly > 0 for calc safety
        
        # Visual Elements for Sliding Window
        dot_center = Dot(color=WHITE)
        dot_left = Dot(color=WHITE).scale(0.8)
        dot_right = Dot(color=WHITE).scale(0.8)
        tangent_line = Line(color=RED)
        
        def update_tangent_elements(m):
            t = t_tracker.get_value()
            dt_step = 2.0 # The "width" of the secant window
            
            p_c = ax_alt.c2p(t, alt_func(t))
            p_l = ax_alt.c2p(max(0, t - dt_step), alt_func(max(0, t - dt_step)))
            p_r = ax_alt.c2p(min(25, t + dt_step), alt_func(min(25, t + dt_step)))
            
            dot_center.move_to(p_c)
            dot_left.move_to(p_l)
            dot_right.move_to(p_r)
            
            # Draw line through left and right points
            tangent_line.put_start_and_end_on(p_l, p_r)
            # Make it longer visually?
            # tangent_line.scale(1.5) # Scale resets center, careful. 
            # put_start_and_end defines center. scaling around center is fine.
            tangent_line.scale(1.2)

        # Group them
        sliding_group = VGroup(dot_center, dot_left, dot_right, tangent_line)
        sliding_group.add_updater(update_tangent_elements)
        
        self.add(sliding_group)
        
        # Animate!
        # Sync the tracker with the creation of the velocity curve
        duration = 8.0
        self.play(
            t_tracker.animate.set_value(24.9), 
            Create(curve_vel),
            run_time=duration,
            rate_func=linear
        )
        
        sliding_group.remove_updater(update_tangent_elements)
        self.play(FadeOut(sliding_group))
        self.wait(1)
        
        # --- Phase 2: Shift ---
        # Fade out Altitude stuff
        self.play(
            FadeOut(ax_alt), FadeOut(lbl_alt), FadeOut(curve_alt)
        )
        
        # Move Velocity to Left
        ax_vel_target = Axes(**config_vel).to_edge(LEFT, buff=0.5)
        curve_vel_target = ax_vel_target.plot(lambda t: vel_func(t), color=RED, x_range=[0, 25])
        # We need to act on the mobjects themselves to keep them valid
        # Easier to just ApplyMethod move_to
        
        self.play(
            ax_vel.animate.move_to(ax_vel_target.get_center()),
            lbl_vel.animate.next_to(ax_vel_target, UP),
            curve_vel.animate.move_to(curve_vel_target.get_center()).align_to(curve_vel_target, LEFT) # Curves are tricky to move because they are paths
            # Actually, standard VGroup move works fine if grouped
        )
        # Re-align exactly just in case
        # Or just construct new ones and fade transform?
        # Let's try transform to be safe on coordinates
        
        # Actually simplest: Create new Acceleration Axis on Right
        ax_acc = Axes(**config_acc).to_edge(RIGHT, buff=0.5)
        lbl_acc = Text("Acceleration (m/s²)", font_size=20, color=YELLOW).next_to(ax_acc, UP)
        curve_acc = ax_acc.plot(lambda t: acc_func(t), color=YELLOW, x_range=[0, 25])
        
        self.play(Create(ax_acc), Write(lbl_acc))
        
        # --- Phase 3: Vel -> Accel ---
        # Now sliding tangent is on Velocity Curve (RED)
        # And drawing Accel Curve (YELLOW)
        
        t_tracker.set_value(0.1)
        
        dot_center.color = WHITE
        dot_left.color = WHITE
        dot_right.color = WHITE
        tangent_line.color = YELLOW 
        
        def update_tangent_elements_vel(m):
            t = t_tracker.get_value()
            dt_step = 2.0
            
            # Using ax_vel coordinates now!
            # Note: ax_vel has moved. c2p should respect the new position if it was moved correctly.
            
            p_c = ax_vel.c2p(t, vel_func(t))
            p_l = ax_vel.c2p(max(0, t - dt_step), vel_func(max(0, t - dt_step)))
            p_r = ax_vel.c2p(min(25, t + dt_step), vel_func(min(25, t + dt_step)))
            
            dot_center.move_to(p_c)
            dot_left.move_to(p_l)
            dot_right.move_to(p_r)
            tangent_line.put_start_and_end_on(p_l, p_r)
            tangent_line.scale(1.2)

        sliding_group = VGroup(dot_center, dot_left, dot_right, tangent_line)
        sliding_group.add_updater(update_tangent_elements_vel)
        self.add(sliding_group)
        
        self.play(
            t_tracker.animate.set_value(24.9), 
            Create(curve_acc),
            run_time=duration,
            rate_func=linear
        )
        
        sliding_group.remove_updater(update_tangent_elements_vel)
        self.play(FadeOut(sliding_group))
        self.wait(2)
