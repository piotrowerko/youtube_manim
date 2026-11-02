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
        if not self.derivation(pi_u, sub_row, pi_q, arrow, main_eq):
            self.cue("main_eq")
            self.play(FadeIn(arrow), run_time=0.3)
            self.play(Write(main_eq), run_time=1.0)
        self.cue("eq_box")
        self.play(Create(eq_box), run_time=0.6)
        if self.BRACES_LAST:
            name_brackets()
        self.pause(3.0)
        self.ending()

    def derivation(self, pi_u, sub_row, pi_q, arrow, main_eq):
        """Steps between the derivative and the main equation - none in the
        base scene. Returns True when the main equation has been shown."""
        return False

    def ending(self):
        """Hold until the end of the voice-over - nothing in the base scene."""


# Voice-over recordings play back to back under the scene: the kept pieces in
# playback order (recording, first and last source frame of the 30 fps project),
# as cut on track A2. Recording 8A (the derivation from dPi/dQ = 0 to the main
# equation) is inserted into recording 8 after "... upraszcza się jeszcze bardziej".
PIECES = [(4, 0, 3484), (5, 0, 2898),
          (6, 0, 2593), (6, 2692, 2831),
          (7, 86, 981), (7, 1039, 1435), (7, 1478, 3794),
          (8, 1272, 3311), ("8A", 78, 5484), (8, 3312, 5872)]


def at(n, t):
    """Moment t (s, of the uncut recording n) in scene time; a moment that
    was cut out snaps to the start of the next kept piece."""
    f, acc = t * 30, 0
    for r, a, b in PIECES:
        if r == n:
            if f < a:
                return acc / 30
            if f <= b + 1:
                return (acc + f - a) / 30
        acc += b - a + 1
    raise ValueError((n, t))


