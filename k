/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  v2506                                 |
|   \\  /    A nd           | Website:  www.openfoam.com                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
// WRITTEN BY CHRIS DILLOW | NOVEMBER 29, 2025 | TROPOCHIEF RC PLANE PROJECT
// FIELD: Turbulent Kinetic Energy
FoamFile
{
    version 2.0;
    format ascii;
    class volScalarField;
    location "0";
    object k;
}

dimensions [0 2 -2 0 0 0 0]; // m^2/s^2

// ~1% turbulence at 30 m/s (order-of-magnitude)
internalField uniform 0.135;

boundaryField
{
    inlet
    {
        type fixedValue;
        value uniform 0.135;
    }

    outlet
    {
        type zeroGradient;
    }

    top
    {
        type zeroGradient;
    }

    bottom
    {
        type zeroGradient;
    }

    airfoil
    {
        type kqRWallFunction;
        value uniform 0.135;
    }

    frontAndBack
    {
        type empty;
    }
}