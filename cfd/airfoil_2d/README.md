# CFD Case Setup Overview
2D CFD was automated and controlled through [`automate_2d_openFOAM.py`](https://github.com/chrisdillow/Tropochief-RC-Plane/edit/main/cfd/airfoil_2d/automate_2d_openFOAM.py), which allowed for mass parametric assembly of OpenFOAM case preconditions and consequent executions, data normalization, visualization, scoring, and ranking.

*All `baseCase/` and `baseCase_detailed/` files are uploaded in .txt format for GitHub compatibility. To be compatible with OpenFOAM after downloading, the extensions must be removed.*

This case uses the standard OpenFOAM folder structure:

- `0/` – Initial & boundary conditions for each physics field  
- `constant/` – Mesh + physical properties  
- `system/` – Solver & numerical settings  

To improve readability for people unfamiliar with CFD, the human-readable versions of 
these files also exist in `0_field_definitions/`:

| Purpose | OpenFOAM File | Human-Readable File |
|---------|---------------|---------------------|
| Velocity Field | `U` | `velocityField_U` |
| Pressure Field | `p` | `pressureField_p` |
| Turbulent Viscosity | `nut` | `turbulentViscosity_nut` |
| Turbulence Kinetic Energy | `k` | `turbulenceKineticEnergy_k` |
| Turbulence Dissipation Rate | `omega` | `turbulenceDissipationRate_omega` |
| Fluid Density Field | `rho` | `fluidDensity_rho` |

The solver requires the original OpenFOAM filenames inside `0/`.
The human-readable versions are provided for clarity and documentation.
