from manim import *
import numpy as np
from scipy.interpolate import interp1d

class IntegrationVisualization(Scene):
    def construct(self):
        # --- 1. Physics & Data Setup ---
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
        
        # Consistent Noise
        np.random.seed(42)
        noise = np.cumsum(np.random.normal(0, 0.5, len(t_data)))
        kernel_size = 15
        noise_smooth = np.convolve(noise, np.ones(kernel_size)/kernel_size, mode='same')
        y_smooth_data = np.clip(y_raw + noise_smooth, 0, None)
        
        alt_func = interp1d(t_data, y_smooth_data, kind='cubic', fill_value="extrapolate")
        
        # Compute Velocity
        ts = np.linspace(0, 25, 200)
        dt_fine = ts[1] - ts[0]
        ys = alt_func(ts)
        vs = np.zeros_like(ys)
        vs[1:-1] = (ys[2:] - ys[:-2]) / (2*dt_fine)
        vs[0] = (ys[1] - ys[0]) / dt_fine
        vs[-1] = (ys[-1] - ys[-2]) / dt_fine
        
        vel_func = interp1d(ts, vs, kind='linear', fill_value="extrapolate")
        
        # Compute Speed (Absolute Velocity)
        speed_func = lambda t: abs(vel_func(t))

        # --- 2. Scene Setup ---
        
        # Left Axis: Initial Velocity -> Becomes Speed
        conf_vel = {"x_range": [0, 25, 5], "y_range": [-100, 100, 50], "x_length": 6, "y_length": 4}
        
        # Right Axis: Total Distance (Accumulated Speed)
        # Total distance ~ 1000m+
        conf_dist = {"x_range": [0, 25, 5], "y_range": [0, 1200, 200], "x_length": 6, "y_length": 4}
        
        ax_left = Axes(**conf_vel, axis_config={"include_numbers": True, "font_size": 20}).to_edge(LEFT, buff=0.5)
        ax_right = Axes(**conf_dist, axis_config={"include_numbers": True, "font_size": 20}).to_edge(RIGHT, buff=0.5)
        
        lbl_vel = Text("Velocity (m/s)", font_size=24, color=RED).next_to(ax_left, UP)
        lbl_dist = Text("Total Distance (m)", font_size=24, color=GREEN).next_to(ax_right, UP)
        
        # 1. Show Velocity Curve
        c_vel = ax_left.plot(lambda t: vel_func(t), color=RED, x_range=[0, 25])
        v_zero_line = ax_left.get_horizontal_line(ax_left.c2p(25, 0), color=WHITE, stroke_width=1)
        
        self.play(Create(ax_left), Write(lbl_vel), Create(c_vel), Create(v_zero_line))
        self.wait(1)
        
        # 2. Transform to Speed Curve
        lbl_speed = Text("Speed |v(t)|", font_size=24, color=ORANGE).next_to(ax_left, UP)
        c_speed = ax_left.plot(lambda t: speed_func(t), color=ORANGE, x_range=[0, 25])
        
        intro_flip = Text("Integrate Speed to Total Distance", font_size=32).to_edge(UP)
        self.play(Write(intro_flip))
        
        self.play(
            Transform(c_vel, c_speed), # Transform Red Velocity to Orange Speed
            Transform(lbl_vel, lbl_speed)
        )
        self.wait(1)
        
        # 3. Setup Right Axis
        self.play(Create(ax_right), Write(lbl_dist))
        
        # --- 4. Integration Loop ---
        dt_step = 1.0 
        steps = int(25 / dt_step)
        
        current_time = 0.0
        current_distance = 0.0
        
        curve_group = VGroup()
        trapezoid_group = VGroup()
        
        area_tracker = ValueTracker(0)
        area_label = Integer(0, unit=" m").next_to(lbl_dist, RIGHT, buff=0.5).set_color(GREEN)
        area_label.add_updater(lambda m: m.set_value(area_tracker.get_value()))
        self.add(area_label)
        
        for i in range(steps):
            t_start = current_time
            t_end = current_time + dt_step
            
            # Physics values (using SPEED now)
            s_start = speed_func(t_start)
            s_end = speed_func(t_end)
            
            # Trapezoid Area under SPEED curve
            area_chunk = 0.5 * (s_start + s_end) * dt_step
            next_distance = current_distance + area_chunk
            
            # Points on Left Graph (Speed)
            p1 = ax_left.c2p(t_start, s_start)
            p2 = ax_left.c2p(t_end, s_end)
            p1_base = ax_left.c2p(t_start, 0)
            p2_base = ax_left.c2p(t_end, 0)
            
            # Create Trapezoid Shape
            trap = Polygon(p1_base, p1, p2, p2_base, color=YELLOW, fill_opacity=0.3, stroke_width=2)
            
            self.play(Create(trap), run_time=0.2)
            
            # Points on Right Graph (Distance)
            p_d_start = ax_right.c2p(t_start, current_distance)
            p_d_end = ax_right.c2p(t_end, next_distance)
            
            # Segment on Distance Graph
            dist_segment = Line(p_d_start, p_d_end, color=GREEN, stroke_width=4)
            
            self.play(
                TransformFromCopy(trap, dist_segment),
                area_tracker.animate.set_value(next_distance),
                run_time=0.2
            )
            
            curve_group.add(dist_segment)
            trapezoid_group.add(trap)
            
            current_time = t_end
            current_distance = next_distance
            
            # Fade out older ones to minimize clutter
            if len(trapezoid_group) > 4:
                 self.play(FadeOut(trapezoid_group[-5]), run_time=0.1)

        self.wait(1)
        self.play(FadeOut(trapezoid_group)) # Clean up remaining
        
        # Show smooth curve overlay
        # We need a function for distance(t). It's integral of speed.
        # Let's just create a spline from our discrete points for the visual check
        # Or recalculate. 
        # Actually, let's just leave the piecewise Green line as the "Result" 
        # because "The Trapezoid Method outline in src/numerical/trapezoid.m" produces discrete steps.
        
        final_lbl = Text("Total Distance", font_size=20, color=WHITE).next_to(dist_segment, UP)
        final_lbl.shift(LEFT * final_lbl.width / 2)
        self.play(Write(final_lbl))
        
        self.wait(3)
