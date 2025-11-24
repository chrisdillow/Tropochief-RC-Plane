#Tropochief RC Plane Project
#Chris Dillow
#November 23, 2025
#Airfoil Selection: Preliminary Data Obtainment
#Utilizes XFoil 6.99 for Windows

import subprocess
import pathlib
from pathlib import Path
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import date

# ============================== #
#|         CONFIGURATION        |#
# ============================== #
sns.set_theme(style='whitegrid',context='talk',palette='deep')

username = "Chris Dillow" # Set this to your name for it to be applied to data outputs
# For other users running this script for your own projects, change the AIRFOILS array items
# and other configuration inputs to match your project's needs before running.

AIRFOILS = [
    "naca23012",
    "naca2412",
    "rg15",
    "mh32",
    "e168"
]

AOA_START = -5.0
AOA_END = 18.0
AOA_STEP = 0.5

AOA_RANGE = [round(a,1) for a in np.arange(-5.0,18.0 + 0.5,0.5)] # From -5° to +18° using 0.5° increments
fluidDensity = 1.225 # kg/m^3 | rho, at sealevel standard
dynamicViscocity = 1.8e-5 # kg/(m*s) | mu
characteristicLength = 0.1969 # m | c, Mean Aerodynamic Chord, pulled from design_report.md
fluidVelocity = 30.0 # m/s | V, based on initial design cruise speed estimate

def computeReynolds(fluidDensity,fluidVelocity,characteristicLength,dynamicViscocity):
    return (fluidDensity * fluidVelocity * characteristicLength) / dynamicViscocity

RE = computeReynolds(fluidDensity,fluidVelocity,characteristicLength,dynamicViscocity)
print(f"[PROGRAM] Using Reynolds Number (Re) ≈ {RE:.0f} based on:\n",
      f"Fluid Velocity (V) = {fluidVelocity} m/s\n",
      f"Characteristic Length (c) = {characteristicLength} m.\n")

geometryDirectory = pathlib.Path("geometry")
rawDirectory = pathlib.Path("data_raw")
processedDirectory = pathlib.Path("data_processed")
figureDirectory = pathlib.Path("figures")
xfoilExecutable = pathlib.Path("xfoil/xfoil.exe")

for directory in [geometryDirectory,rawDirectory,processedDirectory,figureDirectory]:
    directory.mkdir(parents=True,exist_ok=True)

if not xfoilExecutable.exists():
    print(f"[ERROR] XFoil not found at {xfoilExecutable}.\n")
    print("Please download the appropriate build for your device and place it in /analysis/airfoil_screening/xfoil/")
else:
    print(f"[PROGRAM] XFoil found at {xfoilExecutable}.\n")

VERBOSE = False # Set to 'True' for detailed XFoil logs and debug prints
DIAGNOSTIC_LINEAR_PLOTS = True # Set to 'False' if you do not want linear region plots

def normalizeSeries(metricSeries: pd.Series) -> pd.Series:
    cleanedSeries = metricSeries.replace([np.inf,-np.inf],np.nan)
    validValues = cleanedSeries.dropna()
    if validValues.empty:
        return pd.Series(0.5,index=metricSeries.index,dtype=float)
    
    minValue = validValues.min()
    maxValue = validValues.max()

    if maxValue == minValue:
        return pd.Series(0.5,index=metricSeries.index,dtype=float)
    
    normalizedValues = (cleanedSeries - minValue) / (maxValue - minValue)
    return normalizedValues.reindex(metricSeries.index)

# ============================== #
#|        XFOIL EXECUTION       |#
# ============================== #
def buildXfoilCommand(airfoilName: str,re: float,aoaRange) -> str:
    airfoilDAT = geometryDirectory / f"{airfoilName}.dat"
    polarFile = rawDirectory / f"{airfoilName}_Re{int(re)}.pol"

    cmdLines = [
        f"LOAD {airfoilDAT}",
        "", # Use a blank line in case XFoil sends a prompt
        "PANE",
        "",
        "PLOP",
        "G",
        "",
        "OPER",
        f"VISC {int(re)}",
        "MACH 0.0",
        "ITER 200", # OPTIONAL: Increase or decrease iterations for refined data
        "PACC",
        f"{polarFile}",
        "", # No dump file
    ]

    # ===== AoA Sweep ===== #
    aoaList = list(aoaRange)
    aStart = aoaList[0]
    aEnd = aoaList[-1]
    aStep = aoaList[1] - aoaList[0] if len(aoaList) > 1 else 1.0

    cmdLines.append(f"ASEQ {aStart} {aEnd} {aStep}")
    cmdLines.append("QUIT")
    cmdLines.append("")

    return "\n".join(cmdLines)

