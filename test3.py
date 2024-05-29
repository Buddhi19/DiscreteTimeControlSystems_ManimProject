import sympy as sp

#substitute s = 2/T * (z-1)/(z+1)

z, s, T = sp.symbols('z s T')

C = (s+2)/(s+10)

C_dz = C.subs(s, 2/T * (z-1)/(z+1))
#simplify
C_dz = sp.simplify(C_dz)

#substitute T=0.1 and evaluate

C_dz = C_dz.subs(T, 0.1).evalf()

z, s, T = sp.symbols('z s T')

C = (s+2)/(s+10)

C_dz = C.subs(s, 2/T * (z-1)/(z+1))
#simplify
C_dz = sp.simplify(C_dz)

#substitute T=0.1 and evaluate

C_dz = C_dz.subs(T, 0.1).evalf()

#print in latex
print(sp.latex(C_dz))