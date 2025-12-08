from manim import *
import numpy as np

class RungeKuttaMethod(Scene):
    def construct(self):
        # 1. Intro
        title = Text("Runge-Kutta 4 Method", font_size=40)
        formula = MathTex(
            r"y_{n+1} = y_n + \frac{h}{6}(k_1 + 2k_2 + 2k_3 + k_4)",
            font_size=32
        ).next_to(title, DOWN)
        self.play(Write(title), Write(formula))
        self.wait(2)
        self.play(FadeOut(title), Uncreate(formula)) # Uncreate for fun

        # 2. Setup Axes
        ax = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            axis_config={"include_numbers": True},
        )
        labels = ax.get_axis_labels(x_label="t", y_label="y")
        
        # ODE: y' = 0.5 * t * (3 - y)  (Just a made up slope field)
        # Solution tends to y=3
        def slope_func(t, y):
             return 1.0 * np.sin(t*2) + 0.5 # Oscillating slope
             # Or simpler: y' = f(t,y)
             # Let's use a function where y(t) is known so we can plot "True" path vs steps
             # y' = cos(t), y(0)=1 => y = sin(t) + 1
             # Slope depends only on t for simplicity of visual?
             # Better: y' = y. Exponential. Too standard.
             # Let's stick to the visual geometry.
        
        # Let's define the visual curve we are 'following'
        # True solution y = 0.5 * t^2 + 1 => y' = t. 
        # k1 at t=0, y=1 => slope=0. 
        
        # Let's use y' = -y + t + 1 (Linear stable system)
        # Solution converges to y = t.
        # Let's just hardcode the function for the visual
        def f(t, y):
             return np.cos(t) + 0.5

        # Initial State
        t0 = 0.5
        y0 = 1.0
        h = 2.0 # Large step for visualization
        
        # Point P0
        p0_coords = ax.c2p(t0, y0)
        dot0 = Dot(p0_coords, color=YELLOW)
        label0 = MathTex("P_n").next_to(dot0, DOWN)

        self.play(Create(ax), Create(labels))
        self.play(FadeIn(dot0), Write(label0))

        # --- k1 ---
        # k1 = f(t0, y0)
        k1 = f(t0, y0)
        # Draw slope k1 at P0
        slope_line_1 = self.get_slope_line(ax, t0, y0, k1, length=h, color=RED)
        label_k1 = MathTex("k_1").next_to(slope_line_1, UP, buff=0.1).set_color(RED)
        
        self.play(Create(slope_line_1), Write(label_k1))
        self.wait(1)
        
        # Move to midpoint
        # point p1_temp = y0 + k1 * h/2
        t_mid = t0 + h/2
        y_mid_1 = y0 + k1 * h/2
        
        dot_mid_1 = Dot(ax.c2p(t_mid, y_mid_1), color=RED_E)
        dashed_1 = DashedLine(p0_coords, ax.c2p(t_mid, y_mid_1), color=RED, dash_length=0.1)
        
        self.play(FadeIn(dashed_1), FadeIn(dot_mid_1))
        
        # --- k2 --- 
        # k2 = f(t_mid, y_mid_1)
        k2 = f(t_mid, y_mid_1)
        # Draw slope k2 at the temporary midpoint
        slope_line_2_temp = self.get_slope_line(ax, t_mid, y_mid_1, k2, length=1, color=GREEN)
        self.play(Create(slope_line_2_temp))
        
        # "Use this slope from P0"
        slope_line_2 = self.get_slope_line(ax, t0, y0, k2, length=h, color=GREEN)
        self.play(TransformFromCopy(slope_line_2_temp, slope_line_2))
        self.play(FadeOut(slope_line_2_temp), FadeOut(dashed_1), FadeOut(dot_mid_1), FadeOut(slope_line_1), FadeOut(label_k1))
        
        label_k2 = MathTex("k_2").next_to(slope_line_2, UP, buff=0.1).set_color(GREEN)
        self.play(Write(label_k2))
        
        # Move to midpoint using k2
        y_mid_2 = y0 + k2 * h/2
        dot_mid_2 = Dot(ax.c2p(t_mid, y_mid_2), color=GREEN_E)
        dashed_2 = DashedLine(p0_coords, ax.c2p(t_mid, y_mid_2), color=GREEN, dash_length=0.1)
        self.play(FadeIn(dashed_2), FadeIn(dot_mid_2))
        
        # --- k3 ---
        # k3 = f(t_mid, y_mid_2)
        k3 = f(t_mid, y_mid_2)
        slope_line_3_temp = self.get_slope_line(ax, t_mid, y_mid_2, k3, length=1, color=BLUE)
        self.play(Create(slope_line_3_temp))
        
        slope_line_3 = self.get_slope_line(ax, t0, y0, k3, length=h, color=BLUE)
        self.play(TransformFromCopy(slope_line_3_temp, slope_line_3))
        self.play(FadeOut(slope_line_3_temp), FadeOut(dashed_2), FadeOut(dot_mid_2), FadeOut(slope_line_2), FadeOut(label_k2))
        
        label_k3 = MathTex("k_3").next_to(slope_line_3, UP, buff=0.1).set_color(BLUE)
        self.play(Write(label_k3))
        
        # Move to end using k3
        t_end = t0 + h
        y_end_temp = y0 + k3 * h
        dot_end_temp = Dot(ax.c2p(t_end, y_end_temp), color=BLUE_E)
        dashed_3 = DashedLine(p0_coords, ax.c2p(t_end, y_end_temp), color=BLUE, dash_length=0.1)
        self.play(FadeIn(dashed_3), FadeIn(dot_end_temp))
        
        # --- k4 ---
        # k4 = f(t_end, y_end_temp)
        k4 = f(t_end, y_end_temp)
        slope_line_4_temp = self.get_slope_line(ax, t_end, y_end_temp, k4, length=1, color=ORANGE)
        self.play(Create(slope_line_4_temp))
        
        slope_line_4 = self.get_slope_line(ax, t0, y0, k4, length=h, color=ORANGE)
        self.play(TransformFromCopy(slope_line_4_temp, slope_line_4))
        self.play(FadeOut(slope_line_4_temp), FadeOut(dashed_3), FadeOut(dot_end_temp), FadeOut(slope_line_3), FadeOut(label_k3))
        
        label_k4 = MathTex("k_4").next_to(slope_line_4, UP, buff=0.1).set_color(ORANGE)
        self.play(Write(label_k4))
        
        # --- Weighted Average ---
        # Final slope k_avg = (k1 + 2k2 + 2k3 + k4)/6
        # Just show the final result
        k_avg = (k1 + 2*k2 + 2*k3 + k4) / 6
        
        final_vec = self.get_slope_line(ax, t0, y0, k_avg, length=h, color=PURPLE)
        label_avg = MathTex("Mean Slope").next_to(final_vec, DOWN).set_color(PURPLE)
        
        self.play(ReplacementTransform(slope_line_4, final_vec), FadeOut(label_k4))
        self.play(Write(label_avg))
        
        final_y = y0 + k_avg * h
        final_dot = Dot(ax.c2p(t_end, final_y), color=YELLOW)
        final_label = MathTex("P_{n+1}").next_to(final_dot, RIGHT)
        
        self.play(Transform(dot0.copy(), final_dot), Write(final_label))
        self.wait(2)
        
    def get_slope_line(self, ax, t, y, slope, length=1.0, color=WHITE):
        # Create a line with slope 'slope' passing through (t,y)
        # Vector is (1, slope). Normalize or scale to dx=length?
        # Let's scale dx=length
        p1 = ax.c2p(t, y)
        p2 = ax.c2p(t + length, y + slope*length)
        return Line(p1, p2, color=color)
