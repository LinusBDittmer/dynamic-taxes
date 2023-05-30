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

Note that this step will take a while. The next step is performed entirely by the internal setup script, therefore you just have to download and execute it. Run the following lines of code and replace `<workspace>` with the directory where you want to put the code and `<conda-env>` with the name of your conda environment (here: dynamic-taxes).

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

- `--config` Opens the configuration file. Dynamic-Taxes might force you to do this if important variables are unset
- `--script <script-file>` The instructions should be read from `<script-file>`. See Script Files in Dynamic-Taxes for more information.
- `--noexec` Build the python (and perhaps qsub file), but do not execute them.
- `--cluster` Execute the script on the cluster as a job with qsub
- `--local` Execute the script locally. If both `--cluster` and `--local` are set, `--cluster` takes priority.
- `--load-dir <file>` Load ESA data from a directory of .out files, which are named `[...]_[number].out` (Regex: `[a-zA-Z0-9]*_[0-9]+\.out`) The trailing number is used as an indication for the timestamp.
- `--load-json <file>` Load ESA data from a .json file.
- `--save-json <output>` Only activate when `--load-dir` is active too. The data loaded from the directory is then saved into `<output>`.
- `--ta <output>` Render the TA spectrum. Make sure that the `--script` flag is not set if using this. The file will be rendered to `<output>`.png
- `--esa <output>` Render all ESA spectra to `<output>_[number].png`
  
## Script Files in Dynamic-Taxes

For more complex instructions, Dynamic-Taxes allows the generation of script files which allow multiple lines of pseudocode to be executed for generation of TA and ESA spectra. The following commands are allowed:

- `set config <key> to <value>`
Sets the value for the config key `<key>` to `<value>`. Note that this is completely constrained to this script's runtime and does not affect the default values. Use `dt --config` for that.
- `load <directory|jsonfile.json>` 
Loads all data from the specified location. If the specified locator ends in `.json`, it is treated as a JSON file, otherwise it is assumed to be a directory.
- `read <directory|jsonfile.json>` 
Alias for `load`
- `save json to <output>`
The data loaded from directories is saved into `<output>.json`
- `render ta to <output>` 
If data has been loaded, the resulting TA spectrum is rendered to `<output>.png`
- `render all esa to <output>` 
If data has been loaded, all ESA spectra are rendered to `<output>_[esatimestamp].png`
- `render every <num>[+<offset>] esa to <output>` 
If data has been loaded, every _num_ ESA spectrum starting with _offset_ (if specified) is rendered to `<output>_[timestamp].png`
- `render esa <num> to <output>`
If data has been loaded, the ESA spectrum with index _num> is rendered to `<output>.png`. _Keep in mind that indexing always starts at 0_
- `render slice at wavelength <wavelength> to <output>` 
If data has been loaded, a slice of the TA spectrum at `<wavelengt>` nm is rendered to `<output>.png`
- `render <avg|averaged> slice at wavelength <wavelength> spanning <halfspan> to <output>`
If data has been loaded, the time-dependent absorption is averaged between `<wavelength> - <halfspan>` and `<wavelength> + <halfspan>` and the standard deviation over said interval is calculated. It is rendered to `<output>.png`
- `# Comment` 
A comment. Inline comments are also allowed.

## Examples

In all subseqent examples, we will assume that our directory has the following structure:

```
├── data
│   ├── traj_0001.out
│   ├── traj_0100.out
│   ├── traj_0200.out
│   ├── ...
│   └── traj_2500.out
├── data_json.json
└── ...
```


### Scripting Examples

The following example is a basic script rendering the TA spectrum with data loaded from a directory.

```
# Loading data from directory ./data
load ./data
# Rendering the TA spectrum
render ta to ta_spectrum.png
```

Note that you can achieve the exact same thing with the shell command:
```
dt --load-dir ./data --ta ta_spectrum.png
```

Scripts shine when you want to achieve something more complicated. Here, it is shown how to load from multiple sources:


```
# Loading data
# Note that loading from multiple sources does not override any data and the ESA spectra 
# are resorted according to their timestamp after loading.
load data_json.json
load ./data

# Rendering the TA spectrum
render ta to ./output/ta_spectrum.png
# Rendering all ESA spectra
# Suppose the timestamp difference is 100, then the filenames will be esa_0.png, 
# esa_100.png, ...
render all esa to ./esa_output/esa
# Render esa spectra of index 1, 6, 11, ...
render every 5+1 esa to ./output/esa_offset
```

The next example shows how to utilise the ESA commands:

```
# Loading data
load ./data

# Rendering all ESA spectra
# Suppose the timestamp difference is 100, then the filenames will be esa_0.png, 
# esa_100.png, ...
render all esa to ./esa_output/esa
# Render esa spectra of index 1, 6, 11, ...
render every 5+1 esa to ./output/esa_offset
# Render first esa spectrum
render esa 0 to first_esa_spectrum.png
```

This examples shows the usage of slices:

```
# Loading data
load ./data

# Rendering a slice at 420 nm
render slice at wavelength 420 to slice_420.png
# Rendering a slice averaged between (420-69) and (420+69) nm.
render avg slice at wavelength 420 spanning 69 to slice_420_avg.png
```

Here is how you can set configs in runtime.

```
# Loading data
load ./data

# Setting the wavelength_range
set config wavelength_range_lower to 100
set config wavelength_range_upper to 1000

# Renderin the TA spectrum
render ta to ta_spectrum.png
```

### Command line Examples

There are a handful of shortcuts that can be directly accessed from the command line. These are

- Creating a TA spectrum from a data directory:
```
dynamic-taxes --load-dir ./data --ta ta_spectrum.png
```
- Creating all ESA spectra from a data directory:
```
dynamic-taxes --load-dir ./data --esa esa_spectra/esa
```
- Creating a TA spectrum from a json file:
```
dynamic-taxes --load-json data_json.json --ta ta_spectrum.png
```
- Creating all ESA spectra from a json file:
```
dynamic-taxes --load-json data_json.json --esa esa_spectra/esa
```

