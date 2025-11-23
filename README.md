# Tropochief-RC-Plane
A full-stack project to design, develop, and test all aspects of a remote controlled plane spanning mechanical design, electronics design, embedded programming, aerodynamics simulation, testing, and documentation.

# Project Overview

- **Airframe Control Surfaces** Modeled and drafted in CAD then 3D printed for production
- **Onboard Avionics PCB** consisting of an MCU, IMU, RF, servo and ESC drive
- **Handheld Ground Controller** utilizing a custom PCB, gimbals, and RF design
- **Firmware** for plane and controller, encompassing attitude estimation, stabilization, and RC protocol
- **CFD Analysis** Performed in OpenFOAM for wing/airfoil validation
- **Testing, Logging, and Documentation**

The Tropochief project is a from-scratch, non-proprietary project intended to showcase mechanical, electrical, and software engineering skills in an aerospace context.

---

## Project Goals

- Design a small, stable electric remote controlled aircraft.
- Implement custom avionics and transmitter hardware utilizing self-designed PCBs and 3D printed assembly components.
- Write the complete firmware stack:
  - RC link protocol (TX ↔ RX)
  - Attitude estimation (IMU fusion)
  - Cascaded PID stabilization of roll/pitch/yaw
- Validate aerodynamic performance with CFD through OpenFOAM and basic analytical methods.
- Document build, tuning, and testing as if for a design review.

---

## Repository Structure

```text
rc-plane-fullstack/
├── images/
├── analysis/
│   └── airfoil_screening/
│
├── airframe/
│   ├── cad/
│   │   ├── fuselage/
│   │   ├── wing/
│   │   ├── tail/
│   │   └── control_surfaces/
│   ├── mass_properties/
│   └── mounting_and_cooling.md
│
├── avionics/
│   ├── pcb/
│   │   ├── kicad/
│   │   ├── gerbers/
│   │   └── bom/
│   └── firmware/
│       ├── src/
│       │  ├── control/
│       │  ├── drivers/
│       │  ├── rc/
│       │  ├── util/
│       │  ├── boardConfig.cpp
│       │  └── main.cpp
│       ├── include/
│       │  ├── control/
│       │  ├── drivers/
│       │  ├── rc/
│       │  ├── util/
│       │  └── boardConfig.h
│       └── tests/
│
├── controller/
│   ├── cad/
│   ├── pcb/
│   │   ├── kicad/
│   │   ├── gerbers/
│   │   └── bom/
│   └── firmware/
│       ├── src/
│       │  ├── drivers/
│       │  ├── ui/
│       │  ├── boardConfig.cpp
│       │  ├── calibration.cpp
│       │  ├── calibration.cpp
│       │  └── rcFrame.cpp
│       ├── include/
│       └── tests/
│
├── cfd/
│   ├── airfoil_2d/
│   │   ├── case_setup/
│   │   └── postprocessing/
│   └── wing_3d/
│       ├── case_setup/
│       ├── mesh/
│       └── postprocessing/
│
├── sim/
│   ├── python/
│   └── matlab_octave/
│
└── docs/
    ├── requirements.md
    ├── test_plan.md
    ├── flight_logs/
    ├── diagrams/
    └── design_report.md
