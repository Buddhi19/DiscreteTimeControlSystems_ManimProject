import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import dlti, dimpulse

# Define symbolic variables
z, T = sp.symbols('z T')

# Define the transfer function components
numerator1 = 6 * (1 - sp.exp(-2 * T))
denominator1 = z - sp.exp(-2 * T)
G1 = numerator1 / denominator1

numerator2 = 4 * (1 - sp.exp(-3 * T))
denominator2 = z - sp.exp(-3 * T)
G2 = numerator2 / denominator2

# Combine the transfer functions
G = G1 - G2

# Substitute a specific value for T
T_val = 2
G = G.subs(T, T_val)

# Simplify the expression
G = sp.simplify(G)

# Extract numerator and denominator
num, den = sp.fraction(G)  # Get numerator and denominator

# Convert the symbolic expressions to polynomials
num_poly = sp.Poly(num, z)
den_poly = sp.Poly(den, z)

# Get the coefficients as lists
num_coeffs = num_poly.all_coeffs()
den_coeffs = den_poly.all_coeffs()

# Convert coefficients from sympy to numpy float
num_coeffs = [float(coef) for coef in num_coeffs]
den_coeffs = [float(coef) for coef in den_coeffs]

# Create transfer function in scipy
G_tf = dlti(num_coeffs, den_coeffs)

# Plot the impulse response
t = np.arange(0, 6)

# Plot the impulse response
t_out, impulse_response = dimpulse(G_tf, t=t)
plt.stem(t, np.squeeze(impulse_response))
plt.title('Impulse Response of G(z)')
plt.xlabel('n')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()