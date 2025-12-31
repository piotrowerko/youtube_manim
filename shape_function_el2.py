from manim import *

class ShapeFunctionTriK3D_E2(ThreeDScene):
    """3D visualization of triangular shape function Nk for node k."""

    def construct(self):
        # --- kontrola wysokości wykresu ---
        z_scale = 0.55  # zmniejsz np. do 0.4 jeśli nadal za wysokie

        # Local coordinates anchored at node i: i(0,0), k(0,-2), r(-2,-2)
        axes = ThreeDAxes(
            x_range=[-2.2, 0.6, 0.5],
            y_range=[-2.2, 0.6, 0.5],
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
            frame_center=axes.c2p(-0.8, -1.0, 0.2),
        )

        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        z_label = axes.get_z_axis_label("Nk")

        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(z_label))

        # Shape function for node k:
        # Nk(x,y) = 0.5x - 0.5y
        def Nk(x, y):
            return 0.5 * x - 0.5 * y

        # --- Parametryzacja trójkąta ---
        # Wierzchołki: i(0,0), k(0,-2), r(-2,-2)
        # P(u,v) = i + u*(k-i) + v*(r-i),  u>=0, v>=0, u+v<=1
        # Żeby Surface mogło użyć prostokątnego (u,v) in [0,1]^2:
        # u2 = u*(1-v) => u2+v <= 1
        def tri_point(u, v):
            u2 = u * (1 - v)
            x = -2 * v
            y = -2 * u2 - 2 * v
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

        # Corner nodes on base z=0
        nodes_data = [
            ("i", (0, 0)),
            ("k", (0, -2)),
            ("r", (-2, -2)),
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

            # Label przy podstawie
            t = MathTex(name, color=YELLOW).scale(0.9)
            t.move_to(axes.c2p(x, y, 0) + 0.18 * OUT)
            nodes.add(t)

        self.play(FadeIn(nodes))

        # Equation fixed in frame (bez indeksów dolnych)
        equation = MathTex(r"Nk(x,y)=0.5x-0.5y").scale(0.8)
        equation.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(equation)
        self.play(FadeIn(equation))

        # Camera rotation
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(8)
        self.stop_ambient_camera_rotation()

        self.move_camera(phi=60 * DEGREES, theta=30 * DEGREES, run_time=2)
        self.wait(2)

if __name__ == "__main__":
    scene = ShapeFunctionTriK3D_E2()
    scene.render()
