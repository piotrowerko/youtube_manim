#  https://docs.manim.community/en/stable/examples.html
#  manim -pql anim_pio1.py SineCurveUnitCircle
# highier quality: 
# manim -p anim_pio1.py PointMovingOnShapes

# Tutorial:
#  https://www.youtube.com/watch?v=KHGoFDB-raE&ab_channel=BrianAmedee

# manim -p force_reactions.py Beam

from manim import *
import numpy as np


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
        tria_1, tria_2, slide = self._add_supports(x_init1, x_init2)
        self.play(GrowFromEdge(tria_1, UP), 
                  GrowFromEdge(tria_2, UP), 
                  GrowFromCenter(slide), run_time=3)
        #self.play(GrowFromCenter(tria_2),run_time=3)
        self.wait()

    def _show_beam(self, x1, x2, *args):
        x_start = np.array([x1, 2, 0])
        x_end = np.array([x2, 2, 0])
        beam = Line(x_start, x_end)
        return beam
        #self.add(beam)
    
    def _add_supports(self, x1, x2):
        x_start = np.array([x1, 2, 0])
        x_end = np.array([x2, 2, 0])
        tria_1 = Triangle().scale(0.5)
        tria_2 = Triangle().scale(0.5)
        tria_1.move_to(x_start, UP)
        tria_2.move_to(x_end, UP)
        vector = np.array([0,-0.9,0])
        slide = self._show_beam(x_end[0] - 0.5, x_end[0] + 0.5)
        slide.shift(vector)
        return tria_1, tria_2, slide
        

def main():
    my_scene = Beam()
    my_scene.construct()


if __name__ == '__main__':
    main()
    