def runXfoil(airfoilName,re,aoaRange):
    if not xfoilExecutable.exists():
        raise FileNotFoundError(
            f"XFoil executable not found at {xfoilExecutable}.\n"
            f"Place xfoil.exe in the xfoil directory and rerun.\n"
        )

    script = buildXfoilCommand(airfoilName,re,aoaRange)
    print(f"[PROGRAM] Running XFoil for {airfoilName} at Re={re:.0f}...\n")
    if VERBOSE:
        print(f"[DEBUG] XFoil command script for {airfoilName}:\n{script}\n")
    
    result = subprocess.run(
        [str(xfoilExecutable)],
        input=script.replace("\n","\r\n"),
        text=True,
        capture_output=True
    )

    polarFile = rawDirectory / f"{airfoilName}_Re{int(re)}.pol"
    polarExists = polarFile.exists()

    if not polarExists:
        print(f"[ERROR] XFoil did not produce a polar file for {airfoilName}.\n")
        print(f"         Expected: {polarFile}\n")
        if VERBOSE:
            print(f"[DEBUG] XFoil STDOUT:\n",result.stdout)
            print(f"[DEBUG] XFoil STDERR:\n",result.stderr)
        return
    
    if result.returncode != 0:
        print(
            f"[WARNING] XFoil returned nonzero exit code ({result.returncode}) "
            f"for {airfoilName}, but a polar file was created. Proceeding.\n"
        )
        if VERBOSE:
            print(f"[DEBUG] XFoil STDOUT (truncated):\n")
            print(f"\n".join(result.stdout.splitlines()[:80]))
            print(f"\n[DEBUG] XFoil STDERR:",result.stderr)
    else:
        if VERBOSE:
            print(f"[DEBUG] XFoil completed cleanly for {airfoilName}.\n")
    
    print(f"[PROGRAM] XFoil process complete for {airfoilName}.\n")

for candidate in AIRFOILS:
    runXfoil(candidate,RE,AOA_RANGE)

# ============================== #
#|   LOAD DATAFRAMES AND MERGE  |#
# ============================== #
def parsePolar(airfoilName):
    polarFile = rawDirectory / f"{airfoilName}_Re{int(RE)}.pol"
    if not polarFile.exists():
        raise FileNotFoundError(f"Polar file not found: {polarFile}\n")
    
    rows = []
    with polarFile.open() as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#") or line.startswith("-----"):
                continue
            parts = line.split()
            if len(parts) != 7:
                continue
            try:
                alpha = float(parts[0])
                cl = float(parts[1])
                cd = float(parts[2])
                cdp = float(parts[3]) # Pressure Drag Coefficient
                cm = float(parts[4])
                topXtr = float(parts[5])
                botXtr = float(parts[6])
                rows.append({
                    "alpha": alpha,
                    "cl": cl,
                    "cd": cd,
                    "cdp": cdp,
                    "cm": cm,
                    "top_xtr": topXtr,
                    "bot_xtr": botXtr,
                })
            except ValueError:
                continue
    dataframe = pd.DataFrame(rows)
    outCSV = processedDirectory / f"{airfoilName}_polar.csv"
    dataframe.to_csv(outCSV,index=False)
    print(f"[PROGRAM] Saved processed polar CSV for {airfoilName} to {outCSV}.\n")
    return dataframe

dataframes = []
for candidate in AIRFOILS:
    dataframe = parsePolar(candidate)
    dataframe['airfoil'] = candidate.upper()
    dataframes.append(dataframe)

allPolars = pd.concat(dataframes,ignore_index=True)
allPolars['cl_cd'] = allPolars['cl'] / allPolars['cd']
print(f"[PROGRAM] Combined polar dataframe shape:",allPolars.shape)

