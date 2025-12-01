#Tropochief RC Plane Project
#Chris Dillow
#November 28, 2025
#Airfoil Selection: Verify Preliminary Data, Extract Refined and Advanced Data
#Utilizes OpenFOAM2512 and WSL Ubuntu 24.04

# ============================== #
# |    PROGRAM DESCRIPTION     | #
# ============================== #
# Iterates airfoil candidates through OpenFOAM, normalizes results,
# prepares results graphs, scores candidates in key behaviors, and
# ends with a composite score ranking based on these behaviors.
#   IF YOU ARE RUNNING THIS FOR YOUR OWN PROJECT:
#       You will need to adjust the configuration below to your needs.
#       You will also need to adjust the baseCase and baseCase_detailed
#       files to suit your OpenFOAM needs; be especially sure to make the test area
#       size compatible with your airfoil size, and all file declarations consistent
#       with your version of OpenFOAM.
#   TODO: After finishing the Tropochief project, I may revisit this file to add
#       OpenFOAM file-generation helpers so you do not have to know OpenFOAM to
#       set your CFD parameters.

import subprocess
import shutil
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date

# ============================== #
# |       CONFIGURATION        | #
# ============================== #
# ===== USER SETTINGS ===== #
username = "Chris Dillow" # Your name here
projectName = "Tropochief RC Plane Project" # Your project's name here
MAC = 0.1968803805 # meters | From design_report.md | Change to fit your needs
U_INF = 30.0 # Should match your magUInf in the forceCoeffs of OpenFOAM
AIRFOILS = [
    "NACA2412",
    "E168"
] # Fill array with your own candidates, ensuring they match their folder names
AOA_LIST = list(range(-4,19)) # Set your range of angle of attack
# Where the repo is mounted inside WSL:
WSL_ROOT_DIR = "/mnt/c/Users/cares/Documents/Engineering/TROPOCHIEF_RC_PLANE/cfd/airfoil_2d"
# ^^ Change this to the WSL-compatible path of your root directory; ensure no whitespaces
SOLVER = "simpleFoam" # Set to your choice of OpenFOAM solve
FOAM_BASHRC_PATH = "/usr/lib/openfoam/openfoam2412/etc/bashrc" # Set to your personal install directory
VERBOSE = True # Set to 'True' to include DEBUG prints, 'False' to omit
meshOnly = False # Set to 'True' to verify meshes, else leave 'False'
DEBUG_WSL = True
RUN_DETAILED_ANALYSIS = True # Set to 'False' if you only want the sweep
RUN_DETAILED_ONLY = True # Set to 'True' to only run the detailed case(s); 'False' for all cases
DETAILED_AOA_LIST = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16] # Key AoAs: Cruise, near-stall, and post-stall
DETAILED_SAMPLE_NAME = "cpLine" # Must match the controlDict functionObject name
DATA_HANDLING_ONLY = False # Set to 'True' if you do not have CFD results, set to 'False' to run CFD and all postprocessing

# ===== CONFIG INITIALIZERS ===== #
sns.set_theme(style='whitegrid',context='talk',palette='deep')
THIS_FILE = Path(__file__).resolve()
ROOT_DIR = THIS_FILE.parent
PLOT_DIR = ROOT_DIR / "postprocessing" / "plots"
BASE_CASE_DIR = ROOT_DIR / "baseCase"
AOA_MARKER_RELATIVE = Path("constant") / "aoa_degrees.txt"
RESULTS_CSV = ROOT_DIR / "airfoil_cfd_results.csv"
DETAILED_BASE_CASE_DIR = ROOT_DIR / "baseCase_detailed"
DETAILED_PLOT_DIR = ROOT_DIR / "postprocessing" / "plots_detailed"
CP_SAMPLE_DIR = ROOT_DIR / "cp_samples"
CP_FILENAME_TEMPLATE = "{airfoil}_alpha{alpha:.1f}_Cp.csv"

# ==== SCORING / ANALYSIS PARAMETERS ==== #
#   If you intend to score on different features, you will need to set up
#   those features' calculations and their weights in the POSTPROCESSING,
#   METRIC EXTRACTION, and SCORING sections of this file.

# --- For Python Screening Verification --- #
TARGET_LIFT_CURVE_SLOPE = 0.10 # Desired dCl/dα per degree
MAX_SLOPE_DEVIATION = 0.05 # Deviation at which score = 0
CRUISE_ALPHA_MIN = 2.0 # Lower bound of the cruise band in degrees
CRUISE_ALPHA_MAX = 8.0 # Upper bound of the cruise band in degrees

# ============================== #
# |         UTILITIES          | #
# ============================== #
def setInletVelocityForAoA(caseDir: Path, alphaDeg: float, UInf: float = U_INF) -> None:
    Upath = caseDir / "0" / "U"
    if not Upath.exists():
        print(f"[WARNING] No 0/U file found in {caseDir}, skipping inlet velocity update.\n")
        return

    alphaRad = np.radians(alphaDeg)
    Ux = UInf * np.cos(alphaRad)
    Uy = UInf * np.sin(alphaRad)
    Uz = 0.0

    text = Upath.read_text(encoding="utf-8")
    lines = text.splitlines()

    outLines = []
    insideInlet = False
    updatedInlet = False

    for line in lines:
        stripped = line.strip()

        if stripped == "inlet":
            insideInlet = True
            outLines.append(line)
            continue

        if insideInlet and stripped.startswith("}"):
            insideInlet = False
            outLines.append(line)
            continue

        if (
            insideInlet
            and ("value" in stripped)
            and ("uniform" in stripped)
            and not updatedInlet
        ):
            indent = line[:len(line) - len(line.lstrip())]
            newLine = f"{indent}value       uniform ({Ux:.6f} {Uy:.6f} {Uz:.6f});"
            outLines.append(newLine)
            updatedInlet = True
            continue

        outLines.append(line)

    newText = f"\n".join(outLines) + f"\n"
    Upath.write_text(newText, encoding="utf-8")

    print(
        f"[SETUP] Updated inlet U for {caseDir} | "
        f"alpha = {alphaDeg}°, U = ({Ux:.3f}, {Uy:.3f}, {Uz:.3f}) m/s\n"
    )

