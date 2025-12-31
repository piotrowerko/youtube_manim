from manim import *

class ShapeFunctionTriNk3D_E3(ThreeDScene):
    """3D visualization of triangular shape function Nk for node k (element e.III)."""

    def construct(self):
        z_scale = 0.55  # spłaszczenie wysokości (zmniejsz, jeśli trzeba)

        # Local coordinates anchored at node i = (0,0)
        # Triangle vertices: i(0,0), k(0,2), j(2,2)
        axes = ThreeDAxes(
            x_range=[-0.2, 2.3, 0.5],
            y_range=[-0.2, 2.3, 0.5],
            z_range=[0.0, 1.1 * z_scale, 0.2],
            x_length=4.2,
            y_length=4.2,
            z_length=2.2,
            axis_config={"color": WHITE, "stroke_width": 2},
        )

        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=45 * DEGREES,
            focal_distance=8,
            frame_center=axes.c2p(1.0, 1.2, 0.2),
        )

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("Nk")

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(z_label))

        # Nk(x,y) = -0.5x + 0.5y
        def Nk(x, y):
            return -0.5 * x + 0.5 * y

        # Parametryzacja trójkąta:
        # i(0,0), k(0,2), j(2,2)
        # P(u,v) = i + u*(k-i) + v*(j-i), u>=0, v>=0, u+v<=1
        # a w (x,y): x = 2v, y = 2(u+v)
        def tri_point(u, v):
            u2 = u * (1 - v)      # gwarantuje u2 + v <= 1
            x = 2 * v
            y = 2 * (u2 + v)
            z = z_scale * Nk(x, y)
            return axes.c2p(x, y, z)

        surface = Surface(
            lambda u, v: tri_point(u, v),
            u_range=[0, 1],
            v_range=[0, 1],
            resolution=(28, 28),
            fill_opacity=0.75,
            stroke_color=WHITE,
            stroke_width=0.5,
        )
        surface.set_fill_by_checkerboard(BLUE, RED, opacity=0.75)
        self.play(Create(surface))

        # Nodes: i(0,0), k(0,2), j(2,2)
        nodes_data = [
            ("i", (0, 0)),
            ("k", (0, 2)),
            ("j", (2, 2)),
        ]

        nodes = VGroup()
        for name, (x, y) in nodes_data:
            base = Dot3D(axes.c2p(x, y, 0), radius=0.09, color=BLUE)
            nodes.add(base)

            z1 = z_scale * Nk(x, y)
            top = Dot3D(axes.c2p(x, y, z1), radius=0.08, color=YELLOW)
            nodes.add(top)

            if abs(z1) > 0.01:
                nodes.add(Line3D(axes.c2p(x, y, 0), axes.c2p(x, y, z1), color=YELLOW, stroke_width=3))

            t = MathTex(name, color=YELLOW).scale(0.9)
            t.move_to(axes.c2p(x, y, 0) + 0.18 * OUT)
            nodes.add(t)

        self.play(FadeIn(nodes))

        equation = MathTex(r"Nk(x,y)=-0.5x+0.5y").scale(0.8)
        equation.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(equation)
        self.play(FadeIn(equation))

        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(8)
        self.stop_ambient_camera_rotation()

        self.move_camera(phi=60 * DEGREES, theta=30 * DEGREES, run_time=2)
        self.wait(2)

if __name__ == "__main__":
    scene = ShapeFunctionTriNk3D_E3()
    scene.render()
