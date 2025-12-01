# CFD Case Setup Overview
2D CFD was automated and controlled through [`automate_2d_openFOAM.py`](https://github.com/chrisdillow/Tropochief-RC-Plane/edit/main/cfd/airfoil_2d/automate_2d_openFOAM.py), which allowed for mass parametric assembly of OpenFOAM case preconditions and consequent executions, data normalization, visualization, scoring, and ranking.

This case uses the standard OpenFOAM folder structure:

- `0/` – Initial & boundary conditions for each physics field  
- `constant/` – Mesh + physical properties  
- `system/` – Solver & numerical settings  

To improve readability for people unfamiliar with CFD, the human-readable versions of 
these files also exist in `0_field_definitions/`:

| Purpose | OpenFOAM File | Human-Readable File |
|---------|---------------|---------------------|
| Velocity field | `U` | `velocityField_U` |
| Pressure field | `p` | `pressureField_p` |
| Turbulent viscosity | `nut` | `turbulentViscosity_nut` |
| Turbulence kinetic energy | `k` | `turbulenceKineticEnergy_k` |
| Turbulence dissipation rate | `omega` | `turbulenceDissipationRate_omega` |

The solver requires the original OpenFOAM filenames inside `0/`.
The human-readable versions are provided for clarity and documentation.
