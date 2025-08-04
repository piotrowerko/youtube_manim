import os
from manim import *
import matplotlib.pyplot as plt  # do zapisu klatek

class NumericalIntegralShorts(Scene):
    def __init__(self, **kwargs):
        # Konfigurowanie pionowych wymiarów (9:16)
        config.pixel_width = 540
        config.pixel_height = 960
        config.frame_width = 5.4
        config.frame_height = 9.6
        super().__init__(**kwargs)

    def construct(self):
        # Tytuł
        title = Text("Całka oznaczona\njako granica sumy pól", font_size=32, line_spacing=0.8)
        title.to_edge(UP)
        self.play(FadeIn(title))

        # Tworzenie osi
        axes = Axes(
            x_range=[0, 2, 0.5],
            y_range=[0, 4, 1],
            x_length=4,
            y_length=4,
            axis_config={"include_numbers": True},
        )
        axes.to_edge(DOWN, buff=0.5)

        # Etykiety osi
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label))

        # Wykres funkcji y = x^2
        parabola = axes.plot(lambda x: x**2, x_range=[0,2], color=YELLOW)
        func_label = MathTex("y = x^2").next_to(parabola, UR, buff=0.2).scale(0.7)
        self.play(Create(parabola), FadeIn(func_label))

        # Tekst do wyświetlania przybliżenia pola
        sum_text = MathTex("S \\approx ?").scale(0.8)
        sum_text.to_corner(UR)
        self.play(FadeIn(sum_text))

        # Funkcja do obliczania przybliżenia pola (suma Riemanna) i aktualizacji tekstu
        def update_sum_text(n):
            dx = 2 / n
            total_area = 0
            for k in range(n):
                x_left = k * dx
                x_mid = x_left + dx/2
                height = x_mid**2
                total_area += height * dx
            sum_text.become(MathTex(f"S \\approx {total_area:.3f}").scale(0.8).to_corner(UR))

        # Funkcja tworząca prostokąty Riemanna
        def get_riemann_rectangles(n):
            return axes.get_riemann_rectangles(
                graph=parabola,
                x_range=[0, 2],
                dx=2/n,
                stroke_width=0.5,
                stroke_color=WHITE,
                fill_opacity=0.5,
                input_sample_type="center",  # midpoint
            )

        # Początkowe n=2
        n_current = 2
        rects_2 = get_riemann_rectangles(n_current)
        update_sum_text(n_current)
        self.play(Create(rects_2))
        self.wait(1)

        # KLATKA 1
        frame_image = self.camera.get_image()
        plt.imsave("numerical_integral_keyframe_1.png", frame_image)

        # Przejście 2 -> 4
        n_next = 4
        rects_4 = get_riemann_rectangles(n_next)
        update_sum_text(n_next)
        self.play(Transform(rects_2, rects_4), run_time=2)
        self.wait(1)

        # KLATKA 2
        frame_image = self.camera.get_image()
        plt.imsave("numerical_integral_keyframe_2.png", frame_image)

        # Przejście 4 -> 8
        n_next = 8
        rects_8 = get_riemann_rectangles(n_next)
        update_sum_text(n_next)
        self.play(Transform(rects_2, rects_8), run_time=2)
        self.wait(1)

        # KLATKA 3
        frame_image = self.camera.get_image()
        plt.imsave("numerical_integral_keyframe_3.png", frame_image)

        # Przejście 8 -> 16
        n_next = 16
        rects_16 = get_riemann_rectangles(n_next)
        update_sum_text(n_next)
        self.play(Transform(rects_2, rects_16), run_time=2)
        self.wait(1)

        # KLATKA 4
        frame_image = self.camera.get_image()
        plt.imsave("numerical_integral_keyframe_4.png", frame_image)

        # Chwila pauzy, aby zakończyć animację
        self.wait(2)


if __name__ == "__main__":
    # Uruchamianie z -r 540,960 w pliku .py
    os.system(
        "manim -p -ql numerical_integral_shorts.py NumericalIntegralShorts -r 540,960"
    )
