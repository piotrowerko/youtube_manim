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
from manim.mobject.geometry.tips import ArrowTriangleTip,\
                                        ArrowSquareTip, ArrowSquareFilledTip,\
                                        ArrowCircleTip, ArrowCircleFilledTip
import numpy as np


class Beam(Scene):
    def construct(self):
        x_init1 = np.array([-5,2,0])
        x_init2 = np.array([5,2,0])
        load_array = np.array([-1,2,0])
        load_array_begin = np.array([0, 1.9, 0])
        r_t = 0.5
        
        # draw_beam:
        data_for_beam = {'x1': x_init1,
                         'x2': x_init2,
                         'stroke_width': 20}
        beam = self._draw_line2(**data_for_beam)
        self.wait()
        self.play(GrowFromCenter(beam),run_time=r_t)
        self.wait()
        tria_1, tria_2, slide = self._add_supports(x_init1, x_init2)
        self.play(GrowFromEdge(tria_1, UP), 
                  GrowFromEdge(tria_2, UP), 
                  GrowFromCenter(slide), run_time=r_t)
        
        # animate force load:
        force_load = Arrow(load_array+load_array_begin, 
                           load_array+np.array([0, 0.1, 0]), 
                           color=GOLD, 
                           buff=0.1,
                           max_stroke_width_to_length_ratio=5)
        self.play(GrowArrow(force_load), run_time=r_t)
        
        # animate reactions:
        reactions = self._add_reactions(x_init1, x_init2, load_array_begin)
        for i in reactions:
            self.play(GrowArrow(i), run_time=r_t)
        self.wait()
        react_labels = self._add_react_labels(x_init1, x_init2)
        for i in react_labels:
            self.play(Write(i)) 
        
        # play horisontal eqations:
        balance_condision_1, calc_rah = self._add_balance_condisions()
        self.play(Write(balance_condision_1)) 
        self.play(Write(calc_rah))
        #self.play(FadeOut(balance_condision_1, shift=DOWN))
        hor_eqs = VGroup(balance_condision_1, calc_rah)
        self.play(hor_eqs.animate.shift([-4,-2,0]).scale(0.6))
        
        # cross over the Rah:
        self._add_crossing_line(x_init1=x_init1,run_time=r_t)
        
        # add dimensions:
        dimensions = self._add_dimensions(x_init1, x_init2, load_array)
        dim_anims = [GrowFromCenter(i) for i in dimensions]
        dimensions_anim = AnimationGroup(*dim_anims)   
        self.play(dimensions_anim, run_time=r_t)
        self.wait()
        
        # move load horizontally:
        moving_part_hor = VGroup(force_load, 
                                 dimensions[2], 
                                 dimensions[3])
        self.play(moving_part_hor.animate.shift([6,0,0]))
        self.wait()
        self.play(moving_part_hor.animate.shift([-10,0,0]))
        self.wait()
        self.play(moving_part_hor.animate.shift([5,0,0]))
        self.wait()
        
    def _add_crossing_line(self, x_init1, run_time):
        # cross over the Rah:
        data_for_first_crossing_line = {'x1': x_init1-np.array([2,0,0]),
                                        'x2': x_init1-np.array([0.2,0,0]),
                                        'stroke_width': 10,
                                        'color': YELLOW_E}
        crs_line1 = self._draw_line2(**data_for_first_crossing_line)
        self.play(GrowFromCenter(crs_line1),run_time=run_time)
        
    def _draw_line2(self, x1, x2, **kwargs):
        x_start = x1
        x_end = x2
        try:
            color = kwargs['color']
        except KeyError:
            color = 'WHITE'
        beam = Line(x_start, x_end, 
                    stroke_width=kwargs['stroke_width'], 
                    color=color)
        return beam
    
    def _add_supports(self, x1, x2):
        x_start = x1
        x_end = x2
        tria_1 = Triangle().scale(0.5)
        tria_2 = Triangle().scale(0.5)
        tria_1.move_to(x_start, UP)
        tria_2.move_to(x_end, UP)
        vector = np.array([0,-0.9,0])
        slide = self._draw_line2(x_end + np.array([-0.5,0,0]), x_end + np.array([0.5,0,0]), stroke_width=5)
        slide.shift(vector)
        return tria_1, tria_2, slide
    
    def _add_reactions(self, x1, x2, load_array_begin):
        vert_val_rav = load_array_begin[1]
        hor_pos_of_load = 5 + load_array_begin[0]
        beam_length = x2[0] - x1[0]
        off_set_a = 0.6
        off_set_b = 0.9
        shift_1 = np.array([0, -vert_val_rav * (hor_pos_of_load / beam_length)-off_set_a, 0])
        shift_2 = np.array([0, -off_set_a, 0])
        shift_3 = np.array([0,-0.9,0])
        shift_4 = np.array([-1.5,0,0])
        vert_reaction_a = Arrow(x1+shift_1, 
                                x1+shift_2, 
                                color=RED,
                                buff=0,
                                max_stroke_width_to_length_ratio=5)
        vert_reaction_b = Arrow(x2+shift_1, 
                                x2+shift_3, 
                                color=RED,
                                buff=0,
                                max_stroke_width_to_length_ratio=7)
        horiz_reaction_a = Arrow(x1+shift_4, 
                                x1, 
                                color=RED,
                                buff=0,
                                max_stroke_width_to_length_ratio=5)
        return vert_reaction_a, vert_reaction_b, horiz_reaction_a
    
    def _add_react_labels(self, x1, x2, *args):
        shift_1 = np.array([0,-2.1,0])
        x_start = x1 + shift_1
        x_end = x2 + shift_1
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
    
    def _add_dimensions(self, x1, x2, load_array):
        shift_dim_down = np.array([0,-1.5,0])
        slight_mod_of_tips = np.array([0.1,0.1,0])
        vert_mod_of_tips = np.array([0,0.2,0])
        
        data_for_first_dim_line = {'x1': x1+shift_dim_down,
                                   'x2': x2+shift_dim_down,
                                   'stroke_width': 4,
                                   'color': YELLOW_A}
        data_for_addit_1a = {'x1': x1-slight_mod_of_tips+shift_dim_down,
                             'x2': x1+slight_mod_of_tips+shift_dim_down,
                             'stroke_width': 4,
                             'color': YELLOW_A}
        dim_line1 = self._draw_line2(**data_for_first_dim_line)
        adit_line_1a = self._draw_line2(**data_for_addit_1a)
        adit_line_1b = adit_line_1a.copy()
        adit_line_1b.move_to(load_array+shift_dim_down)
        
        data_for_addit_v = {'x1': load_array + vert_mod_of_tips * 2 + shift_dim_down,
                            'x2': load_array - vert_mod_of_tips + shift_dim_down,
                            'stroke_width': 2,
                            'color': YELLOW_A}
        adit_line_v = self._draw_line2(**data_for_addit_v)
        
        adit_line_2b = adit_line_1b.copy()
        adit_line_2b.move_to(x2+shift_dim_down)
        
        dimensions = (dim_line1, 
                      adit_line_1a, 
                      adit_line_1b, 
                      adit_line_v, 
                      adit_line_2b)
        
        return dimensions
        
    def _moving_load_anim(self, dimensions):
        pass

def main():
    my_scene = Beam()
    my_scene.construct()


if __name__ == '__main__':
    main()
    
