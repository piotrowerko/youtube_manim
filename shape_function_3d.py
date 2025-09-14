from manim import *

class ShapeFunction3D(ThreeDScene):
    """3D visualization of bilinear shape function for rectangular element."""

    def construct(self):
        # Create 3D coordinate axes centered on rectangle
        axes = ThreeDAxes(
            x_range=[0, 2.2, 0.5],
            y_range=[0, 2.2, 0.5], 
            z_range=[0, 1.2, 0.2],
            x_length=4,
            y_length=4,
            z_length=3,
            axis_config={"color": WHITE, "stroke_width": 2}
        )
        
        # Set up 3D camera with focus on center of rectangle (1,1,0.5)
        self.set_camera_orientation(
            phi=70 * DEGREES, 
            theta=45 * DEGREES,
            focal_distance=8,  # Odsuń kamerę dalej
            frame_center=axes.c2p(1, 1, 0.3)  # Centruj na środku prostokąta
        )
        
        # Add axis labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y") 
        z_label = axes.get_z_axis_label("N_i")
        
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(z_label))

        # Define the shape function N_i(x,y) = (a-x)(b-y)/(ab) for a=2, b=2
        def shape_function(u, v):
            x = u * 2  # map [0,1] to [0,2]
            y = v * 2  # map [0,1] to [0,2]
            a, b = 2, 2
            return (a - x) * (b - y) / (a * b)

        # Create the 3D surface
        surface = Surface(
            lambda u, v: axes.c2p(u * 2, v * 2, shape_function(u, v)),
            u_range=[0, 1],
            v_range=[0, 1],
            resolution=(20, 20),
            fill_color=BLUE,
            fill_opacity=0.7,
            stroke_color=WHITE,
            stroke_width=0.5
        )
        
        # Color the surface based on height
        surface.set_fill_by_checkerboard(BLUE, RED, opacity=0.7)
        
        self.play(Create(surface))

        # Mark the four corner nodes of rectangular element (MES)
        # Węzły prostokąta: i(0,0), j(2,0), k(2,2), r(0,2)
        # Funkcja kształtu N_i ma wartość 1 w węźle i, 0 w pozostałych węzłach
        corner_points = [
            (0, 0, 0),  # Węzeł i na podstawie (z=0)
            (2, 0, 0),  # Węzeł j na podstawie (z=0) 
            (2, 2, 0),  # Węzeł k na podstawie (z=0)
            (0, 2, 0)   # Węzeł r na podstawie (z=0)
        ]
        
        # Wartości funkcji kształtu w węzłach
        shape_values = [
            shape_function(0, 0),  # N_i(0,0) = 1 
            shape_function(1, 0),  # N_i(2,0) = 0
            shape_function(1, 1),  # N_i(2,2) = 0
            shape_function(0, 1)   # N_i(0,2) = 0
        ]
        
        corner_labels = ["i", "j", "k", "r"]
        corner_colors = [RED, BLUE, BLUE, BLUE]  # Węzeł i wyróżniony czerwonym
        
        nodes = VGroup()
        for (x, y, z_base), label, color, n_value in zip(corner_points, corner_labels, corner_colors, shape_values):
            # Punkt na podstawie prostokąta (z=0) - niebieska kropka
            base_point = Dot3D(axes.c2p(x, y, z_base), radius=0.1, color=BLUE)
            nodes.add(base_point)
            
            # Punkt na powierzchni funkcji kształtu
            z_surface = n_value
            surface_point = Dot3D(axes.c2p(x, y, z_surface), radius=0.08, color=color)
            nodes.add(surface_point)
            
            # Linia łącząca podstawę z powierzchnią
            if abs(z_surface - z_base) > 0.01:
                connecting_line = Line3D(
                    axes.c2p(x, y, z_base), 
                    axes.c2p(x, y, z_surface), 
                    color=color, 
                    stroke_width=3
                )
                nodes.add(connecting_line)
            
            # Etykieta węzła przy niebieskiej kropce na płaszczyźnie XY (obraca się z animacją)
            label_text = MathTex(label, color=YELLOW).scale(1.0)
            # Pozycjonowanie etykiet bardzo blisko niebieskich kropek
            if label == "i":  # (0,0,0)
                label_text.move_to(axes.c2p(x-0.15, y-0.15, z_base + 0.05))
            elif label == "j":  # (2,0,0)
                label_text.move_to(axes.c2p(x+0.15, y-0.15, z_base + 0.05))
            elif label == "k":  # (2,2,0)
                label_text.move_to(axes.c2p(x+0.15, y+0.15, z_base + 0.05))
            else:  # r (0,2,0)
                label_text.move_to(axes.c2p(x-0.15, y+0.15, z_base + 0.05))
            
            # NIE używamy add_fixed_in_frame_mobjects - etykiety będą się obracać z animacją
            nodes.add(label_text)
        
        self.play(FadeIn(nodes))

        # Add function equation (fixed to frame)
        equation = MathTex(
            r"N_i(x,y) = \frac{(a-x)(b-y)}{ab} = \frac{(2-x)(2-y)}{4}"
        ).scale(0.6)
        equation.to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(equation)
        self.play(FadeIn(equation))

        # Rotate the camera around the surface
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(8)
        self.stop_ambient_camera_rotation()

        # Final close-up rotation
        self.move_camera(phi=60 * DEGREES, theta=30 * DEGREES, run_time=2)
        self.wait(2)

if __name__ == "__main__":
    scene = ShapeFunction3D()
    scene.render()
