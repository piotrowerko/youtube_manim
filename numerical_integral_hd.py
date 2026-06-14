import os
import numpy as np
from manim import *


# Function: parabola with a "wavelet" (sinusoidal oscillation) on top.
# f(x) = x^2 + 0.5 * sin(6x)
def f(x):
    return x**2 + 0.5 * np.sin(6 * x)


class NumericalIntegralHD(MovingCameraScene):
    """Definite integral as the limit of a sum of areas (Riemann) in Full HD 16:9.

    At the end the camera zooms into a single sample rectangle to show that
    locally the function is approximated by a horizontal (constant) sample.
    """

    def __init__(self, **kwargs):
        # Standard Full HD format (16:9)
        config.pixel_width = 1920
        config.pixel_height = 1080
        config.frame_width = 14.222222
        config.frame_height = 8.0
        super().__init__(**kwargs)

    def construct(self):
        # Save the camera state so we can zoom in and restore it later.
        self.camera.frame.save_state()

        x_min, x_max = 0.0, 2.0

        # --- Title ---
        title = Text(
            "Definite integral as the limit of a sum of areas",
            font_size=40,
        )
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.3))

        # --- Axes (on the right side of the screen) ---
        axes = Axes(
            x_range=[0, 2, 0.5],
            y_range=[0, 5, 1],
            x_length=7.5,
            y_length=5.2,
            axis_config={"include_numbers": True, "font_size": 24},
            tips=False,
        )
        axes.to_edge(RIGHT, buff=0.8).shift(DOWN * 0.4)

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label))

        # --- Graph of f(x) = x^2 + 0.5 sin(6x) ---
        graph = axes.plot(f, x_range=[x_min, x_max, 0.005], color=YELLOW)
        self.play(Create(graph), run_time=2)

        # --- Formulas (on the left side of the screen) ---
        func_formula = MathTex(
            r"f(x) = x^2 + \tfrac{1}{2}\sin(6x)",
            font_size=42,
        )
        integral_formula = MathTex(
            r"S = \int_{0}^{2} f(x)\,dx",
            font_size=42,
        )
        riemann_formula = MathTex(
            r"S \approx \sum_{k=1}^{n} f(x_k^{*})\,\Delta x",
            font_size=42,
        )

        formulas = VGroup(func_formula, integral_formula, riemann_formula)
        formulas.arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        formulas.to_edge(LEFT, buff=0.7).shift(UP * 0.3)

        self.play(Write(func_formula))
        self.play(Write(integral_formula))
        self.play(Write(riemann_formula))

        # --- Area approximation counter ---
        n_label = MathTex(r"n = 2", font_size=40)
        sum_label = MathTex(r"S \approx ?", font_size=40)
        info = VGroup(n_label, sum_label).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        info.next_to(formulas, DOWN, buff=0.8, aligned_edge=LEFT)
        self.play(FadeIn(info))

        def midpoint_sum(n):
            dx = (x_max - x_min) / n
            total = 0.0
            for k in range(n):
                x_mid = x_min + (k + 0.5) * dx
                total += f(x_mid) * dx
            return total

        def update_info(n):
            new_n = MathTex(rf"n = {n}", font_size=40)
            new_s = MathTex(rf"S \approx {midpoint_sum(n):.4f}", font_size=40)
            new_info = VGroup(new_n, new_s).arrange(
                DOWN, aligned_edge=LEFT, buff=0.35
            )
            new_info.next_to(formulas, DOWN, buff=0.8, aligned_edge=LEFT)
            return new_info

        def get_rects(n):
            return axes.get_riemann_rectangles(
                graph=graph,
                x_range=[x_min, x_max],
                dx=(x_max - x_min) / n,
                stroke_width=0.6,
                stroke_color=WHITE,
                fill_opacity=0.55,
                input_sample_type="center",
            )

        # --- Initial n = 2 ---
        n_current = 2
        rects = get_rects(n_current)
        self.play(
            Create(rects),
            Transform(info, update_info(n_current)),
        )
        self.wait(1)

        # --- Refining the partition ---
        for n_next in [4, 8, 16, 32, 64]:
            new_rects = get_rects(n_next)
            self.play(
                Transform(rects, new_rects),
                Transform(info, update_info(n_next)),
                run_time=1.8,
            )
            self.wait(0.6)

        self.wait(1)

        # --- ZOOM: single (horizontal) sample function ---
        # Pick one rectangle from the n = 64 partition and zoom into it to show
        # that locally the function is approximated by a constant (horizontal)
        # sample value f(x_k^*).
        n_zoom = 64
        dx = (x_max - x_min) / n_zoom
        # Pick a rectangle in a near-flat region of the curve (a local maximum
        # of the wavelet) so the horizontal sample function lines up perfectly
        # with the curve - the constant approximation is clearest there.
        k_sel = 9
        x_left = x_min + k_sel * dx
        x_mid = x_left + dx / 2
        x_right = x_left + dx
        sample_height = f(x_mid)

        # Point the camera focuses on: the top edge of the rectangle.
        zoom_point = axes.c2p(x_mid, sample_height)

        # Camera frame width ~ 5 rectangle widths (a single sample plus a bit
        # of context). Scene/x-unit scale = x_length / span.
        units_per_x = axes.x_length / (x_max - x_min)
        frame_w = units_per_x * (5 * dx)
        # Scale matched to the target (zoomed-in) camera frame. When the camera
        # zooms in, stroke widths scale together with the scene, so we multiply
        # widths by this value to keep their apparent size.
        zoom_scale = frame_w / config.frame_width

        # Highlighted single sample rectangle.
        highlight_rect = Polygon(
            axes.c2p(x_left, 0),
            axes.c2p(x_left, sample_height),
            axes.c2p(x_right, sample_height),
            axes.c2p(x_right, 0),
            stroke_color=RED,
            stroke_width=6 * zoom_scale,
            fill_color=RED,
            fill_opacity=0.4,
        )
        self.play(FadeIn(highlight_rect))

        # Zoom the camera onto the top of the single sample rectangle.
        self.play(
            self.camera.frame.animate.set(width=frame_w).move_to(zoom_point),
            run_time=3,
        )
        self.wait(0.5)

        # Horizontal sample line at height f(x_k^*) - extended beyond the
        # rectangle to emphasize that it is a constant (horizontal) function.
        # The width is multiplied by zoom_scale because line widths scale
        # together with the scene when the camera zooms in.
        sample_line = Line(
            axes.c2p(x_mid - 2 * dx, sample_height),
            axes.c2p(x_mid + 2 * dx, sample_height),
            color=RED,
            stroke_width=6 * zoom_scale,
        )
        self.play(Create(sample_line))

        # Label: horizontal (constant) sample function.
        sample_label = MathTex(
            r"f(x_k^{*}) = \text{const}", font_size=42, color=RED
        )
        sample_label.scale(zoom_scale)
        sample_label.move_to(zoom_point + UP * 0.075)

        horiz_note = Text(
            "sample function (horizontal)",
            font_size=30,
            color=WHITE,
        )
        horiz_note.scale(zoom_scale)
        horiz_note.next_to(sample_label, UP, buff=0.03)

        self.play(FadeIn(sample_label, shift=UP * 0.02))
        self.play(FadeIn(horiz_note))
        self.wait(2)

        # Return to the full view.
        self.play(Restore(self.camera.frame), run_time=2)
        self.wait(2)


if __name__ == "__main__":
    # Render in Full HD quality (1920x1080, 60 fps).
    os.system(
        "manim -p -qh numerical_integral_hd.py NumericalIntegralHD"
    )
