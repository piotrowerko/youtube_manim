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
        # coord_origin = target_position
        coord_origin = elem1_copy_poly.get_center()
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
# --- widths from actual element geometry (fix left too short / right too long) ---
        center_x = coord_origin[0]
        center_y = coord_origin[1]
        verts = elem1_copy_poly.get_vertices()
        xs = [v[0] for v in verts]
        ys = [v[1] for v in verts]

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        # half-widths / half-height measured from the real polygon geometry
        elem_half_width_left  = center_x - min_x
        elem_half_width_right = max_x - center_x
        elem_half_height      = 0.5 * (max_y - min_y)
        
        # a) Show 1.5 limit: highlight in integral + vertical dimension + top boundary function
        # Highlight 1.5 in integral (create new integral with highlighted 1.5)
        integral_formula_highlighted_15 = MathTex(
            r"\mathbf{K}_1 = \int_{-1.5}^{\mathbf{1.5}} \int_{-1}^{1} \mathbf{B}^T \mathbf{D} \mathbf{B} \, h \, dx \, dy"
        ).scale(0.35)
        integral_formula_highlighted_15.move_to(integral_pos)
        self.play(Transform(integral_formula, integral_formula_highlighted_15))
        
        # Vertical dimension 1.5 (from center to top edge, extended by 10%, moved right by 2%)
        dim_15_x = center_x + elem_half_width_right + 0.3 + 0.02 * config.frame_width
        dim_15_line = Line(
            [dim_15_x, center_y, 0],
            [dim_15_x, max_y, 0],
            stroke_width=2, color=GREEN
        )
        dim_15_tick_top = Line(
            [dim_15_x - 0.1, max_y, 0],
            [dim_15_x + 0.1, max_y, 0],
            stroke_width=2, color=GREEN
        )
        dim_15_tick_center = Line(
            [dim_15_x - 0.1, center_y, 0],
            [dim_15_x + 0.1, center_y, 0],
            stroke_width=2, color=GREEN
        )
        dim_15_label = MathTex(r"\mathbf{1.5}").scale(0.3).move_to([dim_15_x + 0.25, target_position[1] + elem_half_height/2, 0])
        dim_15_group = VGroup(dim_15_line, dim_15_tick_top, dim_15_tick_center, dim_15_label)
        
        # Top boundary function y = 1.5 (9% higher total: 5% + 2% + 2%)
        top_boundary = DashedLine(
            [min_x, max_y, 0],
            [max_x, max_y, 0],
            stroke_width=4, color=GREEN, dash_length=0.1
        )
        top_boundary_label = MathTex(r"y = 1.5").scale(0.25)
        top_boundary_label.move_to(
                        target_position
                        + RIGHT * elem_half_width_left  * 0.2
                        + UP * elem_half_height * 1.12
                        + UP * 0.15
                    )
        
        # Dramatic highlighting of 1.5 - grows from the specific "1.5" position in integral
        integral_15_pos = integral_pos + RIGHT * (0.8 - 0.1 * config.frame_width) + UP * 0.1  # 10% left from previous position
        integral_temp_large = MathTex(r"\mathbf{1.5}").scale(0.35).set_color(GREEN)
        integral_temp_large.move_to(integral_15_pos)  # Start at the "1.5" position
        
        self.play(
            Create(dim_15_group), Create(top_boundary), FadeIn(top_boundary_label),
            integral_temp_large.animate.scale(3.0).move_to(integral_pos + UP * 0.8)  # Grow and move up
        )
        self.wait(0.5)
        self.play(integral_temp_large.animate.scale(1/3.0).move_to(integral_15_pos))  # Shrink back to "1.5" position
        self.play(FadeOut(integral_temp_large))
        
        # b) Show -1.5 limit: highlight in integral + vertical dimension + bottom boundary function
        integral_formula_highlighted_neg15 = MathTex(
            r"\mathbf{K}_1 = \int_{\mathbf{-1.5}}^{1.5} \int_{-1}^{1} \mathbf{B}^T \mathbf{D} \mathbf{B} \, h \, dx \, dy"
        ).scale(0.35)
        integral_formula_highlighted_neg15.move_to(integral_pos)
        self.play(Transform(integral_formula, integral_formula_highlighted_neg15))
        
        # Vertical dimension -1.5 (from center to bottom edge)
        dim_neg15_line = Line(
            [dim_15_x, center_y, 0],
            [dim_15_x, min_y, 0],
            stroke_width=2, color=GREEN
        )
        dim_neg15_tick_bottom = Line(
            [dim_15_x - 0.1, min_y, 0],
            [dim_15_x + 0.1, min_y, 0],
            stroke_width=2, color=GREEN
        )
        dim_neg15_label = MathTex(r"\mathbf{-1.5}").scale(0.3).move_to([dim_15_x + 0.3, target_position[1] - elem_half_height/2, 0])
        dim_neg15_group = VGroup(dim_neg15_line, dim_neg15_tick_bottom, dim_neg15_label)
        
        # Bottom boundary function y = -1.5
        bottom_boundary = DashedLine(
            [min_x, min_y, 0],
            [max_x, min_y, 0],
            stroke_width=4, color=GREEN, dash_length=0.1
        )
        bottom_boundary_label = MathTex(r"y = -1.5").scale(0.25)
        bottom_boundary_label.move_to(target_position + RIGHT * elem_half_width_left * 0.2 + DOWN * elem_half_height - DOWN * 0.15)  # 5% left of previous
        
        # Dramatic highlighting of -1.5 - grows from the specific "-1.5" position in integral (lower position)
        integral_neg15_pos = integral_pos + LEFT * 0.5 + DOWN * 0.1  # Lower position for bottom limit
        integral_temp_large_neg15 = MathTex(r"\mathbf{-1.5}").scale(0.35).set_color(GREEN)
        integral_temp_large_neg15.move_to(integral_neg15_pos)  # Start at the "-1.5" position
        
        self.play(
            Create(dim_neg15_group), Create(bottom_boundary), FadeIn(bottom_boundary_label),
            integral_temp_large_neg15.animate.scale(3.0).move_to(integral_pos + DOWN * 0.8)  # Grow and move down
        )
        self.wait(0.5)
        self.play(integral_temp_large_neg15.animate.scale(1/3.0).move_to(integral_neg15_pos))  # Shrink back to "-1.5" position
        self.play(FadeOut(integral_temp_large_neg15))
        
        # c) Show 1 limit: highlight in integral + horizontal dimension
        integral_formula_highlighted_1 = MathTex(
            r"\mathbf{K}_1 = \int_{-1.5}^{1.5} \int_{-1}^{\mathbf{1}} \mathbf{B}^T \mathbf{D} \mathbf{B} \, h \, dx \, dy"
        ).scale(0.35)
        integral_formula_highlighted_1.move_to(integral_pos)
        self.play(Transform(integral_formula, integral_formula_highlighted_1))
        
        # Horizontal dimension 1 (from center to right edge, below element, trimmed by 5%)
        dim_1_y = center_y - elem_half_height - 0.4 - 0.04 * config.frame_height  # Below element, 4% lower
        dim_1_line = Line(
            [center_x, dim_1_y, 0],
            [center_x + elem_half_width_right, dim_1_y, 0],  # <-- zostaje, bo już jest pełne
            stroke_width=2, color=BLUE
        )
        dim_1_tick_right = Line(
            [center_x + elem_half_width_right, dim_1_y - 0.1, 0],
            [center_x + elem_half_width_right, dim_1_y + 0.1, 0],
            stroke_width=2, color=BLUE
        )
        dim_1_tick_center = Line(
            [center_x, dim_1_y - 0.1, 0],
            [center_x, dim_1_y + 0.1, 0],
            stroke_width=2, color=BLUE
        )
        dim_1_label = MathTex(r"\mathbf{1}").scale(0.3).move_to([center_x + elem_half_width_right/2, dim_1_y - 0.2, 0])
        dim_1_group = VGroup(dim_1_line, dim_1_tick_right, dim_1_tick_center, dim_1_label)
        
        # Dramatic highlighting of 1 - grows from the specific "1" position in integral (14% left)
        integral_1_pos = integral_pos + RIGHT * (1.8 - 0.14 * config.frame_width) + UP * 0.1  # 14% left from previous position
        integral_temp_large_1 = MathTex(r"\mathbf{1}").scale(0.35).set_color(BLUE)
        integral_temp_large_1.move_to(integral_1_pos)  # Start at the "1" position
        
        self.play(
            Create(dim_1_group),
            integral_temp_large_1.animate.scale(3.0).move_to(integral_pos + RIGHT * 1.0)  # Grow and move right
        )
        self.wait(0.5)
        self.play(integral_temp_large_1.animate.scale(1/3.0).move_to(integral_1_pos))  # Shrink back to "1" position
        self.play(FadeOut(integral_temp_large_1))
        
        # d) Show -1 limit: highlight in integral + horizontal dimension  
        integral_formula_highlighted_neg1 = MathTex(
            r"\mathbf{K}_1 = \int_{-1.5}^{1.5} \int_{\mathbf{-1}}^{1} \mathbf{B}^T \mathbf{D} \mathbf{B} \, h \, dx \, dy"
        ).scale(0.35)
        integral_formula_highlighted_neg1.move_to(integral_pos)
        self.play(Transform(integral_formula, integral_formula_highlighted_neg1))
        
        # Horizontal dimension -1 (from center to left edge, below element, shortened by 35%)
        dim_neg1_line = Line(
            [center_x, dim_1_y, 0],  # Center
            [center_x - elem_half_width_left, dim_1_y, 0],  # Left edge (trimmed by 15%)
            stroke_width=2, color=BLUE
        )
        dim_neg1_tick_left = Line(
            [center_x - elem_half_width_left, dim_1_y - 0.1, 0],
            [center_x - elem_half_width_left, dim_1_y + 0.1, 0],
            stroke_width=2, color=BLUE
        )
        dim_neg1_label = MathTex(r"\mathbf{-1}").scale(0.3).move_to([center_x - elem_half_width_left/2, dim_1_y - 0.2, 0])
        dim_neg1_group = VGroup(dim_neg1_line, dim_neg1_tick_left, dim_neg1_label)
        
        # Dramatic highlighting of -1 - grows from the specific "-1" position in integral (in down and right from "1")
        integral_neg1_pos = integral_pos + RIGHT * (1.8 - 0.14 * config.frame_width) + DOWN * 0.1  # Same horizontal as "1" but lower
        integral_temp_large_neg1 = MathTex(r"\mathbf{-1}").scale(0.35).set_color(BLUE)
        integral_temp_large_neg1.move_to(integral_neg1_pos)  # Start at the "-1" position
        
        self.play(
            Create(dim_neg1_group),
            integral_temp_large_neg1.animate.scale(3.0).move_to(integral_pos + LEFT * 1.0)  # Grow and move left
        )
        self.wait(0.5)
        self.play(integral_temp_large_neg1.animate.scale(1/3.0).move_to(integral_neg1_pos))  # Shrink back to "-1" position
        self.play(FadeOut(integral_temp_large_neg1))

        # ----- Final hold -----
        self.wait(3)

        # ============================================================
        # NEW STEP: cleanup + move only the integral + show Bt*D*B*h
        # ============================================================

        # 1) Fade out all matrix expressions + titles from previous step
        to_fade = VGroup(
            full_b_matrix,          # numeric B
            d_matrix_group,         # D title + symbolic + "=" + numeric
            bt_matrix_title,        # "Transposed B matrix:"
            bt_matrix,              # B^T matrix itself
            integral_title          # "Element stiffness matrix:"
        )
        self.play(FadeOut(to_fade))

        # 2) Keep ONLY integral_formula and move it up under the horizontal dimension (-1..1)
        integral_target_pos = np.array([center_x, dim_1_y - 0.55, 0])  # pod wymiar -1..1
        self.play(integral_formula.animate.move_to(integral_target_pos).scale(1.05))

        # 3) Show the integrand matrix: B^T * D * B * h
        integrand_title = MathTex(r"\mathbf{B}^T \mathbf{D}\mathbf{B}\,h \;=\;").scale(0.40)
        integrand_title.next_to(integral_formula, DOWN, buff=0.25)
        integrand_title.move_to([0, integrand_title.get_center()[1], 0])  # center X

        BTDBh_tex = r"""
        \begin{bmatrix}
        0.025\left(4.633 x - 4.633\right)\left(x-1\right) + 0.013\left(14.250 y - 21.375\right)\left(2y-3\right) &
        0.025\left(x-1\right)\left(4.983 y - 7.475\right) + 0.013\left(4.633 x - 4.633\right)\left(2y-3\right) &
        -0.025\left(4.633 x - 4.633\right)\left(x+1\right) - 0.013\left(14.250 y - 21.375\right)\left(2y-3\right) &
        -0.025\left(x+1\right)\left(4.983 y - 7.475\right) - 0.013\left(4.633 x - 4.633\right)\left(2y-3\right) &
        0.025\left(4.633 x - 4.633\right)\left(x+1\right) + 0.013\left(14.250 y - 21.375\right)\left(2y+3\right) &
        0.025\left(x+1\right)\left(4.983 y - 7.475\right) + 0.013\left(4.633 x - 4.633\right)\left(2y+3\right) &
        -0.025\left(4.633 x - 4.633\right)\left(x-1\right) - 0.013\left(14.250 y - 21.375\right)\left(2y+3\right) &
        -0.025\left(x-1\right)\left(4.983 y - 7.475\right) - 0.013\left(4.633 x - 4.633\right)\left(2y+3\right)
        \\
        0.025\left(x-1\right)\left(4.633 y - 6.950\right) + 0.013\left(4.983 x - 4.983\right)\left(2y-3\right) &
        0.025\left(14.250 x - 14.250\right)\left(x-1\right) + 0.013\left(4.633 y - 6.950\right)\left(2y-3\right) &
        -0.025\left(x+1\right)\left(4.633 y - 6.950\right) - 0.013\left(4.983 x - 4.983\right)\left(2y-3\right) &
        -0.025\left(14.250 x - 14.250\right)\left(x+1\right) - 0.013\left(4.633 y - 6.950\right)\left(2y-3\right) &
        0.025\left(x+1\right)\left(4.633 y - 6.950\right) + 0.013\left(4.983 x - 4.983\right)\left(2y+3\right) &
        0.025\left(14.250 x - 14.250\right)\left(x+1\right) + 0.013\left(4.633 y - 6.950\right)\left(2y+3\right) &
        -0.025\left(x-1\right)\left(4.633 y - 6.950\right) - 0.013\left(4.983 x - 4.983\right)\left(2y+3\right) &
        -0.025\left(14.250 x - 14.250\right)\left(x-1\right) - 0.013\left(4.633 y - 6.950\right)\left(2y+3\right)
        \\
        0.025\left(x-1\right)\left(-4.633 x - 4.633\right) + 0.013\left(2y-3\right)\left(-14.250 y + 21.375\right) &
        0.013\left(-4.633 x - 4.633\right)\left(2y-3\right) + 0.025\left(x-1\right)\left(-4.983 y + 7.475\right) &
        -0.025\left(x+1\right)\left(-4.633 x - 4.633\right) - 0.013\left(2y-3\right)\left(-14.250 y + 21.375\right) &
        -0.013\left(-4.633 x - 4.633\right)\left(2y-3\right) - 0.025\left(x+1\right)\left(-4.983 y + 7.475\right) &
        0.025\left(x+1\right)\left(-4.633 x - 4.633\right) + 0.013\left(2y+3\right)\left(-14.250 y + 21.375\right) &
        0.013\left(-4.633 x - 4.633\right)\left(2y+3\right) + 0.025\left(x+1\right)\left(-4.983 y + 7.475\right) &
        -0.025\left(x-1\right)\left(-4.633 x - 4.633\right) - 0.013\left(2y+3\right)\left(-14.250 y + 21.375\right) &
        -0.013\left(-4.633 x - 4.633\right)\left(2y+3\right) - 0.025\left(x-1\right)\left(-4.983 y + 7.475\right)
        \\
        0.013\left(-4.983 x - 4.983\right)\left(2y-3\right) + 0.025\left(x-1\right)\left(-4.633 y + 6.950\right) &
        0.025\left(x-1\right)\left(-14.250 x - 14.250\right) + 0.013\left(2y-3\right)\left(-4.633 y + 6.950\right) &
        -0.013\left(-4.983 x - 4.983\right)\left(2y-3\right) - 0.025\left(x+1\right)\left(-4.633 y + 6.950\right) &
        -0.025\left(x+1\right)\left(-14.250 x - 14.250\right) - 0.013\left(2y-3\right)\left(-4.633 y + 6.950\right) &
        0.013\left(-4.983 x - 4.983\right)\left(2y+3\right) + 0.025\left(x+1\right)\left(-4.633 y + 6.950\right) &
        0.025\left(x+1\right)\left(-14.250 x - 14.250\right) + 0.013\left(2y+3\right)\left(-4.633 y + 6.950\right) &
        -0.013\left(-4.983 x - 4.983\right)\left(2y+3\right) - 0.025\left(x-1\right)\left(-4.633 y + 6.950\right) &
        -0.025\left(x-1\right)\left(-14.250 x - 14.250\right) - 0.013\left(2y+3\right)\left(-4.633 y + 6.950\right)
        \\
        0.025\left(4.633 x + 4.633\right)\left(x-1\right) + 0.013\left(14.250 y + 21.375\right)\left(2y-3\right) &
        0.025\left(x-1\right)\left(4.983 y + 7.475\right) + 0.013\left(4.633 x + 4.633\right)\left(2y-3\right) &
        -0.025\left(4.633 x + 4.633\right)\left(x+1\right) - 0.013\left(14.250 y + 21.375\right)\left(2y-3\right) &
        -0.025\left(x+1\right)\left(4.983 y + 7.475\right) - 0.013\left(4.633 x + 4.633\right)\left(2y-3\right) &
        0.025\left(4.633 x + 4.633\right)\left(x+1\right) + 0.013\left(14.250 y + 21.375\right)\left(2y+3\right) &
        0.025\left(x+1\right)\left(4.983 y + 7.475\right) + 0.013\left(4.633 x + 4.633\right)\left(2y+3\right) &
        -0.025\left(4.633 x + 4.633\right)\left(x-1\right) - 0.013\left(14.250 y + 21.375\right)\left(2y+3\right) &
        -0.025\left(x-1\right)\left(4.983 y + 7.475\right) - 0.013\left(4.633 x + 4.633\right)\left(2y+3\right)
        \\
        0.025\left(x-1\right)\left(4.633 y + 6.950\right) + 0.013\left(4.983 x + 4.983\right)\left(2y-3\right) &
        0.025\left(14.250 x + 14.250\right)\left(x-1\right) + 0.013\left(4.633 y + 6.950\right)\left(2y-3\right) &
        -0.025\left(x+1\right)\left(4.633 y + 6.950\right) - 0.013\left(4.983 x + 4.983\right)\left(2y-3\right) &
        -0.025\left(14.250 x + 14.250\right)\left(x+1\right) - 0.013\left(4.633 y + 6.950\right)\left(2y-3\right) &
        0.025\left(x+1\right)\left(4.633 y + 6.950\right) + 0.013\left(4.983 x + 4.983\right)\left(2y+3\right) &
        0.025\left(14.250 x + 14.250\right)\left(x+1\right) + 0.013\left(4.633 y + 6.950\right)\left(2y+3\right) &
        -0.025\left(x-1\right)\left(4.633 y + 6.950\right) - 0.013\left(4.983 x + 4.983\right)\left(2y+3\right) &
        -0.025\left(14.250 x + 14.250\right)\left(x-1\right) - 0.013\left(4.633 y + 6.950\right)\left(2y+3\right)
        \\
        0.025\left(x-1\right)\left(-4.633 x + 4.633\right) + 0.013\left(2y-3\right)\left(-14.250 y - 21.375\right) &
        0.013\left(-4.633 x + 4.633\right)\left(2y-3\right) + 0.025\left(x-1\right)\left(-4.983 y - 7.475\right) &
        -0.025\left(x+1\right)\left(-4.633 x + 4.633\right) - 0.013\left(2y-3\right)\left(-14.250 y - 21.375\right) &
        -0.013\left(-4.633 x + 4.633\right)\left(2y-3\right) - 0.025\left(x+1\right)\left(-4.983 y - 7.475\right) &
        0.025\left(x+1\right)\left(-4.633 x + 4.633\right) + 0.013\left(2y+3\right)\left(-14.250 y - 21.375\right) &
        0.013\left(-4.633 x + 4.633\right)\left(2y+3\right) + 0.025\left(x+1\right)\left(-4.983 y - 7.475\right) &
        -0.025\left(x-1\right)\left(-4.633 x + 4.633\right) - 0.013\left(2y+3\right)\left(-14.250 y - 21.375\right) &
        -0.013\left(-4.633 x + 4.633\right)\left(2y+3\right) - 0.025\left(x-1\right)\left(-4.983 y - 7.475\right)
        \\
        0.013\left(-4.983 x + 4.983\right)\left(2y-3\right) + 0.025\left(x-1\right)\left(-4.633 y - 6.950\right) &
        0.025\left(x-1\right)\left(-14.250 x + 14.250\right) + 0.013\left(2y-3\right)\left(-4.633 y - 6.950\right) &
        -0.013\left(-4.983 x + 4.983\right)\left(2y-3\right) - 0.025\left(x+1\right)\left(-4.633 y - 6.950\right) &
        -0.025\left(x+1\right)\left(-14.250 x + 14.250\right) - 0.013\left(2y-3\right)\left(-4.633 y - 6.950\right) &
        0.013\left(-4.983 x + 4.983\right)\left(2y+3\right) + 0.025\left(x+1\right)\left(-4.633 y - 6.950\right) &
        0.025\left(x+1\right)\left(-14.250 x + 14.250\right) + 0.013\left(2y+3\right)\left(-4.633 y - 6.950\right) &
        -0.013\left(-4.983 x + 4.983\right)\left(2y+3\right) - 0.025\left(x-1\right)\left(-4.633 y - 6.950\right) &
        -0.025\left(x-1\right)\left(-14.250 x + 14.250\right) - 0.013\left(2y+3\right)\left(-4.633 y - 6.950\right)
        \end{bmatrix}
        """

        # ------------------------------------------------------------
        # Integrand: split 8x8 matrix into two 8x4 blocks stacked
        # ------------------------------------------------------------

        integrand_title = MathTex(r"\mathbf{B}^T \mathbf{D}\mathbf{B}\,h \;=\;").scale(0.42)
        integrand_title.next_to(integral_formula, DOWN, buff=0.22)
        integrand_title.move_to([0, integrand_title.get_center()[1], 0])  # center X


        def split_bmatrix_into_two(BTDBh_tex: str):
            """Return (left_tex, right_tex) where each is an 8x4 bmatrix as a LaTeX string."""
            s = BTDBh_tex.strip()

            begin_tag = r"\begin{bmatrix}"
            end_tag = r"\end{bmatrix}"
            i0 = s.find(begin_tag)
            i1 = s.rfind(end_tag)
            if i0 == -1 or i1 == -1:
                raise ValueError("BTDBh_tex must contain \\begin{bmatrix} ... \\end{bmatrix}")

            body = s[i0 + len(begin_tag):i1].strip()

            raw_rows = [r.strip() for r in body.split(r"\\") if r.strip()]
            rows_cols = []
            for r in raw_rows:
                cols = [c.strip() for c in r.split("&")]
                if len(cols) != 8:
                    raise ValueError(f"Expected 8 columns per row, got {len(cols)} in row:\n{r}")
                rows_cols.append(cols)

            left_rows = [row[:4] for row in rows_cols]
            right_rows = [row[4:] for row in rows_cols]

            def build_bmatrix(rows_4cols):
                lines = []
                for row in rows_4cols:
                    lines.append(" & ".join(row))
                return r"\begin{bmatrix}" + "\n" + r"\\ ".join(lines) + "\n" + r"\end{bmatrix}"

            return build_bmatrix(left_rows), build_bmatrix(right_rows)


        BTDBh_left_tex, BTDBh_right_tex = split_bmatrix_into_two(BTDBh_tex)

        integrand_left = MathTex(BTDBh_left_tex)
        integrand_right = MathTex(BTDBh_right_tex)

        # Layout parameters
        left_margin = 0.20
        right_margin = 0.20
        block_width = config.frame_width * 0.90  # stabilniej niż kombinacje z marginami

        # First block: full width-ish, glued to left
        integrand_left.set_width(block_width)
        integrand_left.next_to(integrand_title, DOWN, buff=0.10)

        frame_left_x = -config.frame_width / 2 + left_margin
        integrand_left.shift(RIGHT * (frame_left_x - integrand_left.get_left()[0]))

        # Second block: same width, but shifted right (start at ~10% frame)
        integrand_right.set_width(block_width)
        integrand_right.next_to(integrand_left, DOWN, buff=0.12)

        start_10_x = -config.frame_width / 2 + 0.10 * config.frame_width + left_margin * 0.2
        integrand_right.shift(RIGHT * (start_10_x - integrand_right.get_left()[0]))

        # --- HARD CLAMP: keep integrand_right fully inside frame horizontally ---
        frame_left = -config.frame_width / 2 + left_margin
        frame_right =  config.frame_width / 2 - right_margin

        # if it goes out on the right, shift left
        over_right = integrand_right.get_right()[0] - frame_right
        if over_right > 0:
            integrand_right.shift(LEFT * over_right)

        # if it goes out on the left (rare), shift right
        over_left = frame_left - integrand_right.get_left()[0]
        if over_left > 0:
            integrand_right.shift(RIGHT * over_left)

        integrand_group = VGroup(integrand_title, integrand_left, integrand_right)

        # Bottom clamp for integrand group
        bottom_margin_integrand = 0.35
        bottom_limit_integrand = -config.frame_height / 2 + bottom_margin_integrand
        if integrand_group.get_bottom()[1] < bottom_limit_integrand:
            integrand_group.shift(UP * (bottom_limit_integrand - integrand_group.get_bottom()[1]))

        # --- IMPORTANT: z-index so integrand never gets covered later ---
        integrand_title.set_z_index(30)
        integrand_left.set_z_index(30)
        integrand_right.set_z_index(30)

        # Animate integrand
        self.play(FadeIn(integrand_title))
        self.play(FadeIn(integrand_left))
        self.play(FadeIn(integrand_right))

        # ============================================================
        # STEP: keep only first element of BTDBh (a_11), enlarge it
        # ============================================================

        # 1) Fade out the two big strips (we replace them by a_11 cleanly)
        self.play(FadeOut(integrand_left), FadeOut(integrand_right))

        # 2) Create a clean first-entry formula a_11(x,y)
        a11_tex = (
            r"a_{11}(x,y)="
            r"0.025\left(4.633 x - 4.633\right)\left(x-1\right)"
            r"+0.013\left(14.250 y - 21.375\right)\left(2y-3\right)"
        )
        a11 = MathTex(a11_tex).scale(0.55)
        a11.next_to(integrand_title, DOWN, buff=0.18)
        a11.move_to([0, a11.get_center()[1], 0])

        # 3) Emphasize / enlarge
        self.play(FadeIn(a11))
        self.play(a11.animate.scale(1.35).shift(UP*0.05))

        # ============================================================
        # STEP: double integration of a_11 over x∈[-1,1], y∈[-1.5,1.5]
        # ============================================================

        # Show the target integral for K_11 (correct limits)
        k11_int_0 = MathTex(
            r"K_{11}=\int_{-1.5}^{1.5}\int_{-1}^{1} a_{11}(x,y)\,dx\,dy"
        ).scale(0.50)
        k11_int_0.next_to(a11, DOWN, buff=0.22)
        k11_int_0.move_to([0, k11_int_0.get_center()[1], 0])
        self.play(FadeIn(k11_int_0))

        # Timing (as you had)
        TRANSFORM_RT = 1.6   # czas przekształcenia (sekundy)
        PAUSE_T = 0.6        # pauza między krokami

        # Substitute a11(x,y) (correct limits)
        k11_int_1 = MathTex(
            r"K_{11}=\int_{-1.5}^{1.5}\int_{-1}^{1}"
            r"\Big("
            r"0.025(4.633x-4.633)(x-1)"
            r"+0.013(14.250y-21.375)(2y-3)"
            r"\Big)\,dx\,dy"
        ).scale(0.42)
        k11_int_1.next_to(a11, DOWN, buff=0.22)
        k11_int_1.move_to([0, k11_int_1.get_center()[1], 0])

        self.play(Transform(k11_int_0, k11_int_1), run_time=TRANSFORM_RT)
        self.wait(PAUSE_T)

        # Integrate w.r.t. x first (correct limits)
        k11_int_2 = MathTex(
            r"K_{11}=\int_{-1.5}^{1.5}\left[ \int_{-1}^{1} 0.025(4.633x-4.633)(x-1)\,dx \right]dy"
            r"+\int_{-1.5}^{1.5}\left[\int_{-1}^{1} 0.013(14.250y-21.375)(2y-3)\,dx\right]dy"
        ).scale(0.36)
        k11_int_2.next_to(a11, DOWN, buff=0.22)
        k11_int_2.move_to([0, k11_int_2.get_center()[1], 0])

        self.play(Transform(k11_int_0, k11_int_2), run_time=TRANSFORM_RT)
        self.wait(PAUSE_T)

        # Second term independent of x => inner integral gives factor 2 (still correct limits)
        k11_int_3 = MathTex(
            r"K_{11}=\int_{-1.5}^{1.5}\left[ \int_{-1}^{1} 0.025(4.633x-4.633)(x-1)\,dx \right]dy"
            r"+\int_{-1.5}^{1.5} \left[ 2\cdot 0.013(14.250y-21.375)(2y-3)\right]dy"
        ).scale(0.36)
        k11_int_3.next_to(a11, DOWN, buff=0.22)
        k11_int_3.move_to([0, k11_int_3.get_center()[1], 0])

        self.play(Transform(k11_int_0, k11_int_3), run_time=TRANSFORM_RT)
        self.wait(PAUSE_T)

        # Final numeric result (your computed K1 matrix)
        k11_value = MathTex(r"K_{11}=7\,339\,166.7").scale(0.60)
        k11_value.next_to(k11_int_0, DOWN, buff=0.22)
        k11_value.move_to([0, k11_value.get_center()[1], 0])

        self.play(FadeIn(k11_value))
        self.wait(1)


        # ============================================================
        # STEP: Build resulting K, starting from K_11  (ROBUST, ALWAYS VISIBLE)
        # ============================================================

        # Clean up: keep only K_11 value for a moment
        self.play(FadeOut(integrand_title), FadeOut(a11), FadeOut(k11_int_0))

        # ----------------------------
        # Controls (tune only here)
        # ----------------------------
        # Where to place the matrix block (absolute Y in scene coords)
        target_y = -config.frame_height * 0.30   # lower part of screen, but not at the very bottom

        # Hard size limits for the whole block (title + matrix)
        max_w = config.frame_width * 0.96
        max_h = config.frame_height * 0.34       # increase to 0.38 if you still want bigger

        # Typography / spacing
        title_scale = 0.62

        entry_scale = 0.60          # size of numeric entries (after shortening)
        box_scale   = 0.62          # size of boxes
        num_x_squash = 0.92         # horizontal squeeze for digits (Community Manim friendly)

        h_buff = 1.05               # IMPORTANT: column spacing
        v_buff = 0.34               # row spacing
        title_gap = 0.20

        top_margin = 0.40
        bottom_margin = 0.25

        # ------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------
        def clamp_to_frame(mobj, top_margin=0.4, bottom_margin=0.25):
            top_limit = config.frame_height/2 - top_margin
            bottom_limit = -config.frame_height/2 + bottom_margin
            if mobj.get_top()[1] > top_limit:
                mobj.shift(DOWN * (mobj.get_top()[1] - top_limit))
            if mobj.get_bottom()[1] < bottom_limit:
                mobj.shift(UP * (bottom_limit - mobj.get_bottom()[1]))

        def fit_uniform(mobj, max_w, max_h):
            if mobj.width == 0 or mobj.height == 0:
                return
            s = min(max_w / mobj.width, max_h / mobj.height, 1.0)
            mobj.scale(s)

        def fmt_num(s: str) -> str:
            # reserve minus sign width + add thinspace at end to visually separate columns
            s = s.strip()
            if s.startswith("-"):
                return s + r"\,"
            return r"\phantom{-}" + s + r"\,"

        # ------------------------------------------------------------
        # Data: skeleton + VISUAL numeric matrix (scaled by 10^6)
        # ------------------------------------------------------------
        boxes_data = [[r"\Box"] * 8 for _ in range(8)]

        K1_data_vis = [
            ["7.34", "2.16", "-5.95", "0.08", "-3.67", "-2.16", "2.28", "-0.08"],
            ["2.16", "4.94", "-0.08", "-0.66", "-2.16", "-2.47", "0.08", "-1.81"],
            ["-5.95","-0.08","7.34", "-2.16", "2.28", "0.08", "-3.67","2.16"],
            ["0.08", "-0.66","-2.16","4.94", "-0.08","-1.81","2.16", "-2.47"],
            ["-3.67","-2.16","2.28","-0.08","7.34","2.16","-5.95","0.08"],
            ["-2.16","-2.47","0.08","-1.81","2.16","4.94","-0.08","-0.66"],
            ["2.28","0.08","-3.67","2.16","-5.95","-0.08","7.34","-2.16"],
            ["-0.08","-1.81","2.16","-2.47","0.08","-0.66","-2.16","4.94"],
        ]

        # ------------------------------------------------------------
        # Title: K1 = 10^6 ·
        # ------------------------------------------------------------
        K_title = MathTex(r"\mathbf{K}_1 = 10^6 \cdot").scale(title_scale)

        # ------------------------------------------------------------
        # Build numeric matrix FIRST (target geometry)
        # ------------------------------------------------------------
        def num_entry_mobj(s: str):
            m = MathTex(fmt_num(s)).scale(entry_scale)
            m.scale([num_x_squash, 1, 1])  # <-- works in Community Manim
            return m

        K_full = Matrix(
            K1_data_vis,
            element_to_mobject=num_entry_mobj,
            h_buff=h_buff,
            v_buff=v_buff,
        )

        K_full_pack = VGroup(K_title, K_full).arrange(RIGHT, buff=title_gap)

        # Put it where we want (absolute), then fit and clamp
        K_full_pack.move_to([0, target_y, 0])
        fit_uniform(K_full_pack, max_w, max_h)
        clamp_to_frame(K_full_pack, top_margin, bottom_margin)

        # ------------------------------------------------------------
        # Build skeleton matrix and match EXACTLY to numeric geometry
        # ------------------------------------------------------------
        def box_entry_mobj(s: str):
            return MathTex(s).scale(box_scale)

        K_skel = Matrix(
            boxes_data,
            element_to_mobject=box_entry_mobj,
            h_buff=h_buff,
            v_buff=v_buff,
        )

        # match size to numeric matrix part only, then build pack in the same place
        K_skel.match_width(K_full)
        K_skel.match_height(K_full)
        K_skel.move_to(K_full.get_center())

        K_skel_pack = VGroup(K_title.copy(), K_skel).arrange(RIGHT, buff=title_gap)
        K_skel_pack.move_to(K_full_pack.get_center())

        # ------------------------------------------------------------
        # Show skeleton (this MUST appear now)
        # ------------------------------------------------------------
        self.play(FadeIn(K_skel_pack), run_time=0.8)

        # ------------------------------------------------------------
        # Move K11 value into first box (0,0)
        # Since we show 10^6 factor, display 7.34
        # ------------------------------------------------------------
        k11_vis = MathTex(fmt_num("7.34")).scale(entry_scale)
        k11_vis.scale([num_x_squash, 1, 1])
        k11_vis.move_to(k11_value.get_center())

        self.play(Transform(k11_value, k11_vis), run_time=0.6)

        k11_cell = K_skel.get_entries()[0]  # (0,0)
        self.play(k11_value.animate.move_to(k11_cell.get_center()), run_time=0.9)
        self.wait(0.2)

        # ------------------------------------------------------------
        # Swap skeleton -> numeric
        # ------------------------------------------------------------
        self.play(FadeOut(K_skel_pack), FadeIn(K_full_pack), run_time=1.0)

        # Remove the moved-in standalone number (now redundant)
        self.play(FadeOut(k11_value), run_time=0.3)

        self.wait(2.0)

        # ============================================================
        # NEXT STEP: clear side sketches, remove integral, re-layout
        # ============================================================

        # 1) Hide left & right full-structure sketches
        # (they exist in your scene; just fade them out)
        self.play(
            FadeOut(miniatura_all_with_labels),
            FadeOut(discretized_group),
            run_time=0.9
        )

        # 2) Remove the integral formula if it is still on screen
        # (safe try: if not present, no harm as long as it's defined; in your code it is)
        self.play(FadeOut(integral_formula), run_time=0.6)

        # 3) Move element 1 + all its boundary/dimension decorations to the LEFT edge
        # We'll collect everything that visually belongs to the element+limits.
        # Use what is present in your code: elem1_full_copy, coord_system, syn_dof_systems,
        # plus the green/blue dimension groups and boundary labels.
        element_with_limits = VGroup(
            elem1_full_copy,
            coord_system,
            syn_dof_systems,
            # green y-limits
            dim_15_group, dim_neg15_group,
            top_boundary, top_boundary_label,
            bottom_boundary, bottom_boundary_label,
            # blue x-limits
            dim_1_group, dim_neg1_group,
        )

        self.play(
            element_with_limits.animate.to_edge(LEFT, buff=0.35),
            run_time=1.0
        )

        # 4) Move numeric stiffness matrix K1 up under the top edge and shrink a bit
        self.play(
            K_full_pack.animate
                .scale(0.85)
                .to_edge(UP, buff=0.25),
            run_time=1.0
        )

        # Optional short pause
        self.wait(1.0)

        # ============================================================
        # TOPOLOGY MATRIX (Element 1): rows = global Q, cols = elem DOF
        # ============================================================

        # --- Element 1 mapping: i=6, j=1, k=2, r=5 ---
        # Columns: [ih, iv, jh, jv, kh, kv, rh, rv]
        # Ones:
        # Q11 -> ih, Q12 -> iv
        # Q1  -> jh, Q2  -> jv
        # Q3  -> kh, Q4  -> kv
        # Q9  -> rh, Q10 -> rv

        def red_digit(s: str):
            return MathTex(s).set_color(RED).scale(0.55)

        # build 12x8 data
        Z, O = "0", "1"
        topo_data = [[Z]*8 for _ in range(12)]
        def set1(q_row, col): topo_data[q_row][col] = O

        # cols: 0 ih,1 iv,2 jh,3 jv,4 kh,5 kv,6 rh,7 rv
        set1(10, 0)  # Q11 -> ih
        set1(11, 1)  # Q12 -> iv
        set1(0,  2)  # Q1  -> jh
        set1(1,  3)  # Q2  -> jv
        set1(2,  4)  # Q3  -> kh
        set1(3,  5)  # Q4  -> kv
        set1(8,  6)  # Q9  -> rh
        set1(9,  7)  # Q10 -> rv

        # matrix
        topo_M = Matrix(
            topo_data,
            element_to_mobject=red_digit,
            h_buff=0.55,
            v_buff=0.33,
        )

        # --- column headers ---
        col_headers = ["ih", "iv", "jh", "jv", "kh", "kv", "rh", "rv"]
        col_labels = VGroup(*[MathTex(h).scale(0.45) for h in col_headers])

        entries = topo_M.get_entries()
        for j in range(8):
            top_entry = entries[j]  # row 0 col j
            col_labels[j].move_to(top_entry.get_center() + UP * 0.55)

        # --- row labels Q1..Q12 (PLACE THEM WITH A HARD GAP FROM MATRIX BRACKET) ---
        row_labels = VGroup(*[MathTex(fr"Q_{{{k}}}").scale(0.55) for k in range(1, 13)])

        # hard geometry gaps (tune here)
        gap_Q_to_matrix   = 0.40   # bigger -> Q further left (fix overlap)
        gap_brace_to_Q    = 0.18
        gap_circle_to_brace = 0.22

        x_mat_left = topo_M.get_left()[0]
        for i in range(12):
            y = entries[i*8].get_center()[1]
            # put label center so that its RIGHT edge sits gap_Q_to_matrix left of matrix left edge
            row_labels[i].move_to([x_mat_left - gap_Q_to_matrix - row_labels[i].width/2, y, 0])

        # --- braces + node circles (NOW they won't collide) ---
        pair_braces = VGroup()
        node_circles = VGroup()

        for p in range(6):
            r0 = 2*p
            r1 = 2*p + 1

            pair_vg = VGroup(row_labels[r0], row_labels[r1])
            brace = Brace(pair_vg, LEFT, buff=gap_brace_to_Q)

            circ = Circle(radius=0.18, color=BLUE, stroke_width=3)
            num = MathTex(str(p+1)).scale(0.45).set_color(BLUE)
            circ_grp = VGroup(circ, num)
            circ_grp.next_to(brace, LEFT, buff=gap_circle_to_brace)

            pair_braces.add(brace)
            node_circles.add(circ_grp)

        # --- pack + position ---
        topo_pack = VGroup(topo_M, col_labels, row_labels, pair_braces, node_circles)

        # place it (as before): under K1, pushed to right
        topo_pack.next_to(K_full_pack, DOWN, buff=0.35)
        topo_pack.to_edge(RIGHT, buff=0.35)

        # vertical clamp
        bottom_limit = -config.frame_height/2 + 0.25
        if topo_pack.get_bottom()[1] < bottom_limit:
            topo_pack.shift(UP * (bottom_limit - topo_pack.get_bottom()[1]))

        # animate
        self.play(FadeIn(topo_M), run_time=0.8)
        self.play(LaggedStartMap(FadeIn, col_labels, lag_ratio=0.08), run_time=0.6)
        self.play(LaggedStartMap(FadeIn, row_labels, lag_ratio=0.05), run_time=0.6)
        self.play(LaggedStartMap(FadeIn, pair_braces, lag_ratio=0.08), run_time=0.6)
        self.play(LaggedStartMap(FadeIn, node_circles, lag_ratio=0.08), run_time=0.6)
        self.wait(2.0)


        # ============================================================
        # FINAL LAYOUT + MAGIC: K1 (with DOF labels) + T highlighting + KG^(1) assembly
        # Wklej po tym, jak masz na ekranie: K_full_pack, K_full, topo_pack, topo_M, row_labels, col_labels
        # ============================================================

        # ----------------------------
        # 0) Make sure K1 + T are smaller so KG can dominate
        # ----------------------------
        self.play(
            K_full_pack.animate.scale(0.78).to_edge(UP, buff=0.22).shift(LEFT * 0.20),
            topo_pack.animate.scale(0.85).to_edge(RIGHT, buff=0.25).shift(DOWN * 0.05),
            run_time=0.9
        )

        # ----------------------------
        # 1) Add DOF labels to K1 (top + left): ih iv jh jv kh kv rh rv
        # ----------------------------
        dof_names = ["ih", "iv", "jh", "jv", "kh", "kv", "rh", "rv"]

        # K_full is your Matrix(8x8)
        K_entries = K_full.get_entries()  # 64 entries, row-major

        K_col_dofs = VGroup(*[MathTex(n).scale(0.42) for n in dof_names])

        # place column DOFs above row 0 entries
        for j in range(8):
            e = K_entries[j]  # row 0 col j
            K_col_dofs[j].move_to(e.get_center() + UP * 0.28)


        # --- ROW DOFs (local) moved to the RIGHT of K1 ---
        K_row_dofs = VGroup(*[MathTex(n).scale(0.42) for n in dof_names])

        x_right = max(e.get_right()[0] for e in K_entries) + 0.45

        for i in range(8):
            e = K_entries[i * 8]  # row i, col 0
            K_row_dofs[i].move_to([x_right, e.get_center()[1], 0])

        K_dofs_pack = VGroup(K_col_dofs, K_row_dofs)
        self.play(FadeIn(K_dofs_pack), run_time=0.6)


        # ----------------------------
        # 2) Build GLOBAL matrix KG^(1) as wide rectangles (12x12), big & readable
        # ----------------------------
        # Mapping local DOF index -> global Q index (0-based for Q1..Q12)
        loc_to_glob = {
            0: 10,  # ih -> Q11
            1: 11,  # iv -> Q12
            2: 0,   # jh -> Q1
            3: 1,   # jv -> Q2
            4: 2,   # kh -> Q3
            5: 3,   # kv -> Q4
            6: 8,   # rh -> Q9
            7: 9,   # rv -> Q10
        }

        # Geometry for KG grid
        cell_w = 0.44   # wide
        cell_h = 0.30   # shorter -> rectangles
        grid_cols = 12
        grid_rows = 12

        # top-left anchor for grid (we position later)
        grid_cells = VGroup()
        for r in range(grid_rows):
            for c in range(grid_cols):
                rect = Rectangle(width=cell_w, height=cell_h, stroke_width=1.6)
                rect.set_stroke(WHITE, opacity=0.85)
                rect.set_fill(opacity=0.0)
                grid_cells.add(rect)

        # arrange into a grid manually
        grid_group = VGroup()
        idx = 0
        for r in range(grid_rows):
            row = VGroup()
            for c in range(grid_cols):
                row.add(grid_cells[idx])
                idx += 1
            row.arrange(RIGHT, buff=0.0)
            grid_group.add(row)
        grid_group.arrange(DOWN, buff=0.0)


        # ------------------------------------------------------------
        # KG title + brackets (robust: always follow grid_group)
        # ------------------------------------------------------------

        kg_left_br_raw  = MathTex(r"\left[").set_color(WHITE)
        kg_right_br_raw = MathTex(r"\right]").set_color(WHITE)

        def fit_bracket_height(br, target_height, pad=1.02):
            b = br.copy()
            b.stretch_to_fit_height(target_height * pad)
            return b

        kg_left_br = always_redraw(
            lambda: fit_bracket_height(kg_left_br_raw, grid_group.height, pad=1.03)
                .next_to(grid_group, LEFT, buff=0.15)
                .align_to(grid_group, DOWN)
        )

        kg_right_br = always_redraw(
            lambda: fit_bracket_height(kg_right_br_raw, grid_group.height, pad=1.03)
                .next_to(grid_group, RIGHT, buff=0.15)
                .align_to(grid_group, DOWN)
        )

        # --- TITLE nad KG (też always_redraw, żeby nie "uciekał") ---
        kg_title = always_redraw(
            lambda: MathTex(r"\mathbf{K}_G^{(1)} =")
                .scale(0.85)
                .next_to(grid_group, UP, buff=0.55)   # <-- tu PODNOSISZ napis
        )



        # global DOF labels top (Q1..Q12) and left (Q1..Q12) for KG
        kg_top_labels = VGroup(*[MathTex(fr"Q_{{{k}}}").scale(0.45) for k in range(1, 13)])
        kg_left_labels = VGroup(*[MathTex(fr"Q_{{{k}}}").scale(0.55) for k in range(1, 13)])

        # place top labels above each column center
        for c in range(12):
            col_center = grid_group[0][c].get_center()
            kg_top_labels[c].move_to(col_center + UP * 0.40).rotate(PI/2)  # vertical like on your screenshot

        # place left labels beside each row center
        for r in range(12):
            row_center = grid_group[r][0].get_center()
            kg_left_labels[r].move_to(row_center + LEFT * 0.75)

        # braces + node circles (1..6) grouping rows by 2 (Q1..Q12)
        kg_pair_braces = VGroup()
        kg_node_circles = VGroup()
        for p in range(6):
            r0 = 2*p
            r1 = 2*p + 1
            pair = VGroup(kg_left_labels[r0], kg_left_labels[r1])
            brace = Brace(pair, LEFT, buff=0.10)
            circ = Circle(radius=0.18, color=BLUE, stroke_width=3)
            num = MathTex(str(p+1)).scale(0.45).set_color(BLUE)
            circ_grp = VGroup(circ, num).move_to(circ.get_center())
            circ_grp.next_to(brace, LEFT, buff=0.18)
            kg_pair_braces.add(brace)
            kg_node_circles.add(circ_grp)

        kg_pack = VGroup(
            kg_title,
            kg_left_br, kg_right_br,
            grid_group,
            kg_top_labels,
            kg_left_labels,
            kg_pair_braces,
            kg_node_circles
        )

        # Place KG on the bottom-left / center, big but not hitting T
        kg_pack.scale(1.05)
        kg_pack.to_edge(DOWN, buff=0.25).shift(LEFT * 1.1)

        # Safety clamp: keep inside frame
        bottom_limit = -config.frame_height/2 + 0.20
        if kg_pack.get_bottom()[1] < bottom_limit:
            kg_pack.shift(UP * (bottom_limit - kg_pack.get_bottom()[1]))

        left_limit = -config.frame_width/2 + 0.20
        if kg_pack.get_left()[0] < left_limit:
            kg_pack.shift(RIGHT * (left_limit - kg_pack.get_left()[0]))

        # Now ensure KG does NOT cover topo labels on the right:
        # if it gets too close to topo_pack, shift it left a bit more and slightly down
        if kg_pack.get_right()[0] > topo_pack.get_left()[0] - 0.25:
            kg_pack.shift(LEFT * (kg_pack.get_right()[0] - (topo_pack.get_left()[0] - 0.25)))

        self.play(FadeIn(kg_title), run_time=0.4)
        self.play(FadeIn(grid_group), FadeIn(kg_left_br), FadeIn(kg_right_br), run_time=0.7)
        self.play(LaggedStartMap(FadeIn, kg_top_labels, lag_ratio=0.03), run_time=0.6)
        self.play(LaggedStartMap(FadeIn, kg_left_labels, lag_ratio=0.03), run_time=0.6)
        self.play(LaggedStartMap(FadeIn, kg_pair_braces, lag_ratio=0.06), run_time=0.6)
        self.play(LaggedStartMap(FadeIn, kg_node_circles, lag_ratio=0.06), run_time=0.6)
        self.wait(0.5)

        # ----------------------------
        # 3) Helpers for highlighting T and moving numbers into KG
        # ----------------------------

        # --- Your topo matrix objects (rename here if different) ---
        T = topo_M        # <-- JEŚLI INNA NAZWA
        T_entries = T.get_entries()
        T_row_labels = row_labels   # <-- JEŚLI INNA NAZWA
        T_col_labels = col_labels   # <-- JEŚLI INNA NAZWA

        def T_cell_center(q_index_0based, loc_col):
            """Return center of topology entry at row q (0..11), col loc (0..7)."""
            return T_entries[q_index_0based * 8 + loc_col].get_center()

        def highlight_T_row(q_index_0based, color=YELLOW):
            row_group = VGroup(*[T_entries[q_index_0based * 8 + j] for j in range(8)])
            return SurroundingRectangle(row_group, color=color, buff=0.05)

        def highlight_T_col(loc_col, color=YELLOW):
            col_group = VGroup(*[T_entries[i * 8 + loc_col] for i in range(12)])
            return SurroundingRectangle(col_group, color=color, buff=0.05)

        def highlight_T_one(q_index_0based, loc_col, color=YELLOW):
            cell = T_entries[q_index_0based * 8 + loc_col]
            return SurroundingRectangle(cell, color=color, buff=0.04)

        # KG cell center
        def KG_cell_center(qr_0based, qc_0based):
            return grid_group[qr_0based][qc_0based].get_center()

        def highlight_KG_cell(qr_0based, qc_0based, color=YELLOW):
            return SurroundingRectangle(grid_group[qr_0based][qc_0based], color=color, buff=0.03)

        # K1 entry highlight
        def K1_entry_at(i, j):
            return K_entries[i * 8 + j]

        def highlight_K1_cell(i, j, color=YELLOW):
            return SurroundingRectangle(K1_entry_at(i, j), color=color, buff=0.04)

        # Create a number mobject for KG (bigger font)
        def make_KG_value(text):
            return MathTex(text).scale(0.33)  # bigger than before

        # ----------------------------
        # 4) "Magic" animation: show mapping using T row/col highlights + number transfer
        # ----------------------------

        # choose representative transfers (nice variety)
        demo_pairs = [
            (2, 0),  # K1[2,0] -> (jh, ih) -> (Q1,Q11)
            (0, 4),
            (6, 3),
            (3, 6),
            (2, 6),
            (6, 1),
        ]

        # build K1_data_vis from your existing list (must exist in your code)
        # K1_data_vis is 8x8 list of strings like "7.34", "-5.95", ...
        # If not present, you must use your own variable.

        placed_values = VGroup()  # keep KG values so they stay visible

        for (li, lj) in demo_pairs:
            gi = loc_to_glob[li]
            gj = loc_to_glob[lj]
            val = K1_data_vis[li][lj]

            # highlight K1 cell
            k1_h = highlight_K1_cell(li, lj, color=YELLOW)

            # highlight topology selections for row/col mapping
            # For T^T K T intuition: select column for local DOF and row for global DOF
            Tcol_i = highlight_T_col(li, color=BLUE)
            Trow_i = highlight_T_row(gi, color=BLUE)
            Tone_i = highlight_T_one(gi, li, color=YELLOW)

            Tcol_j = highlight_T_col(lj, color=GREEN)
            Trow_j = highlight_T_row(gj, color=GREEN)
            Tone_j = highlight_T_one(gj, lj, color=YELLOW)

            # highlight destination KG cell
            kg_h = highlight_KG_cell(gi, gj, color=YELLOW)

            # number copy from K1 cell and move
            moving = MathTex(val).scale(0.55)
            moving.move_to(K1_entry_at(li, lj).get_center())

            dest = make_KG_value(val)
            dest.move_to(KG_cell_center(gi, gj))

            # play
            self.play(Create(k1_h), run_time=0.20)
            self.play(Create(Tcol_i), Create(Trow_i), Create(Tone_i), run_time=0.25)
            self.play(Create(Tcol_j), Create(Trow_j), Create(Tone_j), run_time=0.25)
            self.play(Create(kg_h), run_time=0.20)

            self.play(TransformFromCopy(K1_entry_at(li, lj), moving), run_time=0.25)
            self.play(moving.animate.move_to(dest.get_center()), run_time=0.55)
            self.play(Transform(moving, dest), run_time=0.25)

            placed_values.add(dest)

            # cleanup highlights
            self.play(
                FadeOut(k1_h),
                FadeOut(Tcol_i), FadeOut(Trow_i), FadeOut(Tone_i),
                FadeOut(Tcol_j), FadeOut(Trow_j), FadeOut(Tone_j),
                FadeOut(kg_h),
                run_time=0.25
            )
            self.wait(0.10)

        # ----------------------------
        # 5) Fast fill: place remaining mapped entries quickly (optional but nice)
        # ----------------------------
        # We'll populate only the 8x8 mapped block positions in KG (because only one element).
        # Already placed some demo entries; we add the rest fast.

        already = set((loc_to_glob[i], loc_to_glob[j]) for (i, j) in demo_pairs)

        rest_values = VGroup()
        for li in range(8):
            for lj in range(8):
                gi = loc_to_glob[li]
                gj = loc_to_glob[lj]
                if (gi, gj) in already:
                    continue
                val = K1_data_vis[li][lj]
                m = make_KG_value(val)
                m.move_to(KG_cell_center(gi, gj))
                m.set_opacity(0.95)
                rest_values.add(m)

        self.play(FadeIn(rest_values), run_time=0.8)
        self.wait(1.5)

        # keep everything on screen





if __name__ == "__main__":
    import sys
    
    scene = MESStructureScene()


    # scene.render()

    # manim -pql mes_3_el.py MESStructureScene --from_animation_number 90
 