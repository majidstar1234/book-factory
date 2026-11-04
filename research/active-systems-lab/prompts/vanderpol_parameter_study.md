# Numerical parameter study: Van der Pol oscillator

Act as a careful computational dynamics researcher. Analyze the Van der Pol system

\[
\dot x=y,\qquad \dot y=\mu(1-x^2)y-x,
\]

for \(\mu\in\{0.1,0.2,0.5,1,2,3,5\}\), and discuss the limiting case \(\mu=0\) separately.

For each positive parameter:

1. Integrate long enough to remove transients. State the solver, tolerances, maximum step, initial condition, integration horizon, and transient interval.
2. Estimate the limit-cycle period \(T(\mu)\) using repeated same-direction crossings or another justified phase marker.
3. Compute the transverse Floquet exponent using the planar autonomous-system identity
   \[
   \lambda_\perp(\mu)=\frac{1}{T}\int_0^T \mu[1-x_\mu(t)^2]dt.
   \]
4. Compute the one-period transverse multiplier
   \[
   \rho(\mu)=\exp\left(\int_0^T\mu[1-x_\mu(t)^2]dt\right).
   \]
   Explain why a stable limit cycle should have \(\lambda_\perp<0\) and \(0<\rho<1\).
5. Perform convergence checks by tightening tolerances and reducing maximum step. Do not report more significant digits than justified.
6. Provide a table with \(\mu,T,\lambda_\perp,\rho\), numerical settings, and convergence differences.
7. Supply complete executable Python code using SciPy/NumPy/Matplotlib, plus CSV output and plots if execution is available. If you cannot execute code, explicitly label all values as not computed and provide code only.

For \(\mu=0\), the system is the harmonic oscillator \(\ddot x+x=0\). Explain that periodic motion persists but there is no attracting limit cycle and no transverse decay of an amplitude perturbation.

Scientific interpretation:
- Distinguish persistence of oscillation from attraction back to a particular limit cycle.
- Do not claim that activity is universally necessary for structural persistence.
- State that the result concerns this model and this parameter range only.
- Do not fabricate numerical values, plots, CSV files, or execution claims.

Return sections: Methods, Numerical results, Convergence and validation, Interpretation, Limitations, Complete code.