class EnergyMinimumSceneVoiced(EnergyMinimumScene):
    """The same scene paced to the voice-over recordings 4-8.

    Every step starts at the word it belongs to (whisper word timestamps);
    between them the screen simply holds.
    """

    TOTAL = sum(b - a + 1 for _, a, b in PIECES) / 30
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
    # recording 8A: from dPi/dQ = 0 to the main equation, step by step
    CUES.update({
        "ins": at("8A", 3.0),       # "Po zróżniczkowaniu dostajemy"
        "A": at("8A", 6.0),         # "następujące równanie"
        "A_lhs": at("8A", 8.8),     # "po lewej stronie jest całka po powierzchni"
        "A_B": at("8A", 18.5),      # "czyli macierz B"
        "A_D": at("8A", 23.1),      # "macierzą sprężystości D"
        "A_rhs": at("8A", 30.7),    # "suma całek odpowiadających za obciążenia"
        "A_qv": at("8A", 35.2),     # "Pierwsza to jest obciążenie ... w całym ciele"
        "A_qs": at("8A", 54.2),     # "A ostatnia całka ... na brzegu ciała"
        "B": at("8A", 62.8),        # "tę ostatnią całkę możemy rozpisać"
        "B_known": at("8A", 67.6),  # "znane obciążenia na brzegu"
        "B_unknown": at("8A", 70.8),  # "a druga nieznane siły"
        "B_R": at("8A", 78.1),      # "reakcje oznaczone literą R"
        "B_eq": at("8A", 85.0),     # "mamy następujące równanie"
        "C_fem": at("8A", 90.8),    # "tu wchodzi MES"
        "C": at("8A", 101.6),       # "Całka po całym ciele staje się sumą"
        "C_T": at("8A", 113.9),     # "macierze T"
        "D": at("8A", 137.5),       # "zastąpić symbolami"
        "D_K": at("8A", 140.6),     # "symbolem K"
        "D_P": at("8A", 146.9),     # "symbolem P"
        "D_m": at("8A", 150.9),     # "Takich składników jest tyle"
        "D_R": at("8A", 157.6),     # "zostaje jeszcze R"
        "glob": at("8A", 165.5),    # "Globalna macierz sztywności"
        "g_Q": at("8A", 174.1),     # "Razy wektor przemieszczeń"
        "g_P": at("8A", 178.1),     # "globalnemu wektorowi obciążeń"
        "g_R": at("8A", 181.3),     # "plus wektorowi reakcji"
        "restore": at(8, 110.6),    # back to recording 8: "Otrzymujemy układ równań"
    })
    RT = {"axes": 0.6, "graph": 1.0, "rects": 1.0, "park": 1.0, "pi_u": 2.0,
          "pi_q": 3.0}

    def derivation(self, pi_u, sub_row, pi_q, arrow, main_eq):
        C_R = RED_B
        Y1, Y2, Y3 = 1.25, 0.0, -1.3

        def tex(*parts, size=33):
            return MathTex(*parts, font_size=size)

        # ---- A: the derivative written out ----
        eq_a = tex(
            r"\Big(\int_{A}\mathbf{B}^{T}\mathbf{D}\,\mathbf{B}\,h\,dA\Big)",   # 0
            r"\mathbf{Q}", r"\;=\;",                                           # 1 2
            r"\int_{A}\mathbf{N}^{T}\mathbf{q}_{V}\,h\,dA",                    # 3
            r"\;+\;",                                                          # 4
            r"\int_{\Gamma}\mathbf{N}^{T}\mathbf{q}_{S}\,h\,ds",               # 5
        )
        eq_a[0].set_color(C_K)
        eq_a[3].set_color(C_P)
        eq_a[5].set_color(C_P)
        eq_a.move_to([0, Y1, 0])

        self.cue("ins")
        self.play(FadeOut(pi_u), FadeOut(sub_row),
                  pi_q.animate.move_to([0.0, 2.45, 0]), run_time=1.0)
        self.cue("A")
        self.play(Write(eq_a), run_time=1.5)
        self.cue("A_lhs")
        self.play(Circumscribe(eq_a[0], color=C_K, buff=0.08), run_time=1.5)
        # glyphs of ( int_A B^T D B h dA ): 3, 4 = B^T, 5 = D, 6 = B
        self.cue("A_B")
        self.play(Indicate(VGroup(*eq_a[0][3:5], eq_a[0][6]), color=C_N), run_time=1.2)
        self.cue("A_D")
        self.play(Indicate(eq_a[0][5], color=WHITE), run_time=1.2)
        self.cue("A_rhs")
        self.play(Circumscribe(VGroup(*eq_a[3:6]), color=C_P, buff=0.08), run_time=1.5)
        self.cue("A_qv")
        self.play(Indicate(eq_a[3], color=C_P, scale_factor=1.15), run_time=1.2)
        self.cue("A_qs")
        self.play(Indicate(eq_a[5], color=C_P, scale_factor=1.15), run_time=1.2)

        # ---- B: the boundary splits into a loaded and a supported part ----
        eq_b = tex(
            r"\int_{\Gamma}\mathbf{N}^{T}\mathbf{q}_{S}\,h\,ds",               # 0
            r"\;=\;",                                                          # 1
            r"\int_{\Gamma_q}\mathbf{N}^{T}\mathbf{q}_{S}\,h\,ds",             # 2
            r"\;+\;",                                                          # 3
            r"\int_{\Gamma_u}\mathbf{N}^{T}\mathbf{q}_{S}\,h\,ds",             # 4
        )
        eq_b[0].set_color(C_P)
        eq_b[2].set_color(C_P)
        eq_b.move_to([0, Y2 + 0.15, 0])
        lbl_q = Text("known load", font_size=20, color=C_P).next_to(eq_b[2], DOWN, buff=0.18)
        lbl_u = Text("support forces", font_size=20, color=C_R).next_to(eq_b[4], DOWN, buff=0.18)
        br_r = Brace(eq_b[4], DOWN, buff=0.08, color=C_R)
        r_sym = MathTex(r"\mathbf{R}", font_size=34, color=C_R).next_to(br_r, DOWN, buff=0.08)

        self.cue("B")
        self.play(TransformFromCopy(eq_a[5], eq_b[0]), run_time=0.8)
        self.play(Write(VGroup(*eq_b[1:])), run_time=1.2)
        self.cue("B_known")
        self.play(Indicate(eq_b[2], color=C_P, scale_factor=1.12), FadeIn(lbl_q), run_time=1.0)
        self.cue("B_unknown")
        self.play(eq_b[4].animate.set_color(C_R), FadeIn(lbl_u), run_time=1.0)
        self.cue("B_R")
        self.play(FadeOut(lbl_u), GrowFromCenter(br_r), FadeIn(r_sym, shift=UP * 0.1),
                  run_time=0.9)

        eq_ar = tex(
            r"\Big(\int_{A}\mathbf{B}^{T}\mathbf{D}\,\mathbf{B}\,h\,dA\Big)",
            r"\mathbf{Q}", r"\;=\;",
            r"\int_{A}\mathbf{N}^{T}\mathbf{q}_{V}\,h\,dA",
            r"\;+\;",
            r"\int_{\Gamma_q}\mathbf{N}^{T}\mathbf{q}_{S}\,h\,ds",
            r"\;+\;", r"\mathbf{R}",
        )
        eq_ar[0].set_color(C_K)
        eq_ar[3].set_color(C_P)
        eq_ar[5].set_color(C_P)
        eq_ar[7].set_color(C_R)
        eq_ar.move_to([0, Y1, 0])
        self.cue("B_eq")
        self.play(
            ReplacementTransform(VGroup(*eq_a[:5]), VGroup(*eq_ar[:5])),
            ReplacementTransform(eq_a[5], eq_ar[5]),
            FadeIn(eq_ar[6]),
            ReplacementTransform(r_sym, eq_ar[7]),
            FadeOut(VGroup(eq_b, br_r, lbl_q)),
            run_time=1.4,
        )

        # ---- C: finite elements - the integral over the body is a sum over elements ----
        fem = Text("FEM: body  =  sum of elements", font_size=24, color=YELLOW)
        fem.move_to([0, Y2 + 0.55, 0])
        eq_c = tex(
            r"\Big(\sum_{e}",                                                  # 0
            r"\mathbf{T}_e^{T}",                                               # 1
            r"\Big(\int_{A_e}\mathbf{B}_e^{T}\mathbf{D}\,\mathbf{B}_e\,h\,dA\Big)",  # 2
            r"\mathbf{T}_e",                                                   # 3
            r"\Big)\,\mathbf{Q}", r"\;=\;",                                    # 4 5
            r"\sum_{e}",                                                       # 6
            r"\mathbf{T}_e^{T}",                                               # 7
            r"\Big(\int_{A_e}\mathbf{N}_e^{T}\mathbf{q}_{V}\,h\,dA"
            r"+\int_{\Gamma_{q,e}}\mathbf{N}_e^{T}\mathbf{q}_{S}\,h\,ds\Big)",  # 8
            r"\;+\;", r"\mathbf{R}",                                           # 9 10
            size=30,
        )
        eq_c[2].set_color(C_K)
        eq_c[8].set_color(C_P)
        eq_c[10].set_color(C_R)
        eq_c.move_to([0, Y2 - 0.2, 0])

        self.cue("C_fem")
        self.play(FadeIn(fem, shift=DOWN * 0.15), run_time=0.7)
        self.cue("C")
        self.play(Write(eq_c), run_time=2.0)
        self.cue("C_T")
        self.play(*[Indicate(eq_c[i], color=YELLOW, scale_factor=1.3) for i in (1, 3, 7)],
                  run_time=1.4)

        # ---- D: element integrals get names, K_e and P_e ----
        eq_d = tex(
            r"\big(",                                                          # 0
            r"\mathbf{T}_1^{T}\mathbf{K}_1\mathbf{T}_1",                       # 1
            r"+",                                                              # 2
            r"\mathbf{T}_2^{T}\mathbf{K}_2\mathbf{T}_2",                       # 3
            r"+\dots+",                                                        # 4
            r"\mathbf{T}_m^{T}\mathbf{K}_m\mathbf{T}_m",                       # 5
            r"\big)\,\mathbf{Q}", r"\;=\;",                                    # 6 7
            r"\mathbf{T}_1^{T}\mathbf{P}_1",                                   # 8
            r"+",                                                              # 9
            r"\mathbf{T}_2^{T}\mathbf{P}_2",                                   # 10
            r"+\dots+",                                                        # 11
            r"\mathbf{T}_m^{T}\mathbf{P}_m",                                   # 12
            r"\;+\;", r"\mathbf{R}",                                           # 13 14
            size=33,
        )
        k_parts = VGroup(eq_d[1], eq_d[3], eq_d[5])
        p_parts = VGroup(eq_d[8], eq_d[10], eq_d[12])
        k_parts.set_color(C_K)
        p_parts.set_color(C_P)
        eq_d[14].set_color(C_R)
        eq_d.move_to([0, Y3, 0])
        self.cue("D")
        self.play(FadeOut(fem), Write(eq_d), run_time=1.8)
        self.cue("D_K")
        self.play(Indicate(k_parts, color=C_K, scale_factor=1.15), run_time=1.2)
        self.cue("D_P")
        self.play(Indicate(p_parts, color=C_P, scale_factor=1.15), run_time=1.2)
        self.cue("D_m")
        self.play(Indicate(VGroup(eq_d[4], eq_d[5], eq_d[11], eq_d[12]),
                           color=YELLOW, scale_factor=1.15), run_time=1.4)
        self.cue("D_R")
        self.play(Indicate(eq_d[14], color=C_R, scale_factor=1.4), run_time=1.0)

        # ---- the main equation, already in its place at the bottom ----
        self.cue("glob")
        self.play(FadeIn(arrow), run_time=0.3)
        self.play(Write(main_eq), run_time=1.0)
        self.cue("g_Q")
        self.play(Indicate(main_eq[2], scale_factor=1.3), run_time=1.0)
        self.cue("g_P")
        self.play(Indicate(main_eq[4], color=C_P, scale_factor=1.3), run_time=1.0)
        self.cue("g_R")
        self.play(Indicate(main_eq[6], color=C_R, scale_factor=1.3), run_time=1.0)

        # ---- back to recording 8: the two forms of the functional return ----
        self.cue("restore")
        self.play(FadeOut(VGroup(eq_ar, eq_c, eq_d)),
                  pi_q.animate.move_to([0.0, -0.60, 0]),
                  FadeIn(pi_u), FadeIn(sub_row), run_time=1.2)
        return True

    def ending(self):
        dt = self.TOTAL - self.renderer.time
        if dt > 0:
            self.wait(dt)


if __name__ == "__main__":
    # Full HD, 60 fps - same as the other clips used in the film.
    os.system("manim -qh energy_minimum.py EnergyMinimumScene")