def DATtoSTL(datPath,stlPath,thickness=0.01,chord: float = None) -> None:
    if chord is None:
        chord = MAC

    os.makedirs(os.path.dirname(stlPath),exist_ok=True)

    coords = np.loadtxt(datPath,comments='#',skiprows=1)
    xRaw = coords[:,0]
    yRaw = coords[:,1]

    x = xRaw * chord
    y = yRaw * chord

    z0 = 0.0
    z1 = thickness

    if np.allclose([x[0],y[0]],[x[-1],y[-1]]):
        x = x[:-1]
        y = y[:-1]
    
    with open(stlPath,"w") as file:
        file.write(f"solid airfoil\n")

        def writeTri(a,b,c):
            file.write(f"  facet normal 0 0 0\n")
            file.write(f"    outer loop\n")
            file.write(f"      vertex {a[0]} {a[1]} {a[2]}\n")
            file.write(f"      vertex {b[0]} {b[1]} {b[2]}\n")
            file.write(f"      vertex {c[0]} {c[1]} {c[2]}\n")
            file.write(f"    endloop\n")
            file.write(f"  endfacet\n")

        n = len(x)

        for i in range(n - 1):
            p1 = (x[i],y[i],z0)
            p2 = (x[i+1],y[i+1],z0)
            p3 = (x[i+1],y[i+1],z1)
            p4 = (x[i],y[i],z1)

            writeTri(p1,p2,p3)
            writeTri(p1,p3,p4)
        
        p0_bot = (x[0],y[0],z0)
        for i in range(1,n - 1):
            p1 = (x[i],y[i],z0)
            p2 = (x[i+1],y[i+1],z0)
            writeTri(p0_bot,p1,p2)
        
        p0_top = (x[0],y[0],z1)
        for i in range(1,n - 1):
            p1 = (x[i+1],y[i+1],z1)
            p2 = (x[i],y[i],z1)
            writeTri(p0_top,p1,p2)
        
        file.write(f"endsolid airfoil\n")

def attachAirfoilStlToCase(caseDir: Path,airfoil: str,thickness: float = 0.01) -> None:
    datPath = ROOT_DIR / "geometry" / f"{airfoil.lower()}.dat"
    stlDir = caseDir / "constant" / "triSurface"
    stlDir.mkdir(parents=True,exist_ok=True)
    stlPath = stlDir / "airfoil.stl"

    DATtoSTL(str(datPath),str(stlPath),thickness=thickness,chord=MAC)

# ===== WINDOWS TO LINUX GOVERNANCE ===== #
def windowsCaseToWSL(caseDir: Path) -> str:
    # Converts a case's Windows path to one recognizable by WSL
    relativeDirectory = caseDir.relative_to(ROOT_DIR)
    return f"{WSL_ROOT_DIR}/{relativeDirectory.as_posix()}"

