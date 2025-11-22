# Project Requirements
##### Tropochief Aircraft Project
##### Chris Dillow
##### Version 1.0 | November 22, 2025
##### Status: Stage 1 - System Definition Complete

## 1 | Introduction
This document defines the project requirements for the Tropochief RC aircraft, including functional behavior, system interfaces, avionics capabilities, RF communication expectations, power system constraints, and airframe integration considerations. These requirements will evolve as the project progresses through design, simulation, fabrication, and testing stages.

## 2 | System Context Requirements
These requirements arise from the System Context Diagram ([Systems Architecture Packet, Pg. A](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/6bd93b936ecec61f42fc100dc52f864d16c5f90f/docs/diagrams/Systems%20Architecture%20Packet.pdf)) and describe how the aircraft system interacts with external actors and the operating environment.

#### 2.1 | Pilot and Ground Controller Interface
- The system must accept manual pilot input though a handheld ground controller.
- The ground controller must transmit command signals wirelessly to the aircraft.
- The system must allow pre-flight configuration and functional testing on the ground.

#### 2.2 | Operating Environment
- The aircraft must operate in an outdoor space subject to wind and gust disturbances.
- The aircraft must remain controllable within typical recreational flight envelopes.
- The system must comply with safe visual line-of-sight operation.

#### 2.3 | Tests and Data Collection
- The aircraft must support a ground testing interface for calibration and firmware updates.
- The system must support retrieval of flight data for post-flight analysis.

## 3 | RF Link Requirements
Derived from the RF Architecture and RF Packet Structure Diagrams ([Systems Architecture Packet, Pg. A1 and A4](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/6bd93b936ecec61f42fc100dc52f864d16c5f90f/docs/diagrams/Systems%20Architecture%20Packet.pdf)).

#### 3.1 | Command Link Performance
- The RF link must operate in the 2.4 GHz ISM band.
- The RF protocol must implement frequency hopping (FHSS).
- The RF link must transmit at least four primary control channels and two auxiliary channels.
- The command update rate must be ≥ 100 Hz (TBD: final value).
- CRC-based error detection must be included in every frame.

#### 3.2 | Failsafe Behavior
- The aircraft must detect loss of valid RF frames within 200 ms.
- Upon failsafe activation, the aircraft must:
  - Set throttle to zero
  - Neutralize control surface outputs

## 4 | Avionics Requirements
Derived from the Avionics Architecture and Avionics Pinout Diagrams ([Systems Architecture Packet, Pg. A3 and A5](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/6bd93b936ecec61f42fc100dc52f864d16c5f90f/docs/diagrams/Systems%20Architecture%20Packet.pdf)).

#### 4.1 | MCU Interfaces
- The avionics MCU must provide at minimum:
  - Two SPI interfaces, one for each of the IMU and RF transceiver
  - Four PWM outputs; for each of the rudder, elevator, and left/right ailerons
  - One UART interface for debugging/telemetry
  - One ADC input for voltage sensing

#### 4.2 | Control Loop Performance
- The avionics control loop must operate between 200 and 500 Hz **(TBD: final value)**.
- The IMU must support update rates suitable for AHRS and stabilization **(≥ 1 KHz; TBD: final value)**.

#### 4.3 | IMU Placement
- The IMU must be mounted near the aircraft's center of gravity.
- The IMU must align with the aircraft's body axes.

## 5 | Power System Requirements
Derived from the Power Architecture Diagram ([Systems Architecture Packet, Pg. A6](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/6bd93b936ecec61f42fc100dc52f864d16c5f90f/docs/diagrams/Systems%20Architecture%20Packet.pdf)).

#### 5.1 | Power Rails
- The aircraft must include two regulated power domains:
  - 5V servo rail
  - 3.3V (or 5->3.3V stepdown) avionics rail

#### 5.2 | Current Capacity
**(TBD: dependencies)**
- Servo rail current rating, **TBD** pending the following:
  - Servo selection
  - Control surface sizing
  - Aerodynamic hinge moment calculations
- Avionics rail ripple performance, **TBD** pending the following:
  - IMU filtering needs
  - PCB layout considerations

#### 5.3 | Battery Characteristics
**(TBD: dependencies)**
- The system must operate from a 3S LiPo battery.
- Capacity 850-1300 mAh, C-rating, and weight, **TBD** pending the following:
  - CFD drag estimates
  - Propulsion sizing
  - Target endurance

## 6 | Airframe Integration Requirements
Derived from [Systems Architecture](https://github.com/chrisdillow/Tropochief-RC-Plane/blob/6bd93b936ecec61f42fc100dc52f864d16c5f90f/docs/diagrams/Systems%20Architecture%20Packet.pdf) and avionics layout constraints.

- The airframe must provide:
  - A component for the avionics PCB **(TBD: footprint)**
  - Mounting location for the LiPo battery **(TBD: capacity)**
  - Routing paths for servo wiring
  - RF antenna placement, minimizing shadowing
- The airframe must maintain CG compatibility with avionics and battery mass.

## 7 | Requirement Evolution and Traceability
- Requirements marked with **"TBD"** will be finalized during Stage 2 and Stage 3 based on:
  - CFD aerodynamic results
  - Airframe mass estimates
  - Propulsion testing
  - Servo torque validation
  - PCB design constraints
- Requirement revisions will be documented in this file and tracked via Git.

## 8 | Next Requirement Development Stage
The next major requirement expansion will occur at:

#### Stage 2 | Airframe CAD and Aerodynamic Sizing
This will introduce:

- Wing loading targets
- Control surface areas
- Structural envelope constraints
- Component placement geometry
- Propulsion thrust requirements
