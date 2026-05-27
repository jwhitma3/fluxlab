# FluxLab

**Note: This project is a work in progress. Expect bugs, breaking changes, and incomplete features as development
continues.**

## Overview

`FluxLab` is a Python GUI tool for measuring emission line fluxes and calculating elemental abundances in planetary
nebulae. It is designed to replace an older, CLI-based IDL pipeline, giving users an intuitive, visual way to plot
spectra and analyze lines.

---

## Project Status & Roadmap

### **Completed Features**

* **Interactive Plotting** – Load spectrum data files with smooth panning and zooming to navigate the data.

### **In Progress**

* **Isolated Line Measurement Tool** – A visual interface for setting integration limits directly on the plot allowing
  for:
    * Direct integration of isolated emission lines.
    * Automatic continuum estimation.
    * Calculate systematic uncertainty using upper, mid, and lower continuum baselines.

### **Planned Features**

* **Gaussian Fitting** – Interface for measuring overlapping or blended spectral features.
* **Line Identification** – Enhanced line identification by plotting data from the Atomic Line List (ALL) and NIST
  databases.
* **Abundance Dashboard** – A dedicated interface using PyNeb to calculate physical conditions ($T_e$, $n_e$) and final
  abundances.
* **LaTeX Table Export** – Format results into publication-ready $\LaTeX$ code.
* **Figure Export** – Export publication-quality graphics of lines and fits.

---

## About the Author

`FluxLab` is developed by Joshua C. Whitman, an undergraduate physics student with a concentration in astronomy at the
University of West Georgia (UWG). *This work is an independent project and is not affiliated with, funded, or endorsed
by UWG.*