from manim import *
import numpy as np


class GaussIntegrationScene(Scene):
    """Show Gauss quadrature points for the 3 FEM elements vs. analytic integration."""

    def construct(self):
        # =====================================================================
        # Title
        # =====================================================================
        title = Text("Gauss Quadrature vs. Analytic Integration", font_size=38)
        title.to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.8)
        self.wait(0.5)

        subtitle = MathTex(
            r"\int_\Omega f \, d\Omega \;\approx\;"
            r"\sum_{i=1}^{n} w_i \, f(\xi_i, \eta_i)"
        ).scale(0.55)
        subtitle.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(subtitle), run_time=0.6)
        self.wait(1.0)

        # =====================================================================
        # Element geometries (local coordinates)
        # =====================================================================
        SC = 0.85

        # --- Element I (rectangle): nodes (0,0),(2,0),(2,3),(0,3) ---
        e1_org = np.array([-5.0, -1.1, 0])

        def e1p(x, y):
            return e1_org + SC * RIGHT * x + SC * UP * y

        e1_poly = Polygon(
            e1p(0, 0), e1p(2, 0), e1p(2, 3), e1p(0, 3),
            stroke_width=3, color=WHITE, fill_color=BLUE_E, fill_opacity=0.12,
        )
        e1_label = MathTex(r"e.\,I").scale(0.48).set_color(GREEN_A)
        e1_label.next_to(e1_poly, UP, buff=0.12)
        e1_type = Text("(rectangle, 4 nodes)", font_size=18, color=GREY_A)
        e1_type.next_to(e1_poly, DOWN, buff=0.15)

        # 2×2 Gauss points for rectangle (in natural coords ξ,η ∈ [-1,1])
        # mapped to local coords: x = 1 + ξ, y = 1.5 + 1.5η
        gp_rect = [(-1 / np.sqrt(3), -1 / np.sqrt(3)),
                    ( 1 / np.sqrt(3), -1 / np.sqrt(3)),
                    (-1 / np.sqrt(3),  1 / np.sqrt(3)),
                    ( 1 / np.sqrt(3),  1 / np.sqrt(3))]

        e1_gp_dots = VGroup()
        e1_gp_labels = VGroup()
        for idx, (xi, eta) in enumerate(gp_rect):
            x_loc = 1.0 + xi
            y_loc = 1.5 + 1.5 * eta
            pt = e1p(x_loc, y_loc)
            dot = Dot(pt, radius=0.08, color=RED)
            lbl = MathTex(f"G_{idx+1}").scale(0.30).set_color(RED)
            lbl.next_to(dot, UR, buff=0.06)
            e1_gp_dots.add(dot)
            e1_gp_labels.add(lbl)

        e1_group = VGroup(e1_poly, e1_label, e1_type, e1_gp_dots, e1_gp_labels)

        # --- Element II (triangle): nodes (0,0),(0,2),(2,2) mapped to local ---
        # In our FEM: i=(0,3), j=(2,3), k=(2,5) but local: i=(0,0), j=(2,0), k=(0,2)
        # Triangle with vertices at (0,0), (2,0), (0,2)
        e2_org = np.array([-0.8, -1.1, 0])

        def e2p(x, y):
            return e2_org + SC * RIGHT * x + SC * UP * y

        e2_poly = Polygon(
            e2p(0, 0), e2p(2, 0), e2p(0, 2),
            stroke_width=3, color=WHITE, fill_color=BLUE_E, fill_opacity=0.12,
        )
        e2_label = MathTex(r"e.\,II").scale(0.48).set_color(GREEN_A)
        e2_label.next_to(e2_poly, UP, buff=0.12)
        e2_type = Text("(CST – Constant Strain Triangle)", font_size=16, color=GREY_A)
        e2_type.next_to(e2_poly, DOWN, buff=0.15)

        # 1-point Gauss for CST triangle — centroid (1/3, 1/3)
        # For CST: B,D,h are constant → 1 point is exact
        e2_centroid = (np.array([0,0,0]) + np.array([2,0,0]) + np.array([0,2,0])) / 3
        e2_gp_pt = e2p(e2_centroid[0], e2_centroid[1])
        e2_gp_dots = VGroup(Dot(e2_gp_pt, radius=0.10, color=RED))
        e2_gp_labels = VGroup(
            MathTex(r"G_1").scale(0.32).set_color(RED).next_to(e2_gp_dots[0], UR, buff=0.06)
        )

        e2_group = VGroup(e2_poly, e2_label, e2_type, e2_gp_dots, e2_gp_labels)

        # --- Element III (triangle): nodes (0,0),(2,2),(0,2) local ---
        e3_org = np.array([3.0, -1.1, 0])

        def e3p(x, y):
            return e3_org + SC * RIGHT * x + SC * UP * y

        e3_poly = Polygon(
            e3p(0, 0), e3p(2, 2), e3p(0, 2),
            stroke_width=3, color=WHITE, fill_color=BLUE_E, fill_opacity=0.12,
        )
        e3_label = MathTex(r"e.\,III").scale(0.48).set_color(GREEN_A)
        e3_label.next_to(e3_poly, UP, buff=0.12)
        e3_type = Text("(CST – Constant Strain Triangle)", font_size=16, color=GREY_A)
        e3_type.next_to(e3_poly, DOWN, buff=0.15)

        # 1-point Gauss for CST triangle — centroid (1/3, 1/3, 1/3)
        vA = np.array([0, 0, 0])
        vB = np.array([2, 2, 0])
        vC = np.array([0, 2, 0])
        e3_centroid = (vA + vB + vC) / 3
        e3_gp_pt = e3p(e3_centroid[0], e3_centroid[1])
        e3_gp_dots = VGroup(Dot(e3_gp_pt, radius=0.10, color=RED))
        e3_gp_labels = VGroup(
            MathTex(r"G_1").scale(0.32).set_color(RED).next_to(e3_gp_dots[0], UR, buff=0.06)
        )

        e3_group = VGroup(e3_poly, e3_label, e3_type, e3_gp_dots, e3_gp_labels)

        # =====================================================================
        # Animate elements appearing
        # =====================================================================
        for grp in [e1_group, e2_group, e3_group]:
            poly = grp[0]
            rest = VGroup(*grp[1:3])
            dots = grp[3]
            lbls = grp[4]

            self.play(Create(poly), FadeIn(rest), run_time=0.6)
            self.play(
                LaggedStartMap(GrowFromCenter, dots, lag_ratio=0.15),
                run_time=0.5,
            )
            self.play(
                LaggedStartMap(FadeIn, lbls, lag_ratio=0.10),
                run_time=0.4,
            )
            self.wait(0.3)

        self.wait(1.0)

        # =====================================================================
        # Formulas below each element
        # =====================================================================
        # Element I: 2×2 Gauss on rectangle
        f1_analytic = MathTex(
            r"\int_{0}^{2}\!\int_{0}^{3} f \, dy\, dx"
        ).scale(0.38)
        f1_approx = MathTex(
            r"\approx \sum_{i=1}^{4} w_i \, f(\xi_i,\eta_i) \cdot |J|"
        ).scale(0.38)
        f1_note = MathTex(r"2 \times 2 \text{ Gauss}").scale(0.34).set_color(RED)
        f1 = VGroup(f1_analytic, f1_approx, f1_note).arrange(DOWN, buff=0.08)
        f1.next_to(e1_type, DOWN, buff=0.15)

        # Element II: 1-point Gauss on CST triangle
        f2_analytic = MathTex(
            r"\int_{0}^{2}\!\int_{0}^{2-x} f \, dy\, dx"
        ).scale(0.38)
        f2_approx = MathTex(
            r"= f\!\left(\tfrac{1}{3},\tfrac{1}{3}\right) \cdot A"
        ).scale(0.38)
        f2_note = MathTex(r"\text{1-pt (exact for CST)}").scale(0.34).set_color(RED)
        f2 = VGroup(f2_analytic, f2_approx, f2_note).arrange(DOWN, buff=0.08)
        f2.next_to(e2_type, DOWN, buff=0.15)

        # Element III: 1-point Gauss on CST triangle
        f3_analytic = MathTex(
            r"\int_{0}^{2}\!\int_{x}^{2} f \, dy\, dx"
        ).scale(0.38)
        f3_approx = MathTex(
            r"= f\!\left(\tfrac{1}{3},\tfrac{1}{3}\right) \cdot A"
        ).scale(0.38)
        f3_note = MathTex(r"\text{1-pt (exact for CST)}").scale(0.34).set_color(RED)
        f3 = VGroup(f3_analytic, f3_approx, f3_note).arrange(DOWN, buff=0.08)
        f3.next_to(e3_type, DOWN, buff=0.15)

        self.play(FadeIn(f1), FadeIn(f2), FadeIn(f3), run_time=0.8)
        self.wait(2.0)

        # =====================================================================
        # Key insight box at the bottom
        # =====================================================================
        insight = MathTex(
            r"\text{No need for symbolic integration — just evaluate }",
            r"f",
            r"\text{ at Gauss points!}"
        ).scale(0.42)
        insight[1].set_color(RED)
        insight_box = SurroundingRectangle(insight, color=YELLOW, buff=0.12, stroke_width=2.5)
        insight_grp = VGroup(insight, insight_box)
        insight_grp.to_edge(DOWN, buff=0.25)

        self.play(Write(insight), run_time=0.8)
        self.play(Create(insight_box), run_time=0.4)

        self.wait(3.0)


if __name__ == "__main__":
    scene = GaussIntegrationScene()
    # manim -pql mes_3el_gauss.py GaussIntegrationScene
