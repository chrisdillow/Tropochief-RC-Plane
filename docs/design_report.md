# Design Report
#### Tropochief Aircraft Project
#### Chris Dillow
#### Version 2.0 | November 24, 2025
#### Status: Stage 1.2b | 2D Airfoil CFD: Python Preliminaries Complete, NACA 23102 and Eppler E168 in Preparations for OpenFOAM

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

## Stage 1.2b | 2D Airfoil CFD
### PRELIM | Candidate Groups and Selection Rationale
A batch of five airfoils were selected to be narrowed by a preliminary screening. These candidates further formed two groups, Baseline and Performance, to have a wider span of behavior to compare for the needs of the project's forward-swept wing design.

Forward-swept wings experience unique added torsion in flight, requiring higher structural consideration for the craft's flight stability and service longevity. Other considerations surrounding forward-swept wings must include the knowledge that they stall at the root outward and maintain aileron control deeper into stall than their neutral- or normally-swept counterparts, and require attention to airfoil choice as they are prone to problems with tip-loaded lift. Because of this:

- Choosing an airfoil that produces an inboard lift bias is desirable
- A section with gentle stall may increase flight test safety at a reasonable aerodynamic performance expense
- There is a preference for a low-moment airfoil to reduce the structural twisting risk under torsion

The preliminary analysis tackles the following objectives:

- Identifying stall behavior differences
- Comparing lift-curve slope variations
- Analyzing low-Reynolds number performance
- Identifying forward-swept stall progression implications

#### Airfoil Candidates

*Some information has been pulled from screening results to give a non-technical reader the best vision of the candidates going in.*

**Baseline Group:**
- **NACA 23012**
![NACA 23012 Airfoil](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/figures/naca23012.gif)
  - A very well-documented and time-tested design that utilizes simple geometry, making it easier to mesh for analysis. It is a safe entry point for this project, but with low performance caps. It is not optimized for low Reynolds number RC flight, which may increase its drag compared to applications on fullsize, gas engine aircraft.
  - **PROS:**
    - A strong candidate for takeoffs, landings, and high lift maneuvering due to its C<sub>l</sub> max
    - It has a good lift-curve slope and predictable linear region, making it easy to trim for moderate-angle cruise
  - **CONS:**
    - Risk of abrupt stalls
    - Despite its high lift, it produces higher drag and therefore lower cruise efficiency
    - Lower cruise efficiency than other candidates due to its higher drag
    - Likely to show a larger pitching moment which can increase tail download and wing torsional loads, which may make for unreconcilable penalties despite the airfoil's lift
- **NACA 2412**
![NACA 2412 Airfoil](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/figures/naca2412.gif)
  - Its camber is located more aft of the leading edge than the NACA 23012 (40% of the chord from the leading edge vs. 12% on the 23012), which contributes to improved lift-to-drag balance over the other NACA airfoil.
  - **PROS:**
    - Boasts the highest stall angle of any candidate while having gentle post-stall behavior, which may mark it as the safest option of the candidates
    - It offers balanced performance between the NACA 23012 and members of the Performance Group
    - A more moderate pitching moment than the 23012
  - **CONS:**
    - While it has lower risks than other candidates, it does not excel in performance; it is a safe option, but not one that makes the aircraft competitive
    - Its cruise L/D is outperformed by MH32 and RG15
    - Lower lift than the 23012

**Performance Group:**
- **RG15**
![RG15 Airfoil](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/figures/rg15.gif)
  - Often used in high performance gliders, this airfoil is optimized for speed. It carries ballast well and has an excellent lift-to-drag ratio. It is optimized for good L/D at moderate Reynolds numbers and a fairly narrow sweet spot for angles of attack.
  - **PROS:**
    - A great candidate for maximizing range/loiter efficiency in the cruise's angle of attack band
    - Its high lift-curve slope translates to a strong lift response per degree in angle of attack in the airfoil's linear range
    - It is suited for a mission segment where we expect the aircraft to spend a lot of time at a specific cruise lift coefficient
  - **CONS:**
    - A sharper stall than either candidate in the Baseline Group
    - It has a narrower comfortable angle of attack range than other candidates, making it less forgiving if the plane flies outside of these conditions
    - Because of its thinner section it may be more structurally demanding than other candidates
    - Being a laminar-optimized airfoil, even small surface imperfections will easily disrupt the boundary layer flow the foil is designed around. It will require higher attention to a fine surface finish than other candidates.
