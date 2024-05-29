import sympy as sp

# Define the symbols
z, T = sp.symbols('z T')

# Define the function G(z)
G_z = 6 * (1 - sp.exp(-2*T)) / (z - sp.exp(-2*T)) - 4 * sp.exp(-3*T) / (z - sp.exp(-3*T))

# Substitute T = 1
G_z_T1 = G_z.subs(T, 0.1)

# Simplify the expression
G_z_T1_simplified = sp.simplify(G_z_T1).evalf()

C_dz = (1.1*z - 0.9)/(1.5*z - 0.5)

Gcl = C_dz * G_z_T1_simplified/(1 + C_dz * G_z_T1_simplified)

print(sp.latex(Gcl))