import os
from manim import *


class RadianInterpretation(Scene):
    def construct(self):
        # Title (optional)
        title = Text("Geometric Interpretation of the Radian", font_size=35)
        title.to_edge(UP)

        # Circle of radius = 3
        circle_radius = 3
        circle = Circle(radius=circle_radius, color=WHITE)

        # Two radii (angle = 1 rad initially)
        radius_line_1 = Line(ORIGIN, circle.point_at_angle(0), color=YELLOW)
        radius_line_2 = Line(ORIGIN, circle.point_at_angle(1), color=YELLOW)

        # Labels for radii, placed at halfway but shifted
        radius_label_1 = MathTex("r")
        midpoint_1 = radius_line_1.point_from_proportion(0.5)
        radius_label_1.move_to(midpoint_1 + 0.3 * UP)  # shift up by 0.3

        radius_label_2 = MathTex("r")
        midpoint_2 = radius_line_2.point_from_proportion(0.5)
        radius_label_2.move_to(midpoint_2 + 0.3 * UP)  # shift up by 0.3

        # --- CRUCIAL PART: ADD UPDATER FOR radius_label_2 ---
        # This makes radius_label_2 follow the second radius upon rotation.
        radius_label_2.add_updater(
            lambda mob: mob.move_to(radius_line_2.point_from_proportion(0.5) + 0.3 * UP)
        )

        # Main arc (0 -> 1 rad) with radius=3
        arc = Arc(radius=circle_radius, start_angle=0, angle=1, color=RED)
        # Arc label for 1 rad
        arc_label = (
            MathTex(r"\text{arc length} = r").next_to(arc, RIGHT, buff=0.1).scale(0.8)
        )

        # Small arc inside the angle (for 1 rad)
        inner_arc_radius = 1
        inner_arc = Arc(radius=inner_arc_radius, start_angle=0, angle=1, color=RED)
        # Single small angle label, placed near the smaller arc
        angle_label = MathTex("1 \\text{ rad}").scale(0.8)
        angle_label.next_to(inner_arc, UP, buff=0.1)

        # Animations
        self.play(FadeIn(title))
        self.play(Create(circle))
        dot_center = Dot(ORIGIN, color=ORANGE)
        self.play(FadeIn(dot_center))

        self.play(Create(radius_line_1))
        self.play(Create(radius_line_2))

        self.play(Create(arc))

        self.play(Write(radius_label_1))
        self.play(Write(radius_label_2))
        self.play(Write(arc_label))

        # Draw the small angle arc and its label (for 1 rad)
        self.play(Create(inner_arc))
        self.play(Write(angle_label))

        self.wait(2)

        # --- TRANSITION FROM 1 rad TO 2 rad ---
        new_arc = Arc(radius=circle_radius, start_angle=0, angle=2, color=RED)
        new_inner_arc = Arc(radius=inner_arc_radius, start_angle=0, angle=2, color=RED)
        # New labels for 2 rad
        new_angle_label = MathTex("2 \\text{ rad}").scale(0.8)
        new_angle_label.next_to(new_inner_arc, UP, buff=0.1)

        new_arc_label = MathTex(r"\text{arc length} = 2r").scale(0.8)
        new_arc_label.next_to(new_arc, RIGHT, buff=0.1)

        # Animate the transformation to 2 rad
        self.play(
            Transform(arc, new_arc),
            Transform(inner_arc, new_inner_arc),
            Transform(angle_label, new_angle_label),
            Transform(arc_label, new_arc_label),
            Rotate(radius_line_2, angle=1, about_point=ORIGIN),
            run_time=2,
        )

        self.wait(2)

        # --- NEW ANIMATION: FROM 2 rad TO pi rad ---
        pi_arc = Arc(radius=circle_radius, start_angle=0, angle=PI, color=RED)
        pi_inner_arc = Arc(radius=inner_arc_radius, start_angle=0, angle=PI, color=RED)

        # pi rad labels
        pi_angle_label = MathTex("\\pi \\text{ rad}").scale(0.8)
        pi_angle_label.next_to(pi_inner_arc, UP, buff=0.1)

        pi_arc_label = MathTex(r"\text{arc length} = \pi r").scale(0.8)
        pi_arc_label.next_to(pi_arc, RIGHT, buff=0.1)

        # Animate the transition to pi rad (half circle)
        # Note: we add (PI - 2) = ~1.14159 to rotate from 2 rad to pi rad
        self.play(
            Transform(arc, pi_arc),
            Transform(inner_arc, pi_inner_arc),
            Transform(angle_label, pi_angle_label),
            Transform(arc_label, pi_arc_label),
            Rotate(radius_line_2, angle=(PI - 2), about_point=ORIGIN),
            run_time=2,
        )

        self.wait(2)

        # You can remove the updater if no longer needed
        # radius_label_2.remove_updater(...)


if __name__ == "__main__":
    os.system("manim -p -ql radian_expl.py RadianInterpretation")
