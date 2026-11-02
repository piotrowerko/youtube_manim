from manim import *


# K2 of element II, which the main scene skips: the integrand B^T D B h is
# constant for the triangle, so the double integral is that constant times the
# area. Drawn inside a band of the 1920x1080 frame (px x 540..1440, y 220..760),
# the empty middle of the frame between the product B^T D B h and T2; cropped
# with ffmpeg and laid over the freeze frame of the main scene.
#
#   manim -qh --frame_rate 30 k2_overlay.py K2Overlay
#   ffmpeg -i K2Overlay.mp4 -vf crop=900:540:540:220 ...

# Recording 16 ("el 2"), uncut times in seconds; the clip starts at T0.
T0 = 196.7
CUES = {k: v - T0 for k, v in {
    "area": 197.0,    # "Całka ze stałej to po prostu ta stała razy pole obszaru"
    "k2": 205.4,      # "I tak dostaniemy macierz sztywności K2"
    "out": 212.3,     # before "No i teraz znowu zobaczymy ... macierz topologii"
}.items()}
END = 212.9 - T0

K2 = [
    ["2.09", "0", "0", "-2.09", "-2.09", "2.09"],
    ["0", "6.41", "-2.24", "0", "2.24", "-6.41"],
    ["0", "-2.24", "6.41", "0", "-6.41", "2.24"],
    ["-2.09", "0", "0", "2.09", "2.09", "-2.09"],
    ["-2.09", "2.24", "-6.41", "2.09", "8.50", "-4.33"],
    ["2.09", "-6.41", "2.24", "-2.09", "-4.33", "8.50"],
]


def px(x, y):
    """Pixel position of the 1920x1080 frame -> scene coordinates."""
    return np.array([(x - 960) / 1920 * config.frame_width, (540 - y) / 1080 * config.frame_height, 0])


class K2Overlay(Scene):
    def cue(self, name):
        dt = CUES[name] - self.renderer.time
        if dt > 1e-3:
            self.wait(dt)
        elif dt < -0.05:
            print(f"cue {name} late by {-dt:.2f} s")

    def construct(self):
        area = MathTex(
            r"\mathbf{K}_2", r"=", r"\big(\mathbf{B}^{T}\mathbf{D}\,\mathbf{B}\,h\big)", r"\cdot", r"A",
            r",\qquad A = \tfrac{1}{2}\cdot 2\cdot 2 = 2\ \text{m}^2",
            font_size=30,
        )
        area[2].set_color(TEAL_A)
        area.move_to(px(990, 285))

        mat = Matrix(
            K2,
            element_to_mobject=lambda s: MathTex(s, font_size=24),
            h_buff=0.78, v_buff=0.40,
            bracket_h_buff=0.12,
        )
        lhs = MathTex(r"\mathbf{K}_2 = 10^{6}\cdot", font_size=30)
        k2 = VGroup(lhs, mat).arrange(RIGHT, buff=0.18)
        k2.scale_to_fit_width(5.9)          # box included, it stays inside the band
        k2.move_to(px(990, 535))
        box = SurroundingRectangle(k2, color=TEAL_A, buff=0.14, stroke_width=2.5, corner_radius=0.08)

        self.cue("area")
        self.play(Write(area), run_time=1.2)
        self.cue("k2")
        self.play(FadeIn(lhs), FadeIn(mat), run_time=0.9)
        self.play(Create(box), run_time=0.5)
        self.cue("out")
        self.play(FadeOut(VGroup(area, k2, box)), run_time=0.5)
        self.wait(max(0.0, END - self.renderer.time))
