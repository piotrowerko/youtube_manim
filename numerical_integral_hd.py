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

    # Timing hooks. The base scene keeps its original pacing; a subclass can
    # pin steps to moments of a voice-over (seconds from the start) via CUES
    # and override run times via RT - see NumericalIntegralHDVoiced.
    CUES = {}
    RT = {}

    def cue(self, name):
        """Wait until the voice-over reaches the moment assigned to this step."""
        if name in self.CUES:
            dt = self.CUES[name] - self.renderer.time
            if dt > 1e-3:
                self.wait(dt)

    def rt(self, name, default):
        return self.RT.get(name, default)

    def pause(self, duration):
        """Fixed pause of the base pacing - with cues, timing comes from them."""
        if not self.CUES:
            self.wait(duration)

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
        self.cue("title")
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
        self.cue("axes")
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label),
                  run_time=self.rt("axes", 1))

        # --- Graph of f(x) = x^2 + 0.5 sin(6x) ---
        graph = axes.plot(f, x_range=[x_min, x_max, 0.005], color=YELLOW)
        self.cue("graph")
        self.play(Create(graph), run_time=self.rt("graph", 2))

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

        self.cue("func_formula")
        self.play(Write(func_formula), run_time=self.rt("formula", 1))
        self.cue("integral_formula")
        self.play(Write(integral_formula), run_time=self.rt("formula", 1))
        self.cue("riemann_formula")
        self.play(Write(riemann_formula), run_time=self.rt("formula", 1))

        # --- Area approximation counter ---
        n_label = MathTex(r"n = 2", font_size=40)
        sum_label = MathTex(r"S \approx ?", font_size=40)
        info = VGroup(n_label, sum_label).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        info.next_to(formulas, DOWN, buff=0.8, aligned_edge=LEFT)
        self.cue("info")
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
        self.cue("n2")
        self.play(
            Create(rects),
            Transform(info, update_info(n_current)),
        )
        self.pause(1)

        # --- Refining the partition ---
        for n_next in [4, 8, 16, 32, 64]:
            new_rects = get_rects(n_next)
            self.cue(f"n{n_next}")
            self.play(
                Transform(rects, new_rects),
                Transform(info, update_info(n_next)),
                run_time=self.rt("refine", 1.8),
            )
            self.pause(0.6)

        self.pause(1)

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
        self.cue("highlight")
        self.play(FadeIn(highlight_rect))

        # Zoom the camera onto the top of the single sample rectangle.
        self.cue("zoom")
        self.play(
            self.camera.frame.animate.set(width=frame_w).move_to(zoom_point),
            run_time=self.rt("zoom", 3),
        )
        self.pause(0.5)

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
        self.cue("sample_line")
        self.play(Create(sample_line), run_time=self.rt("sample_line", 1))

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

        self.cue("sample_label")
        self.play(FadeIn(sample_label, shift=UP * 0.02))
        self.cue("horiz_note")
        self.play(FadeIn(horiz_note))
        self.pause(2)

        # Return to the full view.
        self.cue("restore")
        self.play(Restore(self.camera.frame), run_time=self.rt("restore", 2))
        self.pause(2)

        self.ending(rects, info, formulas, get_rects, midpoint_sum)

    def ending(self, rects, info, formulas, get_rects, midpoint_sum):
        """Extra closing steps - none in the base scene."""


class NumericalIntegralHDVoiced(NumericalIntegralHD):
    """The same scene paced to the voice-over "2- analogia calki oznaczonej".

    CUES are word timestamps of the recording (seconds), so every step starts
    when it is spoken about. The total length equals the recording (133.133 s
    = 3994 frames of the 30 fps project). The closing adds a denser partition
    and the exact value, so the screen still follows the last 25 s of speech.
    """

    TOTAL = 3994 / 30

    CUES = {
        "title": 0.3,
        "axes": 9.6,                 # "Wyobrazmy sobie"
        "graph": 10.6,               # "jakas funkcje"
        "func_formula": 12.3,        # "jakims tam sobie wzorze"
        "integral_formula": 19.9,    # "policzyc analitycznie"
        "riemann_formula": 29.3,     # "znalezc to pole za pomoca sumy"
        "info": 32.6,
        "n2": 37.0,                  # "prostokaty"
        "n4": 41.5,                  # "im bardziej intensywnie"
        "n8": 45.0,
        "n16": 48.0,                 # "wieksza liczbe tych prostokatow"
        "n32": 51.0,                 # "coraz to lepsze przyblizenie"
        "n64": 55.2,
        "highlight": 62.4,           # "Jak przyblizymy sobie ekran"
        "zoom": 63.6,
        "sample_line": 77.1,         # "serii bardzo prostych funkcji"
        "sample_label": 80.9,        # "funkcji horyzontalnych"
        "horiz_note": 86.5,          # "funkcjami probnymi"
        "restore": 93.8,             # "bardzo skomplikowany problem"
        "wave": 102.6,               # "bardzo duzo prostych problemow"
        "n128": 114.8,               # "probkowanie ... odpowiednio gesto"
        "exact": 120.1,              # "niezly inzyniersko wynik"
    }
    RT = {"axes": 1.2, "graph": 2.5, "formula": 1.5, "refine": 2.0,
          "zoom": 4.5, "sample_line": 1.2, "restore": 3.0}

    def ending(self, rects, info, formulas, get_rects, midpoint_sum):
        # "zamieniam na bardzo duzo prostych problemow" - a wave over all the
        # rectangles: every one of them is a simple problem.
        self.cue("wave")
        self.play(LaggedStart(*[Indicate(r, color=BLUE_B, scale_factor=1.0)
                                for r in rects], lag_ratio=0.04), run_time=3.5)

        # "odpowiednio gesto" - an even denser partition.
        self.cue("n128")
        new_info = VGroup(
            MathTex(r"n = 128", font_size=40),
            MathTex(rf"S \approx {midpoint_sum(128):.4f}", font_size=40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        new_info.next_to(formulas, DOWN, buff=0.8, aligned_edge=LEFT)
        self.play(Transform(rects, get_rects(128)), Transform(info, new_info),
                  run_time=2.0)

        # "niezly inzyniersko wynik" - compare with the exact value.
        self.cue("exact")
        exact = 8 / 3 + (1 - np.cos(12)) / 12
        # Next to the approximation - below it there is no room left.
        exact_tex = MathTex(rf"S_{{exact}} = {exact:.4f}", font_size=36, color=GREEN)
        exact_tex.next_to(info[1], RIGHT, buff=0.5)
        box = SurroundingRectangle(info[1], color=GREEN, buff=0.12)
        self.play(Write(exact_tex), Create(box), run_time=1.5)

        dt = self.TOTAL - self.renderer.time
        if dt > 0:
            self.wait(dt)


if __name__ == "__main__":
    # Render in Full HD quality (1920x1080, 60 fps).
    os.system(
        "manim -p -qh numerical_integral_hd.py NumericalIntegralHD"
    )
