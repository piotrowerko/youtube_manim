from manim import *


# Shape function N_i of element 1 shown as a 3D surface, timed to the merged
# recording "12-13 fkszt AB". The height is only a way to draw N_i; the in-plane
# arrows show what it means: the share of node i's unit displacement (Q11, then
# Q12) taken by each point of the element.
#
#   manim -qh --frame_rate 30 shape_function3d_el1_voiced.py ShapeFunction3D_E1_Voiced

# Moments of the merged recording (s); the scene starts at T0.
T0 = 234.0
CUES = {
    "axes": 234.3,       # "No i teraz najważniejsze ... na wizualizacji"
    "surface": 244.6,    # "Tak wygląda ta funkcja kształtu"
    "nodes": 249.8,      # "w tym węźle i"
    "one": 252.4,        # "wynosi 1"
    "zeros": 253.5,      # "a w trzech pozostałych narożnikach ... 0"
    "equation": 258.0,   # "a pomiędzy nimi formuje taką płynną zmianę"
    "rotate": 264.0,     # "Funkcja kształtu tak naprawdę mówi jedno"
    "plane": 286.4,      # "oba te przesuwy są w płaszczyźnie tarczy"
    "q11": 292.5,        # "jak przesuniemy węzeł i ... w prawo ... Q11"
    "field": 304.8,      # "pokazuje o jaką część tego 1 w prawo przesuną się"
    "yellow": 315.2,     # "ta pionowa żółta kreska ... nie oznacza"
    "flat": 322.6,       # "Trzeci wymiar dodałem tylko po to"
    "leader": 342.6,     # "Tym liderem jest węzeł i"
    "vertical": 357.2,   # "Jeśli węzeł i przesunie się pionowo ... Q12"
}
END = 381.3

Z_SCALE = 0.45
ARROW_LEN = 1.4          # scene units for a full unit displacement


def N(x, y):
    return (1 / 12) * (x - 1) * (2 * y - 3)


