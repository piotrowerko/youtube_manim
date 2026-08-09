import os

import numpy as np
from manim import *


# Same function as in NumericalIntegralHD - the analogy has to be visually
# recognisable as "the thing we have just seen". It is shown for the second
# time in the film, so this recap is deliberately fast (~4 s).
def f(x):
    return x**2 + 0.5 * np.sin(6 * x)


# Colour code used throughout:
#   TEAL_A - everything that ends up inside K_glob (same colour as in the film)
#   GOLD   - everything that ends up inside P
#   BLUE_B - the shape functions N and the B matrix built from their derivatives
C_K = TEAL_A
C_P = GOLD
C_N = BLUE_B


class EnergyMinimumScene(Scene):
    """From the integral analogy to the main FEM equation.

    Both forms of the functional stay on screen at the same time, one above the
    other, so the continuous form can be compared term by term with the
    discrete one. Matching terms share a colour, and the three places where the
    shape functions enter are boxed and connected with arrows.

    Symbols follow mes_3_el.py: N, B, D, h, Q, P, R, K_glob (TEAL_A).
    """

    def construct(self):
        # =====================================================================
        # ACT 1 - fast recap of the integral analogy (~4 s)
        # =====================================================================
        title = Text("From a hard problem to a simple one", font_size=40)
        title.to_edge(UP, buff=0.35)
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=0.45)

        axes = Axes(
            x_range=[0, 2, 0.5],
            y_range=[0, 5, 1],
            x_length=7.0,
            y_length=4.4,
            axis_config={"include_numbers": True, "font_size": 22},
            tips=False,
        )
        axes.move_to(DOWN * 0.5)
        graph = axes.plot(f, x_range=[0, 2, 0.005], color=YELLOW)
        curve_lbl = MathTex(r"f(x) = x^2 + \tfrac{1}{2}\sin(6x)", font_size=36)
        curve_lbl.next_to(axes, UP, buff=0.25)

        self.play(Create(axes), run_time=0.35)
        self.play(Create(graph), FadeIn(curve_lbl), run_time=0.55)

        rects = axes.get_riemann_rectangles(
            graph=graph,
            x_range=[0, 2],
            dx=2.0 / 16,
            stroke_width=0.6,
            stroke_color=WHITE,
            fill_opacity=0.55,
            input_sample_type="center",
        )
        self.play(Create(rects), run_time=0.60)

        moral = VGroup(
            Text("one unknown function", font_size=30, color=YELLOW),
            MathTex(r"\longrightarrow", font_size=40),
            Text("many simple, known ones", font_size=30, color=C_N),
        ).arrange(RIGHT, buff=0.35)
        moral.next_to(axes, DOWN, buff=0.35)
        self.play(FadeIn(moral, shift=UP * 0.2), run_time=0.45)
        self.wait(0.70)

        # ---- park the analogy in the top-left corner ----
        analogy = VGroup(axes, graph, rects, curve_lbl, moral)
        self.play(
            analogy.animate.scale(0.36).to_corner(UL, buff=0.40).shift(DOWN * 0.50),
            FadeOut(title),
            run_time=0.80,
        )
        frame_box = SurroundingRectangle(
            analogy, color=GREY_B, stroke_width=1.6, buff=0.20, corner_radius=0.08
        )
        analogy_tag = Text("the same idea", font_size=20, color=GREY_B)
        analogy_tag.next_to(frame_box, DOWN, buff=0.12)
        panel = VGroup(frame_box, analogy_tag, analogy)
        self.play(Create(frame_box), FadeIn(analogy_tag), run_time=0.35)

        # =====================================================================
        # ACT 2 - the continuous form, three terms, colour coded
        # =====================================================================
        head = Text("Principle of minimum total potential energy", font_size=32)
        head.to_edge(UP, buff=0.30)
        self.play(Write(head), run_time=0.6)

        pi_u = MathTex(
            r"\Pi(\mathbf{u})\;=\;",                                       # 0
            r"\tfrac{1}{2}\int_{A}\boldsymbol{\varepsilon}^{T}\mathbf{D}"
            r"\,\boldsymbol{\varepsilon}\,h\,dA",                          # 1 -> K
            r"\;-\;\int_{A}\mathbf{u}^{T}\mathbf{q}_{V}\,h\,dA",           # 2 -> P
            r"\;-\;\int_{\Gamma}\mathbf{u}^{T}\mathbf{q}_{S}\,h\,ds",      # 3 -> P
            font_size=30,
        )
        pi_u[1].set_color(C_K)
        pi_u[2].set_color(C_P)
        pi_u[3].set_color(C_P)
        pi_u.move_to([2.2, 1.30, 0])

        delta_pi = MathTex(r"\delta\Pi = 0", font_size=38, color=YELLOW)
        delta_pi.next_to(pi_u, DOWN, buff=0.40)

        warn = Text(
            "u(x, y) is an unknown field  —  infinitely many unknowns",
            font_size=25,
            color=RED,
        )
        warn.next_to(delta_pi, DOWN, buff=0.30)

        self.play(Write(pi_u), run_time=1.6)
        self.play(FadeIn(delta_pi, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(warn), run_time=0.5)
        self.wait(1.6)

        # =====================================================================
        # ACT 3 - the substitution: this is where N enters
        # =====================================================================
        head2 = Text("Substitute the known shape functions", font_size=32)
        head2.to_edge(UP, buff=0.30)
        self.play(FadeOut(head, shift=UP * 0.15),
                  FadeIn(head2, shift=UP * 0.15),
                  FadeOut(warn), FadeOut(delta_pi), run_time=0.6)

        sub_u = MathTex(
            r"\mathbf{u}(x,y) \;=\; \mathbf{N}(x,y)\,\mathbf{Q}", font_size=32
        )
        sub_e = MathTex(
            r"\boldsymbol{\varepsilon} \;=\; \mathbf{B}\,\mathbf{Q},"
            r"\qquad \mathbf{B} \;=\; \Big[\tfrac{\partial\mathbf{N}}{\partial x},"
            r"\;\tfrac{\partial\mathbf{N}}{\partial y}\Big]",
            font_size=32,
        )
        # B on the left, N on the right - matches the order in which they
        # appear in the discrete functional, so the arrows do not cross.
        sub_row = VGroup(sub_e, sub_u).arrange(RIGHT, buff=1.0)
        sub_row.set_color(C_N)
        sub_row.move_to([1.0, 0.35, 0])

        self.play(Write(sub_row), run_time=1.3)
        self.wait(1.3)

        # =====================================================================
        # ACT 4 - both forms one above the other, term by term
        # =====================================================================
        head3 = Text("The same functional, before and after", font_size=32)
        head3.to_edge(UP, buff=0.30)

        # The analogy panel steps aside - the comparison needs the full width.
        self.play(
            FadeOut(panel, shift=LEFT * 0.6),
            FadeOut(head2, shift=UP * 0.15),
            FadeIn(head3, shift=UP * 0.15),
            pi_u.animate.move_to([0.0, 2.35, 0]),
            sub_row.animate.move_to([0.0, 1.05, 0]),
            run_time=0.9,
        )

        pi_q = MathTex(
            r"\Pi(\mathbf{Q})\;=\;",                       # 0
            r"\tfrac{1}{2}\,\mathbf{Q}^{T}",               # 1
            r"\Big(\int_{A}",                              # 2  K
            r"\mathbf{B}^{T}\mathbf{D}\,\mathbf{B}",       # 3  <- built from N
            r"\,h\,dA\Big)",                               # 4  K
            r"\mathbf{Q}",                                 # 5
            r"\;-\;\mathbf{Q}^{T}",                        # 6
            r"\Big(\int_{A}",                              # 7  P
            r"\mathbf{N}^{T}",                             # 8  <- N itself
            r"\mathbf{q}_{V}\,h\,dA",                      # 9  P
            r"\;+\;\int_{\Gamma}",                         # 10 P
            r"\mathbf{N}^{T}",                             # 11 <- N itself
            r"\mathbf{q}_{S}\,h\,ds\Big)",                 # 12 P
            font_size=28,
        )
        for i in (2, 4):
            pi_q[i].set_color(C_K)
        for i in (7, 9, 10, 12):
            pi_q[i].set_color(C_P)
        pi_q.move_to([0.0, -0.60, 0])

        self.play(Write(pi_q), run_time=2.2)
        self.wait(0.7)

        # ---- box the three places where the shape functions enter ----
        hi_B = SurroundingRectangle(pi_q[3], color=C_N, buff=0.07, stroke_width=2.2)
        hi_N1 = SurroundingRectangle(pi_q[8], color=C_N, buff=0.07, stroke_width=2.2)
        hi_N2 = SurroundingRectangle(pi_q[11], color=C_N, buff=0.07, stroke_width=2.2)

        def link(src, dst):
            return Arrow(
                src.get_bottom() + DOWN * 0.05, dst.get_top(),
                buff=0.08, color=C_N, stroke_width=3,
                max_tip_length_to_length_ratio=0.13,
            )

        arr_B = link(sub_e, hi_B)
        arr_N1 = link(sub_u, hi_N1)
        arr_N2 = link(sub_u, hi_N2)

        self.play(Create(hi_B), GrowArrow(arr_B), run_time=0.7)
        self.play(Create(hi_N1), Create(hi_N2),
                  GrowArrow(arr_N1), GrowArrow(arr_N2), run_time=0.8)
        self.wait(2.2)

        # =====================================================================
        # ACT 5 - name the brackets, then minimise
        # =====================================================================
        self.play(FadeOut(VGroup(hi_B, hi_N1, hi_N2, arr_B, arr_N1, arr_N2)),
                  run_time=0.5)

        br_K = Brace(VGroup(*pi_q[2:5]), DOWN, buff=0.10, color=C_K)
        lbl_K = br_K.get_tex(r"\mathbf{K}_{glob}").set_color(C_K).scale(0.85)
        br_P = Brace(VGroup(*pi_q[7:13]), DOWN, buff=0.10, color=C_P)
        lbl_P = br_P.get_tex(r"\mathbf{P}").set_color(C_P).scale(0.85)

        self.play(GrowFromCenter(br_K), FadeIn(lbl_K),
                  GrowFromCenter(br_P), FadeIn(lbl_P), run_time=0.9)
        self.wait(1.5)

        head4 = Text("Minimum → the main FEM equation", font_size=32)
        head4.to_edge(UP, buff=0.30)
        self.play(FadeOut(head3, shift=UP * 0.15),
                  FadeIn(head4, shift=UP * 0.15), run_time=0.6)

        deriv = MathTex(
            r"\frac{\partial \Pi}{\partial \mathbf{Q}} = \mathbf{0}",
            font_size=36, color=YELLOW,
        )
        deriv.move_to([-4.3, -2.70, 0])

        main_eq = MathTex(
            r"\mathbf{K}_{glob}", r"\cdot", r"\mathbf{Q}",
            r"=", r"\mathbf{P}", r"+", r"\mathbf{R}",
            font_size=50,
        )
        main_eq[0].set_color(C_K)
        main_eq.move_to([1.1, -2.70, 0])
        eq_box = SurroundingRectangle(
            main_eq, color=C_K, stroke_width=2.5, buff=0.26, corner_radius=0.10
        )
        arrow = MathTex(r"\Longrightarrow", font_size=44)
        arrow.move_to([-2.25, -2.70, 0])

        self.play(Write(deriv), run_time=0.8)
        self.play(FadeIn(arrow), run_time=0.3)
        self.play(Write(main_eq), run_time=1.0)
        self.play(Create(eq_box), run_time=0.6)
        self.wait(3.0)


if __name__ == "__main__":
    # Full HD, 60 fps - same as the other clips used in the film.
    os.system("manim -qh energy_minimum.py EnergyMinimumScene")