- **MH32**
![MH32 Airfoil](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/figures/mh32.gif)
  - With more camber than the RG15, it has smoother stall behavior and larger lift at low angles of attack. While not as fast as the RG15, it is more forgiving to fly due to its lower speeds and being less sensitive to the plane's center of gravity. It is fine tuned for excellent L/D in cruise at Reynolds numbers typical of RC planes.
  - **PROS:**
    - It has the top cruise efficiency of all candidates, making it an ideal candidate if our mission priorities include range and efficient climbs
    - A low minimum drag
    - Designed for the exact RC/high-performance project type we are working on
  - **CONS:**
    - Despite its low drag is has only moderate C<sub>l</sub> max and is less forgiving at low speeds
    - The section's thinness will raise structural design demands to combat torsion
    - Likely to have sharper stall characteristics and a narrower linear range than other candidates
- **Eppler E168**
![Eppler E168 Airfoil](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/figures/e168.gif)
  - A moderate-thickness, moderate camber airfoil used in gliders and other RC aircraft. It is expected to have a gentler stall than other members of the Performance Group and may be less sensitive to surface roughness than the RG15.
  - **PROS:**
    - A benign stall and long linear lift region
    - An older airfoil design with a history of good testing; even if it is not selected to move to OpenFOAM it is a good baseline for comparing other airfoils
  - **CONS:**
    - Underperforms other candidates in C<sub>l</sub> max and cruise band $\frac{C_l}{C_d}$
    - It doesn't have its own "niche" where it excels past other candidates
 
