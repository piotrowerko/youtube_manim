from manim import *

import numpy as np


# Plate vs. plane-stress element explained with a knight's shield. Shown next
# to the structure outline at the start of the example, timed to recording 9.
# Everything is drawn inside a band of the 1920x1080 frame (px x 1020..1880,
# y 190..990), which is cropped out with ffmpeg and laid over the main scene.
#
#   manim -qh --frame_rate 30 knight_shield.py KnightShield
#   ffmpeg -i KnightShield.mp4 -vf crop=860:800:1020:190 ...

# Moments of recording 9 (s, uncut recording); the scene starts at T0.
T0 = 34.6
CUES = {
    "knight": 34.8,      # "Kojarzy nam się pewnie słowo tarcza z tarczą rycerza"
    "sword": 40.4,       # "bijemy w tą tarczę mieczem"
    "perp": 42.0,        # "prostopadle do płaszczyzny tarczy"
    "cross": 47.5,       # "nazywamy płytą"
    "clear": 49.7,       # "Tu chodzi o sytuację,"
    "stand": 51.2,       # "postawilibyśmy taką tarczę na sztorc"
    "push": 59.8,        # "I próbowali ją wbić w ziemię"
    "reaction": 62.7,    # "Wtedy siła reakcji z ziemi"
    "hand": 64.4,        # "i nasza siła z dłoni"
    "plane": 65.4,       # "działają w płaszczyźnie tarczy"
    "out": 81.0,         # after "... obciążony jest w swojej płaszczyźnie."
}
END = 82.0

GROUND_Y = -1.9
STEEL = GREY_B
BODY = GREY_D
SHIELD_FACE = BLUE_E
SHIELD_EDGE = BLUE_D


def capsule(a, b, width=0.2, color=STEEL):
    """Limb: a thick line with round caps."""
    ln = Line(a, b, stroke_width=width * 100, color=color)
    ln.set_cap_style(CapStyleType.ROUND)
    return ln


def heater(w=1.0, h=1.0):
    """Heater-shield outline (point down), centred at the origin."""
    tl, tr = np.array([-w / 2, h / 2, 0]), np.array([w / 2, h / 2, 0])
    rs, ls = np.array([w / 2, h * 0.05, 0]), np.array([-w / 2, h * 0.05, 0])
    tip = np.array([0, -h / 2, 0])
    shape = VMobject()
    shape.set_points_as_corners([tl, tr, rs])
    shape.append_vectorized_mobject(ArcBetweenPoints(rs, tip, angle=-PI / 3.2))
    shape.append_vectorized_mobject(ArcBetweenPoints(tip, ls, angle=-PI / 3.2))
    shape.add_line_to(tl)
    return shape


def make_shield(height=2.0):
    """Shield turned with its face towards the right (towards the sword): a narrow,
    sheared heater outline plus the rim on the back side, so its thickness shows."""
    def turn(m):
        return m.apply_function(lambda p: p + np.array([0, 0.3 * p[0], 0]))

    face = turn(heater(1.0, 1.0).stretch(0.3 * height, 0).stretch(height, 1))
    face.set_fill(SHIELD_FACE, 1).set_stroke(SHIELD_EDGE, 3)
    rim = face.copy().shift(LEFT * 0.12).set_stroke(SHIELD_EDGE, 2)
    rim.set_fill(interpolate_color(BLUE_E, BLACK, 0.5), 1)
    cross_v = turn(Line(UP * 0.36 * height, DOWN * 0.3 * height, stroke_width=5, color=GOLD_C))
    cross_h = turn(Line(LEFT * 0.09 * height, RIGHT * 0.09 * height, stroke_width=5,
                        color=GOLD_C).shift(UP * 0.12 * height))
    return VGroup(rim, face, cross_v, cross_h)