# ============================== #
#|         STALL METRICS        |#
# ============================== #
def computeStallMetrics(dataframeAirfoil: pd.DataFrame):
    dataframe = dataframeAirfoil.sort_values("alpha").reset_index(drop=True)
    dataframe = dataframe.dropna(subset=['cl'])

    if dataframe.empty:
        return np.nan,np.nan,np.nan
    
    idxMax = dataframe['cl'].idxmax()
    alphaAtClMax = dataframe.loc[idxMax,'alpha']
    clMax = dataframe.loc[idxMax,'cl']

    postStall = dataframe[dataframe['alpha'] > alphaAtClMax]
    clDrop = np.nan
    if not postStall.empty:
        clMinPost = postStall['cl'].min()
        clDrop = clMax - clMinPost
    
    return alphaAtClMax,clMax,clDrop

stallRows = []
for candidate in AIRFOILS:
    dataframeAirfoil = allPolars[allPolars['airfoil'] == candidate.upper()]
    aMax,clMax,clDrop = computeStallMetrics(dataframeAirfoil)
    stallRows.append({
        "airfoil": candidate.upper(),
        "alphaAtClMax": aMax,
        "clMax": clMax,
        "ClDropPostStall": clDrop,
    })

stallDataframe = pd.DataFrame(stallRows).set_index("airfoil")
print(f"[PROGRAM] Stall characteristics summary:\n")
print(stallDataframe.round(4))

# ============================== #
#|        SLOPE BEHAVIOR        |#
# ============================== #
def estimateLiftCurveLinearRegion(dataframeAirfoil: pd.DataFrame):
    if dataframeAirfoil.empty:
        return float("nan"),float("nan"),float("nan"),float("nan")
    dataframe = dataframeAirfoil.sort_values("alpha").reset_index(drop=True).copy()
    dataframe = dataframe[
        (dataframe['cd'] > 0.0) &
        (dataframe['cd'] < 5.0) &
        (dataframe['cl'].abs() < 3.5)
    ].copy()

    if dataframe.empty:
        return float("nan"),float("nan"),float("nan"),float("nan")

    aMax,clMax,_ = computeStallMetrics(dataframe)
    if np.isnan(aMax):
        aLimit = 8.0
    else:
        aLimit = aMax - 2.0 # "- 2.0" ensures we stay comfortably below stall
    
    candidates = dataframe[
        (dataframe['alpha'] >= -4.0) &
        (dataframe['alpha'] <= aLimit)
    ].copy()

    if len(candidates) < 3:
        return float("nan"),float("nan"),float("nan"),float("nan")
    
    coefficients = np.polyfit(candidates['alpha'],candidates['cl'],1)
    slope,intercept = coefficients[0],coefficients[1]

    clFit = np.polyval(coefficients,candidates['alpha'])
    residuals = candidates['cl'] - clFit

    maskLinear = residuals.abs() <= 0.8 # A thresold of 0.8 Cl units is reasonable
    linear = candidates[maskLinear].copy()

    if len(linear) < 3:
        linear = candidates.copy()
    
    coefficientsFinal = np.polyfit(linear['alpha'],linear['cl'],1)
    slopeFinal,interceptFinal = coefficientsFinal[0],coefficientsFinal[1]
    clFitFinal = np.polyval(coefficientsFinal,linear['alpha'])

    # --- Calculate R^2 --- #
    ssResiduals = np.sum((linear['cl'] - clFitFinal) **2)
    ssTotal = np.sum((linear['cl'] - linear['cl'].mean()) **2)
    r2 = float("nan") if ssTotal == 0 else 1.0 - (ssResiduals / ssTotal)

    alphaLinMin = linear['alpha'].min()
    alphaLinMax = linear['alpha'].max()

    return slopeFinal,alphaLinMin,alphaLinMax,r2

