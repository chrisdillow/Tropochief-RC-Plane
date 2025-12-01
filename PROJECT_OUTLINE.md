# Tropochief RC Plane Project
#### Chris Dillow
###### Outlined November 15, 2025
###### Last Update: December 1, 2025

### Project Synopsis
The Tropochief RC Aircraft Project is a full-stack engineering initiative that spans:
- Airframe Design (CAD, materials, and control surfaces)
- Aerodynamics Analysis (2D and 3D CFD)
- Custom Avionics PCB (microcontroller, IMU, RF linking, regulators)
- Ground Controller PCB and Mechanical Shell
- Embedded C/C++ Flight Control Firmware
- Stabilized Flight Mode (AHRS and PIDs)
- Production-Ready Documentation and Testing Workflows

### Project Goals
- **Technical Goals**
  - Design and build an RC aircraft capable of stable flight at 25-40 m/s
  - Implement a complete avionics stack including IMU, RF, and servo control
  - Develop a custom RC transmitter with joysticks, switches, and a custom protocol
  - Implement onboard attitude estimation (Mahony/Madgwick)
  - Implement stabilization PIDs for roll, pitch, and yaw
  - Validate aerodynamic performance with OpenFOAM CFD
  - Create reusable tooling and documentation
- **Portfolio Goals**
  - Demonstrate multidisciplinary engineering capability
  - Provide a readable, hiring-manager-friendly repository
  - Showcase structure, requirements, testing, and documentation discipline
  - Produce diagrams, deliverables, and logs that show real engineering workflow
  
### Skills and Disciplines Demonstrated
- **Mechanical Engineering**
  - Airframe CAD, control surface linkages, and structural mounts
- **Aerodynamics**
  - Aerodynamic hand calculations, CFD setup, boundary conditions, and postprocessing
- **Electrical Engineering**
  - PCB design, power systems, signal routing, and RF
- **Embedded Systems**
  - Microcontroller firmware, RT scheduling, and drivers
- **Controls Engineering**
  - PIDs, sensor fusion, and mixer design
- **Software Engineering**
  - Modular architecture, versioning, and documentation
- **Testing and Validation**
  - Bench tests, flight tests, logging, and data analysis