def make_knight(arm_targets):
    """Knight in side view facing right; arms reach to the given points."""
    hip = np.array([2.55, -0.25, 0])
    k = VGroup()
    # legs and boots
    for dx, foot in ((-0.15, -0.35), (0.18, 0.05)):
        top = hip + RIGHT * dx
        bottom = np.array([top[0] + foot * 0.4, GROUND_Y + 0.12, 0])
        k.add(capsule(top, bottom, 0.26, STEEL))
        k.add(RoundedRectangle(width=0.42, height=0.16, corner_radius=0.06, color=GREY_C,
                               fill_color=BODY, fill_opacity=1, stroke_width=2)
              .move_to(bottom + RIGHT * 0.1 + DOWN * 0.04))
    # torso with breastplate and belt
    torso = Polygon(hip + LEFT * 0.38, hip + RIGHT * 0.38, hip + UP * 1.25 + RIGHT * 0.46,
                    hip + UP * 1.35 + LEFT * 0.4, color=GREY_C, stroke_width=3,
                    fill_color=BODY, fill_opacity=1)
    belt = Line(hip + LEFT * 0.38 + UP * 0.12, hip + RIGHT * 0.39 + UP * 0.12,
                stroke_width=6, color=GOLD_E)
    k.add(torso, belt)
    # great helm with visor slit and plume
    head_c = hip + UP * 1.75 + RIGHT * 0.05
    helm = RoundedRectangle(width=0.62, height=0.72, corner_radius=0.16, color=GREY_C,
                            fill_color=STEEL, fill_opacity=1, stroke_width=3).move_to(head_c)
    slit = Line(head_c + RIGHT * 0.05 + UP * 0.08, head_c + RIGHT * 0.31 + UP * 0.08,
                stroke_width=4, color=BLACK)
    holes = VGroup(*[Dot(head_c + RIGHT * (0.12 + 0.07 * i) + DOWN * 0.12, radius=0.018,
                         color=BLACK) for i in range(3)])
    plume = ArcBetweenPoints(head_c + UP * 0.34 + LEFT * 0.05, head_c + UP * 0.2 + LEFT * 0.55,
                             angle=PI / 2, stroke_width=10, color=RED_D)
    k.add(helm, slit, holes, plume)
    # arms: shoulder -> hand
    shoulder = hip + UP * 1.15 + RIGHT * 0.1
    for t in arm_targets:
        k.add(capsule(shoulder, t, 0.2, STEEL), Dot(t, radius=0.11, color=GREY_C))
    return k