def plotLinearRegionDiagnostic(airfoilName: str,dataframeAirfoil: pd.DataFrame,
                               slope: float,intercept: float,alphaLinMin: float,
                               alphaLinMax: float,alphaStall: float):
    diagnosticDirectory = figureDirectory / "linear_region"
    diagnosticDirectory.mkdir(parents=True,exist_ok=True)
    
    fig,ax = plt.subplots(figsize=(7,5))

    sns.lineplot(
        data=dataframeAirfoil,
        x="alpha",
        y="cl",
        marker="o",
        ax=ax,
        label="Raw Cl Data"
    )

    alphaValues = np.linspace(dataframeAirfoil['alpha'].min(),dataframeAirfoil['alpha'].max(),200)
    clFit = slope * alphaValues + intercept
    ax.plot(alphaValues,clFit,linestyle='--',label=f"Linear Fit (slope={slope:.3f})")

    ax.axvspan(alphaLinMin,alphaLinMax,color='yellow',alpha=0.2,label="Linear Region")
    if not np.isnan(alphaStall):
        ax.axvline(alphaStall,color='red',linestyle=':',label=f"Stall at {alphaStall:.1f}°")
    
    ax.set_title(f"Linear Lift Region Diagnostic - {airfoilName}")
    ax.set_xlabel("Angle of Attack (°)")
    ax.set_ylabel("Lift Coefficient (Cl)")

    ax.grid(which='major',linestyle='-',linewidth=0.6,alpha=0.7)
    ax.grid(which='minor',linestyle=':',linewidth=0.4,alpha=0.4)
    ax.minorticks_on()

    ax.legend(loc='best')

    fig.tight_layout()
    fig.savefig(diagnosticDirectory / f"{airfoilName}_linear_region.png",dpi=300)
    plt.close(fig)

slopeRows = []
for candidate in AIRFOILS:
    dataframeAirfoil = allPolars[allPolars['airfoil'] == candidate.upper()]
    slope,alphaLinMin,alphaLinMax,r2 = estimateLiftCurveLinearRegion(dataframeAirfoil)

    slopeRows.append({
        "airfoil": candidate.upper(),
        "liftCurveSlope": slope,
        "alphaLinearMin": alphaLinMin,
        "alphaLinearMax": alphaLinMax,
        "linearFitR2": r2,
    })

    if DIAGNOSTIC_LINEAR_PLOTS and not np.isnan(slope):
        intercept = np.mean(dataframeAirfoil['cl'] - slope * dataframeAirfoil['alpha'])
        plotLinearRegionDiagnostic(
            candidate.upper(),
            dataframeAirfoil,
            slope,
            intercept,
            alphaLinMin,
            alphaLinMax,
            aMax,
        )

slopeDataframe = pd.DataFrame(slopeRows).set_index("airfoil")
print(f"[PROGRAM] Approximate lift-curve slopes and linear regions (per degree):\n")
print(slopeDataframe.round({
    "liftCurveSlope": 4,
    "alphaLinearMin": 1,
    "alphaLinearMax": 1,
    "linearFitR2": 3,
}))

# ============================== #
#|  MAKE GENERAL SUMMARY TABLE  |#
# ============================== #
summaryRows = []
for candidate in AIRFOILS:
    dataframe = allPolars[allPolars['airfoil'] == candidate.upper()].copy()
    if dataframe.empty:
        continue
    
    # --- Set Example Metrics --- #
    maxCl = dataframe['cl'].max()
    minCd = dataframe['cd'].min()
    maxClCd = dataframe['cl_cd'].max()

    # --- Approximate the Cruise Band Filter (e.g., -2° to +6°) --- #
    cruiseDataframe = dataframe[(dataframe['alpha'] >= -2) & (dataframe['alpha'] <= 6)]
    cruiseClCd = cruiseDataframe['cl_cd'].max() if not cruiseDataframe.empty else float("nan")

    summaryRows.append({
        "airfoil": candidate.upper(),
        "maxCl": maxCl,
        "minCd": minCd,
        "maxClCd": maxClCd,
        "maxClCd_cruiseBand": cruiseClCd,
    })

summaryDataframe = pd.DataFrame(summaryRows)
summaryDataframe = summaryDataframe.set_index("airfoil")
print(f"\n[PROGRAM] Airfoil performance summary:\n")
print(summaryDataframe.round(4))

# ============================== #
#|    MULTI-OBJECTIVE RANKINGS  |#
# ============================== #
combinedMetrics = (
    summaryDataframe.join(stallDataframe,how='left').join(slopeDataframe,how='left')
)

