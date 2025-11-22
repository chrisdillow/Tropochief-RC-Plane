# Component Decisions and Trade Study
#### Part of Tropochief RC Aircraft Project
#### Chris Dillow
###### Version 1.0 - November 16, 2025

# 1 | Purpose of This Document
This document records evaluated components, alternative options, and the rationale behind each design choice for both the aircraft's avionics PCB and the ground controller PCB.
It provides transparency for future maintainers, reviewers, and hiring managers evaluating its engineering decision-making process.
This document follows industry practice for trade studies and system architecture documentation.

# 2 | Microcontroller Selection
#### 2.1 | Requirements
- Must support a ≥ 100-500 Hz attitude control loop
- Must support IMU over I^2^C / SPI
- Must support ≥ 6 PWM channels for servos and ESC
- Must tolerate RC frame decoding (SBUS / PPM or custom RF)
- Should have mature embedded libraries and HAL
- Should be available in LQFP or QFN for hand assembly

#### 2.2 | Candidate MCUs
- **STM32F4 Series (Cortex-MF4)**
    - High-performance floating point
    - Flight controller standard (PX4, Betaflight)
    - [Manufacturer Datasheet](https://www.st.com/en/microcontrollers-microprocessors/stm32f4-series.html)
    - **PROS:** Excellent performance with a large ecosystem
    - **CONS:** Higher power draw
- **STM32F3 Series (Cortex-M4 with strong analog)**
    - Enhanced ADC and timers
    - Used widely in older Betaflight FCs
    - [Manufacturer Datasheet](https://www.st.com/en/microcontrollers-microprocessors/stm32f3-series.html)
    - **PROS:** A stable microcontroller with great timing
    - **CONS:** It is less powerful than the F4
- **STM32G0 Series (Cortex-M0+)**
  - Cost-efficient with low power requirements
  - [Manufacturer Datasheet](https://www.st.com/en/microcontrollers-microprocessors/stm32g0-series.html)
  - **PROS**: A cheap and simple microcontroller
  - **CONS**: No floating point and may limit AHRS
- **ATSAMD51 (Microchip - Cortex-M4F)**
  - [Manufacturer Datasheet](https://www.microchip.com/en-us/product/atsamd51n19a)
  - **PROS:** The simplicity of the Arduino ecosystem, paired with high clock speeds
  - **CONS:** Not a common choice in UAV control
- **RP2040 (RaspberryPi - Dual M0+)**
  - [Manufacturer Datasheet](https://www.raspberrypi.com/documentation/microcontrollers/silicon.html)
  - **PROS:** PIO subsystem and large community
  - **CONS:** No hardware floating point

#### 2.3 | Familiarity Justification
- **STM32 family** from use in robotics, aerospace, and Betaflight / ArduPilot ecosystems
- **RP2040** from making ecosystem and low-level timing tasks
- **ATSAMD51** from the Arduino / Feather ecosystem
The familiarity with these options will allow for a shorter development time, higher debugging confidence, and access to known high-quality libraries and tools.

#### 2.4 | Preliminary Decision
**Leaning Toward: STM32F405 or STM32F411**

Due to:
- Floating point for AHRS
- Excellent timer subsystem
- Known flight controller heritage
The final decision will be documented once AHRS and PWM timing requirements are tested in firmware prototypes.

# 3 | IMU (Inertial Measurement Unit)
#### 3.1 | Requirements
- A high-rate gyroscope and acclerometer
- Minimal drift
- Good vibration rejection
- SPI preferred
- 1-2 KHz update rate optional

#### 3.2 | Candidate IMUs
- **MPU-6000 / MPU-6050**
    - An industry standard for Betaflight
    - [Manufacturer Datasheet](https://invensense.tdk.com/products/motion-tracking/6-axis/mpu-6050/)
    - **PROS:** Very vibration tolerant
    - **CONS:** Limited availability and at the end of its production life
- **ICM-42688-P**
  - A newer IMU on the market, providing high performance with low noise
  - [Manufacturer Datasheet](https://invensense.tdk.com/products/motion-tracking/6-axis/icm-42688-p/)
  - **PROS:** A modern IMU with low drift
  - **CONS:** More sensitive to board layout
- **BMI-270 (Bosch)**
  - A common IMU in wearables
  - [Manufacturer Datasheet](https://www.bosch-sensortec.com/products/motion-sensors/imus/bmi270/)
  - **PROS:** Very low-power
  - **CONS:** Less proven in flight controllers

#### 3.3 | Preliminary Decision
**Leaning Toward: ICM-42688-P**

Due to:
- Being a strong, modern replacement for the MPU-6000
- Excellent low-noise performance

# 4 | RF Link (Receiver / Transmitter Protocol)
#### 4.1 | Requirements
- ≥ 50-100 Hz update rate
- A range of at least 300-500m for practicality
- Preference for < 150 mA power draw
- Low latency
- Failsafe mode for lost links
- Easy PCB integration (SPI/UART preferred, must be mountable)

#### 4.2 | Candidate Options
- **LoRa (SX127x)**
  - A long range, low-bitrate radio used in IoT
    - Uses chirp spread spectrum for long-distance, low-power communication.
    - While very robust, it has a low update rate which makes it poorly suited for real-time control.
  - [Manufacturer Datasheet](https://www.mouser.com/pdfdocs/sx1276_77_78_79.pdf)
  - **PROS:**
    - An extremely long range into multiple kilometers
    - Very robust to interference
    - Low power consumption
    - Easy to configure via SPI
    - Excellent for telemetry
  - **CONS:**
    - Very low bandwidth
    - High latency
    - Not suitable for real-time RC control
    - Overkill for < 1 km range applications
- **nRF24L01+ (2.4 GHz)**
  - A widely-used 2.4 GHz radio with high throughput and low cost, it is common in DIY transmitters and small robotics systems.
  - [Manufacturer Datasheet](https://cdn.sparkfun.com/assets/3/d/8/5/1/nRF24L01P_Product_Specification_1_0.pdf)
  - **PROS:**
    - Very low cost
    - A high update rate with over 100 Hz possible
    - Low latency
    - Widely used in DIY RC systems
    - Easily found in multiple PCB module variants
    - Low power draw
  - **CONS:**
    - Limited interference resilience
    - There is no native frequency hopping, requiring this to be manually implemented
    - Practical range is under 300 meters without PA / LNA
    - Consumer module QC varies
- **SX1280 / SX1281 (2.4 GHz)**
  - A high performance, long range 2.4 GHz transceiver capable of frequency hopping, low latency, and robust performance. It is the foundation of ExpressLRS.
  - [Manufacturer Datasheet]([https://robu.in/wp-content/uploads/2020/01/0a-esp8285_datasheet_en-1223891.pdf](https://www.mouser.com/datasheet/2/761/sx1280_81-1107808.pdf?srsltid=AfmBOoojazG3oGVzp17xVCja7JZkT6nJp945NEc9WDAj3TKU1FwUZ-_a))
  - **PROS:**
    - It is exceptionally robust for being 2.4 GHz
    - It can achieve very low latencies below 5 milliseconds
    - Supports LoRa and FLRC modulations
    - FHSS (Frequency Hopping Spread Spectrum)
    - Good range even at low power
    - Made of modern silicon and has strong community support
  - **CONS:**
    - More complex integration, though only slightly
    - Requires careful antenna design
    - It has a higher current draw than the nRF24L01+
- **ExpressLRS (ELRS modules using ESP8285/ESP32 and SX1280)**
  - A complete RC protocol stack built on SX1280 radios and ESP-based MCUs. It has ultra low latency, strong error correction, and a mature open source ecosystem.
    - Can be used directly, the plane's own RC protocol can be modeled after it, or the project could use the same chip but write simple 50-100 Hz frames
  - [Manufacturer Datasheet](https://robu.in/wp-content/uploads/2020/01/0a-esp8285_datasheet_en-1223891.pdf)
  - **PROS:**
    - State of the art RC protocol
    - An extremely low latency under 4 milliseconds
    - Long range of 0.5-5 km depending on choice of settings
    - A strong open source community
    - Automatic frequency hopping
    - Supports fully custom firmware builds
  - **CONS:**
    - Higher software complexity
    - Requires ESP-based architecture for full ELRS compatibility
    - May be overkill
    - Protocol is complex to implement from scratch

#### 4.3 | Preliminary Decision
**Leaning Toward: SX1280 with a simple custom control protocol**

Due to:
- Incredible latency
- Much simpler to implement than full ELRS
- Strong middle ground between DIY simplicity and high performance
- Provides the opportunity to practice and demonstrate custom protocol engineering
- Allows later upgrade to ExpressLRS if desired
- Excellent industry relevance and is widely used in RC systems
- Good range
- Modern 2.4 GHz FHSS

# 5 | Power System Components
#### 5.1 | Voltage Regulators
##### 5.1a | Voltage Regulator Requirements
- Must step down 2S-3S LiPo (6.6-12.6 V) to:
  - 5.0 V for servos, ESC BEC bypass
  - 3.3 V for MCU, IMU, and RF
- Must support ≥ 2A continuous on the 5 V rail, where servos are current spikes
- Must have a low ripple for IMU noise immunity
- Preference for a switching regulator for efficiency, as linear LDOs eat too much power
- Should have a small footprint and be available in common packages
- Regulator current requirements remain **TBD** and depend on:
    - Servo torque sizing from aerodynamic control surface area
    - Maximum simultaneous servo deflection under stabilization control

##### 5.1b | Voltage Regulator Candidates
- **MP1584EN (Monolithic Power Systems)**
  - A common inexpensive 3A buck regulator often used in RC, robotics, and 3D printing.
  - [Manufacturer Datasheet](https://www.monolithicpower.com/en/mp1584.html)
  - **PROS:**
    - Cheap and widely available
    - Up to 3A output
    - Adjustable Vout (fixed resistors or pot)
    - A good efficiency in the 80-90% range
  - **CONS:**
    - Produces higher noise than premium regulators
    - Will require a careful layout to avoid EMI
    - Breakout boards often use small indicators
- **TPS5430 / TSP54331 (Texas Instruments)**
  - High quality regulators by Texas Instruments and are commonly used in commercial embedded systems.
  - [Manufacturer Datasheet](https://www.ti.com/lit/ds/symlink/tps54331.pdf)
  - **PROS:**
    - Super reliable
    - Low ripple if properly laid out
    - 3A capable
    - Strong EMI behavior
  - **CONS:**
    - Higher price point
    - Requires more external components
- **AP63203 / AP63205 (Diodes Inc.)**
  - These are modern low noise buck converters with integrated MOFSETs and high switching frequency.
  - [Manufacturer Datasheet](https://cdn.sparkfun.com/assets/e/3/d/9/d/AP63200-AP63201-AP63203-AP63205.pdf)
  - **PROS:**
    - A very low ripple making it excellent for sensors
    - A very small footprint
    - High efficiency
  - **CONS:**
    - 2A typical max current puts it lower than other candidates
    - Some versions are harder to source than other candidates

##### 5.1c | Preliminary Decision
**Learning Toward: TPS54331 (TI)**
Due to:

- Best balance of noise performance, efficiency, and reliability
- Perfect for avionics where IMU noise immunity is important

> ##### DELIVERABLE:
> Choose based on load, thermal budget, and servo load.

#### 5.2 | ESC (Electronic Speed Controller)
##### 5.2a | ESC Requirements
- Must support selected brushless motor current rating (≈ 12-20A)
- Must accept standard RC PWM input
- Should provide a smooth throttle response
- Preference for modern firmware like BLHeli_S or BLHeli_32
- Must NOT supply its own 5V BEC if using an onboard regulator, to avoid conflicts
- Should have reliable startup and minimal weight
- ESC current capacity remains **TBD** and will be finalized after propulsion sizing based on CFD drag estimates and thrust calculations.

##### 5.2b | ESC Candidates
- **BLHeli_S 20A ESC (Generic / Racerstar / T-Motor)**
  - Widely used in FPV drones and has smooth communication, making it good for small fixed-wing crafts.
  - [Manufacturer Datasheet](https://www.getfpv.com/racerstar-rs20a-blheli-s-4-in-1-esc.html?srsltid=AfmBOoqPa-DU0y2fIJs00B6b7kmjIzP9AZPG2898oOfMLSNziYB-rdJG)
  - **PROS:**
    - Smooth throttle
    - 6-8g mass makes it lightweight
    - Good startup behavior and configurabiltiy
  - **CONS:**
    - Many clones with varying quality
    - Needs an external 5V BEC (no onboard regulator in many modules)
- **HobbyWing Skywalker Series**
  - A classic RC fixed-wing ESC with strong reliability.
  - [Manufacturer Datasheet](https://www.hobbywingdirect.com/products/skywalker-esc-20a?srsltid=AfmBOooU8dL675Pgjqgs88mEJCBMAdhjZd-d4jUwo7EC2roHbpMhI1ER)
  - **PROS:**
    - Extremely reliable
    - Designed for airplanes
    - Onboard BEC that can be disabled if needed
    - Good throttle linearity
  - **CONS:**
    - Heavier than other candidates
    - Larger size than other candidates
    - More expensive than other candidates
- **ZTW Mantis 20A ESC**
  - Known for its very stable performance in wings and gliders.
  - [Manufacturer Datasheet](https://ztwesc.com/products/ztw-mantis-slim-g2-20a-2-4s-sbec-for-rc-rc-airplane-f3p-3d-flying)
  - **PROS:**
    - Good thermal performance
    - Solid throttle under load
    - Very smooth startup
  - **CONS:**
    - Less common in the maker ecosystem
    - More expensive and larger than other candidates

##### 5.2c | Preliminary Decision
**Leaning Toward: BLHeli_S 20A ESC**
Due to:

- Best size, weight, and performance for our target aircraft class
- Will require an external 5V regulator, but this is already planned

> ##### DELIVERABLE:
> Select an ESC from candidates.

#### 5.3 | Battery (LiPo)
##### 5.3a | Battery Requirements
- 2S or 3S LiPo
- 850-1300 mAh
- Able to supply the craft systems with 20-30A bursts
- Should keep the wing loading moderate
- Preference for XT30 connector
- Avoid excess mass in nosecone
- Final battery capacity and C-rating are **TBD** and depend on:
    - Drag and lift characteristics from CFD
    - Target endurance time
    - Weight budget required to maintain center of gravity location

##### 5.3b | Battery Candidates
- **2S 1300 mAh (30-50C)**
  - A good mid-power pack, offering lighter weight and lower voltage.
  - [Manufacturer Datasheet](https://maxamps.com/products/lipo-1300-2s-battery?srsltid=AfmBOopqaAQf--Lw7F8wjqROkLNm8mijYJo-R4K59KfHL83iax4TIlip)
  - **PROS:**
    - Light weight
    - Safe power levels
    - Good endurance
  - **CONS:**
    - Lower thrust margin
- **3S 850 mAh (30-75C)**
  - A small high-voltage pack.
  - [Manufacturer Datasheet](https://lv.mouser.com/datasheet/2/855/ASR00036_850mAh-3078656.pdf)
  - **PROS:**
    - High energy-to-weight ratio
    - Great thrust on small motors
  - **CONS:**
    - Shorter flight time
    - Higher motor Kv sensitivity
- **3S 1300 mAh (30-75C)**
  - The most common park-fly battery.
  - [Manufacturer Datasheet](https://maxamps.com/products/lipo-1300-3s-battery?srsltid=AfmBOoqwUF1gni22OVYrBwiBbagINJ0L5hBxECtO_1dg1dJ1_c9CWfBW)
  - **PROS:**
    - Best all-around performance of the candidates
    - Excellent thrust margin
    - Readily available
  - **CONS:**
    - Heavier than other candidates, increasing wing loading

##### 5.3c | Preliminary Decision
**Leaning Toward: 3S 1300 mAh Pack**
Due to:

- Strong performance
- Good availability
- Balanced weight for a 0.8-1.2m wing

> ##### DELIVERABLE:
> Select a battery depending on wing loading, target cruise speed, and motor thrust data.

# 6 | Servo Selection
#### 6.1 | Requirements
- While the elevator and rudder could use the MG90S (see 6.2, Bullet 2), the ailerons may require higher torque depending on final wing design.
- Weight < 13g for micro servos
- Torque ≥ 1.5-2.0 kg*cm for the ailerons and elevator
- Preference for a metal gear for durability
- Standard 3-pin connector
- Smooth centering
- Servo torque requirements are **TBD** pending airfoil selection, control surface geometry, and hinge moment estimation.

#### 6.2 | Servo Candidates
- **SG90 Micro Servo (Plastic Gear)**
  - A very common servo with an ultra low cost.
  - [Manufacturer Datasheet](http://www.ee.ic.ac.uk/pcheung/teaching/DE1_EE/stores/sg90_datasheet.pdf)
  - **PROS:**
    - Cheap
    - Lightweight
    - Very available
  - **CONS:**
    - Utilizes plastic gears, which strip easily
    - Poor centering accuracy
    - Not ideal for aircraft with stabilizers/PIDs
- **MG90S Micro Servo (Metal Gear)**
  - The most common upgrade from the SG90.
  - [Manufacturer Datasheet](https://www.electronicoscaldas.com/datasheet/MG90S_Tower-Pro.pdf?srsltid=AfmBOor04auhRXSi8BbJWCSRzOaxeNjA_8aLjxHJsa7BNN72i6dIx_Tl)
  - **PROS:**
    - Uses metal gears
    - Better centering than its plastic counterpart
    - A good torque of roughly 2.2 kg*cm
    - Reliable for fixed wing craft
  - **CONS:**
    - Slightly heavier than its plastic counterpart
    - Not as smooth as premium servos
- **KST X06 or X08 (Mini High Performance)**
  - These are premium micro servos used in gliders and high-performance aircraft.
  - [Manufacturer Datasheet](https://kstservos.com/products/x06-v6-0-hv-micro-digital-metal-gear-glider-1-8kg-torque-servo-motor?srsltid=AfmBOoqaDYd_oSvcrIyZNZYDPjYfbt0SqMddFjzXnymDxKyjul_zSyj1)
  - **PROS:**
    - Extreme precision
    - Coreless and brushless options
    - Exceptional centering
    - Lightweight
  - **CONS:**
    - Expensive
    - Overkill for a project of this scale

#### 6.3 | Preliminary Decision
**Leaning Toward: MG90S (Metal Gear)**
Due to:

- Best balance of precision, durability, torque, and cost

> ##### DELIVERABLE:
> Select a servo.

# 7 | Connectors and Wiring
#### 7.1 | Requirements
- Must support the expected current
- Must be vibration tolerant
- Must be easy to assemble
- Preference for common ecosystem parts
- Prevent accidental reverse polarity
- Final connector choices depend on:
    - PCB layout constraints from Stage 3
    - EMI/RF susceptibility considerations
    - Mechanical mounting and vibration environment

#### 7.2 | Connector / Wiring Candidates
- **XT30 (Battery Connector)**
  - Common in 30-40A systems and park flyers.
  - [Manufacturer Datasheet](https://www.gobilda.com/xt30-connector-pack-fh-mc-x-5-mh-fc-x-5/?srsltid=AfmBOoqIsUS3nRjB2oDYJG0rNemh0smrZmrVGz3ddstN3tXQDcOEum_B)
  - **PROS:**
    - Robust
    - Hard to misplug
    - Good for continous 30A applications
  - **CONS:**
    - Larger than the JST-PH
- **JST-PH 2.0mm (Sensor/Power)**
  - Common for small electronics and battery balance leads.
  - [Manufacturer Datasheet](https://www.jst-mfg.com/product/index.php?series=199)
  - **PROS:**
    - Lightweight
    - Cheap
    - Good for sensors
  - **CONS:**
    - Not suitable for servo-level currents
- **Servo 3-Pin Header (Standard RC)**
  - A female 3-pin Dupont style header. Generic, with 2.54mm pitch servo connectors.
  - [Manufacturer Datasheet](https://www.scondar.com/wire-to-wire/dupont-2-54mm-pitch-connectors/)
  - **PROS:**
    - RC Standard
    - Very convenient
    - Good for 3-5A servo bursts
  - **CONS:**
    - Not locking
    - Can wiggle loose without foam or glue
- **DF13 (Pixhawk-style locking connectors)**
  - High quality locking connectors used in flying robots.
  - [Manufacturer Datasheet](https://www.mouser.com/datasheet/3/3720/1/Datasheet_AS-CAB-PIXHAWKSET-00_Pixhawk_cable_set.pdf?srsltid=AfmBOooeFhNfflSgkXPmZKjmNP-87ggipQ7L88eNGVWtnxCCdRz6pxnY)
  - **PROS:**
    - Locking
    - Vibration-proof
    - High quality
  - **CONS:**
    - More expensive than other candidates
    - Harder to manually crimp than other candidates

#### 7.3 | Preliminary Decision
**Leaning Toward: XT30 for the battery, JST-PH 2.0 for the sensors, the standard 3-pin header for the servo heads, and option of picking up a DF13 for the IMU or critical avionics signals**

# 8 | Final Notes
- All choices are subject to revision after preliminary CAD and thermal analyses.
- Final component selections will be locked in during schematic design.
- This document will version-track all decisions.
