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

            # Special adjustment for node 2: shift downward by 1.5 × original digit height (at 0.55)
            if idx == 2:
                temp = MathTex("2").scale(0.55)
                base_dy = 1.5 * temp.height
                extra_dx = 0.2 * temp.height
                extra_dy = 0.3 * temp.height
                circ.shift(DOWN * (base_dy + extra_dy) + RIGHT * extra_dx)
                num_label.shift(DOWN * (base_dy + extra_dy) + RIGHT * extra_dx)

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
        elem1_j = MathTex("j").scale(0.52).move_to(map_new(1.8, 0.3))    # near global node 1 (2,0)
        elem1_k = MathTex("k").scale(0.52).move_to(map_new(1.8, 2.7))    # near global node 2 (2,3)
        elem1_r = MathTex("r").scale(0.52).move_to(map_new(0.2, 2.7))    # near global node 5 (0,3)
        internal_labels.add(elem1_i, elem1_j, elem1_k, elem1_r)
        
        # Element 2 (left triangle): i=4, j=5, k=2 (CCW from bottom)
        # Place labels inside element 2, near corresponding global nodes
        elem2_i = MathTex("i").scale(0.52).move_to(map_new(1.8, 4.4))    # near global node 4 (2,5) - moved down
        elem2_j = MathTex("j").scale(0.52).move_to(map_new(0.6, 3.3))    # near global node 5 (0,3) - moved back left
        elem2_k = MathTex("k").scale(0.52).move_to(map_new(1.8, 3.3))    # near global node 2 (2,3)
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
        
        # Create element label "e. I" at birth position
        elem1_label_copy = (
            MathTex(r"e.\ I").scale(0.5 * 0.75).stretch(0.85, 0)
            .move_to(map_elem1_birth(1.0, 1.5))
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
            elem1_global_circles.add(VGroup(circ, num_label))
        
        # Create internal node labels at birth position  
        elem1_internal_copy = VGroup()
        elem1_i_copy = MathTex("i").scale(0.52 * 0.75).move_to(map_elem1_birth(0.2, 0.3))
        elem1_j_copy = MathTex("j").scale(0.52 * 0.75).move_to(map_elem1_birth(1.8, 0.3))
        elem1_k_copy = MathTex("k").scale(0.52 * 0.75).move_to(map_elem1_birth(1.8, 2.7))
        elem1_r_copy = MathTex("r").scale(0.52 * 0.75).move_to(map_elem1_birth(0.2, 2.7))
        elem1_internal_copy.add(elem1_i_copy, elem1_j_copy, elem1_k_copy, elem1_r_copy)
        
        # Group everything
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

        # ----- Final hold -----
        self.wait(2)

if __name__ == "__main__":
    scene = MESStructureScene()
    scene.render()