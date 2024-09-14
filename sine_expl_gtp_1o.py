from manim import *

class SineFunctionExplanation_1o(Scene):
    def construct(self):
        # Create the unit circle
        circle = Circle(radius=2, color=BLUE)
        circle.shift(LEFT * 3)
        self.play(Create(circle))

        # Create the x-axis line for the circle
        circle_x_axis = Line(
            start=circle.get_center(),
            end=circle.get_center() + RIGHT * 2,
            color=WHITE
        )
        self.play(Create(circle_x_axis))

        # Create the axes for the sine curve
        axes = Axes(
            x_range=[0, TAU + 0.1, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=6,
            y_length=3,
            axis_config={"color": WHITE},
            x_axis_config={
                "numbers_to_include": [0, PI / 2, PI, 3 * PI / 2, TAU],
                "include_tip": False,
            },
            y_axis_config={
                "include_numbers": True,
                "include_tip": False,
            },
        )
        axes.shift(RIGHT * 3 + DOWN)
        x_labels = axes.get_axis_labels(x_label="\\theta", y_label="\\sin(\\theta)")

        self.play(Create(axes), Write(x_labels))

        # Create the sine curve
        sine_curve = axes.plot(lambda x: np.sin(x), x_range=[0, TAU], color=RED)
        self.play(Create(sine_curve))

        # Angle tracker
        angle_tracker = ValueTracker(0)

        # Moving dot on the circle
        moving_dot_circle = Dot(point=circle.point_at_angle(0), color=RED)
        self.play(Create(moving_dot_circle))

        # Radius line from the center to the moving dot on the circle
        radius_line = always_redraw(lambda: Line(
            circle.get_center(),
            moving_dot_circle.get_center(),
            color=YELLOW
        ))
        self.play(Create(radius_line))

        # Function to safely create the Angle
        def safe_angle(line1, line2, **kwargs):
            try:
                return Angle(line1, line2, **kwargs)
            except ValueError:
                return VGroup()  # Return an empty group if the angle cannot be computed

        # Angle arc and label
        angle_arc = always_redraw(lambda: safe_angle(
            circle_x_axis,
            radius_line,
            radius=0.5,
            other_angle=False,
            color=YELLOW
        ))
        angle_label = always_redraw(lambda: MathTex("\\theta").next_to(
            angle_arc, direction=RIGHT, buff=0.1
        ))
        self.play(Create(angle_arc), Write(angle_label))

        # Vertical line from the moving dot on the circle to the x-axis
        vert_line_circle = always_redraw(lambda: DashedLine(
            start=moving_dot_circle.get_center(),
            end=[moving_dot_circle.get_center()[0], circle.get_center()[1], 0],
            color=GRAY
        ))
        self.play(Create(vert_line_circle))

        # Horizontal line from the moving dot on the circle to the sine curve
        horizontal_line = always_redraw(lambda: DashedLine(
            start=moving_dot_circle.get_center(),
            end=[moving_dot_circle.get_center()[0] + 6, moving_dot_circle.get_center()[1], 0],
            color=GRAY
        ))
        self.play(Create(horizontal_line))

        # Moving dot on the sine curve
        moving_dot_curve = Dot(color=RED)
        moving_dot_curve.add_updater(lambda d: d.move_to(
            axes.c2p(
                angle_tracker.get_value(),
                np.sin(angle_tracker.get_value())
            )
        ))
        self.play(Create(moving_dot_curve))

        # Vertical line from the moving dot on the sine curve to the x-axis
        vert_line_curve = always_redraw(lambda: DashedLine(
            start=moving_dot_curve.get_center(),
            end=[moving_dot_curve.get_center()[0], axes.c2p(angle_tracker.get_value(), 0)[1], 0],
            color=GRAY
        ))
        self.play(Create(vert_line_curve))

        # Update function for the moving dot on the circle
        def update_moving_dot_circle(dot):
            new_point = circle.point_at_angle(angle_tracker.get_value())
            dot.move_to(new_point)
        moving_dot_circle.add_updater(update_moving_dot_circle)

        # Animate the angle change
        self.play(angle_tracker.animate.set_value(TAU), run_time=10, rate_func=linear)

        # Clean up updaters
        moving_dot_circle.clear_updaters()
        moving_dot_curve.clear_updaters()

        self.wait()

# Run the scene
if __name__ == "__main__":
    from manim import config
    config.media_width = "75%"
    scene = SineFunctionExplanation_1o()
    scene.render()