from manim import *

# Define the scene
class SineFunctionExplanation(Scene):
    def construct(self):
        # Title
        title = Text("Understanding the Sine Function")
        self.play(Write(title))
        self.wait(1)
        self.play(FadeOut(title))
        
        # Create unit circle
        unit_circle = Circle(radius=2).set_color(BLUE)
        center = Dot(ORIGIN)
        self.play(Create(unit_circle), FadeIn(center))
        
        # Axes for the sine wave
        axes = Axes(
            x_range=[0, TAU, PI / 4],
            y_range=[-1.5, 1.5, 0.5],
            axis_config={"color": WHITE},
            tips=False
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="sin(x)")
        
        # Draw axes for sine wave
        self.play(Create(axes), Write(axes_labels))
        
        # Create a dot that moves along the unit circle
        moving_dot = Dot([2, 0, 0], radius=0.08, color=YELLOW)  # Start on the unit circle at (2, 0)
        radius_line = always_redraw(lambda: Line(center.get_center(), moving_dot.get_center(), color=GREEN))
        
        # Angle arc - avoid drawing when the lines are parallel
        angle_arc = always_redraw(
            lambda: Angle(
                Line(ORIGIN, RIGHT), 
                Line(ORIGIN, moving_dot.get_center()), 
                radius=0.5, color=WHITE
            ) if moving_dot.get_center()[1] != 0 else VGroup()
        )
        angle_label = always_redraw(lambda: MathTex(r"\theta").next_to(angle_arc, RIGHT))

        # Y-axis projection line for sine
        projection_line = always_redraw(lambda: DashedLine(moving_dot.get_center(), [moving_dot.get_x(), 0, 0], color=YELLOW))
        y_value_label = always_redraw(lambda: MathTex(r"\sin(\theta)").next_to(moving_dot, UP))

        # Create a parametric function for sine wave
        sine_wave = axes.plot(lambda x: np.sin(x), color=RED, x_range=[0, TAU])

        # Function that moves the dot around the unit circle and traces the sine curve
        def update_moving_dot(mob, dt):
            mob.rotate(dt * PI / 4, about_point=ORIGIN)  # Rotate the dot over time
            return mob

        moving_dot.add_updater(update_moving_dot)
        
        # Adding the moving dot and its elements to the scene
        self.play(FadeIn(moving_dot), Create(radius_line), Create(angle_arc), Write(angle_label), Create(projection_line), Write(y_value_label))

        # Plot the sine curve and add the graph
        self.play(Create(sine_wave))

        # Let the animation run for a while before concluding
        self.wait(5)  

        # Clear everything
        self.play(FadeOut(moving_dot), FadeOut(radius_line), FadeOut(projection_line), FadeOut(y_value_label), FadeOut(unit_circle), FadeOut(sine_wave), FadeOut(axes), FadeOut(axes_labels))

        # End message
        conclusion = Text("The sine of an angle is the y-coordinate of a point on the unit circle.")
        self.play(Write(conclusion))
        self.wait(3)

# Run the scene
if __name__ == "__main__":
    from manim import config
    config.media_width = "75%"
    scene = SineFunctionExplanation()
    scene.render()