class ShapeFunction3D_E1_Voiced(ThreeDScene):
    def cue(self, name):
        dt = CUES[name] - T0 - self.renderer.time
        if dt > 1e-3:
            self.wait(dt)
        elif dt < -0.05:
            print(f"cue {name} late by {-dt:.2f} s")

    def construct(self):
        axes = ThreeDAxes(
            x_range=[-1.2, 1.2, 0.5],
            y_range=[-1.7, 1.7, 0.5],
            z_range=[-0.20, 0.20, 0.05],
            x_length=4,
            y_length=4,
            z_length=2.0,
            axis_config={"color": WHITE, "stroke_width": 2},
        )
        self.set_camera_orientation(
            phi=70 * DEGREES, theta=45 * DEGREES, focal_distance=8,
            frame_center=axes.c2p(0, 0, 0.0),
        )
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("N")

        self.cue("axes")
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(z_label))

        surface = Surface(
            lambda u, v: axes.c2p(u, v, Z_SCALE * N(u, v)),
            u_range=[-1, 1], v_range=[-1.5, 1.5], resolution=(28, 28),
            fill_opacity=0.7, stroke_color=WHITE, stroke_width=0.5,
        )
        surface.set_fill_by_checkerboard(BLUE, RED, opacity=0.7)
        self.cue("surface")
        self.play(Create(surface), run_time=2)

        # corner nodes; node i = (-1, -1.5) is the only one lifted to N = 1
        corners = [(1, -1.5), (1, 1.5), (-1, 1.5), (-1, -1.5)]
        labels = ["(1,-1.5)", "(1,1.5)", "(-1,1.5)", "(-1,-1.5)"]
        nodes, zero_dots = VGroup(), VGroup()
        for (x, y), lab in zip(corners, labels):
            base = Dot3D(axes.c2p(x, y, 0), radius=0.09, color=BLUE, resolution=(6, 6))
            top = Dot3D(axes.c2p(x, y, Z_SCALE * N(x, y)), radius=0.08, color=YELLOW, resolution=(6, 6))
            nodes.add(base, top)
            if N(x, y) > 0.5:
                pole = Line3D(axes.c2p(x, y, 0), axes.c2p(x, y, Z_SCALE * N(x, y)),
                              color=YELLOW, stroke_width=3)
                nodes.add(pole)
                top_i = top
            else:
                zero_dots.add(base)
            t = MathTex(lab, color=YELLOW).scale(0.55)
            t.move_to(axes.c2p(x, y, 0) + 0.15 * OUT)
            nodes.add(t)
        self.cue("nodes")
        self.play(FadeIn(nodes))
        self.cue("one")
        self.play(Flash(top_i, color=YELLOW, flash_radius=0.35), Indicate(pole, color=YELLOW))
        self.cue("zeros")
        self.play(LaggedStart(*[Indicate(d, scale_factor=1.8, color=WHITE) for d in zero_dots],
                              lag_ratio=0.3), run_time=1.5)

        equation = MathTex(r"N_i(x,y)=\frac{1}{12}(x-1)(2y-3)").scale(0.7)
        equation.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(equation)
        equation.set_opacity(0)
        self.cue("equation")
        self.play(equation.animate.set_opacity(1))

        # the camera moves in short steps only; still shots render fast
        self.cue("rotate")
        self.move_camera(theta=-70 * DEGREES, phi=65 * DEGREES, run_time=8)

        # the element itself lies in the plane z = 0
        plate = Polygon(*[axes.c2p(x, y, 0) for x, y in [(-1, -1.5), (1, -1.5), (1, 1.5), (-1, 1.5)]],
                        color=GREEN_B, stroke_width=5, fill_color=GREEN_E, fill_opacity=0.25)
        self.cue("plane")
        self.play(Create(plate), surface.animate.set_fill(opacity=0.35), run_time=1.5)

        # node i moves by 1 to the right: Q11
        p_i = axes.c2p(-1, -1.5, 0)
        q_arrow = Arrow(p_i, p_i + RIGHT * ARROW_LEN, buff=0, color=YELLOW, stroke_width=8,
                        max_tip_length_to_length_ratio=0.2)
        q_label = MathTex(r"Q_{11}=1", color=YELLOW).scale(0.8)
        q_label.move_to(p_i + RIGHT * ARROW_LEN * 0.5 + DOWN * 0.45)
        self.add_fixed_orientation_mobjects(q_label)
        q_label.set_opacity(0)
        self.cue("q11")
        self.play(GrowFromPoint(q_arrow, p_i), q_label.animate.set_opacity(1))

        # every other point follows by N_i times that unit
        def field(direction):
            g = VGroup()
            for x in np.linspace(-1, 1, 5):
                for y in np.linspace(-1.5, 1.5, 5):
                    n = N(x, y)
                    on_edge = abs(y + 1.5) < 1e-6 if direction[0] else abs(x + 1) < 1e-6
                    if n < 0.04 or on_edge:     # the edge of node i's own arrow
                        continue
                    p = axes.c2p(x, y, 0)
                    g.add(Arrow(p, p + direction * ARROW_LEN * n, buff=0, color=ORANGE,
                                stroke_width=5, max_tip_length_to_length_ratio=0.35))
            return g

        f_x = field(RIGHT)
        self.cue("field")
        self.play(LaggedStart(*[GrowFromPoint(a, a.get_start()) for a in f_x], lag_ratio=0.06),
                  run_time=3)

        self.cue("yellow")
        self.play(Indicate(pole, color=RED, scale_factor=1.15), run_time=1.5)
        self.play(Indicate(plate, color=GREEN, scale_factor=1.0), run_time=1.5)

        # seen from above: what really happens is in the plane of the element
        self.cue("flat")
        self.move_camera(phi=25 * DEGREES, theta=-90 * DEGREES, run_time=3)

        self.cue("leader")
        self.play(Indicate(q_arrow, color=YELLOW, scale_factor=1.3), run_time=1.5)

        # the same function serves the vertical displacement Q12
        q_arrow_y = Arrow(p_i, p_i + UP * ARROW_LEN, buff=0, color=YELLOW, stroke_width=8,
                          max_tip_length_to_length_ratio=0.2)
        q_label_y = MathTex(r"Q_{12}=1", color=YELLOW).scale(0.8)
        q_label_y.move_to(p_i + UP * (ARROW_LEN + 0.35) + LEFT * 0.3)
        self.add_fixed_orientation_mobjects(q_label_y)
        q_label_y.set_opacity(0)
        f_y = field(UP)
        self.cue("vertical")
        self.play(ReplacementTransform(q_arrow, q_arrow_y), ReplacementTransform(f_x, f_y),
                  q_label.animate.set_opacity(0), q_label_y.animate.set_opacity(1), run_time=2)

        self.wait(max(0.0, END - T0 - self.renderer.time))
