# Design Report
#### Tropochief Aircraft Project
#### Chris Dillow
#### Version 1.0 | November 22, 2025
#### Status: Stage 1.2a | Baseline Geometry Hand Calculations Complete

## Stage 1.2a | Baseline Geometry Hand Calculations
### RESULTS | Value Summary Table
All calculations to be performed assuming standard sea level conditions unless otherwise stated.
Where present, millimeters are the preferred distance measurement for higher accuracy in the CAD modeling phase.
This substage was used for wing and airfoil calculations. As such, control surfaces, nose, tail, and fuselage calculations remain **TBD**.

| Variable | Name | Value |
| :------: | :------: | :------: |
| *m* | Mass | 1.4 kg |
| *W* | Weight | 13.734 N |
| $\frac{W}{S}$ | Wing Loading | 85 N/m<sup>2</sup> |
| *S* | Wing Area | 161.5764706 mm<sup>2</sup> |
| *b* | Wingspan | 900 mm |
| *AR* | Aspect Ratio | 5.01310616 |
| *λ* | Taper Ratio | 0.3 |
| *c<sub>t</sub>* | Tip Chord | 82.8597285 mm |
| *c<sub>r</sub>* | Root Chord | 276.199095 mm |
| $\overline{c}$ | Mean Aerodynamic Chord (MAC) | 196.8803805 mm |
| *Λ<sub>c/4</sub>* | Quarter-Chord Sweep Angle | -10.0<sup>∘</sup> |
| *V<sub>h</sub>* | Horizontal Tail Volume Coefficient | **TBD,** Target: 0.45 - 0.70 |
| *V<sub>v</sub>* | Vertical Tail Volume Coefficient | **TBD,** Target: 0.02 - 0.04 |
| *S<sub>h</sub>* | Horizontal Tail Area | **TBD** |
| *S<sub>v</sub>* | Vertical Tail Area | **TBD** |
| *L<sub>h</sub>* | Distance from Wing Aerodynamic Center | **TBD** |
| *L<sub>v</sub>* | Distance from Tail Aerodynamic Center | **TBD** |
| *SM* | Static Margin | **TBD,** Target: 8 - 12% MAC |
| *x<sub>NP</sub>* | Neutral Point | **TBD** |
| *x<sub>CG</sub>* | Center of Gravity | **TBD** |

### ==================== WORK ====================
### PRELIM | Assumptions
- Subsonic, incompressible flow regime
- Reynolds number range 120,000 - 300,000
- Symmetric half-wing to be used for later CFD
- Rigid wing assumption (aeroelastic effects neglected at RC scale)

#### FIGURE 1 | Baseline Wing Geometry
This baseline geometry establishes the foundational aerodynamic parameters that will feed into CFD analysis, stability sizing, tail volume calculations, control surface authority studies, and propulsion matching. These results form the initial design loop closure required before proceeding to 2D CFD characterization of the selected airfoil.

![Annotated Wing Planform](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/images/wingPlanform.PNG)

Image Source: [Baseline Wing Geometry](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/BASELINE%20WING%20GEOMETRY.pdf)

### STEP 1 | Set AUW and Wing Loading to derive Wing Area
**Targets:**

- **AUW Mass (*m*):** 1.4 kg
- **Weight (*W*=*mg*):** 1.4 kg * 9.81 m/s<sup>2</sup> = 13.734 N
- **Target Wing Loading ($\frac{W}{S}$):** 85 N/m<sup>2</sup>

As such:
> #### *S* = $\frac{W}{W/S}$ = $\frac{13.734}{85}$ = 0.1615764706 m<sup>2</sup>
> #### Wing Area (*S*) = 0.162 m<sup>2</sup> = 161.6 mm<sup>2</sup>

