from manim import *

import numpy as np


# "The minimum of a function lies where its derivative is zero" - a school
# level reminder shown under the energy formulas of EnergyMinimumSceneVoiced,
# before dPi/dQ = 0 appears there. Everything is drawn inside a band of the
# 1920x1080 frame (px x 160..1760, y 690..1060), which is cropped out with
# ffmpeg and laid over the energy scene in Kdenlive.
#
#   manim -qh --frame_rate 30 derivative_minimum.py DerivativeMinimum
#   ffmpeg -i DerivativeMinimum.mp4 -vf crop=1600:370:160:690 ...

# Moments of recording 8 (s, uncut recording); the scene starts at T0.
T0 = 42.4
CUES = {
    "axes": 42.5,        # "szukamy minimum energii"
    "dot": 56.3,         # "jak się szuka minimum"
    "sweep": 56.8,
    "back": 61.7,        # "Minimum funkcji znajdujemy tam,"
    "zero": 65.6,        # "... pochodna jest równa 0"
    "pi_u": 88.0,        # "energia nie zależy już od nieznanej funkcji,"
    "pi_q": 93.8,        # "tylko od skończonej liczby przemieszczeń w węzłach"
    "out": 97.0,         # dPi/dQ = 0 is written in the energy scene at 97.8
}
END = 97.8


def g(q):
    return 0.45 * (q - 0.4) ** 2 + 0.3


def dg(q):
    return 0.9 * (q - 0.4)


class DerivativeMinimum(Scene):
    def cue(self, name):
        dt = CUES[name] - T0 - self.renderer.time
        if dt > 1e-3:
            self.wait(dt)
        elif dt < -0.05:
            print(f"cue {name} late by {-dt:.2f} s")

    def construct(self):
        axes = Axes(x_range=[-2.2, 2.6, 1], y_range=[0, 3.2, 1], x_length=4.4, y_length=2.2,
                    tips=False, axis_config={"include_ticks": False, "stroke_width": 2})
        axes.move_to([-3.5, -2.65, 0])
        x_lbl = MathTex("Q", font_size=30).next_to(axes.x_axis, RIGHT, buff=0.12)
        y_lbl = MathTex(r"\Pi(Q)", font_size=30).next_to(axes.y_axis.get_top(), LEFT, buff=0.15)
        curve = axes.plot(g, x_range=[-2.1, 2.5, 0.01], color=YELLOW)

        self.cue("axes")
        self.play(Create(axes), FadeIn(x_lbl), FadeIn(y_lbl), run_time=0.8)
        self.play(Create(curve), run_time=1.2)

        # point on the curve with its tangent and the live slope
        q = ValueTracker(-1.6)
        dot = always_redraw(lambda: Dot(axes.c2p(q.get_value(), g(q.get_value())),
                                        radius=0.07, color=WHITE))

        def tangent():
            x = q.get_value()
            p = np.array(axes.c2p(x, g(x)))
            d = np.array(axes.c2p(x + 1, g(x) + dg(x))) - np.array(axes.c2p(x, g(x)))
            d = d / np.linalg.norm(d)
            return Line(p - 0.75 * d, p + 0.75 * d, color=TEAL_A, stroke_width=4)

        tan = always_redraw(tangent)
        lhs = MathTex(r"\frac{d\Pi}{dQ}", "=", font_size=38).move_to([0.3, -2.0, 0])
        val = always_redraw(lambda: DecimalNumber(dg(q.get_value()), num_decimal_places=2,
                                                  include_sign=True, font_size=38, color=TEAL_A)
                            .next_to(lhs, RIGHT, buff=0.18))

        self.cue("dot")
        self.play(FadeIn(dot), Create(tan), FadeIn(lhs), FadeIn(val), run_time=0.5)
        self.cue("sweep")
        self.play(q.animate.set_value(2.2), run_time=3.6, rate_func=smooth)
        self.cue("back")
        self.play(q.animate.set_value(0.4), run_time=2.6, rate_func=smooth)

        self.cue("zero")
        tan.clear_updaters()
        dot.clear_updaters()
        val.clear_updaters()
        zero = MathTex("0", font_size=38, color=YELLOW).next_to(lhs, RIGHT, buff=0.18)
        box = SurroundingRectangle(VGroup(lhs, zero), color=YELLOW, buff=0.12)
        drop = DashedLine(axes.c2p(0.4, g(0.4)), axes.c2p(0.4, 0), color=GREY_B, stroke_width=2)
        self.play(tan.animate.set_color(YELLOW), FadeOut(val), FadeIn(zero),
                  Create(drop), Create(box), run_time=0.8)

        # energy of a function -> energy of n numbers
        pi_u = MathTex(r"\Pi(\mathbf{u})", font_size=38)
        u_note = Text("unknown function", font_size=20, color=GREY_B).next_to(pi_u, DOWN, buff=0.12)
        arrow = MathTex(r"\longrightarrow", font_size=38).next_to(pi_u, RIGHT, buff=0.3)
        pi_q = MathTex(r"\Pi(Q_1,\, Q_2,\, \dots,\, Q_n)", font_size=38)
        pi_q.next_to(arrow, RIGHT, buff=0.3)
        q_note = Text("n nodal displacements", font_size=20, color=GREY_B).next_to(pi_q, DOWN, buff=0.12)
        right = VGroup(pi_u, u_note, arrow, pi_q, q_note)
        right.shift([2.3 - right.get_center()[0], -3.05 - pi_u.get_center()[1], 0])

        self.cue("pi_u")
        self.play(FadeIn(pi_u), FadeIn(u_note), run_time=0.8)
        self.cue("pi_q")
        self.play(FadeIn(arrow, shift=RIGHT * 0.2), FadeIn(pi_q), FadeIn(q_note), run_time=0.9)

        self.cue("out")
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        rest = END - T0 - self.renderer.time
        if rest > 1e-3:
            self.wait(rest)
