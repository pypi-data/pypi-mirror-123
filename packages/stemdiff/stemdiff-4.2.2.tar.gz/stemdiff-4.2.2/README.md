# STEMDIFF :: simple processing of 4D-STEM data

* The STEMDIFF package converts... <br>
  ... a 4D-STEM dataset from a SEM microscope (huge and complex) <br>
  ... to a powder-like 1D diffraction pattern (simple and easy to work with).
* The STEMDIFF package is a key part of our 4D-STEM/PNBD method, <br>
  which was described (together with the package) in open-access publications:
	* publication 1: Nanomaterials 11 (2021) 962.
	  [https://doi.org/10.3390/nano11040962](https://doi.org/10.3390/nano11040962)
	* publication 2: Nanomaterials, submitted.
* Gentle introduction to 4D-STEM/PNBD and STEMDIFF
	* Now:
	  See the above-mentioned publication (namely the not-yet-existing #2).
	* Future:
	  Better documentation = next version of the package (coming soon).

# Typical usage of STEMDIFF package

1. STEMDIFF empoyes Spyder IDE as UI (user interface).
	* This may be slightly non-standard, but it is very efficient.
	* Spyder is easy-to-use and easy-to-install (pip install spyder).
	* Spyder shows program run, text and graphical outputs simultaneously.
2. In a typical STEMDIFF session, you do just three things:
	* In Spyder, open STEMDIFF **master script**.
	* In the opened **master script**, modify a few parameters and run it.
	* See program outputs in Spyder and final outputs in active directory
3. Obtaining **master script** & simple testing of STEMDIFF package:
	* open the directory where stemdiff is installed
	* open subdirectory **demo** + unzip the files into testing directory
	* follow the instructions in the unzipped file **00_readme.txt**

# Brief history of STEMDIFF package

* Version 1.0 = Matlab: just simple summation of 4D-dataset
* Version 2.0 = like v1.0 + post-processing in Jupyter
* Version 3.0 = Python scripts: summation + S-filtering
* Version 4.0 = Python package: summation + S-filtering + deconvolution
	- summation = summation of all 2D-diffractograms
	- S-filtering = sum only diffractograms with strong diffractions = high S
	- deconvolution = reduce the effect of primary beam spread
	  &rarr; better resolution 
* Version 4.2 = like v4.0 + a few important improvements, such as:
	- sum just the central region with the strongest diffractions - higher speed
	- 3 centering types: (0) geometry, (1) weight of 1st, (2) individual weights 
	- better definition of summation and centering parameters
	- improved master script/teplate + better documentation strings