### STEP 2 | Set Wingspan and derive Aspect Ratio
From [PROJECT OUTLINE, 1.1](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/PROJECT_OUTLINE.md#11--plane-type-selection-and-envelope), wingspan (*b*) = 0.9 m.

Aspect Ratio:
> #### *AR* = $\frac{b^2}{S}$ = $\frac{0.9^2}{0.1616}$ = 5.01310616
> #### Baseline Aspect Ratio = ~5.0

### STEP 3 | Taper Ratio and Chords
Opting for a simple tapered forward-swept wing:
  - **Target Taper Ratio (λ)** = c<sub>t</sub> / c<sub>r</sub> = 0.3 (a high performance subsonic jet)
    - **c<sub>t</sub>** is the tip chord, **c<sub>r</sub>** is the root chord
    
**Taper Ratio Reasoning:**

Taper ratio is driven by aerodynamics, structural considerations, and manufacturing for the RC scale. We want a lower induced drag than a constant chord, so we are opting for a tapered chord (hence the tip chord and root chord). This also helps us to avoid tip stall when the taper ratio isn't too small, and assists the plane's load distribution. A constant thickness spar will be easier for us to manufacture and the taper will reduce the increased torsion upon a forward-swept wing configuration by keeping the wing's tips light. It can be made reasonably from readily-available light materials like balsa wood, foam, and composite skins. Below is a table of common taper ratio for different aircraft categories, which informed our selection of 0.3.

| Aircraft Type | Typical Taper Ratio (λ) |
| :--- | :------: |
| Trainer (Basic) | 0.8 - 1.0 |
| Sport Aerobatic | 0.6 - 0.8 |
| Subsonic Jet | 0.3 - 0.6 |
| High-Performance Fighter | 0.2 - 0.4 |

Now, we can solve for the root chord, *c<sub>r</sub>*, utilizing our target taper ratio *λ*, wing surface area *S* calculated in STEP 1, and wingspan *b* as plugged into the following formula:
> #### *S* = $\frac{b}{2}$(c<sub>r</sub> + c<sub>t</sub>) = $\frac{b}{2}$ c<sub>r</sub>(1 + λ)
> **Which when isolating the root chord gives us:**
> #### *c<sub>r</sub>* = $\frac{2S}{b(1 + λ)}$ = $\frac{2⋅0.1616}{0.9⋅(1+0.3)}$ = 0.276199095 m
> #### Root Chord: 0.276 m = 276.2 mm
> **From there, we can calculate the tip chord:**
> #### *c<sub>t</sub>* = λ*c<sub>r</sub>* = 0.3⋅0.276199095 = 0.0828597285 m
> #### Tip Chord: 0.083 m = 82.9 mm

### STEP 4 | Mean Aerodynamic Chord (MAC)
For a tapered wing:
  - $\overline{c}$ = $\frac{2}{3}$ *c<sub>r</sub>*$\frac{1+λ+λ^2}{1+λ}$
    - Where $\overline{c}$ is the Mean Aerodynamic Chord

We will first solve for the numerator and denominator of the lambda (λ) fraction, then implement its result back into the formula.

- **1+λ+λ<sup>2</sup>** = 1 + 0.3 + 0.16 = 1.39
- **1+λ** = 1 + 0.3 = 1.3

Plugging in we get:
> #### $\overline{c}$ = $\frac{2}{3}$⋅0.276⋅$\frac{1.39}{1.3}$ = 0.1968803805 m
> #### Mean Aerodynamic Chord = 0.197 m = 196.9 mm

### STEP 5 | Forward Sweep Angle
We would like to target the Berkut's forward-swept performance without grounding aeroelastic issues, so we will go for a quarter-chord sweep.

- Λ<sub>c/4</sub> = -10<sup>∘</sup>
  - Where Λ<sub>c/4</sub> is the quarter-chord sweep angle, and negative represents a nose-facing direction

This angle will grant us ability to test moderate forward-swept geometry without diving into sweep angles which would become aeroelastically unmanageable with the aircraft's materials.
Later planform sketch(es) will show leading and trailing edge geometry from this sweep.

### STEP 6 | Tail Volume Coefficients
(**TBD:** Flush out the setup, as we do not need $\frac{S_h}{S}$ or $\frac{S_v}{S}$ yet, but it will be important to have in this portion of the document when it is time to calculate.)

**Horizontal Tail Volume Coefficient:**
> #### *V<sub>h</sub>* = $\frac{S_h⋅L_h}{S⋅cbar}$ where "cbar" is $\overline{c}$ (due to markdown formatting issues)
> #### *V<sub>h</sub>* Target: 0.45 - 0.70

**Vertical Tail Volume Coefficient:**
> #### *V<sub>v</sub>* = $\frac{S_v⋅L_v}{Sb}$
> #### *V<sub>v</sub>* Target: 0.02 - 0.04

Wherein:

- **S<sub>h</sub>** and **S<sub>v</sub>** are the horizontal and vertical tail areas respectively
- **L<sub>h</sub>** and **L<sub>v</sub>** are the distance from the wing AC and the tail AC respectively (AC = Aerodynamic Center)

### STEP 7 | Static Margin Target
From [PROJECT OUTLINE, 1.1](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/PROJECT_OUTLINE.md#11--plane-type-selection-and-envelope), we plan to target a static margin of 8 - 12% MAC.
(**TBD:** Plug into formula as values become solidified.)

 - *SM* = $\frac{x_{NP}-x_{CG}}{cbar}$ = 8 - 12%, where "cbar" is $\overline{c}$ (due to markdown formatting issues)
  - **x<sub>CG</sub>** is the aircraft's center of gravity, and **x<sub>NP</sub>** is the aircraft's neutral point at which it would be neutrally stable in pitch

## References
**Reference Standards:**
The following sources were used to guide methodology, not to reproduce proprietary geometry or performance characteristics. All calculations, dimensions, and configurations are original to this project.

- Raymer, D.P. *Aircraft Design: A Conceptual Approach*. AIAA, 5th Edition, 2012.
- Roskam, J. *Airplane Design, Parts I-VIII*. DARcorporation, 2003.
- Etkin, B. and Reid, L.D. *Dynamics of Flight: Stability and Control*. Wiley, 3rd Edition, 1996.
- Torres, G. and Mueller, T.J. "Low Reynolds Number Airfoil Aerodynamics." *Experimental Methods in Low Re*. Flight, 2001.
- Selig Airfoil Database, University of Illinois at Urbana-Champaign, https://m-selig.ae.illinois.edu/ads/coord_database.html
