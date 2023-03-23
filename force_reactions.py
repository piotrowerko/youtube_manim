#  https://docs.manim.community/en/stable/examples.html
#  manim -pql anim_pio1.py SineCurveUnitCircle
# highier quality: 
# manim -p anim_pio1.py PointMovingOnShapes

# Tutorial:
#  https://www.youtube.com/watch?v=KHGoFDB-raE&ab_channel=BrianAmedee

from manim import *

class Beam(Scene):
    def construct(self):
        #self._show_beam(-2, 2)
        x_init1 = -5
        x_init2 = 5
        beam = self._show_beam(x_init1, x_init2)
        #self.play(GrowFromCenter(beam), runtime=0.02)
        self.wait()
        self.play(GrowFromCenter(beam),run_time=3)
        self.wait()
        triangle_1 = self._add_supports(x_init1, x_init2)
        self.play(GrowFromCenter(triangle_1),run_time=3)
        self.wait()

    def _show_beam(self, x1, x2):
        x_start = np.array([x1, 2, 0])
        x_end = np.array([x2, 2, 0])
        beam = Line(x_start, x_end)
        return beam
        #self.add(beam)
    
    def _add_supports(self, x1, x2):
        x_start = np.array([x1, 2, 0])
        x_end = np.array([x2, 2, 0])
        triangle_1 = Triangle().scale(0.5)
        triangle_1.move_to(x_start, UP)
        #triangle_1.scale(0.5)

        return triangle_1   
        

def main():
    pass


if __name__ == '__main__':
    main()
    
