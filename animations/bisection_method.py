from manim import *

class BisectionMethod(Scene):
    def construct(self):
        # 1. Introduction
        title = Text("Bisection Method", font_size=40)
        subtitle = Text("Root Finding Algorithm", font_size=24, color=GRAY).next_to(title, DOWN)
        self.play(Write(title), Write(subtitle))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # 2. Setup Axes and Function
        ax = Axes(
            x_range=[0, 6, 1],
            y_range=[-3, 3, 1],
            axis_config={"include_numbers": True},
            tips=False
        )
        labels = ax.get_axis_labels(x_label="x", y_label="f(x)")
        
        # Function: f(x) = (x-3)^3 / 2 - 0.5 (Just a curve that crosses at x approx 4.something or simple)
        # Let's use something simple: f(x) = x^2 - 4  -> Root at 2 (if x>0)
        # Or better visual: f(x) = 0.5 * (x - 2.5)^3 - (x - 2.5)
        
        def func(x):
            return 0.5 * (x - 3)**3 - 0.5 * (x - 3) + 1 
            # Check roots... too complex to calculate in head for demo
            # Let's use f(x) = ln(x) - 1 => Root at e=2.718...
            # f(0.5) < 0, f(4) > 0
        
        # Let's use a polynomial cubic with a clear root
        # f(x) = (x - 3.5)
        # Actually, let's just draw a curve
        graph = ax.plot(lambda x: 0.3 * (x - 1) * (x - 3) * (x - 5), color=BLUE, x_range=[0, 6])
        # Roots at 1, 3, 5. Let's look for the root at 3 in interval [2, 4]
        # f(2) = 0.3 * (1) * (-1) * (-3) = 0.9 > 0
        # f(4) = 0.3 * (3) * (1) * (-1) = -0.9 < 0
        # Wait, f(2)>0 and f(4)<0, good sign change. Root is 3.

        self.play(Create(ax), Create(labels))
        self.play(Create(graph))
        self.wait(1)

        # 3. Algorithm Visualization
        # Initial Interval [a, b]
        a_val = 2.0
        b_val = 4.0
        
        # Visual markers
        a_line = self.get_vertical_line(ax, a_val, "a", color=RED)
        b_line = self.get_vertical_line(ax, b_val, "b", color=GREEN)
        
        self.play(Create(a_line['line']), Write(a_line['label']))
        self.play(Create(b_line['line']), Write(b_line['label']))
        
        interval_rect = Rectangle(
            width=ax.c2p(b_val,0)[0] - ax.c2p(a_val,0)[0],
            height=6,
            fill_color=YELLOW,
            fill_opacity=0.2,
            stroke_opacity=0
        ).move_to(ax.c2p((a_val+b_val)/2, 0))
        
        self.play(FadeIn(interval_rect))
        
        # Iteration Loop
        iterations = 5
        for i in range(iterations):
            m_val = (a_val + b_val) / 2
            m_line = self.get_vertical_line(ax, m_val, f"m_{i+1}", color=ORANGE)
            
            self.play(Create(m_line['line']), Write(m_line['label']))
            self.wait(0.5)
            
            # Check signs
            f_a = 0.3 * (a_val - 1) * (a_val - 3) * (a_val - 5)
            f_m = 0.3 * (m_val - 1) * (m_val - 3) * (m_val - 5)
            
            # Highlight the sub-interval
            if f_a * f_m < 0:
                # Root is in [a, m]
                new_b = m_val
                discard_rect = Rectangle(
                    width=ax.c2p(b_val,0)[0] - ax.c2p(m_val,0)[0],
                    height=6,
                    fill_color=BLACK,
                    fill_opacity=0.8,
                    stroke_opacity=0
                ).move_to(ax.c2p((m_val+b_val)/2, 0))
                
                self.play(FadeIn(discard_rect))
                self.play(FadeOut(b_line['line']), FadeOut(b_line['label']), FadeOut(discard_rect))
                
                # Update b
                b_val = new_b
                b_line = m_line # The old m becomes new b
                # Rename label? Just leave as m_i for trace history or fade out
                self.play(m_line['label'].animate.become(
                    MathTex("b").move_to(m_line['label']).set_color(GREEN)
                ))
            else:
                # Root is in [m, b]
                new_a = m_val
                discard_rect = Rectangle(
                    width=ax.c2p(m_val,0)[0] - ax.c2p(a_val,0)[0],
                    height=6,
                    fill_color=BLACK,
                    fill_opacity=0.8,
                    stroke_opacity=0
                ).move_to(ax.c2p((a_val+m_val)/2, 0))
                
                self.play(FadeIn(discard_rect))
                self.play(FadeOut(a_line['line']), FadeOut(a_line['label']), FadeOut(discard_rect))
                
                # Update a
                a_val = new_a
                a_line = m_line
                self.play(m_line['label'].animate.become(
                    MathTex("a").move_to(m_line['label']).set_color(RED)
                ))
                
            # Shrink interval highlight
            new_width = ax.c2p(b_val,0)[0] - ax.c2p(a_val,0)[0]
            new_center = ax.c2p((a_val+b_val)/2, 0)
            self.play(interval_rect.animate.set_width(new_width).move_to(new_center))
            self.wait(0.5)

        # Conclusion
        final_root_text = Text(f"Root approx: {(a_val+b_val)/2:.4f}", font_size=24).to_corner(UR)
        self.play(Write(final_root_text))
        self.wait(2)

    def get_vertical_line(self, ax, x_val, label_text, color=WHITE):
        # Create a vertical line spanning the graph height
        start = ax.c2p(x_val, -3)
        end = ax.c2p(x_val, 3)
        line = Line(start, end, color=color)
        
        label = MathTex(label_text, color=color).next_to(line, DOWN)
        return {"line": line, "label": label}