### METHOD | Screening Design
- Candidate .dat files were obtained from [UIUC Airfoil Data Site](https://m-selig.ae.illinois.edu/ads/coord_database.html) and placed into the [`geometry/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/analysis/airfoil_screening/geometry) directory.
- A [Python script](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/airfoil_screening.py) was written to carry project information and iterate the .dat files through [XFoil](https://web.mit.edu/drela/Public/web/xfoil/), then automatically plot results and export CSVs.
- The Python screening served to confirm preliminary assumptions about the airfoils and their behavior, and offer a concise, visual comparison of their behavior in key aspects of flight.
- The script's outputs were reviewed and compared to project targets to narrow the airfoil candidate list for 2D CFD analysis in OpenFOAM.

### RESULTS | Python Preliminary Screening
For in-depth results of the Python preliminary screening, see [`airfoil_selection.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/airfoil_selection.md).

#### Numerical Summary Table
| Candidate Airfoil | Max C<sub>l</sub> | Min C<sub>d</sub> | Max $\frac{C_l}{C_d}$ | Max $\frac{C_l}{C_d}$ Cruise Band |
| :--- | :------: | :------: | :------: | :------: |
| NACA 23012 | 1.3968 | 0.0072 | 70.2711 | 66.4895 |
| NACA 2412 | 1.3680 | 0.0068 | 81.3534 | 81.2534 |
| RG15 | 1.1789 | 0.0062 | 84.4689 | 84.4689 |
| MH32 | 1.1901 | 0.0059 | 89.4894 | 89.4894 |
| Eppler E168 | 1.0982 | 0.0082 | 67.3896 | 67.3896 |

#### Lift-Curve Slope Table
| Candidate Airfoil | Lift-Curve Slope | Alpha Linear Min | Alpha Linear Max | Linear Fit R<sup>2</sup> |
| :--- | :------: | :------: | :------: | :------: |
| NACA 23012 | 0.1048 | -4.0 | 12.0 | 0.9943 |
| NACA 2412 | 0.0893 | -4.0 | 14.0 | 0.9744 |
| RG15 | 0.1093 | -4.0 | 8.0 | 0.9933 |
| MH32 | 0.1023 | -4.0 | 8.0 | 0.9974 |
| Eppler E168 | 0.1023 | -4.0 | 12.0 | 0.9849 |

### C<sub>l</sub> vs. AoA Results Graph
![C<sub>l</sub> vs. AoA Graph](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/figures/cl_vs_aoa.png)

### C<sub>d</sub> vs. AoA Results Graph
![C<sub>d</sub> vs. AoA Graph](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/figures/cd_vs_aoa.png)

### $\frac{C_l}{C_d}$ vs. AoA Results Graph
![$\frac{C_l}{C_d}$ vs. AoA Graph](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/figures/clcd_vs_aoa.png)

### C<sub>m</sub> vs. AoA Results Graph
![C<sub>m</sub> vs. AoA Graph](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/figures/cm_vs_aoa.png)

### Linear Region Graphs by Candidate
![NACA 23012 Linear Region](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/figures/linear_region/NACA23012_linear_region.png)
![NACA 2412 Linear Region](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/figures/linear_region/NACA2412_linear_region.png)
![RG15 Linear Region](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/figures/linear_region/RG15_linear_region.png)
![MH32 Linear Region](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/figures/linear_region/MH32_linear_region.png)
![Eppler E168 Linear Region](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/figures/linear_region/E168_linear_region.png)

### RANKINGS | Multi-Objective Ranking of Candidates
#### Scoring Methodology
To rank the candidates against each other, the three most desirable traits were elected for scoring. The scores were normalized to a 0-1 range and converted to percentages out of 100 for comparison. Maneuverability vs. Torsion and Stability were selected because of the demands of the forward-swept wing configuration, and the latter having an added desirability as reliability and controlability during flight testing are essential to ensure high quality data acquisition.

Each trait's score was calculated on a weighted system. These comprised of:
- **Stability:**
  - 40% of the score came from having a higher stall angle, allowing a greater margin before stall
  - 40% of the score came from having a smaller post-stall lift drop, to provide gentler stalls when they occur
  - 20% of the score came from a lift-curve slope near the target slope of 0.1, which is not too fast and not too aggressive
- **Efficiency:**
  - 70% of the score came from having a higher lift-to-drag ratio in the cruise band
  - 30% of the score came from having a lower overall drag
- **Maneuverability vs. Torsion:**
  - 40% of the score came from having a strong lift-to-curve slope for high control authority
  - 30% of the score came from having a high C<sub>l</sub> max for lift capacity
  - 30% of the score came from not being penalized by high slope multiplied by max lift loads

#### SCORE A | Stability
| Rank | Candidate Airfoil | Score |
| :--- | :-------: | :-------: |
| **1** | Eppler E168 | 84.9% |
| **2** | NACA 2412 | 80.0% |
| **3** | NACA 23012 | 61.3% |
| **4** | RG15 | 3.4% |
| **5** | MH32 | NaN |

#### SCORE B | Efficiency
| Rank | Candidate Airfoil | Score |
| :--- | :-------: | :-------: |
| **1** | MH32 | 100% |
| **2** | RG15 | 81.0% |
| **3** | NACA 2412 | 63.8% |
| **4** | NACA 23012 | 13.4% |
| **5** | Eppler E168 | 2.7% |

#### SCORE C | Maneuverability vs. Torsion
| Rank | Candidate Airfoil | Score |
| :--- | :-------: | :-------: |
| **1** | RG15 | 63.6% |
| **2** | NACA 23012 | 61.1% |
| **3** | MH32 | 57.0% |
| **4** | Eppler E168 | 56.0% |
| **5** | NACA 2412 | 48.5% |

### SELECTION | Candidates to Proceed to OpenFOAM
To determine which candidates will proceed to more complex analysis in OpenFOAM, a composite score was formed based on the scores in Stability, Efficiency, and Maneuverability vs. Torsion.

#### Composite Score Weighting
- 40% of the composite score comes from stability
- 30% of the composite score comes from efficiency
- 30% of the composite score comes from maneuverability vs. torsion

#### Composite Score Rankings
| Rank | Candidate Airfoil | Score |
| :--- | :-------: | :-------: |
| **1** | NACA 2412 | 65.7% |
| **2** | Eppler E168 | 51.6% |
| **3** | MH32<sup>1</sup> | 47.1% |
| **4** | NACA 23012 | 46.9% |
| **5** | RG15 | 44.7% |

<sup>1</sup> *Assumed to have a 0% stability score due to NaN metric return.*

#### Proceeding Candidates
Based on the composite scoring, the **NACA 2412** and **Eppler E168** have been selected to advance to comprehensive 2D CFD analysis in OpenFOAM. This pairing provides one candidate from each performance category, enabling comparison between a benign-stall baseline section and a performance-oriented section with favorable torsional characteristics. The results of the CFD study will determine which airfoil offers the best balance of controllability, structural loading, and aerodynamic performance for the forward-swept Tropochief wing. Following CFD evaluation, any required design compensations (such as torsional stiffening, washout, or control surface sizing) will be incorporated into the final wing configuration.
