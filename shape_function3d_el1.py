from manim import *

class ShapeFunction3D_E1(ThreeDScene):
    """3D visualization of the shape function for the local rectangular element."""

    def construct(self):
        # --- kontrola "wyniosłości" wykresu ---
        z_scale = 0.45  # <--- zmniejsz jeszcze (np. 0.35), jeśli nadal za wysokie

        # Local coordinates: x in [-1,1], y in [-1.5,1.5]
        axes = ThreeDAxes(
            x_range=[-1.2, 1.2, 0.5],
            y_range=[-1.7, 1.7, 0.5],
            z_range=[-0.20, 0.20, 0.05],   # zakres osi Z po spłaszczeniu
            x_length=4,
            y_length=4,
            z_length=2.0,                  # krótsza oś Z
            axis_config={"color": WHITE, "stroke_width": 2}
        )

        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=45 * DEGREES,
            focal_distance=8,
            frame_center=axes.c2p(0, 0, 0.0)
        )

        # Bez indeksów dolnych
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("N")

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(z_label))

        # Shape function: N(x,y) = (1/12) (x-1) (2y-3)
        def N(x, y):
            return (1/12) * (x - 1) * (2*y - 3)

        # Surface over the local domain (spłaszczona w osi Z)
        surface = Surface(
            lambda u, v: axes.c2p(u, v, z_scale * N(u, v)),
            u_range=[-1, 1],
            v_range=[-1.5, 1.5],
            resolution=(28, 28),
            fill_opacity=0.7,
            stroke_color=WHITE,
            stroke_width=0.5
        )
        surface.set_fill_by_checkerboard(BLUE, RED, opacity=0.7)
        self.play(Create(surface))

        # Corner nodes (local)
        corner_points = [
            ( 1, -1.5, 0),
            ( 1,  1.5, 0),
            (-1,  1.5, 0),
            (-1, -1.5, 0),
        ]
        corner_labels = ["(1,-1.5)", "(1,1.5)", "(-1,1.5)", "(-1,-1.5)"]

        nodes = VGroup()
        for (x, y, z0), lab in zip(corner_points, corner_labels):
            base = Dot3D(axes.c2p(x, y, 0), radius=0.09, color=BLUE)
            nodes.add(base)

            z1 = z_scale * N(x, y)  # <--- też spłaszczamy wysokość punktu i linii
            top = Dot3D(axes.c2p(x, y, z1), radius=0.08, color=YELLOW)
            nodes.add(top)

            if abs(z1) > 0.01:
                nodes.add(Line3D(axes.c2p(x, y, 0), axes.c2p(x, y, z1), color=YELLOW, stroke_width=3))

            t = MathTex(lab, color=YELLOW).scale(0.55)
            t.move_to(axes.c2p(x, y, 0) + 0.15 * OUT)
            nodes.add(t)

        self.play(FadeIn(nodes))

        # Equation fixed in frame (bez indeksów)
        equation = MathTex(r"Ni(x,y)=\frac{1}{12}(x-1)(2y-3)").scale(0.7)
        equation.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(equation)
        self.play(FadeIn(equation))

        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(8)
        self.stop_ambient_camera_rotation()

        self.move_camera(phi=60 * DEGREES, theta=30 * DEGREES, run_time=2)
        self.wait(2)

if __name__ == "__main__":
    scene = ShapeFunction3D_E1()
    scene.render()
