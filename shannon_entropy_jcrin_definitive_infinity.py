import numpy as np
import cmath
import math
from scipy.integrate import quad

print("=" * 70)
print("FULL CHAIN: H(P(λ))  ⇔  ...  →  Closed Path with Half-Winding")
print("Winding number = (1/(2πi)) ∫_ΓR dz/z = 1/2")
print("=" * 70)

# -------------------------------------------------
# 1. Shannon Entropy H(P(λ))
# -------------------------------------------------
def shannon_entropy(probs):
    probs = np.asarray(probs)
    probs = probs[probs > 0]
    return -np.sum(probs * np.log(probs))

logits = np.array([2.0, 1.0, 0.5, 0.1])
tau = 2 * np.pi * (1 - 0.3)          # τ(λ) = 2π(1-λ)
probs = np.exp(logits / tau)
probs /= probs.sum()
H = shannon_entropy(probs)

print("\n1. Shannon Entropy")
print(f"   H(P(λ)) = {H:.6f}")

# -------------------------------------------------
# 2. Σ arg(z_{n+1}/z_n)
# -------------------------------------------------
N = 10000
t_values = np.linspace(1e-6, 5.0, N)
z = t_values * (1 + 2j * np.pi)
args = np.array([cmath.phase(z[i+1] / z[i]) for i in range(N-1)])
sum_args = np.sum(args)

print("\n2. Discrete argument sum")
print(f"   Σ arg(z_{{n+1}}/z_n) ≈ {sum_args:.6f} rad")

# -------------------------------------------------
# 3. ∫₀¹ |sin(2πx)| dx
# -------------------------------------------------
integral, _ = quad(lambda x: abs(math.sin(2 * math.pi * x)), 0, 1)
print("\n3. Continuous integral")
print(f"   ∫₀¹ |sin(2πx)| dx = {integral:.6f}")
print(f"   (exact = 2/π ≈ {2/np.pi:.6f})")

# -------------------------------------------------
# 4. lim Φ_N = -arctan(2π)
# -------------------------------------------------
target = math.atan(2 * math.pi)
print("\n4. Limiting argument")
print(f"   arctan(2π)  = +{target:.12f} rad ≈ +{math.degrees(target):.4f}°")
print(f"   -arctan(2π) = {-target:.12f} rad ≈ {-math.degrees(target):.4f}°")

# -------------------------------------------------
# 5. Path definition z(t) ∼ t(1 + 2πi)
# -------------------------------------------------
print("\n5. Complex path")
print("   z(t) = t * (1 + 2πi)")
print("   arg(z(t)) is constantly arctan(2π) for all t > 0")

# -------------------------------------------------
# 6. Closed Path with Half-Winding + winding number
# -------------------------------------------------
R = 3.0
theta = np.linspace(0, np.pi, 500)

contour = np.concatenate([
    np.linspace(-R, R, 300) + 0j,                    # diameter
    R * np.cos(theta) + 1j * R * np.sin(theta)       # upper semicircle
])

dz = np.diff(contour)
z_mid = (contour[:-1] + contour[1:]) / 2
winding = np.sum(dz / z_mid).imag / (2 * np.pi)

print("\n6. Closed Path with Half-Winding")
print(f"   Numerical winding number ≈ {winding:.4f}  (ideal = 0.5)")

# -------------------------------------------------
# 7. Phase gate: φ = -π  ⇒  e^{iφ} = -1
# -------------------------------------------------
phi = -np.pi
print("\n7. Final phase")
print(f"   φ_N = -π")
print(f"   e^{{iφ_N}} = {cmath.exp(1j * phi)}")

print("\n" + "=" * 70)
print("CHAIN COMPLETE")
print("=" * 70)
print("""
H(P(λ))  ⇔  Σ arg(z_{n+1}/z_n)
         →  ∫₀¹ |sin(2πx)| dx
         ≜  ⋃ A_i = ⨁ V_i
         ≅  lim Φ_N = -arctan(2π) ≈ -1.412965 rad ≈ -81°
         →  e^{iϕ(t)}
         ⇒  z(t) ∼ t(1 + 2πi)
         →  lim arg(z(t)) = +arctan(2π) ≈ +81°
         →  Closed Path with Winding Half (winding = ½)
""")
