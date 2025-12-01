/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  v2506                                 |
|   \\  /    A nd           | Website:  www.openfoam.com                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
// WRITTEN BY CHRIS DILLOW | NOVEMBER 29, 2025 | TROPOCHIEF RC PLANE PROJECT
// FIELD: Pressure
FoamFile
{
    version 2.0;
    format ascii;
    class volScalarField;
    location "0";
    object p;
}

dimensions [0 2 -2 0 0 0 0]; // Pa

internalField uniform 0;

boundaryField
{
    inlet
    {
        type zeroGradient;
    }

    outlet
    {
        type fixedValue;
        value uniform 0;
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
        type zeroGradient;
    }

    frontAndBack
    {
        type empty;
    }
}