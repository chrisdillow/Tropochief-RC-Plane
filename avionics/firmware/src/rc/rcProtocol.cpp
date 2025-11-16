// Tropochief Project
// Chris Dillow
// Avionics Firmware RC: Protocol

// ======================================== //
// |           FILE DESCRIPTION           | //
// ======================================== //
// Parse RF packets into normalized channel values [-1.0,+1.0], validate checksum, and handle signal loss detection when no packet has been received
// in a predetermined count of milliseconds.
