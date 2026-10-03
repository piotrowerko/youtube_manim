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

    # Timing hooks. The base scene keeps its original pacing; a subclass can
    # pin steps to moments of a voice-over (seconds from the start) via CUES
    # and override run times via RT - see EnergyMinimumSceneVoiced.
    CUES = {}
    RT = {}
    # Name the K_glob / P brackets after the main equation instead of before.
    BRACES_LAST = False

    def cue(self, name):
        """Wait until the voice-over reaches the moment assigned to this step."""
        if name in self.CUES:
            dt = self.CUES[name] - self.renderer.time
            if dt > 1e-3:
                self.wait(dt)
            elif dt < -0.05:
                print(f"cue {name} late by {-dt:.2f} s")

    def rt(self, name, default):
        return self.RT.get(name, default)

    def pause(self, duration):
        """Fixed pause of the base pacing - with cues, timing comes from them."""
        if not self.CUES:
            self.wait(duration)

    def construct(self):
        # =====================================================================
        # ACT 1 - fast recap of the integral analogy (~4 s)
        # =====================================================================
        title = Text("From a hard problem to a simple one", font_size=40)
        title.to_edge(UP, buff=0.35)
        self.cue("title")
        self.play(FadeIn(title, shift=DOWN * 0.3), run_time=self.rt("title", 0.45))

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

        self.play(Create(axes), run_time=self.rt("axes", 0.35))
        self.play(Create(graph), FadeIn(curve_lbl), run_time=self.rt("graph", 0.55))

        rects = axes.get_riemann_rectangles(
            graph=graph,
            x_range=[0, 2],
            dx=2.0 / 16,
            stroke_width=0.6,
            stroke_color=WHITE,
            fill_opacity=0.55,
            input_sample_type="center",
        )
        self.cue("rects")
        self.play(Create(rects), run_time=self.rt("rects", 0.60))

        moral = VGroup(
            Text("one unknown function", font_size=30, color=YELLOW),
            MathTex(r"\longrightarrow", font_size=40),
            Text("many simple, known ones", font_size=30, color=C_N),
        ).arrange(RIGHT, buff=0.35)
        moral.next_to(axes, DOWN, buff=0.35)
        self.cue("moral")
        self.play(FadeIn(moral, shift=UP * 0.2), run_time=0.45)
        self.pause(0.70)

        # ---- park the analogy in the top-left corner ----
        analogy = VGroup(axes, graph, rects, curve_lbl, moral)
        self.cue("park")
        self.play(
            analogy.animate.scale(0.36).to_corner(UL, buff=0.40).shift(DOWN * 0.50),
            FadeOut(title),
            run_time=self.rt("park", 0.80),
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
        self.cue("head")
        self.play(Write(head), run_time=self.rt("head", 0.6))

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

        self.cue("pi_u")
        self.play(Write(pi_u), run_time=self.rt("pi_u", 1.6))
        self.cue("delta")
        self.play(FadeIn(delta_pi, shift=UP * 0.2), run_time=0.5)
        # Voice-over only: point at the two parts of the formula in turn.
        if "hl_K" in self.CUES:
            self.cue("hl_K")
            self.play(Circumscribe(pi_u[1], color=C_K, buff=0.08), run_time=1.5)
            self.cue("hl_P")
            self.play(Circumscribe(VGroup(pi_u[2], pi_u[3]), color=C_P, buff=0.08),
                      run_time=1.5)
        self.cue("warn")
        self.play(FadeIn(warn), run_time=0.5)
        self.pause(1.6)

        # =====================================================================
        # ACT 3 - the substitution: this is where N enters
        # =====================================================================
        head2 = Text("Substitute the known shape functions", font_size=32)
        head2.to_edge(UP, buff=0.30)
        self.cue("head2")
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

        if "sub_u" in self.CUES:
            # Voice-over: displacements (right) first, strains (left) later.
            self.cue("sub_u")
            self.play(Write(sub_u), run_time=1.0)
            self.cue("sub_e")
            self.play(Write(sub_e), run_time=1.2)
        else:
            self.play(Write(sub_row), run_time=1.3)
        self.pause(1.3)

        # =====================================================================
        # ACT 4 - both forms one above the other, term by term
        # =====================================================================
        head3 = Text("The same functional, before and after", font_size=32)
        head3.to_edge(UP, buff=0.30)

        # The analogy panel steps aside - the comparison needs the full width.
        self.cue("act4")
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

        self.cue("pi_q")
        self.play(Write(pi_q), run_time=self.rt("pi_q", 2.2))
        self.pause(0.7)

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

        self.cue("box_B")
        self.play(Create(hi_B), GrowArrow(arr_B), run_time=0.7)
        self.cue("box_N")
        self.play(Create(hi_N1), Create(hi_N2),
                  GrowArrow(arr_N1), GrowArrow(arr_N2), run_time=0.8)
        self.pause(2.2)

        # =====================================================================
        # ACT 5 - name the brackets, then minimise
        # =====================================================================
        self.cue("unbox")
        self.play(FadeOut(VGroup(hi_B, hi_N1, hi_N2, arr_B, arr_N1, arr_N2)),
                  run_time=0.5)

        br_K = Brace(VGroup(*pi_q[2:5]), DOWN, buff=0.10, color=C_K)
        lbl_K = br_K.get_tex(r"\mathbf{K}_{glob}").set_color(C_K).scale(0.85)
        br_P = Brace(VGroup(*pi_q[7:13]), DOWN, buff=0.10, color=C_P)
        lbl_P = br_P.get_tex(r"\mathbf{P}").set_color(C_P).scale(0.85)

        def name_brackets():
            self.cue("braces")
            self.play(GrowFromCenter(br_K), FadeIn(lbl_K),
                      GrowFromCenter(br_P), FadeIn(lbl_P), run_time=0.9)

        if not self.BRACES_LAST:
            name_brackets()
            self.pause(1.5)

        head4 = Text("Minimum → the main FEM equation", font_size=32)
        head4.to_edge(UP, buff=0.30)
        self.cue("head4")
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

        self.cue("deriv")
        self.play(Write(deriv), run_time=0.8)
        self.cue("main_eq")
        self.play(FadeIn(arrow), run_time=0.3)
        self.play(Write(main_eq), run_time=1.0)
        self.cue("eq_box")
        self.play(Create(eq_box), run_time=0.6)
        if self.BRACES_LAST:
            name_brackets()
        self.pause(3.0)
        self.ending()

    def ending(self):
        """Hold until the end of the voice-over - nothing in the base scene."""


# Voice-over recordings 4-8 play back to back under the scene. For every
# recording: the kept pieces (first, last source frame of the 30 fps project),
# as cut on track A2, so the scene ends exactly with recording 8.
REC_KEPT = {4: [(0, 3484)], 5: [(0, 2898)],
            6: [(0, 2593), (2692, 2831)],
            7: [(86, 981), (1039, 1435), (1478, 3794)],
            8: [(1272, 5872)]}


def rec_len(n):
    return sum(b - a + 1 for a, b in REC_KEPT[n])


def rec_start(n):
    """Start of recording n in seconds from the start of the scene."""
    return sum(rec_len(k) for k in REC_KEPT if k < n) / 30


def at(n, t):
    """Moment t (s, of the uncut recording n) in scene time; a moment that
    was cut out snaps to the start of the next kept piece."""
    f, acc = t * 30, 0
    for a, b in REC_KEPT[n]:
        if f < a:
            break
        if f <= b + 1:
            return rec_start(n) + (acc + f - a) / 30
        acc += b - a + 1
    return rec_start(n) + acc / 30


class EnergyMinimumSceneVoiced(EnergyMinimumScene):
    """The same scene paced to the voice-over recordings 4-8.

    Every step starts at the word it belongs to (whisper word timestamps);
    between them the screen simply holds.
    """

    TOTAL = sum(rec_len(n) for n in REC_KEPT) / 30
    BRACES_LAST = True

    CUES = {
        "title": at(4, 0.5),      # "Podobnie jak w przykladzie z calka"
        "moral": at(4, 4.1),      # "upraszczamy pewien aparat matematyczny"
        "park": at(4, 10.8),      # "Mianowicie dotyczy on ..."
        "head": at(4, 13.4),      # "zasady minimum calkowitej energii"
        "pi_u": at(4, 24.0),      # "I wzor ten opisuje energie"
        "delta": at(4, 108.0),    # "taki stan jest stanem rownowagi"
        "hl_K": at(5, 5.1),       # "Na turkusowo jest energia"
        "hl_P": at(5, 12.7),      # "Po prawej na zloto jest praca"
        "warn": at(5, 38.6),      # "a ona jest niewiadoma"
        "head2": at(6, 20.9),     # "nieznane funkcje ... zastepujemy"
        "sub_u": at(6, 29.7),     # "nazywaja sie funkcjami ksztaltu"
        "sub_e": at(7, 10.5),     # "i odksztalcenia po lewej"
        "act4": at(7, 58.3),      # "No i teraz wykorzystajmy te zaleznosci"
        "pi_q": at(7, 60.2),      # "do budowy nowego ... wzoru"
        "box_B": at(7, 101.8),    # "Ramki pokazuja"
        "box_N": at(7, 108.8),    # "i w obu czlonach pracy obciazen"
        "unbox": at(8, 0.4),
        "head4": at(8, 42.6),     # "szukamy minimum energii"
        "deriv": at(8, 97.8),     # "Wiec wystarczy zwykla pochodna"
        "main_eq": at(8, 112.4),  # "Otrzymujemy uklad rownan"
        "eq_box": at(8, 115.8),   # "macierzowy uklad rownan"
        "braces": at(8, 117.9),   # "Te wszystkie literki K, Q, P"
    }
    RT = {"axes": 0.6, "graph": 1.0, "rects": 1.0, "park": 1.0, "pi_u": 2.0,
          "pi_q": 3.0}

    def ending(self):
        dt = self.TOTAL - self.renderer.time
        if dt > 0:
            self.wait(dt)


if __name__ == "__main__":
    # Full HD, 60 fps - same as the other clips used in the film.
    os.system("manim -qh energy_minimum.py EnergyMinimumScene")
