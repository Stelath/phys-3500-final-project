from manim import *
import numpy as np

class DifferentiationVisualization(Scene):
    def construct(self):
        # Realistic rocket profile:
        # Phase 1 (0-3s): Thrust phase with high positive acceleration
        # Phase 2 (3s-peak): Coast up with gravity deceleration
        # Phase 3 (peak-25s): Fall back down with gravity
        
        t_data = np.linspace(0, 25, 200)
        
        # Build altitude piecewise
        # Build altitude piecewise
        def rocket_altitude(t):
            g = 9.8  # gravity
            thrust_accel = 50.3  # Adjusted for approx 500m peak with high v0
            burn_time = 1.8
            v0 = 0.0 # High initial velocity for very sharp takeoff (no S-curve)
            
            if t <= burn_time:
                # Thrust phase: d = v0*t + 0.5*a*t^2
                alt = v0 * t + 0.5 * thrust_accel * t**2
            else:
                # At end of burn:
                v_burnout = v0 + thrust_accel * burn_time
                h_burnout = v0 * burn_time + 0.5 * thrust_accel * burn_time**2
                
                # Coast phase
                dt = t - burn_time
                alt = h_burnout + v_burnout * dt - 0.5 * g * dt**2
            
            return max(0, alt)
        
        y_smooth_data = np.array([rocket_altitude(t) for t in t_data])
        
        # Add smooth noise (increased slightly as requested)
        np.random.seed(42)
        # Use cumulative sum of random values
        noise = np.cumsum(np.random.normal(0, 0.5, len(t_data))) # Increased noise
        # Apply a low-pass filter
        kernel_size = 15
        noise_smooth = np.convolve(noise, np.ones(kernel_size)/kernel_size, mode='same')
        y_smooth_data = y_smooth_data + noise_smooth
        y_smooth_data = np.clip(y_smooth_data, 0, None) # Ensure noise doesn't put us underground
        
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
            "x_range": [0, 25, 5], "y_range": [-20, 60, 10], 
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
            dt_step = 0.5 # Closer points
            
            p_c = ax_alt.c2p(t, alt_func(t))
            p_l = ax_alt.c2p(max(0, t - dt_step), alt_func(max(0, t - dt_step)))
            p_r = ax_alt.c2p(min(25, t + dt_step), alt_func(min(25, t + dt_step)))
            
            dot_center.move_to(p_c)
            dot_left.move_to(p_l)
            dot_right.move_to(p_r)
            
            # Draw line through left and right points
            tangent_line.put_start_and_end_on(p_l, p_r)
            tangent_line.scale(6.0)

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
            dt_step = 0.5
            
            # Using ax_vel coordinates now!
            # Note: ax_vel has moved. c2p should respect the new position if it was moved correctly.
            
            p_c = ax_vel.c2p(t, vel_func(t))
            p_l = ax_vel.c2p(max(0, t - dt_step), vel_func(max(0, t - dt_step)))
            p_r = ax_vel.c2p(min(25, t + dt_step), vel_func(min(25, t + dt_step)))
            
            dot_center.move_to(p_c)
            dot_left.move_to(p_l)
            dot_right.move_to(p_r)
            tangent_line.put_start_and_end_on(p_l, p_r)
            tangent_line.scale(6.0)

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
