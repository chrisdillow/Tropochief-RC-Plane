# CFD Case Setup Overview

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
