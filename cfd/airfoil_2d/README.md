# CFD Case Setup Overview
2D CFD was automated and controlled through [`automate_2d_openFOAM.py`](https://github.com/chrisdillow/Tropochief-RC-Plane/edit/main/cfd/airfoil_2d/automate_2d_openFOAM.py), which allowed for mass parametric assembly of OpenFOAM case preconditions and consequent executions, data normalization, visualization, scoring, and ranking.

- *All `baseCase/` and `baseCase_detailed/` files are uploaded in .txt format for GitHub compatibility. To be compatible with OpenFOAM after downloading, the extensions must be removed.*
- *All files are written with parametric targets that are replaced by computation results in the Python program.*
- *Because the Python script generates a root directory for each candidate airfoil, and a subfolder for each angle of attack in the test sweep that includes parametrically-modified version of the `baseCase/` and `baseCase_detailed/` templates, they have been excluded from this repository for brevity. The detailed results from these OpenFOAM cases are accumulated and saved into .CSV and .VTK files, written into [`airfoil_cfd_report.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/airfoil_cfd_report.md), visualized, and scored by the Python script.*
  - **CSV Outputs:**
    - [`airfoil_cfd_results.csv`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/airfoil_cfd_results.csv)
    - [`airfoil_cfd_scores.csv`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/airfoil_cfd_scores.csv)
  - **Result Data Visualization:**
    - [`Preliminary Screening Results Verification Plots`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/airfoil_2d/postprocessing/plots)

This case uses the standard OpenFOAM folder structure:

- `0/` – Initial & boundary conditions for each physics field  
- `constant/` – Mesh + physical properties  
- `system/` – Solver & numerical settings  

To improve readability for people unfamiliar with CFD, the human-readable versions of 
these files also exist in `0_field_definitions/`:

| Purpose | OpenFOAM File | Human-Readable File |
|---------|---------------|---------------------|
| Velocity Field | [`U`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/baseCase/0/U.txt) | [`velocityField_U`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/baseCase/0_field_definitions/velocityField_U.txt) |
| Pressure Field | [`p`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/baseCase/0/p.txt) | [`pressureField_p`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/baseCase/0_field_definitions/pressureField_p.txt) |
| Turbulent Viscosity | [`nut`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/baseCase/0/nut.txt) | [`turbulentViscosity_nut`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/baseCase/0_field_definitions/turbulentViscosity_nut.txt) |
| Turbulence Kinetic Energy | [`k`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/baseCase/0/k.txt) | [`turbulenceKineticEnergy_k`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/baseCase/0_field_definitions/turbulenceKineticEnergy_k.txt) |
| Turbulence Dissipation Rate | [`omega`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/baseCase/0/omega.txt) | [`turbulenceDissipationRate_omega`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/baseCase/0_field_definitions/turbulenceDissipationRate_omega.txt) |
| Fluid Density Field | [`rho`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/baseCase/0/rho.txt) | [`fluidDensity_rho`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/baseCase/0_field_definitions/fluidDensity_rho.txt) |

The solver requires the original OpenFOAM filenames inside `0/`.
The human-readable versions are provided for clarity and documentation.
