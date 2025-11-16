// Tropochief Project
// Chris Dillow
// Avionics Firmware Control: Mixer

// ======================================== //
// |           FILE DESCRIPTION           | //
// ======================================== //
// Takes in the control outputs (rollCMD, pitchCMD, yawCMD, throttle) and converts to the following individual surface deflections:
//    Aileron Left/Right, Elevator, Rudder, Throttle (ESC)
// Shall handle different mixing schemes, i.e., a V-tail, if implemented