def runWSLcommandInCase(caseDir: Path,command: str) -> None:
    wslCase = windowsCaseToWSL(caseDir)
    foamInit = f'source "{FOAM_BASHRC_PATH}"' # TODO: Remove if bashCommand runs smooth without
    bashCommand = f'source "{FOAM_BASHRC_PATH}" && cd "{wslCase}" && {command}'
    print(f"[RUN (WSL)] {bashCommand}\n")

    result = subprocess.run(
        ["wsl","bash","-lc",bashCommand],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if result.returncode != 0:
        print(f"[ERROR] WSL command failed in case:",caseDir)
        print(f"STDOUT:\n",result.stdout)
        print(f"STDERR:\n",result.stderr)
    else:
        print(f"[PROGRAM] WSL command finished in:",caseDir)

# ============================== #
# |         CASE SETUP         | #
# ============================== #
# ===== INITIAL SCREENING VERIFICATIONS ===== #
def checkBaseCase() -> None:
    requiredPaths = [
        BASE_CASE_DIR / "0" / "U",
        BASE_CASE_DIR / "0" / "p",
        BASE_CASE_DIR / "constant" / "transportProperties",
        BASE_CASE_DIR / "system" / "controlDict",
        BASE_CASE_DIR / "system" / "fvSchemes",
        BASE_CASE_DIR / "system" / "fvSolution",
    ]
    
    missing = [path for path in requiredPaths if not path.exists()]
    if missing:
        print(f"[WARNING] baseCase directory incomplete. Missing:\n")
        for path in missing:
            print(f"  -{path}\n")
        print("[SETUP] Configure baseCase as a valid OpenFOAM case manually "
              f"before running this script.\n")
    else:
        print(f"[SETUP] baseCase has all basic required files. Proceeding.\n")

def ensureCaseDirectory(airfoil: str,alphaDeg: int) -> Path:
    caseDir = ROOT_DIR / airfoil / f"alpha_{alphaDeg}"
    if not caseDir.exists():
        print(f"[SETUP] Creating case: {caseDir}\n")
        shutil.copytree(BASE_CASE_DIR,caseDir)
    else:
        print(f"[SETUP] Case already exists (skipping template copy): {caseDir}\n")
    return caseDir

def writeAOAmarker(caseDir: Path,alphaDeg: int) -> None:
    markerPath = caseDir / AOA_MARKER_RELATIVE
    markerPath.parent.mkdir(parents=True,exist_ok=True)
    markerPath.write_text(f"{alphaDeg}\n",encoding="utf-8")
    print(f"[SETUP] Wrote AoA marker ({alphaDeg} deg) to {markerPath}\n")

def createAllCases() -> List[Path]:
    allCaseDirs = []
    for airfoil in AIRFOILS:
        for alpha in AOA_LIST:
            caseDir = ensureCaseDirectory(airfoil,alpha)
            attachAirfoilStlToCase(caseDir,airfoil)
            writeAOAmarker(caseDir,alpha)
            setInletVelocityForAoA(caseDir,alpha)
            allCaseDirs.append(caseDir)
    return allCaseDirs

# ===== DETAILED CFD ===== #
def checkDetailedBaseCase() -> None:
    requiredPaths = [
        DETAILED_BASE_CASE_DIR / "0" / "U",
        DETAILED_BASE_CASE_DIR / "0" / "p",
        DETAILED_BASE_CASE_DIR / "constant" / "transportProperties",
        DETAILED_BASE_CASE_DIR / "system" / "controlDict",
        DETAILED_BASE_CASE_DIR / "system" / "fvSchemes",
        DETAILED_BASE_CASE_DIR / "system" / "fvSolution",
    ]

    missing = [path for path in requiredPaths if not path.exists()]
    if missing:
        print(f"[WARNING] baseCase_detailed directory incomplete.Missing:\n")
        for path in missing:
            print(f"  -{path}\n")
        print(f"[SETUP] Configure baseCase_detailed as a valid OpenFOAM case manually "
              f"before running the detailed CFD stage.\n")
    else:
        print(f"[SETUP] baseCase_detailed has all required files. Proceeding.\n")

def ensureDetailedCaseDirectory(airfoil: str,alphaDeg: int) -> Path:
    caseRoot = ROOT_DIR / f"{airfoil}_detailed"
    caseDir = caseRoot / f"alpha_{alphaDeg}"
    if not caseDir.exists():
        print(f"[SETUP] Creating detailed case: {caseDir}\n")
        shutil.copytree(DETAILED_BASE_CASE_DIR,caseDir)
    else:
        print(f"[SETUP] Detailed case already exists (skipping template copy): {caseDir}\n")
    return caseDir

def writeDetailedAoAMarker(caseDir: Path,alphaDeg: int) -> None:
    markerPath = caseDir / AOA_MARKER_RELATIVE
    markerPath.parent.mkdir(parents=True,exist_ok=True)
    markerPath.write_text(f"{alphaDeg}\n",encoding="utf-8")
    print(f"[SETUP] Wrote AoA marker (detailed stage, {alphaDeg}°) to {markerPath}.\n")

def createAllDetailedCases() -> None:
    for airfoil in AIRFOILS:
        for alpha in DETAILED_AOA_LIST:
            caseDir = ensureDetailedCaseDirectory(airfoil,alpha)
            attachAirfoilStlToCase(caseDir,airfoil)
            writeDetailedAoAMarker(caseDir,alpha)
            setInletVelocityForAoA(caseDir,alpha)

# ================================= #
# |      OPENFOAM SIMULATION      | #
# ================================= #
# ===== OPENFOAM EXECUTIONS ===== #
# ----- INITIAL SCREENING VERIFICATIONS ----- #
def runOpenFOAMforCase(caseDir: Path,meshOnly: bool = False) -> None:
    if DEBUG_WSL:
        if meshOnly:
            command = "blockMesh && snappyHexMesh -overwrite"
        else:
            command = f"blockMesh && snappyHexMesh -overwrite && {SOLVER}"
    else:
        if meshOnly:
            command = (
                f"blockMesh > log.blockMesh 2>&1 && "
                f"snappyHexMesh -overwrite > log.snappyHexMesh 2>&1"
            )
        else:
            command = (
                f"blockMesh > log.blockMesh 2>&1 && "
                f"snappyHexMesh -overwrite > log.snappyHexMesh 2>&1 && "
                f"{SOLVER} > log.{SOLVER} 2>&1"
            )
    
    runWSLcommandInCase(caseDir,command)

def runAllCases(meshOnly: bool = False) -> None:
    for airfoil in AIRFOILS:
        for alpha in AOA_LIST:
            caseDir = ROOT_DIR / airfoil / f"alpha_{alpha}"
            print(f"[CASE] {airfoil} at alpha = {alpha} deg\n")
            if not caseDir.exists():
                print(f"[WARNING] Case directory missing for {airfoil} at alpha = {alpha} deg.\n")
                if VERBOSE:
                    print(f"[DEBUG] Check that createAllCases() was called.\n")
                print(f"Skipping {airfoil} at {alpha} degrees AoA.\n")
                continue
            runOpenFOAMforCase(caseDir,meshOnly=meshOnly)
# ----- DETAILED CFD ----- #
def exportVTK(caseDir: Path):
    runWSLcommandInCase(caseDir,"foamToVTK > log.foamToVTK 2>&1")

def runAllDetailedCases(meshOnly: bool = False,exportVTKbool: bool = True) -> None:
    for airfoil in AIRFOILS:
        for alpha in DETAILED_AOA_LIST:
            caseDir = ROOT_DIR / f"{airfoil}_detailed" / f"alpha_{alpha}"
            print(f"[DETAILED CASE] {airfoil} at alpha = {alpha}°.\n")

            if not caseDir.exists():
                print(f"[WARNING] Detailed case directory missing for {airfoil} at alpha = {alpha}°.\n")
                if VERBOSE:
                    print(f"[DEBUG] Check that createAllDetailedCases() was called.\n")
                print(f"[PROGRAM] Skipping detailed case for {airfoil} at {alpha}° AoA.\n")
                continue

            runOpenFOAMforCase(caseDir,meshOnly=meshOnly)

            if exportVTKbool and not meshOnly:
                print(f"[VTK] Exporting VTK for {airfoil} at alpha = {alpha}°.\n")
                exportVTK(caseDir)

# ===== POSTPROCESSING ===== #
# --- INITIAL SCREENING VERIFICATIONS --- #
def extractForceCoefficients(caseDir: Path) -> Optional[Dict[str,float]]:
    coefficientFile = caseDir / "postProcessing" / "force_coefficient" / "0" / "coefficient.dat"
    if not coefficientFile.exists():
        print(f"[WARNING] No coefficient.dat in {caseDir}.\n")
        return None
    
    headerTokens: Optional[List[str]] = None
    lastDataLine: Optional[str] = None

    with coefficientFile.open("r",encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if line.startswith('#'):
                tokens = line.lstrip('#').split()
                if "Time" in tokens or "Cl" in tokens or "Cd" in tokens:
                    headerTokens = tokens
            else:
                lastDataLine = line

    if lastDataLine is None:
        print(f"[WARNING] coefficient.dat is empty in {caseDir}.\n")
        return None
    
    parts = lastDataLine.split()

    def getValue(nameCandidates,defaultIdx=None) -> float:
        if headerTokens:
            colMap = {name: idx for idx,name in enumerate(headerTokens)}
            for candidate in nameCandidates:
                if candidate in colMap:
                    idx = colMap[candidate]
                    break
            else:
                prefix = nameCandidates[0][:2]
                idxCandidates = [
                    i for i,token in enumerate(headerTokens)
                    if token.startswith(prefix)
                ]
                if idxCandidates:
                    idx = idxCandidates[0]
                else:
                    idx = defaultIdx
        else:
            idx = defaultIdx

        if idx is None or idx >= len(parts):
            raise ValueError(
                f"Could not locate any of {nameCandidates} or default index {defaultIdx} "
                f"in coefficient.dat columns {headerTokens} for {caseDir}.\n"
            )

        return float(parts[idx])
    
    try:
        timeVal = getValue(['Time'],defaultIdx=0)
        clVal = getValue(['Cl'],defaultIdx=1)
        cdVal = getValue(['Cd'],defaultIdx=2)
        cmVal = getValue(['CmPitch','CmRoll','CmYaw','Cm'],defaultIdx=3)
    except (IndexError,ValueError) as e:
        print(f"[ERROR] Failed to parse coefficient line in {caseDir}: {lastDataLine}.\n")
        print(f"{e}\n")
        return None
    
    return {
        "time": timeVal,
        "Cl": clVal,
        "Cd": cdVal,
        "Cm": cmVal
    }

def collectResults() -> List[Dict[str,Any]]:
    results: List[Dict[str,Any]] = []
    for airfoil in AIRFOILS:
        for alpha in AOA_LIST:
            caseDir = ROOT_DIR / airfoil / f"alpha_{alpha}"
            coefficients = extractForceCoefficients(caseDir)
            if coefficients is None:
                continue
            row: Dict[str,Any] = {
                "airfoil": airfoil,
                "alpha": alpha,
                **coefficients,
            }
            results.append(row)
    return results

def buildResultsDataframe(results: List[Dict[str,Any]]) -> pd.DataFrame:
    if not results:
        print(f"[WARNING] No CFD results to build dataframe from.\n")
        return pd.DataFrame()
    dataframe = pd.DataFrame(results)
    dataframe['ClCd'] = dataframe['Cl'] / dataframe['Cd']
    dataframe.to_csv(RESULTS_CSV,index=False)
    print(f"[POST] Saved combined CFD results to {RESULTS_CSV}.\n")
    return dataframe

# --- DETAILED CFD ---#
CP_CHORD = MAC

def loadLatestCpRaw(caseDir: Path,surfaceName: str = 'airfoil') -> Optional[pd.DataFrame]:
    surfRoot = caseDir / "postprocessing" / "surfaces"
    if not surfRoot.exists():
        if VERBOSE:
            print(f"[ERROR] No 'surfaces' directory in {caseDir}.\n")
        return None
    
    timeDirs = [directory for directory in surfRoot.iterdir() if directory.is_dir()]
    if not timeDirs:
        if VERBOSE:
            print(f"[ERROR] No time directories under {surfRoot}.\n")
        return None
    
    def timeKey(path: Path) -> float:
        try:
            return float(path.name)
        except ValueError:
            return -1.0
        
    latest = sorted(timeDirs,key=timeKey)[-1]
    cpFile = latest / f"{surfaceName}_cp.raw"

    if not cpFile.exists():
        if VERBOSE:
            print(f"[ERROR] Cp file missing: {cpFile}.\n")
        return None
    
    data = np.loadtxt(cpFile)
    if data.ndim == 1:
        data = data.reshape(1,-1)

    dataframe = pd.DataFrame(data,columns=['x','y','z','cp'])
    dataframe['xOverC'] = dataframe['x']  / CP_CHORD
    return dataframe
            

def collectResultsForDetailedStage() -> List[Dict[str,Any]]:
    results: List[Dict[str,Any]] = []
    for airfoil in AIRFOILS:
        for alpha in DETAILED_AOA_LIST:
            caseDir = ROOT_DIR / f"{airfoil}_detailed" / f"alpha_{alpha}"
            coefficients = extractForceCoefficients(caseDir)
            if coefficients is None:
                continue
            row: Dict[str,Any] = {
                "airfoil": airfoil,
                "alpha": alpha,
                **coefficients,
            }
            results.append(row)
    return results

def buildDetailedResultsDataframe(results: List[Dict[str,Any]]) -> pd.DataFrame:
    if not results:
        print(f"[WARNING] No detailed CFD results to build dataframe from.\n")
        return pd.DataFrame()
    dataframe = pd.DataFrame(results)
    dataframe['ClCd'] = dataframe['Cl'] / dataframe['Cd']
    outCSV = ROOT_DIR / "airfoil_csv_results_detailed.csv"
    dataframe.to_csv(outCSV,index=False)
    print(f"[POST] Saved detailed CFD results to {outCSV}.\n")
    return dataframe

# ================================= #
# |       METRIC EXTRACTION       | #
# ================================= #
# ===== INITIAL SCREENING VERIFICATIONS ===== #
def computeStallMetrics(airfoilDataframe: pd.DataFrame) -> Dict[str,float]:
    dataframe = airfoilDataframe.sort_values("alpha").reset_index(drop=True)
    idxMax = dataframe['Cl'].idxmax()
    clMax = dataframe.loc[idxMax,'Cl']
    alphaAtClMax = dataframe.loc[idxMax,'alpha']

    postStall = dataframe[dataframe['alpha'] > alphaAtClMax]
    if postStall.empty:
        clDrop = np.nan
    else:
        clMinPostStall = postStall['Cl'].min()
        clDrop = clMax - clMinPostStall

    return {
        "alphaAtClMax": alphaAtClMax,
        "clMax": clMax,
        "clDropPostStall": clDrop,
    }

def estimateLiftCurveSlope(airfoilDataframe: pd.DataFrame) -> float:
    dataframe = airfoilDataframe.sort_values("alpha")
    mask = (dataframe['alpha'] >= -2.0) & (dataframe['alpha'] <= 8.0)
    sub = dataframe[mask]
    if len(sub) < 3:
        return np.nan
    
    x = sub['alpha'].to_numpy()
    y = sub['Cl'].to_numpy()
    coefficients = np.polyfit(x,y,1)
    slope = coefficients[0]
    return slope

def computeCruiseEfficiencyMetrics(airfoilDataframe: pd.DataFrame) -> Dict[str,float]:
    dataframe = airfoilDataframe.sort_values("alpha")
    dataframe['ClCd'] = dataframe['Cl'] / dataframe['Cd']
    
    cruiseMask = (dataframe['alpha'] >= CRUISE_ALPHA_MIN) & (dataframe['alpha'] <= CRUISE_ALPHA_MAX)
    cruise = dataframe[cruiseMask]
    if cruise.empty:
        maxClCdCruise = np.nan
    else:
        maxClCdCruise = cruise['ClCd'].max()

    minCdOverall = dataframe['Cd'].min()

    return {
        "maxClCdCruise": maxClCdCruise,
        "minCdOverall": minCdOverall,
    }

def computeAirfoilMetrics(dataframe: pd.DataFrame) -> pd.DataFrame:
    metricsRows: List[Dict[str,Any]] = []
    for airfoil,sub in dataframe.groupby("airfoil"):
        stall = computeStallMetrics(sub)
        slope = estimateLiftCurveSlope(sub)
        efficiency = computeCruiseEfficiencyMetrics(sub)

        row = {
            "airfoil": airfoil,
            "alphaAtClMax": stall['alphaAtClMax'],
            "clMax": stall['clMax'],
            "clDropPostStall": stall['clDropPostStall'],
            "liftCurveSlope": slope,
            "maxClCdCruise": efficiency['maxClCdCruise'],
            "minCdOverall": efficiency['minCdOverall'],
            "loadIndex": slope * stall['clMax'],
        }
        metricsRows.append(row)

    metricsDataframe = pd.DataFrame(metricsRows)
    return metricsDataframe

# ===== DETAILED CFD ===== #
def loadCpDistribution(airfoil: str,alphaDeg: float) -> pd.DataFrame:
    filename = CP_SAMPLE_DIR / CP_FILENAME_TEMPLATE.format(airfoil=airfoil,alpha=alphaDeg)
    if not filename.exists():
        if VERBOSE:
            print(f"[DEBUG] Cp file not found for {airfoil} at alpha = {alphaDeg:.1f}°: {filename}.\n")
        return pd.DataFrame()
    
    dataframe = pd.read_csv(filename)
    if 'x' in dataframe.columns and 'xOverC' not in dataframe.columns:
        dataframe = dataframe.rename(columns={'x': 'xOverC'})
    if 'cp' in dataframe.columns and 'Cp' not in dataframe.columns:
        dataframe = dataframe.rename(columns={'cp': 'Cp'})
    
    return dataframe

def collectCpDistributions() -> pd.DataFrame:
    rows = []
    for airfoil in AIRFOILS:
        for alpha in DETAILED_AOA_LIST:
            caseDir = ROOT_DIR / f"{airfoil}_detailed" / f"alpha_{alpha}"
            dataframeCp = loadLatestCpRaw(caseDir)
            if dataframeCp is None or dataframeCp.empty:
                if VERBOSE:
                    print(f"[WARNING] No Cp data for {airfoil} at alpha = {alpha}°.\n")
                continue

            dataframeLocal = dataframeCp.copy()
            dataframeLocal['airfoil'] = airfoil
            dataframeLocal['alpha'] = alpha
            rows.append(dataframeLocal[['airfoil','alpha','xOverC','cp']])

    if not rows:
        return pd.DataFrame(columns=['airfoil','alpha','xOverC','cp'])
    
    return pd.concat(rows,ignore_index=True)

def computeCpMetrics(allResults: pd.DataFrame) -> pd.DataFrame:
    rows = []
    detailedAngles = np.array(DETAILED_AOA_LIST,dtype=float)

    for airfoil,df in allResults.groupby("airfoil"):
        dataframe = df.sort_values("alpha").copy()
        dataframe['ClCd'] = dataframe['Cl'] / dataframe['Cd']

        cruiseMask = (dataframe['alpha'] >= CRUISE_ALPHA_MIN) & (dataframe['alpha'] <= CRUISE_ALPHA_MAX)
        cruise = dataframe[cruiseMask]

        if cruise.empty:
            if VERBOSE:
                print(f"[DEBUG] No cruise data found for {airfoil}. Skipping Cp metrics.\n")
            continue

        idxMax = cruise['ClCd'].idxmax()
        cruiseAlpha = float(cruise.loc[idxMax,'alpha'])

        idxNearest = np.argmin(np.abs(detailedAngles - cruiseAlpha))
        alphaDetail = detailedAngles[idxNearest]

        caseDir = ROOT_DIR / f"{airfoil}_detailed" / f"alpha_{int(alphaDetail)}"
        cpDataframe = loadLatestCpRaw(caseDir)
        if cpDataframe is None or cpDataframe.empty:
            if VERBOSE:
                print(f"[DEBUG] No Cp surfaces data for {airfoil} at detailed alpha = {alphaDetail:.1f}°. Skipping.\n")
            continue

        cpStd = float(cpDataframe['cp'].std())
        cpMin = float(cpDataframe['cp'].min())

        rows.append({
            "airfoil": airfoil,
            "cruiseAlpha": cruiseAlpha,
            "alphaDetail": alphaDetail,
            "cpStdCruise": cpStd,
            "cpMinCruise": cpMin,
        })
    
    cpMetrics = pd.DataFrame(rows)
    if cpMetrics.empty:
        print(f"[WARNING] The Cp Metrics dataframe was returned empty.\n")
        return cpMetrics
    
    stdMin = cpMetrics['cpStdCruise'].min()
    stdMax = cpMetrics['cpStdCruise'].max()
    if stdMax > stdMin:
        cpMetrics['scoreCpUniformity'] = (stdMax - cpMetrics['cpStdCruise']) / (stdMax - stdMin)
    else:
        cpMetrics['scoreCpUniformity'] = 1.0
    
    minMin = cpMetrics['cpMinCruise'].min()
    minMax = cpMetrics['cpMinCruise'].max()
    if minMax > minMin:
        cpMetrics['scoreCpGentleness'] = (cpMetrics['cpMinCruise'] - minMin) / (minMax - minMin)
    else:
        cpMetrics['scoreCpGentleness'] = 1.0
    
    cpMetrics['scoreCp'] = (0.5 * cpMetrics['scoreCpUniformity']) + (0.5 * cpMetrics['scoreCpGentleness'])
    return cpMetrics

# ================================= #
# |            SCORING            | #
# ================================= #
# ===== INITIAL SCREENING VERIFICATIONS ===== #
def normalizeSeries(series: pd.Series,higherIsBetter: bool = True) -> pd.Series:
    seriesFloat = series.astype(float)
    if seriesFloat.isna().all():
        return pd.Series(np.nan,index=seriesFloat.index)

    if higherIsBetter:
        vMin,vMax = seriesFloat.min(),seriesFloat.max()
    else:
        vMin,vMax = seriesFloat.max(),seriesFloat.min() # Invert
    
    if np.isclose(vMax,vMin):
        # Give a neutral 0.5 to avoid a division by zero error
        return pd.Series(0.5,index=seriesFloat.index)

    norm = (seriesFloat - vMin) / (vMax - vMin)
    return norm

def scoreStability(metricsDataframe: pd.DataFrame) -> pd.Series:
    # === SCORE WEIGHTS === #
    #     40% - Higher stall angle
    #     40% - Smaller post-stall Cl drop
    #     20% - Lift-curve slope near target (~0.1 per degree)
    stallAngleScore = normalizeSeries(metricsDataframe['alphaAtClMax'],higherIsBetter=True)
    dropScore = normalizeSeries(metricsDataframe['clDropPostStall'],higherIsBetter=False)
    slope = metricsDataframe['liftCurveSlope'].astype(float)
    slopeDeviation = (slope - TARGET_LIFT_CURVE_SLOPE).abs()
    slopeScoreRaw = 1.0 - (slopeDeviation / MAX_SLOPE_DEVIATION)
    slopeScoreRaw = slopeScoreRaw.clip(lower=0.0,upper=1.0)

    stability = (0.4 * stallAngleScore) + (0.4 * dropScore) + (0.2 * slopeScoreRaw)
    return (stability * 100.0) # As a percentage

def scoreEfficiency(metricsDataframe: pd.DataFrame) -> pd.Series:
    # === SCORE WEIGHTS === #
    #     70% - Higher Cl/Cd in cruise band
    #     30% - Lower overall Cd
    ClCdScore = normalizeSeries(metricsDataframe['maxClCdCruise'],higherIsBetter=True)
    CdScore = normalizeSeries(metricsDataframe['minCdOverall'],higherIsBetter=False)

    efficiency = (0.7 * ClCdScore) + (0.3 * CdScore)
    return (efficiency * 100.0) # As a percentage

def scoreManeuverVsTorsion(metricsDataframe: pd.DataFrame) -> pd.Series:
    # === SCORE WEIGHTS === #
    #     40% - Stronger lift-curve slope
    #     30% - Higher Cl max
    #     30% - Lower Load Index (slope * clMax)
    slopeScore = normalizeSeries(metricsDataframe['liftCurveSlope'],higherIsBetter=True)
    clMaxScore = normalizeSeries(metricsDataframe['clMax'],higherIsBetter=True)
    loadPenaltyScore = normalizeSeries(metricsDataframe['loadIndex'],higherIsBetter=False)

    ManVsTors = (0.4 * slopeScore) + (0.3 * clMaxScore) + (0.3 * loadPenaltyScore)
    return (ManVsTors * 100.0) # As a percentage

def computeCompositeScore(metricsDataframe: pd.DataFrame) -> pd.DataFrame:
    metricsDataframe = metricsDataframe.copy()

    metricsDataframe['scoreStability'] = scoreStability(metricsDataframe)
    metricsDataframe['scoreEfficiency'] = scoreEfficiency(metricsDataframe)
    metricsDataframe['scoreManeuverTorsion'] = scoreManeuverVsTorsion(metricsDataframe)

    metricsDataframe['scoreComposite'] = (
        # === SCORE WEIGHTS === #
        #     40% - Stability
        #     30% - Efficiency
        #     30% - Maneuverability vs. Torsion
        (0.4 * metricsDataframe['scoreStability']) +
        (0.3 * metricsDataframe['scoreEfficiency']) +
        (0.3 * metricsDataframe['scoreManeuverTorsion'])
    )

    metricsDataframe = metricsDataframe.sort_values("scoreComposite",ascending=False).reset_index(drop=True)
    return metricsDataframe

# ===== DETAILED CFD ===== #
def computeDetailedCompositeScore(baseScores: pd.DataFrame,cpMetrics: pd.DataFrame) -> pd.DataFrame:
    detailedDataframe = baseScores.merge(cpMetrics[['airfoil','scoreCp']],on='airfoil',how='left')

    if detailedDataframe['scoreCp'].isna().all():
        detailedDataframe['scoreCp'] = np.nan
        detailedDataframe['scoreCompositeDetailed'] = detailedDataframe['scoreComposite']
        return detailedDataframe.sort_values("scoreCompositeDetailed",ascending=False).reset_index(drop=True)

    meanCp = detailedDataframe['scoreCp'].dropna().mean()
    detailedDataframe['scoreCp'] = detailedDataframe['scoreCp'].fillna(meanCp)

    detailedDataframe['scoreCompositeDetailed'] = (
        0.35 * detailedDataframe['scoreStability'] +
        0.25 * detailedDataframe['scoreEfficiency'] +
        0.25 * detailedDataframe['scoreManeuverTorsion'] +
        0.15 * detailedDataframe['scoreCp']
    )

    detailedDataframe = detailedDataframe.sort_values("scoreCompositeDetailed",ascending=False).reset_index(drop=True)
    return detailedDataframe

def runDetailedStage(resultsDataframe: pd.DataFrame,scoredDataframe: pd.DataFrame) -> pd.DataFrame:
    print(f"[PROGRAM] Starting detailed Cp-based analysis...\n")

    if resultsDataframe.empty:
        print(f"[ERROR] No results in dataframe. Skipping detailed stage.\n")
        detailedDataframe = scoredDataframe.copy()
        detailedDataframe['scoreCp'] = np.nan
        detailedDataframe['scoreCompositeDetailed'] = detailedDataframe['scoreComposite']
        return detailedDataframe
    
    cpMetrics = computeCpMetrics(resultsDataframe)
    if cpMetrics.empty:
        print(f"[ERROR] No Cp files found. Using previous composite scores only.\n")
        detailedDataframe = scoredDataframe.copy()
        detailedDataframe['scoreCp'] = np.nan
        detailedDataframe['scoreCompositeDetailed'] = detailedDataframe['scoreComposite']
        return detailedDataframe
    
    print(f"[RESULTS] Cp Metrics:\n{cpMetrics}\n")

    detailedDataframe = computeDetailedCompositeScore(scoredDataframe,cpMetrics)
    print(f"[PROGRAM] Detailed composite scores:\n",detailedDataframe[['airfoil','scoreCompositeDetailed']],f"\n")

    return detailedDataframe

# ================================= #
# |        RESULT PLOTTING        | #
# ================================= #
# ===== INITIAL SCREENING VERIFICATIONS ===== #
def buildPlot(dataframe: pd.DataFrame,x: str,y: str,xLabel: str,yLabel: str,
                title: str,filename: Path,hue: str='airfoil'):
    fig,ax = plt.subplots(figsize=(8,6))
    
    sns.lineplot(data=dataframe,x=x,y=y,hue=hue,marker='o',ax=ax)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_title(title)

    ax.grid(which='major',linestyle='-',linewidth=0.6,alpha=0.7)
    ax.grid(which='minor',linestyle=':',linewidth=0.4,alpha=0.5)
    ax.minorticks_on()

    handles,labels = ax.get_legend_handles_labels()
    ax.legend(
        handles,
        labels,
        title='Airfoil',
        loc='center left',
        bbox_to_anchor=(1.02,0.5),
        borderaxespad=0.0,
        frameon=True,
    )

    fig.tight_layout()
    fig.savefig(filename,dpi=300,bbox_inches='tight')
    plt.close(fig)

def makeStandardPlots(dataframe: pd.DataFrame,outDir: Path):
    outDir.mkdir(parents=True,exist_ok=True)

    # ===== Cl vs. AoA ===== #
    buildPlot(
        dataframe=dataframe,
        x='alpha',
        y='Cl',
        xLabel='Angle of Attack (°)',
        yLabel='Coefficient of Lift (Cl)',
        title=f'Cl vs. AoA Verification of Airfoil Finalists\n{projectName} | {username} | {date.today()}',
        filename=outDir / 'Cl_vs_AoA.png'
    )

    # ===== Cd vs. AoA ===== #
    buildPlot(
        dataframe=dataframe,
        x='alpha',
        y='Cd',
        xLabel='Angle of Attack (°)',
        yLabel='Coefficient of Drag (Cd)',
        title=f'Cd vs. AoA Verification of Airfoil Finalists\n{projectName} | {username} | {date.today()}',
        filename=outDir / 'Cd_vs_AoA.png'
    )

    # ===== Cl/Cd vs. AoA ===== #
    buildPlot(
        dataframe=dataframe,
        x='alpha',
        y='ClCd',
        xLabel='Angle of Attack (°)',
        yLabel='Lift-to-Drag Ratio (Cl/Cd)',
        title=f'Cl/Cd vs. AoA Verification of Airfoil Finalists\n{projectName} | {username} | {date.today()}',
        filename=outDir / 'ClCd_vs_AoA.png'
    )

    # ===== Cm vs. AoA ===== #
    buildPlot(
        dataframe=dataframe,
        x='alpha',
        y='Cm',
        xLabel='Angle of Attack (°)',
        yLabel='Pitching Moment Coefficient (Cm)',
        title=f'Cm vs. AoA Verification of Airfoil Finalists\n{projectName} | {username} | {date.today()}',
        filename=outDir / 'Cm_vs_AoA.png'
    )

    print(f"[POST] Standard plots exported to {outDir}.\n")

# ===== DETAILED CFD ===== #
def makeCpPlots(cpDataframe: pd.DataFrame,outDir: Path = DETAILED_PLOT_DIR / "cp_distributions") -> None:
    if cpDataframe.empty:
        print(f"[ERROR] No Cp data to plot.\n")
        return
    
    outDir.mkdir(parents=True,exist_ok=True)

    for (airfoil,alpha),group in cpDataframe.groupby(['airfoil','alpha']):
        groupSorted = group.sort_values('xOverC')

        fig,ax = plt.subplots(figsize=(8,6))
        ax.plot(groupSorted['xOverC'],groupSorted['cp'],marker='o')
        ax.set_xlabel('x/c')
        ax.set_ylabel('Cp')
        ax.set_title(f"{airfoil} Cp Distribution | Alpha = {alpha}°\n"
                     f"{projectName} | {username} | {date.today()}")
        ax.grid(which='both',linestyle=':',linewidth=0.5,alpha=0.7)

        fig.tight_layout()
        filename = outDir / f"{airfoil}_alpha_{alpha:+03d}_cp.png"
        fig.savefig(filename,dpi=300,bbox_inches='tight')
        plt.close(fig)

        if VERBOSE:
            print(f"[POST] Saved Cp plot to {filename}.\n")

# ================================= #
# |      MARKDOWN EXPORTING       | #
# ================================= #
def writeMarkdownReport(dataframe: pd.DataFrame,metricsDataframe: pd.DataFrame,
                        scoredDataframe: pd.DataFrame,detailedScores: Optional[pd.DataFrame] = None,
                        cpNotes: Optional[str] = None,outputPath: Path = ROOT_DIR / "airfoil_cfd_selection.md"):
    lines = []

    lines.append("# OpenFOAM 2D CFD Airfoil Screening Results")
    lines.append(f"##### {projectName}\n##### {username}\n ##### {date.today()}")
    lines.append(f"\n*This report summarizes numerical CFD results for the final 2D airfoil candidates.*\n")

    lines.append(f"## Screening Verification Score Table\n")
    lines.append(f"\n*This table verifies preliminary data gathered in the Python/XFoil analysis of the original five candidates.*\n")
    lines.append(scoredDataframe.to_markdown(index=False))
    lines.append(f"\n")

    if cpNotes:
        lines.append(f"##C<sub>p</sub> Distribution Observations\n")
        lines.append(cpNotes)
        lines.append(f"\n")
    
    if detailedScores is not None:
        best = detailedScores.sort_values("scoreCompositeDetailed",ascending=False).iloc[0]
        lines.append(f"## Highest-Ranked Airfoil for 3D Wing CFD Candidacy\n")
        lines.append(f"**Top-Ranked:** `{best['airfoil']}`\n")
    else:
        best = scoredDataframe.sort_values("scoreComposite",ascending=False).iloc[0]
        lines.append(f"### Provisional Winner\n")
        lines.append(f"**Top-Ranked:** `{best['airfoil']}`\n")
    
    outputPath.write_text(f"\n".join(lines),encoding="utf-8")
    print(f"[POST] Markdown report written to {outputPath}.\n")

# ================================= #
# |           EXECUTION           | #
# ================================= #
def main():
    print(f"[INFO] ROOT_DIR = ", ROOT_DIR)
    print(f"[INFO] BASE_CASE_DIR = ", BASE_CASE_DIR)
    print(f"[INFO] WSL_ROOT_DIR = ", WSL_ROOT_DIR)
    print(f"[INFO] AIRFOILS = ", AIRFOILS)
    print(f"[INFO] AOA_LIST = ", AOA_LIST)

    if not DATA_HANDLING_ONLY:

        if not RUN_DETAILED_ONLY:
            # ===== PRELIMINARY VERIFICATIONS AND DETAILED CFD ===== #
            print(f"[PROGRAM] Verifying initial Python screening results...\n")
            print(f"[SETUP] Checking baseCase...\n")
            checkBaseCase()

            print(f"[SETUP] Creating case directories where needed...\n")
            createAllCases()

            print(f"[PROGRAM] Running OpenFOAM on all cases...\n")
            runAllCases(meshOnly)

            print(f"[POST] Collecting results...\n")
            resultsList = collectResults()
            print(f"[POST] Results collected. {len(resultsList)} result rows.\n")

            if not resultsList:
                print(f"[ERROR] No results found.\n")
                if VERBOSE:
                    print(f"[DEBUG] Check forceCoeffs setup.\n")
                return
            
            print(f"[POST] Building dataframe and CSV...\n")
            dataframe = buildResultsDataframe(resultsList)
            if dataframe.empty:
                print(f"[ERROR] Results dataframe is empty. Cannot compute score.\n")
                return
            
            print(f"[POST] Building verification results plots...\n")
            makeStandardPlots(dataframe, PLOT_DIR)
            
            print(f"[POST] Computing per-airfoil metrics...\n")
            metricsDataframe = computeAirfoilMetrics(dataframe)
            print(f"[POST] Metrics:\n{metricsDataframe}\n")

            print(f"[POST] Computing scores...\n")
            scoredDataframe = computeCompositeScore(metricsDataframe)
            print(f"[POST] Scores:\n{scoredDataframe}\n")

            scoresCSV = ROOT_DIR / "airfoil_cfd_scores.csv"
            scoredDataframe.to_csv(scoresCSV, index=False)
            print(f"[POST] Saved scored metrics to {scoresCSV}.\n")

            # ----- DETAILED CFD ----- #
            if RUN_DETAILED_ANALYSIS:
                print(f"[SETUP] Checking baseCase_detailed...\n")
                checkDetailedBaseCase()
                
                print(f"[SETUP] Creating detailed case directories where needed...\n")
                createAllDetailedCases()

                print(f"[PROGRAM] Running detailed OpenFOAM on select cases...\n")
                runAllDetailedCases(meshOnly, exportVTKbool=True)

                print(f"[PROGRAM] Collecting Cp distributions from detailed cases...\n")
                cpDataframe = collectCpDistributions()
                if cpDataframe.empty:
                    print(f"[ERROR] No Cp distributions found from detailed cases.\n")
                else:
                    makeCpPlots(cpDataframe)

                detailedScores = runDetailedStage(dataframe, scoredDataframe)
                reportPath = ROOT_DIR / "airfoil_cfd_report.md"
                try:
                    writeMarkdownReport(
                        dataframe=dataframe,
                        metricsDataframe=metricsDataframe,
                        scoredDataframe=scoredDataframe,
                        detailedScores=detailedScores,
                        outputPath=reportPath
                    )
                    print(f"[POST] Wrote markdown report to {reportPath}.\n")
                except NameError:
                    print(f"[WARNING] Markdown report generation failed. Skipping.\n")

        else:
            # ===== DETAILED ANALYSES ONLY ===== #
            if not RUN_DETAILED_ANALYSIS:
                print(f"[ERROR] Program was set to run only detailed analysis, "
                      f"but RUN_DETAILED_ANALYSIS was set to False.\n")
                return

            print(f"[POST] Collecting results from existing coarse cases...\n")
            resultsList = collectResults()
            print(f"[POST] Results collected. {len(resultsList)} result rows.\n")

            if not resultsList:
                print(f"[ERROR] No results found.\n")
                if VERBOSE:
                    print(f"[DEBUG] Ensure coarse CFD has already been run and "
                          f"postProcessing/force_coefficient exists.\n")
                return

            print(f"[POST] Building dataframe and CSV...\n")
            dataframe = buildResultsDataframe(resultsList)
            if dataframe.empty:
                print(f"[ERROR] Results dataframe is empty. Cannot compute score.\n")
                return

            print(f"[POST] Building verification results plots...\n")
            makeStandardPlots(dataframe, PLOT_DIR)

            print(f"[POST] Computing per-airfoil metrics...\n")
            metricsDataframe = computeAirfoilMetrics(dataframe)
            print(f"[POST] Metrics:\n{metricsDataframe}\n")

            print(f"[POST] Computing scores...\n")
            scoredDataframe = computeCompositeScore(metricsDataframe)
            print(f"[POST] Scores:\n{scoredDataframe}\n")

            scoresCSV = ROOT_DIR / "airfoil_cfd_scores.csv"
            scoredDataframe.to_csv(scoresCSV, index=False)
            print(f"[POST] Saved scored metrics to {scoresCSV}.\n")

            print(f"[SETUP] Checking baseCase_detailed...\n")
            checkDetailedBaseCase()
            
            print(f"[SETUP] Creating detailed case directories where needed...\n")
            createAllDetailedCases()

            print(f"[PROGRAM] Running detailed OpenFOAM on select cases...\n")
            runAllDetailedCases(meshOnly, exportVTKbool=True)

            print(f"[PROGRAM] Collecting Cp distributions from detailed cases...\n")
            cpDataframe = collectCpDistributions()
            if cpDataframe.empty:
                print(f"[ERROR] No Cp distributions found from detailed cases.\n")
            else:
                makeCpPlots(cpDataframe)

            detailedScores = runDetailedStage(dataframe, scoredDataframe)
            reportPath = ROOT_DIR / "airfoil_cfd_report.md"
            try:
                writeMarkdownReport(
                    dataframe=dataframe,
                    metricsDataframe=metricsDataframe,
                    scoredDataframe=scoredDataframe,
                    detailedScores=detailedScores,
                    outputPath=reportPath
                )
                print(f"[POST] Wrote markdown report to {reportPath}.\n")
            except NameError:
                print(f"[WARNING] Markdown report generation failed. Skipping.\n")

    else:
        # ===== DATA PROCESSING ONLY ===== #
        print(f"[PROGRAM] DATA_HANDLING_ONLY = True\n")
        print(f"[PROGRAM] Skipping CFD and CFD preliminaries.\n")
        print(f"[POST] Collecting results from existing cases...\n")

        resultsList = collectResults()
        print(f"[POST] Results collected. {len(resultsList)} result rows.\n")

        if not resultsList:
            print(f"[ERROR] No results found.\n")
            if VERBOSE:
                print(f"[DEBUG] Ensure CFD has already been run and "
                      f"postProcessing/force_coefficient exists.\n")
            return

        print(f"[POST] Building dataframe and CSV...\n")
        dataframe = buildResultsDataframe(resultsList)
        if dataframe.empty:
            print(f"[ERROR] Results dataframe is empty. Cannot compute score.\n")
            return
        
        print(f"[POST] Building verification results plots...\n")
        makeStandardPlots(dataframe, PLOT_DIR)

        print(f"[POST] Computing per-airfoil metrics...\n")
        metricsDataframe = computeAirfoilMetrics(dataframe)
        print(f"[POST] Metrics:\n{metricsDataframe}\n")

        print(f"[POST] Computing scores...\n")
        scoredDataframe = computeCompositeScore(metricsDataframe)
        print(f"[POST] Scores:\n{scoredDataframe}\n")

        scoresCSV = ROOT_DIR / "airfoil_cfd_scores.csv"
        scoredDataframe.to_csv(scoresCSV, index=False)
        print(f"[POST] Saved scored metrics to {scoresCSV}.\n")

        if RUN_DETAILED_ANALYSIS:
            detailedScores = runDetailedStage(dataframe, scoredDataframe)
            reportPath = ROOT_DIR / "airfoil_cfd_report.md"
            try:
                writeMarkdownReport(
                    dataframe=dataframe,
                    metricsDataframe=metricsDataframe,
                    scoredDataframe=scoredDataframe,
                    detailedScores=detailedScores,
                    outputPath=reportPath
                )
                print(f"[POST] Wrote markdown report to {reportPath}.\n")
            except NameError:
                print(f"[WARNING] Markdown report generation failed. Skipping.\n")


if __name__ == "__main__":
    main()