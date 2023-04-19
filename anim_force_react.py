#  https://docs.manim.community/en/stable/examples.html
#  manim -pql anim_pio1.py SineCurveUnitCircle
# highier quality: 
# manim -p anim_pio1.py PointMovingOnShapes

# Tutorial:
#  https://www.youtube.com/watch?v=KHGoFDB-raE&ab_channel=BrianAmedee
# latech tutorial
# https://www.overleaf.com/learn/latex/Subscripts_and_superscripts
# https://docs.devtaoism.com/docs/html/contents/_2_basic_mobjects.html

# manim -p anim_force_react.py AnimBeam
# manim -pql anim_force_react.py AnimBeam

# colors = [DARK_BROWN, BLUE_E, BLUE_D, BLUE_A, TEAL_B, GREEN_B, YELLOW_E]

import numpy as np
from manim import *
from manim.mobject.geometry.tips import ArrowTriangleTip,\
                                        ArrowSquareTip, ArrowSquareFilledTip,\
                                        ArrowCircleTip, ArrowCircleFilledTip

from beam import Beam


class AnimBeam(Scene):
    
    STARTING_Y = 2.0
    BEAM_LENGTH = 10.0
    IN_REL_LO_POS = - 0.10
    ANIM_TIME = 2
    
    def construct(self):
        x_init1 = np.array([- AnimBeam.BEAM_LENGTH / 2, AnimBeam.STARTING_Y, 0])
        x_init2 = np.array([+ AnimBeam.BEAM_LENGTH / 2, AnimBeam.STARTING_Y, 0])
        load_array = np.array([AnimBeam.BEAM_LENGTH * AnimBeam.IN_REL_LO_POS, AnimBeam.STARTING_Y, 0])  # hor. pos., vert pos. of tip, z value
        load_arrow_height = np.array([0, 2, 0])
        r_t = AnimBeam.ANIM_TIME
        
        # draw_beam:
        data_for_beam = {'x1': x_init1,
                         'x2': x_init2,
                         'stroke_width': 20}
        beam = self._draw_line2(**data_for_beam)
        self.wait()
        self.play(GrowFromCenter(beam),run_time=r_t)
        self.wait()
        
        # add supports:
        tria_1, tria_2, slide = self._add_supports(x_init1, x_init2)
        self.play(GrowFromEdge(tria_1, UP), 
                  GrowFromEdge(tria_2, UP), 
                  GrowFromCenter(slide), 
                  run_time=r_t)
        
        # animate force load:
        force_load, load_value = self._add_force_load(load_array, load_arrow_height)
        self.play(GrowArrow(force_load), 
                  Write(load_value),
                  run_time=r_t)
        
        # add dimensions:
        dimensions = self._add_dimensions(x_init1, x_init2, load_array)
        dim_anims = [GrowFromCenter(i) for i in dimensions]
        dimensions_anim = AnimationGroup(*dim_anims)   
        self.play(dimensions_anim, run_time=r_t)
        self.wait()
        
        # add dimensions descriptions:
        dim_l, on_screen_dim_l, dim_r, on_screen_dim_r = self._add_dims_descrip()
        self.play(Write(on_screen_dim_l))
        self.play(Write(on_screen_dim_r))  
        
        # animate static reactions:
        reactions = self._add_reactions(x_init1, x_init2, load_arrow_height)
        for i in reactions[:2]:
            self.play(GrowArrow(i), run_time=r_t)
        self.wait()
        react_labels = self._add_react_labels(x_init1, x_init2)
        for i in react_labels[:2]:
            self.play(Write(i)) 
        
        # add second horizontal line:
        data_for_h2 = {'x1': x_init1-np.array([0, 3, 0]),
                       'x2': x_init2-np.array([0, 3, 0]),
                       'stroke_width': 5}
        h2 = self._draw_line2(**data_for_h2)
        self.wait()
        self.play(GrowFromCenter(h2), run_time=r_t)
        self.wait()
        
        # add supports:
        tria_1_, tria_2_, slide_ = self._add_supports(x_init1-np.array([0, 3, 0]), 
                                                   x_init2-np.array([0, 3, 0]))
        self.play(GrowFromEdge(tria_1_, UP), 
                  GrowFromEdge(tria_2_, UP), 
                  GrowFromCenter(slide_), 
                  run_time=r_t)
        
        # support displacement and rotation
        angl_line = h2.copy()
        rot = Rotate(angl_line,
               angle=0.099,
               about_point=np.array([AnimBeam.BEAM_LENGTH / 2, AnimBeam.STARTING_Y - 3, 0]),
               rate_func=linear)
        self.play(tria_1_.animate.shift([0,-1,0]))
        self.play(rot, run_time=r_t)
        
        # add brace for vertical displacement denotation:
        data_for_vert_line = {'x1': x_init1-np.array([0, 3, 0]),
                              'x2': x_init1-np.array([0, 4, 0]),
                              'stroke_width': 2,
                              'color': ORANGE}
        vert_line = self._draw_line2(**data_for_vert_line)
        self.wait()
        self.play(GrowFromCenter(vert_line), run_time=r_t)
        self.wait()
        vert_brace = Brace(vert_line, direction=np.array([-1., 0., 0.]))
        vert_brace_txt = vert_brace.get_text("100\%")
        brace_all = VGroup(vert_brace, vert_brace_txt)
        self.play(brace_all.animate(), run_time=r_t)
        self.wait()
        
       # adding load reference line
        data_ref_load_line = {'x1': load_array,
                              'x2': load_array-np.array([0, 4, 0]),
                              'stroke_width': 2,
                              'color': ORANGE}
        ref_load_line = self._draw_line2(**data_ref_load_line)
        self.wait()
        self.play(GrowFromPoint(ref_load_line, load_array), run_time=r_t)
        
        # shortening the reference line
        local_height_l, local_height_r = self._compute_tria_height(load_array[0])
        ref_load_line2 = ref_load_line.copy()
        ref_load_line2.put_start_and_end_on(load_array - np.array([0, 3, 0]), 
                                           load_array - np.array([0, 3+local_height_l, 0]))
        self.play(ReplacementTransform(ref_load_line, ref_load_line2))
        self.wait()
        
        # adding braces to the intermediate line:
        vert_brace2 = Brace(ref_load_line2, direction=np.array([-1., 0., 0.]))
        a = format(local_height_l * 100, '.0f')
        txt_height = f'{a}\%'
        vert_brace_txt2 = vert_brace2.get_text(txt_height)
        brace_all = VGroup(vert_brace2, vert_brace_txt2)
        self.play(brace_all.animate(), run_time=r_t)
        self.wait()


        # DECIMAL UPDATER
        # https://docs.manim.community/en/stable/reference/manim.mobject.text.numbers.DecimalNumber.html
        
        
    def _compute_tria_height(self, hor):
        local_height_l = (-hor + 0.5 * AnimBeam.BEAM_LENGTH) / AnimBeam.BEAM_LENGTH
        local_height_r = 1 - local_height_l
        return local_height_l, local_height_r
      
    def _add_dims_descrip(self):
        dim_l = AnimBeam.BEAM_LENGTH * (0.5 + AnimBeam.IN_REL_LO_POS)
        dim_r = AnimBeam.BEAM_LENGTH * (0.5 - AnimBeam.IN_REL_LO_POS)
        #on_screen_dim_l = Variable(dim_l, Text(""), num_decimal_places=3)
        on_screen_dim_l = DecimalNumber(dim_l, 
                                        num_decimal_places=1, 
                                        include_sign=False, 
                                        unit=r"_{\phantom[~~[m]}")
        on_screen_dim_r = DecimalNumber(dim_r, 
                                        num_decimal_places=1, 
                                        include_sign=False, 
                                        unit=r"_{\phantom[~~[m]}")
        on_screen_dim_l.move_to(np.array([(-0.3 * AnimBeam.BEAM_LENGTH), AnimBeam.STARTING_Y - 1.0, 0]))
        on_screen_dim_r.move_to(np.array([(0.3 * AnimBeam.BEAM_LENGTH), AnimBeam.STARTING_Y - 1.0, 0]))
        return dim_l, on_screen_dim_l, dim_r, on_screen_dim_r
        
    # def _compute_reactions(self, force_placement:'float') -> 'tuple':
    #     belka_1 = Beam(0, [0, force_placement, force_placement], 0)  # cantilevel im, inner dims between point forces, catil. dim (right)
    #     belka_1.compute_reactions([0, 0, -10, 0])  # values of external point forces
    #     return belka_1.Ra, belka_1.Rb
    
    def _add_force_load(self, load_array, load_arrow_height):
        force_load = Arrow(load_array+load_arrow_height, 
                    load_array+np.array([0, 0.1, 0]), 
                    color=YELLOW, 
                    buff=0.1,
                    max_stroke_width_to_length_ratio=5)
        load_value = MathTex(r"10~[kN]", color=YELLOW)
        load_value.move_to(load_array+load_arrow_height / 1.50 + np.array([1, 0, 0]))
        return force_load, load_value
    
    def _add_crossing_line(self, x_init1, run_time):
        # cross over the Rah:
        data_for_first_crossing_line = {'x1': x_init1-np.array([2,0,0]),
                                        'x2': x_init1-np.array([0.2,0,0]),
                                        'stroke_width': 10,
                                        'color': YELLOW_E}
        crs_line1 = self._draw_line2(**data_for_first_crossing_line)
        return crs_line1
        
        
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
        slide = self._draw_line2(x_end + np.array([-0.5,0,0]), 
                                 x_end + np.array([0.5,0,0]), 
                                 stroke_width=5,
                                 color=BLUE)
        slide.shift(vector)
        return tria_1, tria_2, slide
    
    def _add_reactions(self, x1, x2, load_array_begin):
        vert_val_rav = load_array_begin[1]
        hor_pos_of_load = 5 + load_array_begin[0]
        beam_length = x2[0] - x1[0]
        off_set_a = 0.9
        off_set_b = 1.3
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
        shift_1 = np.array([-0.75,-1.5,0])
        shift_2 = np.array([0.75,-1.5,0])
        x_start = x1 + shift_1
        x_end = x2 + shift_2
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
        
        adit_line_v_a = adit_line_v.copy()
        adit_line_v_a.shift(np.array([- AnimBeam.BEAM_LENGTH * (0.5 + AnimBeam.IN_REL_LO_POS), 0, 0]))
        
        adit_line_v_b = adit_line_v_a.copy()
        adit_line_v_b.shift(np.array([AnimBeam.BEAM_LENGTH, 0, 0]))
        
        dimensions = (dim_line1, 
                      adit_line_1a, 
                      adit_line_1b, 
                      adit_line_v, 
                      adit_line_2b,
                      adit_line_v_a,
                      adit_line_v_b)
        
        return dimensions
        
    def _moving_load_anim(self, dimensions):
        pass
    
    
    
    def construct2(self):
        x_init1 = np.array([- AnimBeam.BEAM_LENGTH / 2, AnimBeam.STARTING_Y, 0])
        x_init2 = np.array([+ AnimBeam.BEAM_LENGTH / 2, AnimBeam.STARTING_Y, 0])
        load_array = np.array([- AnimBeam.BEAM_LENGTH * 0.1, AnimBeam.STARTING_Y, 0])  # hor. pos., vert pos. of tip, z value
        load_arrow_height = np.array([0, 2, 0])
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
        force_load = self._add_force_load(load_array, load_arrow_height)
        self.play(GrowArrow(force_load), run_time=r_t)
        
        # animate reactions:
        reactions = self._add_reactions(x_init1, x_init2, load_arrow_height)
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
        
        # cross over the Rah and fade out:
        crs_line1 = self._add_crossing_line(x_init1=x_init1,run_time=r_t)
        self.play(GrowFromCenter(crs_line1), run_time=r_t)
        self.play(FadeOut(balance_condision_1, 
                          crs_line1,
                          react_labels[2],
                          reactions[2],
                          shift=DOWN))
        
        # add dimensions:
        dimensions = self._add_dimensions(x_init1, x_init2, load_array)
        dim_anims = [GrowFromCenter(i) for i in dimensions]
        dimensions_anim = AnimationGroup(*dim_anims)   
        self.play(dimensions_anim, run_time=r_t)
        self.wait()
        
        # move load and central dimension horizontally:
        moving_part_hor = VGroup(force_load, 
                                 dimensions[2], 
                                 dimensions[3])
        self.play(moving_part_hor.animate.shift([6,0,0]))
        self.wait()
        self.play(moving_part_hor.animate.shift([-10,0,0]))
        self.wait()
        self.play(moving_part_hor.animate.shift([5,0,0]))
        self.wait()
        
        # add consecutive reactions decryptions:
        var = 0.5
        on_screen_var = Variable(var, Text("var"), num_decimal_places=3)
        self.play(Write(on_screen_var))
        self.wait()
        var_tracker = on_screen_var.tracker
        var = 10.5
        self.play(var_tracker.animate.set_value(var))
        self.wait()
    

def main():
    my_scene = AnimBeam()
    my_scene.construct()


if __name__ == '__main__':
    main()
    
