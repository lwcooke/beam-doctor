# beam-doctor
Some simple Python functions for computing telescope configurations that could be used to correct a laser beam's spatial-profile, or generate a desired profile.

In many situations in the lab we find ourselves needing a Gaussian beam of a given set of qualities, and must compute how we can get them by selecting a telescope to work with. The original purpose of this code was to compute the ideal set of lenses, and the distance between them, for correcting the beam output of lasers. The output beams are typically elliptical (especially if amplified by a tapered-amplifier), so it computes lenses for the $x$ and $y$ dimensions seperately, assuming one can use cylindrical lenses to independently correct both. We have also used it to select a telescope from limited lens stock to give us a beam which fits within a set of user-defined constraints; this has saved us a lot of time.

# Required Packages
To use these functions you will require several packages:

* NumPy: an obvious inclusion. Using conda-forge it can be downloaded from [here](https://anaconda.org/conda-forge/numpy).
* SciPy: all we use is stats.linregress, for linear fitting to some input beam-size data to get the divergence from this. Using conda-forge it can be downloaded from [here](https://anaconda.org/conda-forge/scipy).
* prettytable: a nice package for well formated tables in console, which we use to display the resulting telescopes and beam profiles. Using conda-forge it can be downloaded from [here](https://anaconda.org/conda-forge/prettytable).

An easy way to set up an anaconda environment for this would be to paste this into your console: `conda create -n beam-doctor python numpy scipy prettytable`. Don't forget to also install your favorite editor afterwards.

# Function Descriptions
Here we describe the various functions in the `BeamDoctorFunctions.py` module, for easy reading. The functions themselves have reasonably complete documentation as well to understand the specifics.

* `beamprofiler()`: Takes in a set of beam-size measurements at different relative distances, and fits them with a line to extract the divergence half-angle.
* `telescope()`: For a given set of focal lengths, separation distance, and input beam profile ($1$D) this function computes the output beam profile.
* `lensconfigs()`: Computes a list of all possible lens configurations to try, from the input choices of focal lengths. It has a parameter to also try separation distances on either side of the typical $d = f_1 + f_2$, in case the input beam is not collimated.
* `tryall()`: From the initial beam profile this function will call `telescope()` to compute the output profiles for all lens configuration in an input list (typically from `lensconfigs()`).
* `filterall()`: Sorts through a list of given beam profiles and lens configurations to remove any which exceed an input set of tolerances. This function thus allows us to specify the maximum/minimum beam size and divergence we want, and removes all of the attempted configurations which exceed these specifications.
* `beamdoctor()`: From the input beam sizes, this function just calls all the previous functions as they were written to return a well-formatted table of final choices of telescopes that meet specifications.

# Example
To view a detailed example, run the `TelescopeCalculatorExample.ipynb` file, which walks through a calculation (which we used in our research) complete with descriptions.