combinedMetrics['loadMetric'] = combinedMetrics['liftCurveSlope'] * combinedMetrics['maxCl']

combinedMetrics['N_alphaStall'] = normalizeSeries(combinedMetrics['alphaAtClMax'])
combinedMetrics['N_ClDrop'] = normalizeSeries(combinedMetrics['ClDropPostStall'])
combinedMetrics['N_maxCl'] = normalizeSeries(combinedMetrics['maxCl'])
combinedMetrics['N_minCd'] = normalizeSeries(combinedMetrics['minCd'])
combinedMetrics['N_maxClCdCruise'] = normalizeSeries(combinedMetrics['maxClCd_cruiseBand'])
combinedMetrics['N_slope'] = normalizeSeries(combinedMetrics['liftCurveSlope'])
combinedMetrics['N_loadMetric'] = normalizeSeries(combinedMetrics['loadMetric'])

slopeTarget = 0.10
combinedMetrics['slopeDeviation'] = (combinedMetrics['liftCurveSlope'] - slopeTarget).abs()
combinedMetrics['N_slopeDeviation'] = normalizeSeries(combinedMetrics['slopeDeviation'])

# ===== PROJECT-SPECIFIC NOTES ===== #
# For a forward swept wing configuration and prioritizing stability, we want:
# --- STABILITY --- #
#   - a higher stall angle, allowing more margin before stall
#   - a smaller post-stall Cl drop, providing gentler stalls when they occur
#   - a slope near slopeTarget, not too flat nor too aggressive
# --- EFFICIENCY --- #
#   - a high Cl/Cd in the cruise band
#   - low minimum Cd overall
# --- MANUEUVERABILITY AND TORSION --- #
#   - a strong slope for high control authority
#   - a high max Cl for lift capacity
#   - but penalize very high slope * maxCl loads


# ===== SCORE STABILITY ===== #
combinedMetrics['scoreStability'] = (
    0.4 * combinedMetrics['N_alphaStall'] +
    0.4 * (1.0 - combinedMetrics['N_ClDrop']) +
    0.2 * (1.0 - combinedMetrics['N_slopeDeviation'])
)
rankingStability = (
    combinedMetrics[['scoreStability']].sort_values("scoreStability",ascending=False)
)

# ===== SCORE EFFICIENCY ===== #
combinedMetrics['scoreEfficiency'] = (
    0.7 * combinedMetrics['N_maxClCdCruise'] +
    0.3 * (1.0 - combinedMetrics['N_minCd'])
)
rankingEfficiency = (
    combinedMetrics[['scoreEfficiency']].sort_values("scoreEfficiency",ascending=False)
)

# ===== SCORE MANEUVERABILITY VS. WING TORSION ===== #
combinedMetrics['scoreManeuverTorsion'] = (
    0.4 * combinedMetrics['N_slope'] +
    0.3 * combinedMetrics['N_maxCl'] +
    0.3 * (1.0 - combinedMetrics['N_loadMetric'])
)
rankingManeuverTorsion = (
    combinedMetrics[['scoreManeuverTorsion']].sort_values(by="scoreManeuverTorsion",ascending=False)
)

# ===== PRINT RANKINGS ===== #
print(f"[PROGRAM] RANKING - Forward-Swept / Stability-Oriented (Score A):\n")
print(rankingStability.round(3))

print(f"\n[PROGRAM] RANKING - Efficiency (Score B):\n")
print(rankingEfficiency.round(3))

print(f"\n[PROGRAM] RANKING - Maneuverability vs. Torsion (Score C):\n")
print(rankingManeuverTorsion.round(3))

topStability = ", ".join(rankingStability.index[:2]) if not rankingStability.empty else ""
topEfficiency = ", ".join(rankingEfficiency.index[:2]) if not rankingEfficiency.empty else ""
topManeuver = ", ".join(rankingManeuverTorsion.index[:2]) if not rankingManeuverTorsion.empty else ""

# ============================== #
#|        RESULT PLOTTING       |#
# ============================== #
def buildPlot(data: pd.DataFrame,x: str,y: str,xLabel: str,yLabel: str,
              title: str,filename: Path,hue: str='airfoil'):
    fig,ax = plt.subplots(figsize=(8,6))
    
    sns.lineplot(data=data,x=x,y=y,hue=hue,marker='o',ax=ax)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    ax.set_title(title)

    ax.grid(which='major',linestyle='-',linewidth=0.6,alpha=0.7)
    ax.grid(which='minor',linestyle=':',linewidth=0.4,alpha=0.4)
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

