// Tropochief Project
// Chris Dillow
// Avionics Firmware Control: Attitude Estimator

// ======================================== //
// |           FILE DESCRIPTION           | //
// ======================================== //
// Should implement choice of Mahony or Madgwick filter.
// Takes inputs from gyroscope, accelerometer, dt
// Shall output quarternion and/or Euler angles (roll, pitch, and yaw)
// OPTIONAL: If desired, provide a gravity-compensated acceleration estimate.
