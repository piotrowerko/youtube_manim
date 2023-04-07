#  https://docs.manim.community/en/stable/examples.html
#  manim -pql anim_pio1.py SineCurveUnitCircle
# highier quality: 
# manim -p anim_pio1.py PointMovingOnShapes

# Tutorial:
#  https://www.youtube.com/watch?v=KHGoFDB-raE&ab_channel=BrianAmedee
# latech tutorial
# https://www.overleaf.com/learn/latex/Subscripts_and_superscripts
# https://docs.devtaoism.com/docs/html/contents/_2_basic_mobjects.html

# manim -p force_reactions.py Beam
# manim -pql force_reactions.py Beam

# colors = [DARK_BROWN, BLUE_E, BLUE_D, BLUE_A, TEAL_B, GREEN_B, YELLOW_E]

from manim import *
import numpy as np


class Beam(Scene):
    def construct(self):
        x_init1 = -5
        x_init2 = 5
        r_t = 0.5
        beam = self._draw_line(x_init1, x_init2, stroke_width=20)
        self.wait()
        self.play(GrowFromCenter(beam),run_time=r_t)
        self.wait()
        tria_1, tria_2, slide = self._add_supports(x_init1, x_init2)
        self.play(GrowFromEdge(tria_1, UP), 
                  GrowFromEdge(tria_2, UP), 
                  GrowFromCenter(slide), run_time=r_t)
        force_load = Arrow(np.array([-1, 3.5, 0]), 
                           np.array([-1, 1.8, 0]), 
                           color=GOLD, 
                           max_stroke_width_to_length_ratio=5)
        self.play(GrowArrow(force_load), run_time=r_t)
        reactions = self._add_reactions(x_init1, x_init2)
        for i in reactions:
            self.play(GrowArrow(i), run_time=r_t)
        self.wait()
        react_labels = self._add_react_labels(x_init1, x_init2)
        for i in react_labels:
            self.play(Write(i)) 
        
        balance_condision_1, calc_rah = self._add_balance_condisions()
        self.play(Write(balance_condision_1)) 
        self.play(Write(calc_rah)) 
        self.play(FadeOut(balance_condision_1, shift=DOWN))

    def _draw_line(self, x1, x2, stroke_width=5):
        x_start = np.array([x1, 2, 0])
        x_end = np.array([x2, 2, 0])
        beam = Line(x_start, x_end, stroke_width=stroke_width)
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
        slide = self._draw_line(x_end[0] - 0.5, x_end[0] + 0.5)
        slide.shift(vector)
        return tria_1, tria_2, slide
    
    def _add_reactions(self, x1, x2):
        vert_reaction_a = Arrow(np.array([x1, 0, 0]), 
                                np.array([x1, 1.4, 0]), 
                                color=RED,
                                max_stroke_width_to_length_ratio=5)
        vert_reaction_b = Arrow(np.array([x2, 0, 0]), 
                                np.array([x2, 1.2, 0]), 
                                color=RED,
                                max_stroke_width_to_length_ratio=7)
        horiz_reaction_a = Arrow(np.array([x1-1.5, 2, 0]), 
                                np.array([x1, 2, 0]), 
                                color=RED,
                                max_stroke_width_to_length_ratio=5)
        return vert_reaction_a, vert_reaction_b, horiz_reaction_a
    
    # def _add_formula(self):
    #     equation = MathTex(
    #         r"e^x = x^0 + x^1 + \frac{1}{2} x^2 + \frac{1}{6} x^3 + \cdots + \frac{1}{n!} x^n + \cdots",
    #     )
    #     equation.set_color_by_tex("x", YELLOW)
    #     return equation
    def _add_react_labels(self, x1, x2, *args):
        x_start = np.array([x1, -0.1, 0])
        x_end = np.array([x2, -0.1, 0])
        rah_vector = np.array([-1.75, 2.1, 0])
        r_a_v = MathTex(r"R_A^V", color=YELLOW)
        r_a_v.move_to(x_start)
        r_b_v = MathTex(r"R_B^V", color=YELLOW)
        r_b_v.move_to(x_end)
        r_a_h = MathTex(r"R_A^H", color=YELLOW)
        r_a_h.move_to(x_start+rah_vector)
        return r_a_v, r_b_v, r_a_h
    
    def _add_balance_condisions(self):
        balance_condision_1 = MathTex(r"\sum_{i=1}^{n} F_i^{Hor} = 0", color=BLUE_A)
        calc_rah = MathTex(r"R_A^H - 0 = 0 => R_A^H = 0 [kN]", color=BLUE_A).move_to([0,-1,0])
        return balance_condision_1, calc_rah
        
        

def main():
    my_scene = Beam()
    my_scene.construct()


if __name__ == '__main__':
    main()
    
