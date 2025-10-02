class Beam():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    
    
    def compute_reactions(self, P):
        self.P = P
        self.Rb = (P[0] * (self.a) - P[1] * self.b[0] - 
                   P[2] * sum(self.b[0:2]) - 
                           P[3] * (sum(self.b) + self.c)) / sum(self.b)
        self.Ra = - self.Rb - sum(P)
    
    
    def compute_shear_forces(self):
        T = []
        T.append(self.P[0])
        T.append(self.P[0] + self.Ra)
        T.append(T[1] + self.P[1])
        T.append(T[2] + self.P[2])
        T.append(T[3] + self.Rb)
        T.append(T[4] + self.P[3])
        self.T = T
        if T[4] + self.P[3] == 0.0:
            print('check ok')


    def compute_bending_moments(self):
        M = [0]
        M.append(self.a * self.T[0])
        M.append(M[1] + self.b[0] * self.T[1])
        M.append(M[2] + self.b[1] * self.T[2])
        M.append(M[3] + self.b[2] * self.T[3])
        M.append(round((M[4] + self.c * self.T[4]), 3))
        self.M = M


    def compute_deflections(self, E, I):
        """Compute slopes and deflections along the beam assuming constant E and I.

        The geometry is interpreted as a beam with an overhang of length ``a`` on
        the left, three internal spans defined by ``b`` between the two supports,
        and an overhang of length ``c`` on the right. The vertical reactions at
        the supports are taken to act at ``x = a`` (support A) and
        ``x = a + sum(b)`` (support B). Deflection boundary conditions are
        enforced at those two locations.

        Parameters
        ----------
        E : float
            Young's modulus of the beam material.
        I : float
            Second moment of area (area moment of inertia) of the beam section.
        """

        if not hasattr(self, "M"):
            raise ValueError("Call compute_bending_moments before deflections.")
        if E == 0 or I == 0:
            raise ValueError("E and I must be non-zero.")

        segment_lengths = [self.a, *self.b, self.c]
        x_positions = [0.0]
        for length in segment_lengths:
            x_positions.append(x_positions[-1] + length)

        EI = E * I
        curvature = [moment / EI for moment in self.M]

        theta_rel = [0.0]
        for idx in range(1, len(curvature)):
            dx = segment_lengths[idx - 1]
            avg_curvature = 0.5 * (curvature[idx - 1] + curvature[idx])
            theta_rel.append(theta_rel[-1] + avg_curvature * dx)

        w_rel = [0.0]
        for idx in range(1, len(theta_rel)):
            dx = segment_lengths[idx - 1]
            avg_theta = 0.5 * (theta_rel[idx - 1] + theta_rel[idx])
            w_rel.append(w_rel[-1] + avg_theta * dx)

        support_a_idx = 1
        support_b_idx = 4
        x_a = x_positions[support_a_idx]
        x_b = x_positions[support_b_idx]
        if x_b == x_a:
            raise ValueError("Support locations coincide; check beam geometry.")

        theta0 = (w_rel[support_a_idx] - w_rel[support_b_idx]) / (x_b - x_a)
        w0 = -w_rel[support_a_idx] - theta0 * x_a

        slopes = [theta0 + value for value in theta_rel]
        deflections = [w0 + theta0 * x_positions[i] + w_rel[i]
                       for i in range(len(x_positions))]

        self.x = x_positions
        self.slopes = slopes
        self.deflections = deflections
