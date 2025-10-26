from manim import *
import numpy as np

class MESStructureScene(Scene):
    """2‑D polygonal structure with distributed load, support, material properties and dimensions."""

    def construct(self):
        # ----- Basic scaling factors -----
        M_TO_UNIT = 0.77  # 1 m ⇒ 0.77 scene units (110% of original 0.7)
        ORIGIN_SHIFT = LEFT * 3 + DOWN * 2  # shift so geometry is centered on screen

        # ----- Geometry definition (in metres) -----
        raw_pts_m = [
            (0, 0), (2, 0), (2, 3), (4, 5), (2, 5), (0, 3), (0, 0)  # zamknięcie polygonu
        ]

        # Convert to manim Vec points (z=0) & shift
        pts = [
            ORIGIN_SHIFT + M_TO_UNIT * RIGHT * x + M_TO_UNIT * UP * y
            for x, y in raw_pts_m
        ]

        # ----- Draw structure polygon -----
        poly = Polygon(*pts, color=BLACK, stroke_width=4, fill_color=GREY, fill_opacity=0.5)
        self.play(Create(poly))

        # ----- Material info inside polygon -----
        mat_text = MathTex(r"E = 75\,\text{GPa}\\ \nu = 0.35\\ \text{gr} = 0.15\,\text{m}")
        mat_text.scale(0.5)
        # Place at better position inside structure (around point (1,2))
        mat_position = ORIGIN_SHIFT + M_TO_UNIT * RIGHT * 1.0 + M_TO_UNIT * UP * 2.0
        mat_text.move_to(mat_position)
        self.play(FadeIn(mat_text))

        # ----- Distributed load on the top edge (2;5) – (4;5) -----
        start_m = raw_pts_m[4]  # (2,5)
        end_m = raw_pts_m[3]    # (4,5)
        start = ORIGIN_SHIFT + M_TO_UNIT * RIGHT * start_m[0] + M_TO_UNIT * UP * start_m[1]
        end = ORIGIN_SHIFT + M_TO_UNIT * RIGHT * end_m[0] + M_TO_UNIT * UP * end_m[1]

        # Draw guiding line (invisible) for arrow placement
        guide_line = Line(start, end)
        n_arrows = 7
        arrows = VGroup()
        max_arrow_len = 1.0
        min_arrow_len = 0.5
        for i in range(n_arrows):
            # Avoid placing arrows exactly at the endpoints so the last one does not stick out
            edge_margin = 0.06
            t = edge_margin + (1 - 2 * edge_margin) * (i / (n_arrows - 1))
            base_point = guide_line.point_from_proportion(t)
            length = interpolate(max_arrow_len, min_arrow_len, t)
            # Strzałki kończą się dokładnie na górnej krawędzi struktury
            arr = Arrow(
                base_point + UP * length,  # zaczynają się powyżej
                base_point,  # kończą się dokładnie na krawędzi
                buff=0,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.25,
            )
            arrows.add(arr)
        self.play(LaggedStartMap(Create, arrows, lag_ratio=0.1))

        # Load magnitude labels
        label_left = MathTex(r"16\,\text{kN/m}").scale(0.75).next_to(arrows[0], LEFT, buff=0.2)
        label_right = MathTex(r"8\,\text{kN/m}").scale(0.75).next_to(arrows[-1], RIGHT, buff=0.2)
        self.play(FadeIn(label_left), FadeIn(label_right))

        # ----- Fixed support at the bottom edge (0;0) – (2;0) -----
        sup_start_m = raw_pts_m[0]
        sup_end_m = raw_pts_m[1]
        sup_start = ORIGIN_SHIFT + M_TO_UNIT * RIGHT * sup_start_m[0] + M_TO_UNIT * UP * sup_start_m[1]
        sup_end = ORIGIN_SHIFT + M_TO_UNIT * RIGHT * sup_end_m[0] + M_TO_UNIT * UP * sup_end_m[1]
        base_line = Line(sup_start, sup_end, color=BLACK, stroke_width=4)
        hatch = VGroup()
        hatch_spacing = 0.25
        n_hatch = int(base_line.get_length() / hatch_spacing)
        for i in range(n_hatch):
            pos = base_line.point_from_proportion(i / (n_hatch - 1))
            h = Line(pos, pos + DOWN * 0.4 + RIGHT * 0.4, stroke_width=3)
            hatch.add(h)
        self.play(Create(base_line), LaggedStartMap(Create, hatch, lag_ratio=0.05))

        # ----- Global coordinate system (2D continuum) -----
        # Position to the right of the main structure
        global_coord_origin = ORIGIN_SHIFT + RIGHT * 5.5 + UP * 1.5
        global_coord_scale = 1.5  # large coordinate system
        
        # X-axis (horizontal) - red L-shape with stub
        x_line_pos = Line(
            global_coord_origin,
            global_coord_origin + RIGHT * global_coord_scale * 0.9,
            stroke_width=6,
            color=RED
        )
        x_line_neg = Line(
            global_coord_origin,
            global_coord_origin + LEFT * global_coord_scale * 0.2,
            stroke_width=6,
            color=RED
        )
        x_arrowhead = Triangle(color=RED, fill_opacity=1.0).scale(0.1).move_to(global_coord_origin + RIGHT * global_coord_scale).rotate(-PI/2)
        
        # Y-axis (vertical) - red L-shape with stub
        y_line_pos = Line(
            global_coord_origin,
            global_coord_origin + UP * global_coord_scale * 0.9,
            stroke_width=6,
            color=RED
        )
        y_line_neg = Line(
            global_coord_origin,
            global_coord_origin + DOWN * global_coord_scale * 0.2,
            stroke_width=6,
            color=RED
        )
        y_arrowhead = Triangle(color=RED, fill_opacity=1.0).scale(0.1).move_to(global_coord_origin + UP * global_coord_scale)
        
        # Labels for global axes
        x_global_label = MathTex("X").scale(0.8).move_to(global_coord_origin + RIGHT * global_coord_scale + RIGHT * 0.2 + DOWN * 0.15)
        y_global_label = MathTex("Y").scale(0.8).move_to(global_coord_origin + UP * global_coord_scale + UP * 0.2 + LEFT * 0.15)
        
        # Group global coordinate system
        global_coord_system = VGroup(
            x_line_pos, x_line_neg, x_arrowhead,
            y_line_pos, y_line_neg, y_arrowhead,
            x_global_label, y_global_label
        )
        
        # Animate appearance of global coordinate system
        self.play(Create(global_coord_system))

        # ----- Dimensioning -----
        dims = VGroup()
        
        # Horizontal bottom dimension 2 m - dalej od struktury
        dim_bottom = DoubleArrow(
            ORIGIN_SHIFT + M_TO_UNIT * RIGHT * 0 + DOWN * 1.5,
            ORIGIN_SHIFT + M_TO_UNIT * RIGHT * 2 + DOWN * 1.5,
            buff=0.05,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.1
        )
        text_bottom = MathTex(r"2\,\text{m}").scale(0.7).next_to(dim_bottom, DOWN, buff=0.15)
        dims.add(dim_bottom, text_bottom)

        # Horizontal top extension dimension 2 m - dalej powyżej strzałek
        dim_top = DoubleArrow(
            start + UP * 1.5,
            end + UP * 1.5,
            buff=0.05,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.1
        )
        text_top = MathTex(r"2\,\text{m}").scale(0.7).next_to(dim_top, UP, buff=0.15)
        dims.add(dim_top, text_top)

        # Vertical left dimension 3 m - dalej na lewo
        dim_left = DoubleArrow(
            ORIGIN_SHIFT + M_TO_UNIT * RIGHT * (-0.8) + M_TO_UNIT * UP * 0,
            ORIGIN_SHIFT + M_TO_UNIT * RIGHT * (-0.8) + M_TO_UNIT * UP * 3,
            buff=0.05,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.1
        )
        text_left = MathTex(r"3\,\text{m}").scale(0.7).next_to(dim_left, LEFT, buff=0.15)
        dims.add(dim_left, text_left)

        # Vertical right dimension 2 m (from y=3 to y=5) - dalej na prawo
        x_offset = 1.0
        dim_right = DoubleArrow(
            ORIGIN_SHIFT + M_TO_UNIT * RIGHT * (4 + x_offset) + M_TO_UNIT * UP * 3,
            ORIGIN_SHIFT + M_TO_UNIT * RIGHT * (4 + x_offset) + M_TO_UNIT * UP * 5,
            buff=0.05,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.1
        )
        text_right = MathTex(r"2\,\text{m}").scale(0.7).next_to(dim_right, RIGHT, buff=0.15)
        dims.add(dim_right, text_right)

        # ----- Dashed extension lines connecting dimensions to the geometry -----
        extension_lines = VGroup()

        # Bottom (0,0)–(2,0) → dim_bottom (vertical dashed lines)
        y_bottom_dim = dim_bottom.get_start()[1]
        ext_b_left = DashedLine(
            sup_start,
            sup_start + (y_bottom_dim - sup_start[1]) * UP,
            dash_length=0.08,
            stroke_width=1,
        )
        ext_b_right = DashedLine(
            sup_end,
            sup_end + (y_bottom_dim - sup_end[1]) * UP,
            dash_length=0.08,
            stroke_width=1,
        )
        extension_lines.add(ext_b_left, ext_b_right)

        # Top (2,5)–(4,5) → dim_top (vertical dashed lines)
        y_top_dim = dim_top.get_start()[1]
        ext_t_left = DashedLine(
            start,
            start + (y_top_dim - start[1]) * UP,
            dash_length=0.08,
            stroke_width=1,
        )
        ext_t_right = DashedLine(
            end,
            end + (y_top_dim - end[1]) * UP,
            dash_length=0.08,
            stroke_width=1,
        )
        extension_lines.add(ext_t_left, ext_t_right)

        # Left vertical (x=0, y=0..3) → dim_left (horizontal dashed lines)
        x_left_dim = dim_left.get_start()[0]
        left_top_m = raw_pts_m[5]  # (0,3)
        p_left_bottom = sup_start  # (0,0)
        p_left_top = ORIGIN_SHIFT + M_TO_UNIT * RIGHT * left_top_m[0] + M_TO_UNIT * UP * left_top_m[1]
        ext_l_bottom = DashedLine(
            p_left_bottom,
            p_left_bottom + (x_left_dim - p_left_bottom[0]) * RIGHT,
            dash_length=0.08,
            stroke_width=1,
        )
        ext_l_top = DashedLine(
            p_left_top,
            p_left_top + (x_left_dim - p_left_top[0]) * RIGHT,
            dash_length=0.08,
            stroke_width=1,
        )
        extension_lines.add(ext_l_bottom, ext_l_top)

        # Right vertical (x=4, y=3..5) → dim_right (horizontal dashed lines)
        x_right_dim = dim_right.get_start()[0]
        p_right_bottom = ORIGIN_SHIFT + M_TO_UNIT * RIGHT * 4 + M_TO_UNIT * UP * 3
        p_right_top = end  # (4,5)
        ext_r_bottom = DashedLine(
            p_right_bottom,
            p_right_bottom + (x_right_dim - p_right_bottom[0]) * RIGHT,
            dash_length=0.08,
            stroke_width=1,
        )
        ext_r_top = DashedLine(
            p_right_top,
            p_right_top + (x_right_dim - p_right_top[0]) * RIGHT,
            dash_length=0.08,
            stroke_width=1,
        )
        extension_lines.add(ext_r_bottom, ext_r_top)

        # Show extension lines before the dimension arrows/texts
        self.play(LaggedStartMap(Create, extension_lines, lag_ratio=0.05))

        # Animuj linie wymiarowe i teksty osobno dla lepszej kontroli
        dimension_lines = VGroup()
        dimension_texts = VGroup()
        
        # Oddziel linie od tekstów
        for i in range(0, len(dims), 2):
            dimension_lines.add(dims[i])     # linie wymiarowe (indeksy parzyste)
        for i in range(1, len(dims), 2):
            dimension_texts.add(dims[i])     # teksty (indeksy nieparzyste)
        
        # Najpierw pokaż linie wymiarowe
        self.play(LaggedStartMap(Create, dimension_lines, lag_ratio=0.1))
        # Potem pokaż teksty z opisami
        self.play(LaggedStartMap(FadeIn, dimension_texts, lag_ratio=0.1))

        # wait for 10 seconds
        self.wait(10)

        # ----- Stage 2: minimize and move the whole drawing to top-left -----
        original_group = VGroup(
            poly,
            mat_text,
            arrows,
            label_left,
            label_right,
            base_line,
            hatch,
            dims,
            extension_lines,
        )

        # Fade out the global coordinate system before moving the main structure
        self.play(FadeOut(global_coord_system))

        self.play(
            original_group.animate
            .scale(0.65)
            .to_edge(UP, buff=0.3)
            .to_edge(LEFT, buff=0.3)
        )


        # ----- Stage 3: spawn a "clean" copy of the structure (no dims/loads), slightly to the right of original birth place -----
        NEW_ORIGIN_SHIFT = ORIGIN_SHIFT + RIGHT * 2.5 + UP * 0.4
        NEW_M_TO_UNIT = M_TO_UNIT * 1.1  # 10% larger
        new_pts = [
            NEW_ORIGIN_SHIFT + NEW_M_TO_UNIT * RIGHT * x + NEW_M_TO_UNIT * UP * y
            for x, y in raw_pts_m
        ]
        poly_clean = Polygon(
            *new_pts,
            color=BLUE_D,
            stroke_width=4,
            fill_color=BLUE_E,
            fill_opacity=0.0,
        )
        self.play(Create(poly_clean))

        # ----- Stage 3a: discretization into 3 finite elements on the clean structure -----
        def map_new(x: float, y: float):
            return NEW_ORIGIN_SHIFT + NEW_M_TO_UNIT * RIGHT * x + NEW_M_TO_UNIT * UP * y

        # Internal partition lines: (0,3)-(2,3) and (2,3)-(2,5)
        part_line_h = Line(map_new(0, 3), map_new(2, 3), color=RED, stroke_width=3)
        part_line_v = Line(map_new(2, 3), map_new(2, 5), color=RED, stroke_width=3)
        self.play(Create(VGroup(part_line_h, part_line_v)))

        # Element labels at centroids
        centroid_rect = map_new(1.0, 1.5)               # lower rectangle
        centroid_tri1 = map_new(4.0/3.0, 11.0/3.0)      # left top triangle
        centroid_tri2 = map_new(8.0/3.0, 13.0/3.0)      # right top triangle

        label_e1 = (
            MathTex(r"e.\ I").scale(0.5).stretch(0.85, 0).move_to(centroid_rect)
        )
        label_e2 = (
            MathTex(r"e.\ II").scale(0.5).stretch(0.85, 0).move_to(centroid_tri1)
        )
        label_e3 = (
            MathTex(r"e.\ III").scale(0.5).stretch(0.85, 0).move_to(centroid_tri2)
        )
        self.play(FadeIn(VGroup(label_e1, label_e2, label_e3)))

        # ----- Stage 3b: node numbering CCW starting at (2,0); labels outside the structure -----
        node_coords_m = [(2, 0), (2, 3), (4, 5), (2, 5), (0, 3), (0, 0)]
        node_points = [map_new(x, y) for (x, y) in node_coords_m]
        center_point = np.mean(np.array(node_points), axis=0)

        circles_with_labels = VGroup()
        offset_distance = 0.35
        circle_radius = 0.18
        for idx, p in enumerate(node_points, start=1):
            direction_vec = p - center_point
            norm = np.linalg.norm(direction_vec)
            unit = (direction_vec / norm) if norm > 1e-6 else np.array([1.0, 0.0, 0.0])
            target_pos = p + unit * offset_distance

            circ = Circle(
                radius=circle_radius,
                color=WHITE,
                stroke_width=2.5,
                fill_opacity=0.0,
            ).move_to(target_pos)

            # 10% smaller digits relative to previous (0.55 → 0.495)
            num_label = MathTex(str(idx)).scale(0.495).move_to(target_pos)

            # Special adjustment for node 2: shift downward and right to make room for DOF
            if idx == 2:
                temp = MathTex("2").scale(0.55)
                base_dy = 1.5 * temp.height
                extra_dx = 2.5 * temp.height  # moved further right to make room for DOF
                extra_dy = 0.3 * temp.height
                circ.shift(DOWN * (base_dy + extra_dy) + RIGHT * extra_dx)
                num_label.shift(DOWN * (base_dy + extra_dy) + RIGHT * extra_dx)
            
            # Special adjustment for node 3: shift right to make room for DOF
            if idx == 3:
                temp = MathTex("3").scale(0.55)
                extra_dx = 0.4 * temp.height  # shift right to avoid DOF
                circ.shift(RIGHT * extra_dx)
                num_label.shift(RIGHT * extra_dx)
            
            # Special adjustment for node 4: shift right to make room for DOF
            if idx == 4:
                temp = MathTex("4").scale(0.55)
                extra_dx = 2 * temp.height  # moved further right to avoid DOF
                circ.shift(RIGHT * extra_dx)
                num_label.shift(RIGHT * extra_dx)

            circles_with_labels.add(VGroup(circ, num_label))

        # Strictly sequential appearance: each node (circle, then digit) completes before next starts
        node_anims = []
        for group in circles_with_labels:
            circ, num_label = group
            node_anims.append(
                Succession(
                    Create(circ, run_time=0.6),
                    FadeIn(num_label, shift=0.1 * UP, run_time=0.4),
                )
            )
        self.play(Succession(*node_anims))

        # ----- Stage 3c: internal node numbering for each finite element -----
        internal_labels = VGroup()
        
        # Element 1 (rectangle): i=6, j=1, k=2, l=5 (CCW from bottom-left)
        # Place labels inside element 1, near corresponding global nodes
        elem1_i = MathTex("i").scale(0.52).move_to(map_new(0.2, 0.3))    # near global node 6 (0,0)
        elem1_j = MathTex("j").scale(0.52).move_to(map_new(1.6, 0.3))    # near global node 1 (2,0) - moved left to avoid Q1
        elem1_k = MathTex("k").scale(0.52).move_to(map_new(1.8, 2.7))    # near global node 2 (2,3)
        elem1_r = MathTex("r").scale(0.52).move_to(map_new(0.2, 2.7))    # near global node 5 (0,3)
        internal_labels.add(elem1_i, elem1_j, elem1_k, elem1_r)
        
        # Element 2 (left triangle): i=4, j=5, k=2 (CCW from bottom)
        # Place labels inside element 2, near corresponding global nodes
        elem2_i = MathTex("i").scale(0.52).move_to(map_new(1.8, 4.4))    # near global node 4 (2,5) - moved down
        elem2_j = MathTex("j").scale(0.52).move_to(map_new(0.6, 3.3))    # near global node 5 (0,3) - moved back left
        elem2_k = MathTex("k").scale(0.52).move_to(map_new(1.6, 3.3))    # near global node 2 (2,3) - moved left to avoid Q3
        internal_labels.add(elem2_i, elem2_j, elem2_k)
        
        # Element 3 (right triangle): i=2, j=3, k=4 (CCW from bottom-left)
        # Place labels inside element 3, near corresponding global nodes
        elem3_i = MathTex("i").scale(0.52).move_to(map_new(2.2, 3.5))    # near global node 2 (2,3) - moved down
        elem3_j = MathTex("j").scale(0.52).move_to(map_new(3.4, 4.7))    # near global node 3 (4,5) - moved right
        elem3_k = MathTex("k").scale(0.52).move_to(map_new(2.2, 4.7))    # near global node 4 (2,5)
        internal_labels.add(elem3_i, elem3_j, elem3_k)
        
        # Sequential appearance by alphabet within each element: elem1 (i,j,k,l) → elem2 (i,j,k) → elem3 (i,j,k)
        internal_anims = []
        
        # Element 1: i, j, k, l (alphabetical order)
        for label in [elem1_i, elem1_j, elem1_k, elem1_r]:
            internal_anims.append(
                AnimationGroup(
                    GrowFromCenter(label, run_time=0.6),
                    label.animate.scale(1.3).set_color(YELLOW)
                )
            )
            internal_anims.append(
                label.animate.scale(1/1.3).set_color(WHITE)
            )
        
        # Element 2: i, j, k (alphabetical order)
        for label in [elem2_i, elem2_j, elem2_k]:
            internal_anims.append(
                AnimationGroup(
                    GrowFromCenter(label, run_time=0.6),
                    label.animate.scale(1.3).set_color(YELLOW)
                )
            )
            internal_anims.append(
                label.animate.scale(1/1.3).set_color(WHITE)
            )
        
        # Element 3: i, j, k (alphabetical order)
        for label in [elem3_i, elem3_j, elem3_k]:
            internal_anims.append(
                AnimationGroup(
                    GrowFromCenter(label, run_time=0.6),
                    label.animate.scale(1.3).set_color(YELLOW)
                )
            )
            internal_anims.append(
                label.animate.scale(1/1.3).set_color(WHITE)
            )
        
        self.play(Succession(*internal_anims))

        # ----- Stage 3d: add degrees of freedom (DOF) coordinate systems at each node -----
        dof_systems = VGroup()
        
        # Node coordinates and their global DOF numbering (CCW from node 1)
        # Node 1: (2,0) -> Q1,Q2; Node 2: (2,3) -> Q3,Q4; Node 3: (4,5) -> Q5,Q6
        # Node 4: (2,5) -> Q7,Q8; Node 5: (0,3) -> Q9,Q10; Node 6: (0,0) -> Q11,Q12
        node_dof_data = [
            (2, 0, "Q_1", "Q_2"),    # Node 1
            (2, 3, "Q_3", "Q_4"),    # Node 2  
            (4, 5, "Q_5", "Q_6"),    # Node 3
            (2, 5, "Q_7", "Q_8"),    # Node 4
            (0, 3, "Q_9", "Q_{10}"), # Node 5
            (0, 0, "Q_{11}", "Q_{12}") # Node 6
        ]
        
        dof_scale = 0.2  # smaller than main coordinate system
        stub_length = dof_scale * 0.2  # small stubs
        
        for x, y, q_x, q_y in node_dof_data:
            node_pos = map_new(x, y)
            
            # X-axis (horizontal DOF) - white L-shape with stubs
            x_line_pos = Line(
                node_pos,
                node_pos + RIGHT * dof_scale * 0.9,
                stroke_width=2,
                color=WHITE
            )
            x_line_neg = Line(
                node_pos,
                node_pos + LEFT * stub_length,
                stroke_width=2,
                color=WHITE
            )
            x_arrowhead = Triangle(color=WHITE, fill_opacity=1.0).scale(0.03).move_to(node_pos + RIGHT * dof_scale).rotate(-PI/2)
            
            # Y-axis (vertical DOF) - white L-shape with stubs
            y_line_pos = Line(
                node_pos,
                node_pos + UP * dof_scale * 0.9,
                stroke_width=2,
                color=WHITE
            )
            y_line_neg = Line(
                node_pos,
                node_pos + DOWN * stub_length,
                stroke_width=2,
                color=WHITE
            )
            y_arrowhead = Triangle(color=WHITE, fill_opacity=1.0).scale(0.03).move_to(node_pos + UP * dof_scale)
            
            # Labels for DOFs
            x_label = MathTex(q_x).scale(0.40).move_to(node_pos + RIGHT * dof_scale + RIGHT * 0.1 + DOWN * 0.08)
            y_label = MathTex(q_y).scale(0.40).move_to(node_pos + UP * dof_scale + UP * 0.1 + LEFT * 0.15)
            
            # Group this node's DOF system
            node_dof = VGroup(
                x_line_pos, x_line_neg, x_arrowhead,
                y_line_pos, y_line_neg, y_arrowhead,
                x_label, y_label
            )
            dof_systems.add(node_dof)
        
        # Animate appearance of all DOF systems
        self.play(LaggedStartMap(FadeIn, dof_systems, lag_ratio=0.1))

        # wait for 6 seconds
        self.wait(10)

        # ----- Stage 4: minimize and move the discretized structure to top-right -----
        discretized_group = VGroup(
            poly_clean,
            part_line_h,
            part_line_v,
            label_e1,
            label_e2,
            label_e3,
            circles_with_labels,
            internal_labels,
            dof_systems,
        )

        self.play(
            discretized_group.animate
            .scale(0.75)
            .to_edge(UP, buff=0.3)
            .to_edge(RIGHT, buff=0.3)
        )

        # ----- Stage 5: extract element 1 copy from exact MES position to center -----
        # Create element 1 copy at the EXACT position within the discretized group
        # This means using the same positioning as the original element 1 in the MES structure
        
        # Element 1 copy - start exactly where element 1 is in the discretized structure
        elem1_pts_m = [(0, 0), (2, 0), (2, 3), (0, 3), (0, 0)]
        
        # Use the same mapping as the discretized structure, then apply the group transformations
        def map_elem1_birth(x: float, y: float):
            # Original position in NEW coordinate system
            pos = NEW_ORIGIN_SHIFT + NEW_M_TO_UNIT * RIGHT * x + NEW_M_TO_UNIT * UP * y
            # Apply the same transformations as discretized_group: scale 0.75, move to top-right
            pos = pos * 0.75
            pos += RIGHT * (config.frame_width/2 - 3.75) + UP * (config.frame_height/2 - 3.0)
            return pos
        
        # Create polygon at exact birth position
        elem1_birth_pts = [map_elem1_birth(x, y) for x, y in elem1_pts_m]
        elem1_copy_poly = Polygon(*elem1_birth_pts, color=BLUE_D, stroke_width=3, fill_opacity=0.0)
        
        # Create element label "e. I" at birth position - shifted right and up
        elem1_label_copy = (
            MathTex(r"e.\ I").scale(0.5 * 0.75).stretch(0.85, 0)
            .move_to(map_elem1_birth(1.4, 2.2))  # moved right and up from center
        )
        
        # Create global node labels at birth position
        elem1_global_nodes = [(0, 0, "6"), (2, 0, "1"), (2, 3, "2"), (0, 3, "5")]
        elem1_global_circles = VGroup()
        
        birth_offset_distance = 0.35 * 0.75
        birth_circle_radius = 0.18 * 0.75
        
        for x, y, num in elem1_global_nodes:
            node_pos = map_elem1_birth(x, y)
            elem_center = map_elem1_birth(1.0, 1.5)
            direction_vec = node_pos - elem_center
            norm = np.linalg.norm(direction_vec)
            unit = (direction_vec / norm) if norm > 1e-6 else np.array([1.0, 0.0, 0.0])
            target_pos = node_pos + unit * birth_offset_distance
            
            circ = Circle(radius=birth_circle_radius, color=WHITE, stroke_width=2.5, fill_opacity=0.0).move_to(target_pos)
            num_label = MathTex(num).scale(0.495 * 0.75).move_to(target_pos)
            
            # Special adjustments for syn_e1 global node labels
            if num == "1":  # Node 1 - move down a bit
                temp = MathTex("1").scale(0.495 * 0.75)
                extra_dy = 1 * temp.height
                circ.shift(DOWN * extra_dy)
                num_label.shift(DOWN * extra_dy)
            elif num == "2":  # Node 2 - move right
                temp = MathTex("2").scale(0.495 * 0.75)
                extra_dx = 1.5 * temp.height
                circ.shift(RIGHT * extra_dx)
                num_label.shift(RIGHT * extra_dx)
            elif num == "5":  # Node 5 - move left
                temp = MathTex("5").scale(0.495 * 0.75)
                extra_dx = -2.5 * temp.height
                circ.shift(RIGHT * extra_dx)
                num_label.shift(RIGHT * extra_dx)
            
            elem1_global_circles.add(VGroup(circ, num_label))
        
        # Create internal node labels at birth position  
        elem1_internal_copy = VGroup()
        elem1_i_copy = MathTex("i").scale(0.52 * 0.75).move_to(map_elem1_birth(0.2, 0.3))
        elem1_j_copy = MathTex("j").scale(0.52 * 0.75).move_to(map_elem1_birth(1.45, 0.3))  # moved minimally right
        elem1_k_copy = MathTex("k").scale(0.52 * 0.75).move_to(map_elem1_birth(1.8, 2.7))
        elem1_r_copy = MathTex("r").scale(0.52 * 0.75).move_to(map_elem1_birth(0.2, 2.6))  # moved back up
        elem1_internal_copy.add(elem1_i_copy, elem1_j_copy, elem1_k_copy, elem1_r_copy)
        
        # Group everything (without coordinate system initially)
        elem1_full_copy = VGroup(elem1_copy_poly, elem1_label_copy, elem1_global_circles, elem1_internal_copy)
        
        # First: appear at exact birth position 
        self.play(FadeIn(elem1_full_copy))
        
        # Second: move to center and scale up
        target_position = UP * 2.3  # closer to top edge
        target_scale = 1.2  # smaller, more reasonable size
        
        self.play(
            elem1_full_copy.animate
            .scale(target_scale)
            .move_to(target_position)
        )
        
        # Third: add coordinate system after positioning
        # Create L-shaped coordinate system at final position (center of syn_e1)
        coord_origin = target_position
        coord_scale = 0.3  # small coordinate system
        
        # X-axis (horizontal) - main line to positive direction + small stub to negative
        stub_length = coord_scale * 0.15  # small stub length
        x_line_positive = Line(
            coord_origin,
            coord_origin + RIGHT * coord_scale * 0.9,  # slightly shorter to make room for arrowhead
            stroke_width=4,
            color=RED
        )
        x_line_negative = Line(
            coord_origin,
            coord_origin + LEFT * stub_length,  # small stub in negative direction
            stroke_width=4,
            color=RED
        )
        x_arrowhead = Triangle(color=RED, fill_opacity=1.0).scale(0.05).move_to(coord_origin + RIGHT * coord_scale).rotate(-PI/2)
        x_axis = VGroup(x_line_positive, x_line_negative, x_arrowhead)
        x_label = MathTex("x_1").scale(0.4).move_to(coord_origin + RIGHT * coord_scale + RIGHT * 0.15 + DOWN * 0.12)
        
        # Y-axis (vertical) - main line to positive direction + small stub to negative
        y_line_positive = Line(
            coord_origin,
            coord_origin + UP * coord_scale * 0.9,  # slightly shorter to make room for arrowhead
            stroke_width=4,
            color=RED
        )
        y_line_negative = Line(
            coord_origin,
            coord_origin + DOWN * stub_length,  # small stub in negative direction
            stroke_width=4,
            color=RED
        )
        y_arrowhead = Triangle(color=RED, fill_opacity=1.0).scale(0.05).move_to(coord_origin + UP * coord_scale)
        y_axis = VGroup(y_line_positive, y_line_negative, y_arrowhead)
        y_label = MathTex("y_1").scale(0.4).move_to(coord_origin + UP * coord_scale + UP * 0.15 + LEFT * 0.12)
        
        coord_system = VGroup(x_axis, x_label, y_axis, y_label)
        
        # Animate appearance of coordinate system
        self.play(FadeIn(coord_system))
        
        # ----- Fourth: add DOF systems for syn_e1 nodes (nodes 6,1,2,5) -----
        syn_dof_systems = VGroup()
        
        # DOF data for syn_e1 nodes only (corresponding to element 1)
        # Use the same coordinate mapping as syn_e1 was created with
        syn_dof_data = [
            (0, 0, "Q_{11}", "Q_{12}"),  # Node 6 (i)
            (2, 0, "Q_1", "Q_2"),        # Node 1 (j)
            (2, 3, "Q_3", "Q_4"),        # Node 2 (k)
            (0, 3, "Q_9", "Q_{10}")      # Node 5 (r)
        ]
        
        def map_syn_dof(x: float, y: float):
            # Get actual vertex positions from the polygon after transformation
            # elem1_copy_poly should have the exact vertex positions after scaling and moving
            polygon_vertices = elem1_copy_poly.get_vertices()
            
            # Map our corner coordinates to polygon vertices
            # elem1_pts_m = [(0, 0), (2, 0), (2, 3), (0, 3), (0, 0)]
            corner_map = {
                (0, 0): polygon_vertices[0],  # bottom-left
                (2, 0): polygon_vertices[1],  # bottom-right  
                (2, 3): polygon_vertices[2],  # top-right
                (0, 3): polygon_vertices[3],  # top-left
            }
            
            # Return the actual vertex position
            return corner_map.get((x, y), target_position)
        
        syn_dof_scale = 0.2 * target_scale  # scale with syn_e1
        syn_stub_length = syn_dof_scale * 0.2
        
        for x, y, q_x, q_y in syn_dof_data:
            node_pos = map_syn_dof(x, y)
            
            # X-axis (horizontal DOF) - white L-shape with stubs
            x_line_pos = Line(
                node_pos,
                node_pos + RIGHT * syn_dof_scale * 0.9,
                stroke_width=2,
                color=WHITE
            )
            x_line_neg = Line(
                node_pos,
                node_pos + LEFT * syn_stub_length,
                stroke_width=2,
                color=WHITE
            )
            x_arrowhead = Triangle(color=WHITE, fill_opacity=1.0).scale(0.03 * target_scale).move_to(node_pos + RIGHT * syn_dof_scale).rotate(-PI/2)
            
            # Y-axis (vertical DOF) - white L-shape with stubs
            y_line_pos = Line(
                node_pos,
                node_pos + UP * syn_dof_scale * 0.9,
                stroke_width=2,
                color=WHITE
            )
            y_line_neg = Line(
                node_pos,
                node_pos + DOWN * syn_stub_length,
                stroke_width=2,
                color=WHITE
            )
            y_arrowhead = Triangle(color=WHITE, fill_opacity=1.0).scale(0.03 * target_scale).move_to(node_pos + UP * syn_dof_scale)
            
            # Labels for DOFs - positioned to avoid overlap
            x_label = MathTex(q_x).scale(0.25 * target_scale).move_to(node_pos + RIGHT * syn_dof_scale + RIGHT * 0.1 * target_scale + DOWN * 0.08 * target_scale)
            y_label = MathTex(q_y).scale(0.25 * target_scale).move_to(node_pos + UP * syn_dof_scale + UP * 0.1 * target_scale + LEFT * 0.08 * target_scale)
            
            # Group this node's DOF system
            node_dof = VGroup(
                x_line_pos, x_line_neg, x_arrowhead,
                y_line_pos, y_line_neg, y_arrowhead,
                x_label, y_label
            )
            syn_dof_systems.add(node_dof)
        
        # Animate appearance of syn_e1 DOF systems
        self.play(LaggedStartMap(FadeIn, syn_dof_systems, lag_ratio=0.1))

        # ----- Stage 6: Shape function derivation starting with polynomial form -----
        # Position much lower to avoid overlapping with constructions
        shape_func_pos = target_position + DOWN * 3.5
        
        # Title for polynomial derivation section
        poly_title = MathTex(r"\text{Shape Function Derivation from Polynomial Form}").scale(0.4)
        poly_title.move_to(shape_func_pos + UP * 1.1)
        self.play(FadeIn(poly_title))
        
        # Position for polynomial derivation steps - moved much lower to avoid overlap
        poly_deriv_pos = shape_func_pos + DOWN * 2.0  # Much lower from DOWN * 0.5
        
        # Step 1: Start with bilinear form
        poly_step1 = MathTex(r"\text{Start with bilinear form:}").scale(0.35)
        poly_step1.move_to(poly_deriv_pos + UP * 2.8)
        self.play(FadeIn(poly_step1))
        
        poly_step1_eq = MathTex(r"N(\xi,\eta) = a_0 + a_1\xi + a_2\eta + a_3\xi\eta").scale(0.35)
        poly_step1_eq.move_to(poly_deriv_pos + UP * 2.4)
        self.play(FadeIn(poly_step1_eq))
        
        # Step 2: Node i = (-1,-1) and Kronecker conditions
        poly_step2 = MathTex(r"\text{Node }i = (-1,-1)\text{. Kronecker conditions:}").scale(0.35)
        poly_step2.move_to(poly_deriv_pos + UP * 1.9)
        self.play(FadeIn(poly_step2))
        
        poly_step2_eq = MathTex(
            r"N(-1,-1) = 1, \quad N(+1,-1) = 0, \quad N(-1,+1) = 0, \quad N(+1,+1) = 0"
        ).scale(0.30)
        poly_step2_eq.move_to(poly_deriv_pos + UP * 1.5)
        self.play(FadeIn(poly_step2_eq))
        
        # Step 3: Linear system
        poly_step3 = MathTex(r"\text{Linear system:}").scale(0.35)
        poly_step3.move_to(poly_deriv_pos + UP * 1.0)
        self.play(FadeIn(poly_step3))
        
        poly_step3_eq = MathTex(
            r"\begin{aligned}"
            r"a_0 - a_1 - a_2 + a_3 &= 1\\[0.1em]"
            r"a_0 + a_1 - a_2 - a_3 &= 0\\[0.1em]"
            r"a_0 - a_1 + a_2 - a_3 &= 0\\[0.1em]"
            r"a_0 + a_1 + a_2 + a_3 &= 0"
            r"\end{aligned}"
        ).scale(0.28)
        poly_step3_eq.move_to(poly_deriv_pos + UP * 0.3)
        self.play(FadeIn(poly_step3_eq))
        
        # Step 4: Solution - moved to right column (higher up)
        poly_step4 = MathTex(r"\text{Solution:}").scale(0.35)
        poly_step4.move_to(poly_deriv_pos + RIGHT * 4.5 + UP * 2.8)  # Right column, much higher up
        self.play(FadeIn(poly_step4))
        
        poly_step4_eq = MathTex(
            r"a_0 = \frac{1}{4}, \quad a_1 = -\frac{1}{4}, \quad a_2 = -\frac{1}{4}, \quad a_3 = \frac{1}{4}"
        ).scale(0.30)
        poly_step4_eq.move_to(poly_deriv_pos + RIGHT * 4.5 + UP * 2.4)  # Right column
        self.play(FadeIn(poly_step4_eq))
        
        # Step 5: Therefore - moved to right column (higher up)
        poly_step5 = MathTex(r"\text{Therefore:}").scale(0.35)
        poly_step5.move_to(poly_deriv_pos + RIGHT * 4.5 + UP * 1.9)  # Right column, higher up
        self.play(FadeIn(poly_step5))
        
        poly_step5_eq = MathTex(
            r"N_i(\xi,\eta) = \frac{1}{4} - \frac{1}{4}\xi - \frac{1}{4}\eta + \frac{1}{4}\xi\eta = \frac{1}{4}(1-\xi)(1-\eta)"
        ).scale(0.30)
        poly_step5_eq.move_to(poly_deriv_pos + RIGHT * 4.5 + UP * 1.5)  # Right column, higher up
        self.play(FadeIn(poly_step5_eq))
        
        # Step 6: Mapping to physical coordinates - right column (higher up)
        poly_step6 = MathTex(r"\text{Mapping to physical coordinates for rectangle }a \times b\text{:}").scale(0.35)
        poly_step6.move_to(poly_deriv_pos + RIGHT * 4.5 + UP * 1.0)  # Right column, higher up
        self.play(FadeIn(poly_step6))
        
        poly_step6_eq = MathTex(
            r"\xi = \frac{2x}{a}, \quad \eta = \frac{2y}{b} \quad \Leftrightarrow \quad x = \frac{a}{2}\xi, \quad y = \frac{b}{2}\eta"
        ).scale(0.30)
        poly_step6_eq.move_to(poly_deriv_pos + RIGHT * 4.5 + UP * 0.6)  # Right column, higher up
        self.play(FadeIn(poly_step6_eq))
        
        # Step 7: Final substitution - right column (higher up)
        poly_step7 = MathTex(r"\text{Substitute:}").scale(0.35)
        poly_step7.move_to(poly_deriv_pos + RIGHT * 4.5 + UP * 0.1)  # Right column, higher up
        self.play(FadeIn(poly_step7))
        
        poly_step7_eq = MathTex(
            r"N_i(x,y) = \frac{1}{4}\left(1-\frac{2x}{a}\right)\left(1-\frac{2y}{b}\right)"
        ).scale(0.35)
        poly_step7_eq.move_to(poly_deriv_pos + RIGHT * 4.5 + DOWN * 0.3)  # Right column, final result higher up
        
        # Highlight the final result
        poly_highlight_box = SurroundingRectangle(poly_step7_eq, color=YELLOW, buff=0.1)
        self.play(FadeIn(poly_step7_eq))
        self.play(Create(poly_highlight_box))
        
        # Hold the polynomial derivation for a moment
        self.wait(3)
        
        # Group polynomial derivation elements except final result
        polynomial_derivation_steps = VGroup(
            poly_title, poly_step1, poly_step1_eq, poly_step2, poly_step2_eq,
            poly_step3, poly_step3_eq, poly_step4, poly_step4_eq,
            poly_step5, poly_step5_eq, poly_step6, poly_step6_eq,
            poly_step7  # Only the "Substitute:" label, not the equation
        )
        
        # Keep final result visible (poly_step7_eq and poly_highlight_box)
        final_result = VGroup(poly_step7_eq, poly_highlight_box)
        
        # Animate disappearance of derivation steps, keep final result
        self.play(FadeOut(polynomial_derivation_steps))
        
        # Hide first final result before showing second derivation
        self.play(FadeOut(final_result))  # Hide first yellow box before second derivation starts
        
        # Now show the existing bilinear derivation
        # Title for shape function section (smaller)
        title = MathTex(r"\text{Bilinear Shape Function for Node }i").scale(0.4)
        title.move_to(shape_func_pos + UP * 1.5)
        self.play(FadeIn(title))
        
        # Mathematical derivation positioned centrally with more space - moved further down
        deriv_pos = shape_func_pos + DOWN * 1.0  # Moved down from DOWN * 0.2 to DOWN * 1.0
        
        # Step 1: Natural coordinates introduction
        step1 = MathTex(r"\text{Natural coordinates: } \xi = \frac{2x}{a}, \; \eta = \frac{2y}{b}").scale(0.32)
        step1.move_to(deriv_pos + UP * 1.8)
        self.play(FadeIn(step1))
        
        # Step 2: Transform to [-1,1] × [-1,1] space - more spacing
        step2 = MathTex(r"[0,a] \times [0,b] \rightarrow [-1,1] \times [-1,1]").scale(0.33)
        step2.move_to(deriv_pos + UP * 1.2)  # Much more space between steps
        self.play(FadeIn(step2))
        
        # Step 3: Standard bilinear shape functions - increased spacing and size
        step3 = MathTex(
            r"\begin{aligned}"
            r"N_i(\xi,\eta) &= \frac{1}{4}(1-\xi)(1-\eta)\\"
            r"N_j(\xi,\eta) &= \frac{1}{4}(1+\xi)(1-\eta)\\"
            r"N_k(\xi,\eta) &= \frac{1}{4}(1+\xi)(1+\eta)\\"
            r"N_r(\xi,\eta) &= \frac{1}{4}(1-\xi)(1+\eta)"
            r"\end{aligned}"
        ).scale(0.30)
        step3.move_to(deriv_pos + UP * 0.2)  # Much more space from previous step
        self.play(FadeIn(step3))
        
        # Step 4: Substitute natural coordinates - more spacing
        step4 = MathTex(r"\text{Substitute: } \xi = \frac{2x}{a}, \; \eta = \frac{2y}{b}").scale(0.33)
        step4.move_to(deriv_pos + DOWN * 0.8)  # Much more space between steps
        self.play(FadeIn(step4))
        
        # Step 5: Final results (highlighted) - positioned to the right with more space
        step5 = MathTex(
            r"\begin{aligned}"
            r"N_i(x,y) &= \frac{1}{4}\left(1-\frac{2x}{a}\right)\left(1-\frac{2y}{b}\right)\\"
            r"N_j(x,y) &= \frac{1}{4}\left(1+\frac{2x}{a}\right)\left(1-\frac{2y}{b}\right)\\"
            r"N_k(x,y) &= \frac{1}{4}\left(1+\frac{2x}{a}\right)\left(1+\frac{2y}{b}\right)\\"
            r"N_r(x,y) &= \frac{1}{4}\left(1-\frac{2x}{a}\right)\left(1+\frac{2y}{b}\right)"
            r"\end{aligned}"
        ).scale(0.31)
        step5.move_to(deriv_pos + RIGHT * 3.0 + DOWN * 0.5)  # Much more to the right and centered vertically
        
        highlight_box2 = SurroundingRectangle(step5, color=YELLOW, buff=0.1)
        self.play(FadeIn(step5))
        self.play(Create(highlight_box2))
        
        # Hold second derivation for a moment
        self.wait(3)
        
        # Group second derivation elements except final result
        second_derivation_steps = VGroup(title, step1, step2, step3, step4)
        
        # Keep second final result visible (step5 and highlight_box2)  
        second_final_result = VGroup(step5, highlight_box2)
        
        # Hide derivation steps, keep second yellow box
        self.play(FadeOut(second_derivation_steps))  # Hide derivation steps, keep second yellow box
        
        # Add dimension labels to the miniaturized construction (top-left)
        # The construction was scaled by 0.65 and moved to top-left corner
        # Original construction position after scaling and moving: UP + EDGE + LEFT + EDGE
        
        # Add 'a = ' before the horizontal bottom dimension '2 m' 
        a_label = MathTex(r"a = ").scale(0.4)
        # Position: wyżej o 15% wysokości ekranu, w lewo o 8% szerokości ekranu (jeszcze bardziej w lewo)
        frame_height = config.frame_height
        frame_width = config.frame_width
        a_label.move_to(LEFT * (5.0 + 0.08 * frame_width) + DOWN * (2.5 - 0.15 * frame_height))
        self.play(FadeIn(a_label))
        
        # Add 'b = ' near the vertical left dimension '3 m'  
        b_label = MathTex(r"b = ").scale(0.4)
        # Position: wyżej o 5% wysokości ekranu, w lewo o 6% szerokości ekranu (poprawiony kierunek)
        b_label.move_to(LEFT * (6.0 + 0.06 * frame_width) + UP * (0.5 + 0.05 * frame_height))
        self.play(FadeIn(b_label))
        
        # Briefly highlight the dimension labels
        a_highlight = SurroundingRectangle(VGroup(a_label), color=YELLOW, buff=0.05)
        b_highlight = SurroundingRectangle(VGroup(b_label), color=YELLOW, buff=0.05) 
        
        self.play(Create(a_highlight), Create(b_highlight))
        self.wait(1)
        self.play(FadeOut(a_highlight), FadeOut(b_highlight))
        
        # Move second yellow box further right
        second_final_result.move_to(deriv_pos + RIGHT * 5.5 + DOWN * 0.5)  # Much further right
        
        # Add shape function matrix in the center (lower to avoid syn_el_1)
        matrix_pos = ORIGIN + DOWN * 1.5  # Lower position
        
        matrix_title = MathTex(r"\text{Shape Function Matrix:}").scale(0.5)
        matrix_title.move_to(matrix_pos + UP * 2.0)  # Lower title
        self.play(FadeIn(matrix_title))
        
        # Shape function matrix N (complete without dots)
        shape_matrix = MathTex(
            r"\mathbf{N} = \begin{bmatrix}"
            r"N_i & 0 & N_j & 0 & N_k & 0 & N_r & 0 \\"
            r"0 & N_i & 0 & N_j & 0 & N_k & 0 & N_r"
            r"\end{bmatrix}"
        ).scale(0.35)
        shape_matrix.move_to(matrix_pos + UP * 1.0)
        self.play(FadeIn(shape_matrix))
        
        # Complete substituted matrix with actual functions
        substituted_matrix = MathTex(
            r"\mathbf{N} = \begin{bmatrix}"
            r"\frac{1}{4}(1-\frac{2x}{a})(1-\frac{2y}{b}) & 0 & \frac{1}{4}(1+\frac{2x}{a})(1-\frac{2y}{b}) & 0 & \frac{1}{4}(1+\frac{2x}{a})(1+\frac{2y}{b}) & 0 & \frac{1}{4}(1-\frac{2x}{a})(1+\frac{2y}{b}) & 0 \\"
            r"0 & \frac{1}{4}(1-\frac{2x}{a})(1-\frac{2y}{b}) & 0 & \frac{1}{4}(1+\frac{2x}{a})(1-\frac{2y}{b}) & 0 & \frac{1}{4}(1+\frac{2x}{a})(1+\frac{2y}{b}) & 0 & \frac{1}{4}(1-\frac{2x}{a})(1+\frac{2y}{b})"
            r"\end{bmatrix}"
        ).scale(0.25)
        substituted_matrix.move_to(matrix_pos + UP * 0.2)
        self.play(FadeIn(substituted_matrix))
        
        # Third matrix with specific form requested
        numerical_matrix = MathTex(
            r"\mathbf{N} = \begin{bmatrix}"
            r"\frac{1}{12}(x-1)(2y-3) & 0 & -\frac{1}{12}(x+1)(2y-3) & 0 & \frac{1}{12}(x+1)(2y+3) & 0 & -\frac{1}{12}(x-1)(2y+3) & 0 \\"
            r"0 & \frac{1}{12}(x-1)(2y-3) & 0 & -\frac{1}{12}(x+1)(2y-3) & 0 & \frac{1}{12}(x+1)(2y+3) & 0 & -\frac{1}{12}(x-1)(2y+3)"
            r"\end{bmatrix}"
        ).scale(0.275)  # 10% increase from 0.25
        # Move left by 10% of screen width
        numerical_matrix.move_to(matrix_pos + DOWN * 0.8 + LEFT * 0.1 * config.frame_width)
        self.play(FadeIn(numerical_matrix))
        
        # ----- NEW ANIMATION STEPS START HERE -----
        
        # Step 1: Fade out the yellow box
        self.play(FadeOut(second_final_result))
        
        # Step 2: Scale down miniatura_all (including a= and b= labels) by additional 20% and move up by 10% of screen height
        miniatura_all_with_labels = VGroup(original_group, a_label, b_label)
        self.play(
            miniatura_all_with_labels.animate
            .scale(0.8)  # Scale by 0.8 to get 20% reduction
            .shift(UP * 0.1 * config.frame_height)  # Move up by 10% of screen height
        )
        
        # Step 3: Scale down miniatura_mes by additional 20% and move up by 7% of screen height
        self.play(
            discretized_group.animate
            .scale(0.8)  # Scale by 0.8 to get 20% reduction
            .shift(UP * 0.07 * config.frame_height)  # Move up by 7% of screen height
        )
        
        # Step 4: Remove all matrices except the last one
        matrices_to_remove = VGroup(matrix_title, shape_matrix, substituted_matrix)
        self.play(FadeOut(matrices_to_remove))
        
        # Step 5: Move the last matrix up under syn_el_1 and shift right (higher by 5% screen height)
        final_matrix_pos = target_position + DOWN * 2.8 + UP * 0.1 * config.frame_height  # Higher by 5% of screen height
        self.play(
            numerical_matrix.animate.move_to(final_matrix_pos + RIGHT * 0.08 * config.frame_width)  # 8% right
        )
        
        # ----- Step 6: Add strain-displacement derivations -----
        derivation_start_pos = final_matrix_pos + DOWN * 1.2 + UP * 0.08 * config.frame_height  # Below the N matrix, raised by 8%
        
        # Small strains definition
        strain_def_text = MathTex(r"\text{From the definition of small strains:}").scale(0.35)
        strain_def_text.move_to(derivation_start_pos)
        self.play(FadeIn(strain_def_text))
        
        strain_def_eq = MathTex(
            r"\varepsilon_x = \frac{\partial u}{\partial x}, \quad "
            r"\varepsilon_y = \frac{\partial v}{\partial y}, \quad "
            r"\gamma_{xy} = \frac{\partial u}{\partial y} + \frac{\partial v}{\partial x}"
        ).scale(0.3)
        strain_def_eq.move_to(derivation_start_pos + DOWN * 0.4)
        self.play(FadeIn(strain_def_eq))
        
        # Displacement interpolation
        disp_interp_text = MathTex(r"\text{Displacement field is interpolated using shape functions:}").scale(0.35)
        disp_interp_text.move_to(derivation_start_pos + DOWN * 0.8)
        self.play(FadeIn(disp_interp_text))
        
        disp_interp_eq = MathTex(
            r"u = \sum_{i=1}^{4} N_i u_i, \qquad v = \sum_{i=1}^{4} N_i v_i"
        ).scale(0.3)
        disp_interp_eq.move_to(derivation_start_pos + DOWN * 1.2)
        self.play(FadeIn(disp_interp_eq))
        
        # Therefore text
        therefore_text = MathTex(r"\text{Therefore:}").scale(0.35)
        therefore_text.move_to(derivation_start_pos + DOWN * 1.6)
        self.play(FadeIn(therefore_text))
        
        # Full strain-displacement equation with L and N matrices
        strain_eq = MathTex(
            r"\begin{bmatrix} \varepsilon_x \\ \varepsilon_y \\ \gamma_{xy} \end{bmatrix} = "
            r"\begin{bmatrix} \frac{\partial}{\partial x} & 0 \\ 0 & \frac{\partial}{\partial y} \\ \frac{\partial}{\partial y} & \frac{\partial}{\partial x} \end{bmatrix} "
            r"\begin{bmatrix} N_1 & 0 & N_2 & 0 & N_3 & 0 & N_4 & 0 \\ 0 & N_1 & 0 & N_2 & 0 & N_3 & 0 & N_4 \end{bmatrix} "
            r"\begin{bmatrix} u_1 \\ v_1 \\ u_2 \\ v_2 \\ u_3 \\ v_3 \\ u_4 \\ v_4 \end{bmatrix} = B \, d"
        ).scale(0.22)
        strain_eq.move_to(derivation_start_pos + DOWN * 2.0)
        self.play(FadeIn(strain_eq))
        
        # B matrix definition
        b_matrix_text = MathTex(r"\text{where } B = L \, N \text{ has the form:}").scale(0.35)
        b_matrix_text.move_to(derivation_start_pos + DOWN * 2.4)
        self.play(FadeIn(b_matrix_text))
        
        # Compact B matrix
        b_matrix = MathTex(
            r"B = \begin{bmatrix}"
            r"N_{1,x} & 0 & N_{2,x} & 0 & N_{3,x} & 0 & N_{4,x} & 0 \\"
            r"0 & N_{1,y} & 0 & N_{2,y} & 0 & N_{3,y} & 0 & N_{4,y} \\"
            r"N_{1,y} & N_{1,x} & N_{2,y} & N_{2,x} & N_{3,y} & N_{3,x} & N_{4,y} & N_{4,x}"
            r"\end{bmatrix}"
        ).scale(0.25)
        b_matrix.move_to(derivation_start_pos + DOWN * 3.0)
        self.play(FadeIn(b_matrix))
        
        # Derivatives definition - positioned to the right of B matrix at same height
        derivatives_def = MathTex(
            r"N_{i,x} = \frac{\partial N_i}{\partial x}, \qquad N_{i,y} = \frac{\partial N_i}{\partial y}"
        ).scale(0.3)
        derivatives_def.move_to(derivation_start_pos + DOWN * 3.0 + RIGHT * 3.5)  # Same height as B matrix, to the right
        self.play(FadeIn(derivatives_def))

        # ----- Step 7: New animation steps -----
        
        # Step 7a: Remove derivations from "From the definition..." to "has the form"
        elements_to_remove = VGroup(
            strain_def_text, strain_def_eq, disp_interp_text, disp_interp_eq,
            therefore_text, strain_eq, b_matrix_text
        )
        self.play(FadeOut(elements_to_remove))
        
        # Step 7b: Move B matrix and derivatives under N matrix (5% higher)
        b_matrix_pos = final_matrix_pos + DOWN * 1.0 + UP * 0.05 * config.frame_height  # 5% higher
        
        # Move existing B matrix and derivatives
        self.play(
            b_matrix.animate.move_to(b_matrix_pos),
            derivatives_def.animate.move_to(b_matrix_pos + RIGHT * 3.5)
        )
        
        # Step 7c: Show derivative calculation for first component (10% higher - reduced by 5%)
        calc_pos = b_matrix_pos + DOWN * 1.5 + UP * 0.10 * config.frame_height  # 10% higher (was 15%, now reduced by 5%)
        
        # Compact calculation in one line
        calc_example = MathTex(
            r"\text{Example: } N_1 = \frac{1}{12}(x-1)(2y-3) \Rightarrow \frac{\partial N_1}{\partial y} = \frac{1}{12}(x-1)"
        ).scale(0.3)
        calc_example.move_to(calc_pos)
        self.play(FadeIn(calc_example))
        
        # Step 7d: Show all derivatives in compact form
        all_derivatives = MathTex(
            r"N_{1,x} = \frac{1}{12}(2y-3), N_{1,y} = \frac{1}{12}(x-1), "
            r"N_{2,x} = -\frac{1}{12}(2y-3), N_{2,y} = -\frac{1}{12}(x+1)"
        ).scale(0.25)
        all_derivatives.move_to(calc_pos + DOWN * 0.5)
        self.play(FadeIn(all_derivatives))
        
        all_derivatives2 = MathTex(
            r"N_{3,x} = \frac{1}{12}(2y+3), N_{3,y} = \frac{1}{12}(x+1), "
            r"N_{4,x} = -\frac{1}{12}(2y+3), N_{4,y} = -\frac{1}{12}(x-1)"
        ).scale(0.25)
        all_derivatives2.move_to(calc_pos + DOWN * 0.8)
        self.play(FadeIn(all_derivatives2))
        
        # Show complete B matrix with calculated values (15% larger)
        full_b_matrix = MathTex(
            r"B = \frac{1}{12}\begin{bmatrix}"
            r"(2y-3) & 0 & -(2y-3) & 0 & (2y+3) & 0 & -(2y+3) & 0 \\"
            r"0 & (x-1) & 0 & -(x+1) & 0 & (x+1) & 0 & -(x-1) \\"
            r"(x-1) & (2y-3) & -(x+1) & -(2y-3) & (x+1) & (2y+3) & -(x-1) & -(2y+3)"
            r"\end{bmatrix}"
        ).scale(0.28)  # Larger font for better readability
        full_b_matrix.move_to(calc_pos + DOWN * 1.5)  # Much closer
        self.play(FadeIn(full_b_matrix))

        # ----- Step 8: New animation steps -----
        
        # Step 8a: Remove everything except numerical B matrix
        elements_to_remove_step8 = VGroup(
            calc_example, all_derivatives, all_derivatives2,
            b_matrix, derivatives_def,  # Remove symbolic B matrix and derivatives definitions
            numerical_matrix  # Remove the full N matrix as well
        )
        self.play(FadeOut(elements_to_remove_step8))
        
        # Step 8b: Move B matrix up by 25% of screen height
        b_matrix_final_pos = full_b_matrix.get_center() + UP * 0.25 * config.frame_height
        self.play(full_b_matrix.animate.move_to(b_matrix_final_pos))
        
        # Step 8c: Introduce elasticity matrix D (8% higher)
        d_matrix_pos = b_matrix_final_pos + DOWN * 2.0 + UP * 0.08 * config.frame_height  # 8% higher
        
        d_matrix_title = MathTex(r"\text{Elasticity matrix for plane stress:}").scale(0.4)
        d_matrix_title.move_to(d_matrix_pos + UP * 0.5)
        self.play(FadeIn(d_matrix_title))
        
        # Symbolic and numerical D matrices side by side (closer together)
        d_matrix_symbolic = MathTex(
            r"\mathbf{D} = \frac{E}{1-\nu^2} \begin{bmatrix}"
            r"1 & \nu & 0 \\"
            r"\nu & 1 & 0 \\"
            r"0 & 0 & \frac{1-\nu}{2}"
            r"\end{bmatrix}"
        ).scale(0.35)
        d_matrix_symbolic.move_to(d_matrix_pos + LEFT * 1.2)  # Closer to center
        self.play(FadeIn(d_matrix_symbolic))
        
        # Equals sign
        equals_sign = MathTex(r"=").scale(0.5)
        equals_sign.move_to(d_matrix_pos + RIGHT * 0.2)  # Slightly right of center
        self.play(FadeIn(equals_sign))
        
        # Numerical D matrix
        d_matrix_numerical = MathTex(
            r"\begin{bmatrix}"
            r"85.5 & 29.9 & 0 \\"
            r"29.9 & 85.5 & 0 \\"
            r"0 & 0 & 27.8"
            r"\end{bmatrix}"
        ).scale(0.35)
        d_matrix_numerical.move_to(d_matrix_pos + RIGHT * 1.4)  # Closer to center
        self.play(FadeIn(d_matrix_numerical))

        # ----- Step 9: Show transposed B matrix -----
        
        # Step 9a: Shrink B matrix and move to the right, move D matrix to the left
        # Move D matrix elements to the left (additional 10% screen width)
        d_matrix_group = VGroup(d_matrix_title, d_matrix_symbolic, equals_sign, d_matrix_numerical)
        self.play(d_matrix_group.animate.shift(LEFT * (3.0 + 0.1 * config.frame_width)))
        
        # Shrink and move B matrix to the right
        self.play(
            full_b_matrix.animate
            .scale(0.7)  # Shrink by 30%
            .shift(RIGHT * 4.0)  # Move to the right
        )
        
        # Step 9b: Show transposed B matrix (6% lower to make room for horizontal dimensions)
        bt_matrix_pos = b_matrix_final_pos + DOWN * 0.06 * config.frame_height  # 6% lower
        
        bt_matrix_title = MathTex(r"\text{Transposed B matrix:}").scale(0.4)
        bt_matrix_title.move_to(bt_matrix_pos + UP * 1.0)  # Above the matrix
        self.play(FadeIn(bt_matrix_title))
        
        # B^T matrix with given values (larger font for better readability)
        bt_matrix = MathTex(
            r"\mathbf{B}^T = \begin{bmatrix}"
            r"\frac{1}{6}y - \frac{1}{4} & 0 & \frac{1}{6}x - \frac{1}{6} \\"
            r"0 & \frac{1}{6}x - \frac{1}{6} & \frac{1}{6}y - \frac{1}{4} \\"
            r"-\frac{1}{6}y + \frac{1}{4} & 0 & -\frac{1}{6}x - \frac{1}{6} \\"
            r"0 & -\frac{1}{6}x - \frac{1}{6} & -\frac{1}{6}y + \frac{1}{4} \\"
            r"\frac{1}{6}y + \frac{1}{4} & 0 & \frac{1}{6}x + \frac{1}{6} \\"
            r"0 & \frac{1}{6}x + \frac{1}{6} & \frac{1}{6}y + \frac{1}{4} \\"
            r"-\frac{1}{6}y - \frac{1}{4} & 0 & -\frac{1}{6}x + \frac{1}{6} \\"
            r"0 & -\frac{1}{6}x + \frac{1}{6} & -\frac{1}{6}y - \frac{1}{4}"
            r"\end{bmatrix}"
        ).scale(0.3)  # Increased from 0.25 to 0.3 for better readability
        bt_matrix.move_to(bt_matrix_pos)
        self.play(FadeIn(bt_matrix))
        
        # Show stiffness matrix integral formula (higher position)
        integral_pos = bt_matrix_pos + DOWN * 2.0  # Higher position
        
        integral_title = MathTex(r"\text{Element stiffness matrix:}").scale(0.4)
        integral_title.move_to(integral_pos + UP * 0.5)
        self.play(FadeIn(integral_title))
        
        # Integral formula with correct double integral (2 integral signs)
        integral_formula = MathTex(
            r"\mathbf{K}_1 = \int_{-1.5}^{1.5} \int_{-1}^{1} \mathbf{B}^T \mathbf{D} \mathbf{B} \, h \, dx \, dy"
        ).scale(0.35)
        integral_formula.move_to(integral_pos)
        self.play(FadeIn(integral_formula))
        
        # Sequential demonstration of integration limits with dimensions and boundary functions
        # Get actual syn_el_1 boundaries
        elem_half_width_full = 1.2 * target_scale  # Full half width
        elem_half_width = elem_half_width_full * 0.35  # Shortened by 65% total (35% + 30% additional)
        elem_half_width_left = elem_half_width_full * 0.55  # Left side trimmed by 45% total (15% + 30%)
        elem_half_width_right = elem_half_width_full * 0.65  # Right side trimmed by 35% total (5% + 30%)
        elem_half_height = 0.9 * target_scale  # Half height of syn_el_1
        
        # a) Show 1.5 limit: highlight in integral + vertical dimension + top boundary function
        # Highlight 1.5 in integral (create new integral with highlighted 1.5)
        integral_formula_highlighted_15 = MathTex(
            r"\mathbf{K}_1 = \int_{-1.5}^{\mathbf{1.5}} \int_{-1}^{1} \mathbf{B}^T \mathbf{D} \mathbf{B} \, h \, dx \, dy"
        ).scale(0.35)
        integral_formula_highlighted_15.move_to(integral_pos)
        self.play(Transform(integral_formula, integral_formula_highlighted_15))
        
        # Vertical dimension 1.5 (from center to top edge, extended by 10%, moved right by 2%)
        dim_15_x = target_position[0] + elem_half_width + 0.3 + 0.02 * config.frame_width
        dim_15_line = Line(
            [dim_15_x, target_position[1], 0],
            [dim_15_x, target_position[1] + elem_half_height * 1.1, 0],  # Extended by 10%
            stroke_width=2, color=GREEN
        )
        dim_15_tick_top = Line(
            [dim_15_x - 0.1, target_position[1] + elem_half_height * 1.1, 0],
            [dim_15_x + 0.1, target_position[1] + elem_half_height * 1.1, 0],
            stroke_width=2, color=GREEN
        )
        dim_15_tick_center = Line(
            [dim_15_x - 0.1, target_position[1], 0],
            [dim_15_x + 0.1, target_position[1], 0],
            stroke_width=2, color=GREEN
        )
        dim_15_label = MathTex(r"\mathbf{1.5}").scale(0.3).move_to([dim_15_x + 0.25, target_position[1] + elem_half_height/2, 0])
        dim_15_group = VGroup(dim_15_line, dim_15_tick_top, dim_15_tick_center, dim_15_label)
        
        # Top boundary function y = 1.5 (7% higher total: 5% + 2%)
        top_boundary = DashedLine(
            target_position + LEFT * elem_half_width_full + UP * elem_half_height * 1.07,  # 7% higher
            target_position + RIGHT * elem_half_width_full + UP * elem_half_height * 1.07,
            stroke_width=4, color=GREEN, dash_length=0.1
        )
        top_boundary_label = MathTex(r"y = 1.5").scale(0.25)
        top_boundary_label.move_to(target_position + RIGHT * elem_half_width_full * 0.2 + UP * elem_half_height * 1.07 + UP * 0.15)  # 5% left, 2% higher
        
        # Dramatic highlighting of 1.5 - grows from integral position
        integral_temp_large = MathTex(r"\mathbf{1.5}").scale(0.35).set_color(GREEN)
        integral_temp_large.move_to(integral_pos)  # Start at integral position
        
        self.play(
            Create(dim_15_group), Create(top_boundary), FadeIn(top_boundary_label),
            integral_temp_large.animate.scale(3.0).move_to(integral_pos + UP * 0.8)  # Grow and move up
        )
        self.wait(0.5)
        self.play(integral_temp_large.animate.scale(1/3.0).move_to(integral_pos))  # Shrink back to original
        self.play(FadeOut(integral_temp_large))
        
        # b) Show -1.5 limit: highlight in integral + vertical dimension + bottom boundary function
        integral_formula_highlighted_neg15 = MathTex(
            r"\mathbf{K}_1 = \int_{\mathbf{-1.5}}^{1.5} \int_{-1}^{1} \mathbf{B}^T \mathbf{D} \mathbf{B} \, h \, dx \, dy"
        ).scale(0.35)
        integral_formula_highlighted_neg15.move_to(integral_pos)
        self.play(Transform(integral_formula, integral_formula_highlighted_neg15))
        
        # Vertical dimension -1.5 (from center to bottom edge)
        dim_neg15_line = Line(
            [dim_15_x, target_position[1], 0],
            [dim_15_x, target_position[1] - elem_half_height, 0],
            stroke_width=2, color=GREEN
        )
        dim_neg15_tick_bottom = Line(
            [dim_15_x - 0.1, target_position[1] - elem_half_height, 0],
            [dim_15_x + 0.1, target_position[1] - elem_half_height, 0],
            stroke_width=2, color=GREEN
        )
        dim_neg15_label = MathTex(r"\mathbf{-1.5}").scale(0.3).move_to([dim_15_x + 0.3, target_position[1] - elem_half_height/2, 0])
        dim_neg15_group = VGroup(dim_neg15_line, dim_neg15_tick_bottom, dim_neg15_label)
        
        # Bottom boundary function y = -1.5
        bottom_boundary = DashedLine(
            target_position + LEFT * elem_half_width_full + DOWN * elem_half_height,
            target_position + RIGHT * elem_half_width_full + DOWN * elem_half_height,
            stroke_width=4, color=GREEN, dash_length=0.1
        )
        bottom_boundary_label = MathTex(r"y = -1.5").scale(0.25)
        bottom_boundary_label.move_to(target_position + RIGHT * elem_half_width_full * 0.2 + DOWN * elem_half_height - DOWN * 0.15)  # 5% left of previous
        
        # Dramatic highlighting of -1.5 - grows from integral position
        integral_temp_large_neg15 = MathTex(r"\mathbf{-1.5}").scale(0.35).set_color(GREEN)
        integral_temp_large_neg15.move_to(integral_pos)  # Start at integral position
        
        self.play(
            Create(dim_neg15_group), Create(bottom_boundary), FadeIn(bottom_boundary_label),
            integral_temp_large_neg15.animate.scale(3.0).move_to(integral_pos + DOWN * 0.8)  # Grow and move down
        )
        self.wait(0.5)
        self.play(integral_temp_large_neg15.animate.scale(1/3.0).move_to(integral_pos))  # Shrink back
        self.play(FadeOut(integral_temp_large_neg15))
        
        # c) Show 1 limit: highlight in integral + horizontal dimension
        integral_formula_highlighted_1 = MathTex(
            r"\mathbf{K}_1 = \int_{-1.5}^{1.5} \int_{-1}^{\mathbf{1}} \mathbf{B}^T \mathbf{D} \mathbf{B} \, h \, dx \, dy"
        ).scale(0.35)
        integral_formula_highlighted_1.move_to(integral_pos)
        self.play(Transform(integral_formula, integral_formula_highlighted_1))
        
        # Horizontal dimension 1 (from center to right edge, below element, trimmed by 5%)
        dim_1_y = target_position[1] - elem_half_height - 0.4 - 0.04 * config.frame_height  # Below element, 4% lower
        dim_1_line = Line(
            [target_position[0], dim_1_y, 0],  # Center
            [target_position[0] + elem_half_width_right, dim_1_y, 0],  # Right edge (trimmed by 5%)
            stroke_width=2, color=BLUE
        )
        dim_1_tick_right = Line(
            [target_position[0] + elem_half_width_right, dim_1_y - 0.1, 0],
            [target_position[0] + elem_half_width_right, dim_1_y + 0.1, 0],
            stroke_width=2, color=BLUE
        )
        dim_1_tick_center = Line(
            [target_position[0], dim_1_y - 0.1, 0],
            [target_position[0], dim_1_y + 0.1, 0],
            stroke_width=2, color=BLUE
        )
        dim_1_label = MathTex(r"\mathbf{1}").scale(0.3).move_to([target_position[0] + elem_half_width_right/2, dim_1_y - 0.2, 0])
        dim_1_group = VGroup(dim_1_line, dim_1_tick_right, dim_1_tick_center, dim_1_label)
        
        # Dramatic highlighting of 1 - grows from integral position
        integral_temp_large_1 = MathTex(r"\mathbf{1}").scale(0.35).set_color(BLUE)
        integral_temp_large_1.move_to(integral_pos)  # Start at integral position
        
        self.play(
            Create(dim_1_group),
            integral_temp_large_1.animate.scale(3.0).move_to(integral_pos + RIGHT * 1.0)  # Grow and move right
        )
        self.wait(0.5)
        self.play(integral_temp_large_1.animate.scale(1/3.0).move_to(integral_pos))  # Shrink back
        self.play(FadeOut(integral_temp_large_1))
        
        # d) Show -1 limit: highlight in integral + horizontal dimension  
        integral_formula_highlighted_neg1 = MathTex(
            r"\mathbf{K}_1 = \int_{-1.5}^{1.5} \int_{\mathbf{-1}}^{1} \mathbf{B}^T \mathbf{D} \mathbf{B} \, h \, dx \, dy"
        ).scale(0.35)
        integral_formula_highlighted_neg1.move_to(integral_pos)
        self.play(Transform(integral_formula, integral_formula_highlighted_neg1))
        
        # Horizontal dimension -1 (from center to left edge, below element, shortened by 35%)
        dim_neg1_line = Line(
            [target_position[0], dim_1_y, 0],  # Center
            [target_position[0] - elem_half_width_left, dim_1_y, 0],  # Left edge (trimmed by 15%)
            stroke_width=2, color=BLUE
        )
        dim_neg1_tick_left = Line(
            [target_position[0] - elem_half_width_left, dim_1_y - 0.1, 0],
            [target_position[0] - elem_half_width_left, dim_1_y + 0.1, 0],
            stroke_width=2, color=BLUE
        )
        dim_neg1_label = MathTex(r"\mathbf{-1}").scale(0.3).move_to([target_position[0] - elem_half_width_left/2, dim_1_y - 0.2, 0])
        dim_neg1_group = VGroup(dim_neg1_line, dim_neg1_tick_left, dim_neg1_label)
        
        # Dramatic highlighting of -1 - grows from integral position
        integral_temp_large_neg1 = MathTex(r"\mathbf{-1}").scale(0.35).set_color(BLUE)
        integral_temp_large_neg1.move_to(integral_pos)  # Start at integral position
        
        self.play(
            Create(dim_neg1_group),
            integral_temp_large_neg1.animate.scale(3.0).move_to(integral_pos + LEFT * 1.0)  # Grow and move left
        )
        self.wait(0.5)
        self.play(integral_temp_large_neg1.animate.scale(1/3.0).move_to(integral_pos))  # Shrink back
        self.play(FadeOut(integral_temp_large_neg1))

        # ----- Final hold -----
        self.wait(3)

if __name__ == "__main__":
    import sys
    

    # Low quality, fast rendering for testing
    # from manim import config
    # config.quality = "low_quality"  # 480p15 - much faster
    # config.frame_rate = 15
    # config.pixel_height = 480
    # config.pixel_width = 854
    # print("🚀 Quick render mode: 480p15 for fast testing")

    # # Medium quality for preview
    # from manim import config
    # config.quality = "medium_quality"  # 720p30
    # config.frame_rate = 30
    # config.pixel_height = 720
    # config.pixel_width = 1280
    # print("⚡ Medium render mode: 720p30 for preview")

    
    scene = MESStructureScene()
    scene.render()