# Project Outline - Quicklinks Index
- [Project Overview](https://github.com/chrisdillow/Tropochief-RC-Plane/edit/main/PROJECT_OUTLINE.md#project-overview)
- [GitHub Repo General Directory](https://github.com/chrisdillow/Tropochief-RC-Plane/edit/main/PROJECT_OUTLINE.md#github-repo-general-directory)
- [Project Outline](https://github.com/chrisdillow/Tropochief-RC-Plane/edit/main/PROJECT_OUTLINE.md#project-outline)
- [Timeline](https://github.com/chrisdillow/Tropochief-RC-Plane/edit/main/PROJECT_OUTLINE.md#timeline)

# Deliverables by Stage w/ Links and Progress Markers
*Completed stages are marked by* ✅. *The current in-progress stage is marked by* 🛠️.
- 🛠️ [STAGE 1](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/PROJECT_OUTLINE.md#stage-1-deliverables)
- [STAGE 2](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/PROJECT_OUTLINE.md#stage-2-deliverables)
- [STAGE 3](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/PROJECT_OUTLINE.md#stage-3-deliverables)
- [STAGE 4](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/PROJECT_OUTLINE.md#stage-4-deliverables)
- [STAGE 5](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/PROJECT_OUTLINE.md#stage-5-deliverables)
- [STAGE 6](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/PROJECT_OUTLINE.md#stage-6-deliverables)
- [STAGE 7](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/PROJECT_OUTLINE.md#stage-7-deliverables)

# Project Overview

#### Airframe and Flight Control Surfaces
- Wing, tail, fuselage, and control surfaces
- Linkages (horns, pushrods, servo mounts)
- PCB mounting, battery bay
- Cooling airflow

#### Avionics PCB
- MCU (e.g., STM32 / ATSAMD / RP2040)
- IMU for gyro and acceleration, possible barometrics
- RF receiver with custom protocol / module
- Servo outputs and and ESC Control
- Power regulation through a 3.3 or 5 volt battery

#### Ground Controller (Body and PCB)
- Custom handled TX with joystick gimbals, switches, and possibly a small display for the craft’s POV
- RF transmitter to match plane’s receiver
- MCU for reading stick inputs, sending RC frames via RF

#### Software and Analysis
- CFD in OpenFOAM to validate wing and airframe stability
- Develop a simple dynamic model for predicted stability
- Plane onboard firmware including RC decoding, the mixer, and servo commands
- Controller onboard firmware including stick readout to RF frames
- Logging, test scripts, documentation

# GitHub Repo General Directory
> **Bold** incidates a top-level directory.

- [**`rc-plane-fullstack/`**](https://github.com/chrisdillow/Tropochief-RC-Plane)
  - [**`airframe/`**](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/airframe)
    - [`cad/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/airframe/cad)
      - [`fuselage/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/airframe/cad/fuselage)
      - [`wing/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/airframe/cad/wing)
      - [`tail/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/airframe/cad/tail)
      - [`control_surfaces/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/airframe/cad/control_surfaces)
    - [`mass_properties/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/airframe/mass_properties)
    - [`mounting_and_cooling.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/airframe/mounting_and_cooling.md)
  - [**`avionics/`**](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/avionics)
    - [`pcb/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/avionics/pcb)
      - [`kicad/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/avionics/pcb/kicad)
      - [`gerbers/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/avionics/pcb/gerbers)
      - [`bom/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/avionics/pcb/bom)
    - [`firmware/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/avionics/firmware)
      - [`src/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/avionics/firmware/src)
      - [`include/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/avionics/firmware/include)
      - [`tests/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/avionics/firmware/tests)
  - [**`controller/`**](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller)
    - [`cad/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller/cad)
    - [`pcb/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller/pcb)
      - [`kicad/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller/pcb/kicad)
      - [`gerbers/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller/pcb/gerbers)
      - [`bom/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller/pcb/bom)
    - [`firmware/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller/firmware)
      - [`src/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller/firmware/src)
      - [`include`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller/firmware/include)
      - [`tests/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller/firmware/tests)
  - [**`cfd/`**](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd)
    - [`airfoil_2d/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/airfoil_2d)
      - [`baseCase/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/airfoil_2d/baseCase)
      - [`baseCase_detailed/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/airfoil_2d/baseCase_detailed)
      - [`geometry/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/airfoil_2d/geometry)
      - [`postprocessing/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/airfoil_2d/postprocessing)
    - [`wing_3d/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/wing_3d)
      - [`mesh/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/wing_3d/mesh)
      - [`case_setup/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/wing_3d/case_setup)
      - [`postprocessing/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/wing_3d/postprocessing)
  - [**`sim/`**](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/sim)
    - [`matlab_octave/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/sim/matlab_octave)
    - [`python/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/sim/python)
  - [**`docs/`**](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/docs)
    - [`requirements.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/docs/requirements.md)
    - [`test_plan.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/docs/test_plan.md)
    - [`flight_logs/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/docs/flight_logs)
    - [`design_report.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/docs/design_report.md)
    - [`component_decisions.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/docs/component_decisions.md)
  - [**`images`**](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/images)
  - [**`analysis`**](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/analysis)
    - [`airfoil_screening`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/analysis/airfoil_screening)

# Project Outline
> This project has a seven-stage development pipeline.
> The current in-progress Stage and Step will be headed with 🛠️
> Completed stages, steps, and deliverables will be headed with ✅

## 🛠️ STAGE 1 | Airframe and Aerodynamics
#### ✅ 1.1 | Plane Type Selection and Envelope
- **Type:** Electric-ducted fan (EDF) or high-power prop jet, inspired by the Su-47 Berkut to utilize forward-swept wings
- **Wingspan (b):** ~0.9 meters
- **Target AUW:** 1.3 - 1.6 kg, including EDF, battery, avionics
- **Wing Loading (W/S):** 80-100 N/m^2, putting it roughly into 'jet' territory versus prior trainer targets
- **Flight Regime:** 25 – 40 m/s (45 - 90 mph)
- **Stability Goal:** Slightly "hot" but positive static margin ≈ 8 - 12% MAC, making it believable as a demonstrator without needing a fully functional fly-by-wire system.

#### 1.2 | Aerodynamic Design Workflow
- **✅ 1.2a | Baseline Geometry – Hand Calculations**
  - Select an airfoil from public options, likely NACA 2412-style
  - Wing area, aspect ratio, tail volume coefficients
  - Estimate wing loading and static margin (e.g., 5 – 15% MAC)
- **🛠️ 1.2b | 2D Airfoil CFD**
  - Simulate the 2D airfoil cross section at various angles of attack
  - Extract the lift curve slope, stall behavior, CI/CD
    - ✅ Python preliminary screening on all candidates
    - 🛠️ OpenFOAM comprehensive analysis
- **1.2c | 3D Wing CFD**
  - Use half wing and symmetry plane to reduce cost
  - Verify:
    - Lift at cruise angle of attack
    - Stall onset
    - Effect of aileron deflections
- **1.2d | Full Fuselage / Wing Pass**
  - This is optional and will make the craft heavier
  - Coarser mesh around full craft for overall drag estimate and flow over tail for different angle of attackand elevator deflections

> #### STAGE 1 DELIVERABLES:
>  ##### PROGRESS: COMPLETED 10/14 TASK ITEMS | 71.43% STAGE COMPLETION
> - 🛠️ Airfoil selection and justification
>    - ✅ Candidate airfoil Python / XFoil analyses
> - ✅ Wing sizing and aerodynamic hand calculations
>     - ✅ [Baseline Wing Geometry](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/BASELINE%20WING%20GEOMETRY.pdf)
>     - ✅ [Design Report, Stage 1.2a | Baseline Geometry Hand Calculations](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/BASELINE%20WING%20GEOMETRY.pdf)
> - ✅ 2D CFD results (plots, coefficient of lift versus angle of attack (C~L~/AoA), coefficient of drag versus angle of attack (C~D~/AoA)
>     - ✅ Preliminary airfoil screening in Python (script: [`airfoil_screening.py`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/airfoil_screening.py))
>     - ✅ Preliminary screening results verification in OpenFOAM (script: [`automate_2d_openFOAM.py`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/automate_2d_openFOAM.py))
>     - 🛠️ Comprehensive 2D CFD results in OpenFOAM | *Cases in processing. Once results and `design_report.md` overview have been updated, this WIP will be changed to completion.*
>       - ✅ Resultant figures, plots, datatables, and behavior desirability scoring in [`airfoil_selection.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/analysis/airfoil_screening/airfoil_selection.md)
>     - ✅ Narrow candidates based on Python screening and test in OpenFOAM
> - 3D CFD results (lift distribution, stall snapshots)
> - 🛠️ Aerodynamic summary in [`docs/design_report.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/docs/design_report.md)
> - ✅ [Systems Architecture Packet](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/6bd93b936ecec61f42fc100dc52f864d16c5f90f/docs/diagrams/Systems%20Architecture%20Packet.pdf)
>   - *This packet defines the system-level interactions, external context, information flow, system boundaries, and functional relationship between the pilot, ground controller, RF link, avionics electronics, sensors, servos, and power system. While not previously tied to this stage, it was important to formulate these decisions upfront.* 
>   - **(A)** System Context Diagram
>   - **(A1)** RF Architecture Diagram
>   - **(A2)** Controller Architecture Diagram
>   - **(A3)** Avionics Architecture Diagram
>   - **(A4)** RF Packet Structure Diagram
>   - **(A5)** Avionics Pinout Diagram
>   - **(A6)** Power Architecture Diagram 

## STAGE 2 | CAD and 3D Printed Structure
- Larger panels may be made using foamboard and components to be 3D printed may include the following:
  - Fuselage nosecone / electronics bay
  - Motor mount and firewall
  - Servo trays
  - Control horns
  - Tail boom clamps
  - Battery and PCB mounts
  - Cooling ducting

#### 2.1 | Control Surfaces and Mechanisms
- For each type of control surface (aileron, elevator, and rudder):
  - 3D print control horns with hole spacing tuned for desired throw versus servo arm length
  - Design servo mounts as a pocket or tray that accepts 9g-class servos, mounted by screws or snap-fits
  - Pushrods to be carbon rod or music wire, with clevis and/or Z-bend ends modeled or bought

#### 2.2 | PCB Mounting and Cooling
- Design considerations for the nose section:
  - Secure PCB with standoffs and screws
  - Ensure:
    - Air inlet under the spinner or nose for cooling
    - Channeled airflow over the ESC and reg chips
    - An exit vent near the fuselage’s rear to avoid pressure buildup
  - Keep the bay PCB away from the battery (heat) and any high-vibration motor axis
  - Possibly add a simple vibration isolating tray using TPU grommets or printed flexures

> #### STAGE 2 DELIVERABLES:
> - Complete 3D CAD model and 2D drawing sets for fuselage, wings, and tail
> - STL files for 3D printed components
> - Exploded assembly diagrams
> - Cooling and airflow reasoning in [`airframe/mounting_and_cooling.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/airframe/mounting_and_cooling.md)
> - All models stored under [`airframe/cad/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/airframe/cad)

## STAGE 3 | Avionics PCB (Aircraft)
#### 3.1 | Functional Blocks
- **3.1a | Power**
  - LiPo input, 2S/3S
  - ESC typically powers the motor; BEC or separate buck to 5 volts
  - LDO/buck from 5 volts to 3.3 volts for logic
  - TVS and reverse polarity protection
- **3.1b | MCU**
  - Pick an MCU with good timers and serial, possibly from the following:
    - STM32F4/F3, STM32G0, ATSAMD51 or RP2040 for familiarity
  - Timers to generate PWM for servos (3 – 6 channels), and one PWM for ESC
- **3.1c | Sensors**
  - 6-DoF IMU (MPU6050, ICM-20602, etc.)
  - Optional barometer like BMP280 or BME280
  - I2C bus with a layout giving good analog ground
- **3.1d | RF / RC Input**
  - **First Option:** Using a separate RF server module outputtting SBUS/PPM, with PCB decoding it
  - **Second Option:** Integrating an RF transceiver (possible 2.4 GHz module) and implementing own protocol (more work but more desirable)
- **3.1e | I/O**
  - Servo connectors for GND, 5V, and signal
  - Programming header (SWD/JTAG or USB if the MCU supports such)

#### 3.2 | PCB Design Notes
  - KiCAD will be used
  - Keep high-current paths such as those of the battery and ESC short and thick
  - Star-ground style or a clear division between power and logic sections
  - IMU should be placed near CG and away from motor/ESC to reduce noise and vibrations
  - Copper pours should be under power regulators to help with heat dissipation
  - Add test pads for IMU signals, RF signals, and RC input

> #### STAGE 3 DELIVERABLES:
> - KiCAD schematic and board layout in [`avionics/pcb/kicad/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/avionics/pcb/kicad)
> - Gerber manufacturing files in [`avionics/pcb/gerbers/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/avionics/pcb/gerbers)
> - Bill of Materials in [`avionics/pcb/bom/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/avionics/pcb/bom)
> - Power system documentation
> - All deliverables to be stored under [`avionics/pcb/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/avionics/pcb) as core directory
> - Update of [`docs/component_decisions.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/docs/component_decisions.md) with component selection and trade study document

## STAGE 4 | Ground Controller and Its PCB
#### 4.1 | Controller Hardware Concept
  - Two quality gimbal joysticks, controlling roll/pitch and yaw/throttle respectively
  - Switches for flight mode, arming
  - Lithium Ion/LiPo inside and charge ciruit
  - An RF module of the same family as that onboard the craft
  - **4.1a | PCB Responsibilities**
    - MCU (similar or simpler to the craft’s)
    - ADC for analog sticks
    - GPIO for switches
    - RF driver
    - Battery life measurement
  
#### 4.2 | Mechanical Design
  - 3D printed shell consisting of 2 to 3 parts for front, back, and a possible mid-frame
  - Mounts for gimbals, PCB, and battery
  - Ergonomic shape, potential of finger grooves for comfort and security

> #### STAGE 4 DELIVERABLES:
> - Controller CAD shell 3D model and 2D drawings in [`controller/cad/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller/cad)
> - Controller PCB schematic and layout in [`controller/pcb/kicad/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller/pcb/kicad)
> - Gerber files for manufacture in [`controller/pcb/gerbers/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller/pcb/gerbers)
> - Bill of Materials in [`controller/pcb/bom/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller/pcb/bom)
> - RF communication notes
> - All deliverables stored under [`controller/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller) as a core directory

## STAGE 5 | Firmware and Control Software
#### 5.1 | Plane Firmware Layers
  - **Layer 1: Drivers**
    - HAL for MCU
    - IMU and barometric drivers
    - PWM generation for the servos and ESC
    - RF / RC frame receiver
  - **Layer 2: Attitude Estimation**
    - Roll/Pitch/Yaw: Implement Mahony or Madgwick filter for IMU
    - Optionally fuse the barometrics for altitude
  - **Layer 3: RC Mapping**
    - Map the RC frames to desired roll, pitch, yaw, and throttle
    - **Modes:**
      - **MANUAL:** stick to servo and mixer
      - **STABILIZED:** stick to attitude target with inner PID loop
  - **Layer 4: Control**
    - Cascaded PIDs:
      - **Inner loop** to stabilize roll, pitch, and yaw (fast)
      - **Outer loop** to convert stick inputs to attitude targets
    - Elevator/aileron/rudder mixing based on control allocation
  - **Layer 5: Safety and Logging**
    - Develop a failsafe for lost signal
    - Disarm conditions
    - Log IMU, attitude, control outputs to SD/UART for post-flight analysis
    
#### 5.2 | Controller Firmware
  - Initialize gimbals (ADC)
  - Calibrate endpoints and pack into binary RC frame, e.g. 16-bit values per channel plus checksum
  - Transmit over RF at fixed rate (considering 50 – 100 Hz)
  - Implement failsafe timeout with user warning, LED indicators for link state, and a possible simple menu and/or craft live POV with OLED display

> #### STAGE 5 DELIVERABLES:
> - [`avionics/firmware/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/avionics/firmware) implementation
> - [`controller/firmware/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/controller/firmware) implementation
> - Driver tests
> - PID and AHRS test logs
> - Servo actuation demonstration
> - RF link communication demonstrated
> - Controller-specific component decisions added to [`docs/component_decisions.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/docs/component_decisions.md)

## STAGE 6 | CFD with OpenFOAM
#### 6.1 | OpenFOAM General Project Layout
  
- [`cfd/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd)
  - [`airfoil_2d/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/airfoil_2d)
    - [`system/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/airfoil_2d/case_setup/baseCase/system)
    - [`constant/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/airfoil_2d/case_setup/baseCase/constant)
    - [`0/*`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/airfoil_2d/case_setup/baseCase/0)
  - [`wing_3d/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/wing_3d)
    - [`mesh/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/wing_3d/mesh)
    - [`system/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/wing_3d/case_setup/baseCase/system)
      - [`constant/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/wing_3d/case_setup/baseCase/constant)
      - [`0/*`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/wing_3d/case_setup/baseCase/0)

*The 0/ directories have duplicate, easier-to-read directories for users unfamiliar with CFD. Please see [`README.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/airfoil_2d/case_setup/README.md) for 2D and [`README.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/cfd/wing_3d/case_setup/README.md) 3D for information so you can browse the directory most suited to your needs. By default, the two directories linked above are the OpenFOAM-ready ones.

#### 6.2 | Work Plan
- **6.2a | 2D Airfoil Case**
  - Clean 2D geometry of the chosen airfoil
  - Simple incompressible flow case at the relevant Reynolds number
  - Post process the Cl versus Angle of Attack, and Cd versus Angle of Attack
  - Use results to confirm the chosen AoA at cruise and estimate the stall margin
- **6.2b | 3D Wing**
  - Half-span with a symmetry plan for cost reduction
  - Include aileron deflection for some cases
  - Look at lift distribution, induced lag, and response to small control surface deflections
- **6.2c | Documentation**
  - For each case, keep mesh details, boundary conditions, and plots from postprocessing/

> #### STAGE 6 DELIVERABLES:
> - Completed airfoil and wing CFD cases
> - Mesh visualization
> - Forces and aerodynamic performance plots
> - 2D deliverables stored under [`cfd/airfoil_2d/postprocessing/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/airfoil_2d/postprocessing), 3D deliverables stored under [`cfd/wing_3d/postprocessing/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/cfd/wing_3d/postprocessing)
> - Stage summary in [`docs/design_report.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/docs/design_report.md)

## STAGE 7 | Testing and Safety
#### 7.1 | Bench Testing
- **7.1a | Electronics**
  - Power on with current-limited bench supply
  - Verify no overheating at the expected load
  - Run servos through full travel repeatedly, logging current and MCU temperatures
- **7.1b | Firmware**
  - Inject fake IMU data and RC commands, verifying control outputs
  - Add testing units for RC frame parsing, attitude filter, and PID controllers
  
#### 7.2 | Ground Integration Testing
- With the plane clamped to a stand:
  - Move the plane, paying attention to live attitude estimates
  - Move the controller sticks, confirm control surface motion, direction, and magnitude
- Move into a range test by walking away with the controller to verify link integrity

#### 7.3 | Flight Testing
- Start with tossed ground tests in a well-padded area like tall grass, not using motor, to test trim an CG
- With the addition of the motor, move into low-level manual flights
- After enabling stabilization, practice gentle, high-altitude flights
- Always fligh in a safe and legal RC flying area clear of people, roads, and obstacles, within applicable regulations
- Log flights in [`docs/flight_logs/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/docs/flight_logs)

> #### STAGE 7 DELIVERABLES:
> - Bench test results
> - Integration test logs
> - Flight logs in [`docs/flight_logs/`](https://github.com/chrisdillow/Tropochief-RC-Plane/tree/main/docs/flight_logs)
> - Final report sections added to [`docs/design_report.md`](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/main/docs/design_report.md)

# Timeline
> Overall expected time, if sole focus is on project, is 10 – 14 weeks.

#### ✅ Weeks 1 – 2
> **START DATE:** November 15, 2025
> 
> **END DATE:** December 1, 2025
> 
> **ON-TIME STATUS:** On Schedule
- ✅ Set requirements and constraints
- ✅ Generate system architecture documents
- ✅ Make rough hand calculations, informing selection of airfoil and component geometry
- ✅ Start 2D airfoil CFD

#### 🛠️ Weeks 3 – 4
> **START DATE:** December 1, 2025
- Build parametric, formula-driven CAD models of the basic airframe
  - Create 2D drawings of the components and assembly per ASME standards
- Model control surfaces and servo mounts
- 🛠️ 3D wing CFD

#### Weeks 5 – 6
- Draft the avionics PCB’s schematics and layout
- Design controller PCB
- Use developed files to order the PCBs’ manufacturing, keeping BOM on file

#### Weeks 7 – 8
- Finish fuselage CAD modeling, PCB mounts, and cooling pathways
- Assemble and solder manufactured PCBs
- Bring up basic firmware (blinky, IMU reading, servo driving)

#### Weeks 9 – 10
- Implement attitude estimation and stabilization loops
- Implement the RC protocol between the controller and craft
- Perform bench and ground testing

#### Weeks 11 – 14
- Walk through the test protocol beginning at glide tests, moving to manual powered flight, and finalizing with testing flight in the stabilized mode
- Tune PIDs, capture logs, iterate
- Create final documentation and get a video of final product in action