# ======== Cl vs. AoA ========= #
buildPlot(data=allPolars,x='alpha',y='cl',xLabel='Angle of Attack (°)',yLabel='Lift Coefficient (Cl)',
          title=f"Cl vs. AoA of Candidate Airfoils\nTropochief RC Plane Project | {username} | {date.today()}",
          filename=figureDirectory / "cl_vs_aoa.png")

# ======== Cd vs. AoA ========= #
buildPlot(data=allPolars,x='alpha',y='cd',xLabel='Angle of Attack (°)',yLabel='Drag Coefficient (Cd)',
          title=f"Cd vs. AoA of Candidate Airfoils\nTropochief RC Plane Project | {username} | {date.today()}",
          filename=figureDirectory / "cd_vs_aoa.png")

# ======= Cl/Cd vs. AoA ======= #
buildPlot(data=allPolars,x='alpha',y='cl_cd',xLabel='Angle of Attack (°)',yLabel='Lift-to-Drag Ratio (Cl/Cd)',
          title=f"Cl/Cd vs. AoA of Candidate Airfoils\nTropochief RC Plane Project | {username} | {date.today()}",
          filename=figureDirectory / "clcd_vs_aoa.png")

# ======== Cm vs. AoA ========= #
buildPlot(data=allPolars,x='alpha',y='cm',xLabel='Angle of Attack (°)',yLabel='Pitching Moment Coefficient (Cm)',
          title=f"Cm vs. AoA of Candidate Airfoils\nTropochief RC Plane Project | {username} | {date.today()}",
          filename=figureDirectory / "cm_vs_aoa.png")

# ============================== #
#|       AUTO-PUSH TO .MD       |#
# ============================== #
selectionMD = pathlib.Path("airfoil_selection.md")

mdLines = [
    f"# Airfoil Selection Study\n",
    f"This document is auto-updated by `airfoil_screening.py`.\n",
    f"Figures are generated in `analysis/airfoil_screening/figures/`.\n",
    f"\n## 1. Cl vs AoA\n",
    f"![Cl vs AoA](figures/cl_vs_aoa.png)\n",
    f"\n## 2. Cd vs AoA\n",
    f"![Cd vs AoA](figures/cd_vs_aoa.png)\n",
    f"\n## 3. Cl/Cd vs AoA\n",
    f"![Cl/Cd vs AoA](figures/clcd_vs_aoa.png)\n",
    f"\n## 4. Cm vs AoA\n",
    f"![Cm vs AoA](figures/cm_vs_aoa.png)\n",
    f"\n## 5. Numerical Summary\n",
    f"\n```text\n",
    summaryDataframe.round(4).to_string(),
    f"\n```\n",
    f"\n## 6. Lift-Curve Slopes\n",
    f"\n```text\n",
    slopeDataframe.round(4).to_string(),
    f"\n```\n",
     "\n## 7. Multi-Objective Rankings\n",
    "\nTop candidates by objective:\n",
    f"\n- Forward-swept / stability-oriented (Score A): {topStability or 'N/A'}\n",
    f"- Efficiency, cruise-focused (Score B): {topEfficiency or 'N/A'}\n",
    f"- Maneuverability vs torsion (Score C): {topManeuver or 'N/A'}\n",
    "\n### 7.1 Score A – Forward-Swept / Stability-Oriented\n",
    "\n```text\n",
    rankingStability.round(3).to_string(),
    "\n```\n",
    "\n### 7.2 Score B – Efficiency\n",
    "\n```text\n",
    rankingEfficiency.round(3).to_string(),
    "\n```\n",
    "\n### 7.3 Score C – Maneuverability vs Torsion\n",
    "\n```text\n",
    rankingManeuverTorsion.round(3).to_string(),
    "\n```\n",
]

selectionMD.write_text("".join(mdLines), encoding="utf-8")
print(f"[PROGRAM] Updated airfoil_selection.md at {selectionMD.resolve()}")