# dynamic-taxes

This library is a Rendering Software for TA and ESA spectra, whose data is extracted from QChem calculations. 

## Installation
It is recommended that this library be installed by pulling the code to local. If conda is not installed, please refer to the [Miniconda Installation](https://docs.conda.io/en/latest/miniconda.html). Next, create a conda environment (here, the name 'dynamic-taxes' is chosen).

```
conda create -n dynamic-taxes
```

Next, the correct dependencies have to be installed. These are NumPy, SciPy and Matplotlib, as well as conda-build to allow conda to see the code.

```
conda activate dynamic-taxes
conda install conda-build
conda install -c conda-forge numpy scipy matplotlib
```

Note that this step will take a while. The next step is performed entirely by the internal setup script, therefore you just have to download and execute it.

```
wget https://raw.githubusercontent.com/LinusBDittmer/dynamic-taxes/master/dynamictaxes/installer.sh
bash installer.sh <workspace> <conda-env>
rm installer.sh
source ~/.bashrc
```

Check afterwards if there exists a folder `<workspace>/dynamictaxes`. If not, try again.  

## Using Dynamic-Taxes
You can call upon dynamic-taxes by using either of the following commands:

```
dynamic-taxes [...]
dt [...]
dyntax [...]
```
The following arguments are allowed:

- `--script <script-file>` The instructions should be read from <script-file>. See Script Files in Dynamic-Taxes for more information.
- `--noexec` Build the python (and perhaps qsub file), but do not execute them.
- `--cluster` Execute the script on the cluster as a job with qsub
- `--local` Execute the script locally. If both `--cluster` and `--local` are set, `--cluster` takes priority.
- `--load-dir <file>` Load ESA data from a directory of .out files, which are named `[...]_[number].out` (Regex: `[a-zA-Z0-9]*_[0-9]+\.out`) The trailing number is used as an indication for the timestamp.
- `--load-json <file>` Load ESA data from a .json file.
- `--save-json <output>` Only activate when `--load-dir` is active too. The data loaded from the directory is then saved into <output>.
- `--ta <output>` Render the TA spectrum. Make sure that the `--script` flag is not set if using this. The file will be rendered to <output>.png
- `--all-esa <output>` Render all ESA spectra to the output
  
## Script Files in Dynamic-Taxes