class KnightShield(Scene):
    def cue(self, name):
        dt = CUES[name] - T0 - self.renderer.time
        if dt > 1e-3:
            self.wait(dt)
        elif dt < -0.05:
            print(f"cue {name} late by {-dt:.2f} s")

    def construct(self):
        # ---------------- the knight holds the shield up ----------------
        shield = make_shield(2.0).move_to([4.05, 0.15, 0])
        hand_hold = shield[1].get_center() + LEFT * 0.12 + UP * 0.1
        knight = make_knight([hand_hold])
        ground = Line([1.2, GROUND_Y, 0], [6.4, GROUND_Y, 0], color=GREY_B, stroke_width=3)

        self.cue("knight")
        self.play(FadeIn(knight), FadeIn(shield), Create(ground), run_time=1.0)

        # ---------------- a sword strikes the face of the shield ----------------
        blade = Polygon([0, 0.045, 0], [1.7, 0.045, 0], [1.7, -0.045, 0], [0, -0.045, 0],
                        [-0.18, 0, 0], color=GREY_A, fill_color=GREY_A, fill_opacity=1,
                        stroke_width=1)
        guard = Rectangle(width=0.08, height=0.5, color=GOLD_C, fill_color=GOLD_C,
                          fill_opacity=1, stroke_width=0).move_to([1.74, 0, 0])
        grip = Rectangle(width=0.45, height=0.1, color=GOLD_E, fill_color=GOLD_E,
                         fill_opacity=1, stroke_width=0).move_to([2.0, 0, 0])
        pommel = Dot([2.26, 0, 0], radius=0.07, color=GOLD_C)
        sword = VGroup(blade, guard, grip, pommel)
        hit_x = shield[1].get_right()[0] + 0.02
        sword.move_to([7.6, 0.35, 0], aligned_edge=LEFT)

        self.cue("sword")
        self.add(sword)
        self.play(sword.animate.move_to([hit_x + 0.18, 0.35, 0], aligned_edge=LEFT),
                  run_time=0.55, rate_func=rush_into)
        sparks = VGroup(*[Line(ORIGIN, 0.28 * np.array([np.cos(a), np.sin(a), 0]),
                               color=YELLOW, stroke_width=3).shift([hit_x + 0.05, 0.35, 0])
                          for a in np.linspace(-1.1, 1.1, 5)])
        self.play(FadeIn(sparks, scale=0.4), Wiggle(shield, scale_value=1.03, rotation_angle=0.03),
                  run_time=0.5)
        self.play(FadeOut(sparks), run_time=0.3)

        self.cue("perp")
        perp = Arrow([6.3, -0.75, 0], [hit_x + 0.05, -0.75, 0], buff=0, color=YELLOW,
                     stroke_width=6, max_tip_length_to_length_ratio=0.18)
        perp_lbl = MathTex(r"\perp", font_size=48, color=YELLOW).next_to(perp, DOWN, buff=0.12)
        self.play(GrowArrow(perp), FadeIn(perp_lbl), run_time=0.7)

        self.cue("cross")
        scene1 = VGroup(knight, shield, sword, perp, perp_lbl)
        cross = VGroup(Line([1.4, 1.95, 0], [6.4, -1.7, 0]), Line([1.4, -1.7, 0], [6.4, 1.95, 0]))
        cross.set_stroke(RED, 9)
        plate = Text("load ⊥ plane  →  plate", font_size=28, color=RED).move_to([3.9, 2.3, 0])
        self.play(Create(cross), FadeIn(plate), run_time=0.7)

        # ---------------- the shield is stood up and pushed into the ground ----------------
        self.cue("clear")
        self.play(FadeOut(sword), FadeOut(perp), FadeOut(perp_lbl), FadeOut(cross),
                  FadeOut(plate), run_time=0.8)

        shield_sz = shield.copy().move_to([4.0, GROUND_Y + 1.0, 0])
        top_c = shield_sz[1].get_top()
        knight_push = make_knight([top_c + LEFT * 0.08 + UP * 0.08, top_c + RIGHT * 0.06 + UP * 0.1])
        self.cue("stand")
        self.play(Transform(knight, knight_push), Transform(shield, shield_sz), run_time=1.4)

        # ground covers the part of the shield that goes in
        soil = Rectangle(width=5.2, height=1.1, stroke_width=0, fill_color=BLACK,
                         fill_opacity=1).move_to([3.8, GROUND_Y - 0.55, 0])
        hatch = VGroup(*[Line([x, GROUND_Y, 0], [x - 0.22, GROUND_Y - 0.22, 0], color=GREY_B,
                              stroke_width=2) for x in np.arange(1.45, 6.4, 0.3)])
        soil.set_z_index(5); hatch.set_z_index(6); ground.set_z_index(6)
        self.add(soil, hatch)

        self.cue("push")
        f_arrow = Arrow(top_c + UP * 1.25 + RIGHT * 0.32, top_c + UP * 0.05 + RIGHT * 0.32, buff=0,
                        color=YELLOW, stroke_width=7, max_tip_length_to_length_ratio=0.22)
        f_lbl = MathTex("F", font_size=40, color=YELLOW).next_to(f_arrow, RIGHT, buff=0.12)
        sink = DOWN * 0.28
        self.play(GrowArrow(f_arrow), FadeIn(f_lbl), run_time=0.6)
        self.play(shield.animate.shift(sink), knight.animate.shift(sink * 0.35),
                  f_arrow.animate.shift(sink), f_lbl.animate.shift(sink), run_time=1.0,
                  rate_func=rush_from)

        self.cue("reaction")
        tip = shield[1].get_bottom()
        r_arrow = Arrow(tip + DOWN * 0.95 + RIGHT * 0.32, tip + DOWN * 0.02 + RIGHT * 0.32, buff=0,
                        color=YELLOW, stroke_width=7, max_tip_length_to_length_ratio=0.22)
        r_arrow.set_z_index(7)
        r_lbl = MathTex("R", font_size=40, color=YELLOW).next_to(r_arrow, RIGHT, buff=0.12)
        r_lbl.set_z_index(7)
        self.play(GrowArrow(r_arrow), FadeIn(r_lbl), run_time=0.6)

        self.cue("hand")
        self.play(Indicate(VGroup(f_arrow, f_lbl), color=YELLOW, scale_factor=1.15), run_time=0.8)

        self.cue("plane")
        axis = DashedLine(f_arrow.get_start() + UP * 0.1 + LEFT * 0.32,
                          r_arrow.get_start() + DOWN * 0.05 + LEFT * 0.32,
                          color=GREEN_B, stroke_width=3).set_z_index(7)
        ok = Text("load in plane  →  plane stress", font_size=28, color=GREEN_B)
        ok.move_to([3.9, 2.3, 0])
        self.play(Create(axis), shield[1].animate.set_fill(interpolate_color(SHIELD_FACE, GREEN_E, 0.45)),
                  FadeIn(ok), run_time=1.0)

        self.cue("out")
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        rest = END - T0 - self.renderer.time
        if rest > 1e-3:
            self.wait(rest)
