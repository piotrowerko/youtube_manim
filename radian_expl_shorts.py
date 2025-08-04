import os
from manim import *


class RadianInterpretationShorts(Scene):
    def __init__(self, **kwargs):
        # Ustawienie rozdzielczości i wymiarów sceny w proporcjach 9:16 (540p)
        config.pixel_width = 540
        config.pixel_height = 960
        # 5.4 : 9.6 = 9 : 16
        config.frame_width = 5.4
        config.frame_height = 9.6
        super().__init__(**kwargs)

    def construct(self):
        # Tytuł rozbity na trzy linie, by lepiej mieścił się w pionie
        title = Text(
            "Geometric\nInterpretation\nof the Radian", font_size=20, line_spacing=0.8
        )
        title.to_edge(UP)

        # Mniejszy promień (1.5), by zmieścić się w 9:16
        circle_radius = 1.5
        circle = Circle(radius=circle_radius, color=WHITE)

        # kropka w centrum okręgu
        dot_center = Dot(ORIGIN, color=ORANGE)

        # Dwa promienie (z kątem = 1 rad)
        radius_line_1 = Line(ORIGIN, circle.point_at_angle(0), color=YELLOW)
        radius_line_2 = Line(ORIGIN, circle.point_at_angle(1), color=YELLOW)

        # Etykiety promieni "r" – przesunięte i pomniejszone
        radius_label_1 = MathTex("r").scale(0.75)  # 25% mniejsze
        midpoint_1 = radius_line_1.point_from_proportion(0.5)
        radius_label_1.move_to(midpoint_1 + 0.2 * DOWN)

        radius_label_2 = MathTex("r").scale(0.75)  # 25% mniejsze
        midpoint_2 = radius_line_2.point_from_proportion(0.5)
        radius_label_2.move_to(midpoint_2 + 0.2 * UP)

        # Updater, aby druga etykieta "r" podążała za promieniem
        radius_label_2.add_updater(
            lambda mob: mob.move_to(radius_line_2.point_from_proportion(0.5) + 0.2 * UP)
        )

        # Główny łuk (od 0 do 1 rad)
        arc = Arc(radius=circle_radius, start_angle=0, angle=1, color=RED)
        # Dwuliniowa etykieta (arc / = r), 25% mniejsza niż wcześniej
        arc_label = MathTex(r"\text{arc}\\= r").scale(0.525)
        arc_label.next_to(arc, RIGHT, buff=0.1)
        # move the arc_label a bit up and very slightly to the left
        arc_label.shift(0.7 * UP + 0.3 * LEFT)

        # Mały łuk do oznaczenia kąta 1 rad, zredukowany 25%
        inner_arc_radius = 0.7
        inner_arc = Arc(radius=inner_arc_radius, start_angle=0, angle=1, color=RED)
        angle_label = MathTex("1 \\text{ rad}").scale(0.525)
        angle_label.next_to(inner_arc, buff=0.1)

        # Animacje: utworzenie tytułu, okręgu, kropki centralnej, promieni, łuku, etykiet
        self.play(FadeIn(title))
        self.play(Create(circle))

        self.play(FadeIn(dot_center))

        self.play(Create(radius_line_1), Create(radius_line_2))
        self.play(Create(arc))

        self.play(Write(radius_label_1), Write(radius_label_2))
        self.play(Write(arc_label))

        self.play(Create(inner_arc), Write(angle_label))
        self.wait(2)

        # Przejście 1 rad -> 2 rad
        arc_2 = Arc(radius=circle_radius, start_angle=0, angle=2, color=RED)
        arc_label_2 = MathTex(r"\text{arc}\\= 2r").scale(0.525)
        arc_label_2.next_to(arc_2, RIGHT, buff=0.1)
        arc_label_2.shift(0.7 * UP + 0.3 * LEFT)

        inner_arc_2 = Arc(radius=inner_arc_radius, start_angle=0, angle=2, color=RED)
        angle_label_2 = MathTex("2 \\text{ rad}").scale(0.525)
        angle_label_2.next_to(inner_arc_2, UP, buff=0.1)

        self.play(
            Transform(arc, arc_2),
            Transform(arc_label, arc_label_2),
            Transform(inner_arc, inner_arc_2),
            Transform(angle_label, angle_label_2),
            Rotate(radius_line_2, angle=1, about_point=ORIGIN),
            run_time=1.5,
        )
        self.wait(2)

        # Przejście 2 rad -> pi rad
        arc_pi = Arc(radius=circle_radius, start_angle=0, angle=PI, color=RED)
        arc_label_pi = MathTex(r"\text{arc}\\= \pi r").scale(0.525)
        arc_label_pi.next_to(arc_pi, RIGHT, buff=0.1)
        arc_label_pi.shift(0.7 * UP + 0.3 * LEFT)

        inner_arc_pi = Arc(radius=inner_arc_radius, start_angle=0, angle=PI, color=RED)
        angle_label_pi = MathTex("\\pi \\text{ rad}").scale(0.525)
        angle_label_pi.next_to(inner_arc_pi, UP, buff=0.1)

        self.play(
            Transform(arc, arc_pi),
            Transform(arc_label, arc_label_pi),
            Transform(inner_arc, inner_arc_pi),
            Transform(angle_label, angle_label_pi),
            Rotate(radius_line_2, angle=(PI - 2), about_point=ORIGIN),
            run_time=1.5,
        )
        self.wait(3)


if __name__ == "__main__":
    # Uruchamiamy z parametrami -r 540,960 (lub bez -r, bo mamy je w kodzie).
    os.system(
        "manim -p -ql radian_expl_shorts.py RadianInterpretationShorts -r 540,960"
    )
