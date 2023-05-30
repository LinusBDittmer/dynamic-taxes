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

| Flag | Description |
| ... | ... |
| `--config` | Opens the configuration file. Dynamic-Taxes might force you to do this if important variables are unset. |
| `--script <script-file>` | The instructions should be read from `<script-file>`. See 'Script Files in Dynamic-Taxes' for more information. |
| `--noexec` | Build the python (and perhaps qsub file), but do not execute them. |
| `--cluster` | Execute the script on the cluster as a job with qsub. |
| `--local` | Execute the script locally. If both `--cluster` and `--local` are set, `--cluster` takes priority. |
| `--load-dir <file>` | Load ESA data from a directory of .out files, which are named `[...]_[number].out` (Regex: `[a-zA-Z0-9]*_[0-9]+\.out`) The trailing number is used as an indication for the timestamp. |
| `--load-json <file>` | Load ESA data from a .json file. |
| `--save-json <output>` | Only activate when `--load-dir` is active too. The data loaded from the directory is then saved into `<output>`. |
| `--ta <output>` | Render the TA spectrum. Make sure that the `--script` flag is not set if using this. The file will be rendered to `<output>.png`. |
| `--esa <output>` | Render all ESA spectra to `<output>_[number].png` |


## Script Files in Dynamic-Taxes

For more complex instructions, Dynamic-Taxes allows the generation of script files which allow multiple lines of pseudocode to be executed for generation of TA and ESA spectra. The following commands are allowed:

| Command | Description |
| ... | ... |
| `set config <key> to <value>` | Sets the value for the config key `<key>` to `<value>`. Note that this is completely constrained to this script's runtime and does not affect the default values. Use `dt --config` for that. |
| `load <directory|jsonfile.json>` | Loads all data from the specified location. If the specified locator ends in `.json`, it is treated as a JSON file, otherwise it is assumed to be a directory. |
| `read <directory|jsonfile.json>` | Alias for `load`. |
| `save json to <output>` | The data loaded from directories is saved into `<output>.json`. |
| `render ta to <output>` | If data has been loaded, the resulting TA spectrum is rendered to `<output>.png`. |
| `render all esa to <output>` | If data has been loaded, all ESA spectra are rendered to `<output>_[esatimestamp].png`. |
| `render every <num>[+<offset>] esa to <output>` | If data has been loaded, every _num_ ESA spectrum starting with _offset_ (if specified) is rendered to `<output>_[timestamp].png`. |
| `render esa <num> to <output>` | If data has been loaded, the ESA spectrum with index _num_ is rendered to `<output>.png`. _Keep in mind that indexing always starts at 0._ |
| `render slice at wavelength <wavelength> to <output>` | If data has been loaded, a slice of the TA spectrum at `<wavelengt>` nm is rendered to `<output>.png`. |
| `render <avg|averaged> slice at wavelength <wavelength> spanning <halfspan> to <output>` | If data has been loaded, the time-dependent absorption is averaged between `<wavelength> - <halfspan>` and `<wavelength> + <halfspan>` and the standard deviation over said interval is calculated. It is rendered to `<output>.png`. |
| `# Comment` | A comment. Inline comments are also allowed. |

## Setting Configs

Dynamic-Taxes allows for multiple ways to set up the configs. Three configs have to be set from the beginning, else the program will terminate. These are:

- `username` Your username. This is relevant for sending jobs to the cluster
- `conda_env` The conda environment which has been set up for Dynamic-Taxes to run in.
- `exec_mode` The default execution mode of Dynamic-Taxes. This can be set to either `local` or `cluster`

You can open the default configs using the command:
```
dynamic-taxes --config
```

Alternatively, you can locally change configs in a script file with the syntax
```
set config <key> to <value>
```
Note that this has no effect on the default configs.
The following fields are set by default

| Name | Datatype | Default | Description |
| --- | --- | --- | --- |
| `username` | `str` | | Your username. This is important for qsub scripts. |
| `conda_env` | `str` | | The conda environment that is set up for Dynamic-Taxes |
| `exec_mode` | `str` | | The default mode of execution. This must be either `local` or `cluster` |
| `wavelength_range_lower` | `numeric` | 200 | The lower end of the spectrum that should be displayed. |
| `wavelength_range_upper` | `numeric` | 1000 | The upper end of the spectrum that should be displayed. |
| `wavelength_res` | `int` | 500 | The number of evaluation points when rendering spectra. |
| `peak_breadth` | `numeric` | 50 | The breadth of a single excitation in nm. |
| `dpi` | `int` | 200 | The DPI at which the images are to be rendered. |
| `timestep_unit` | `str` | ps | The unit of time used in labelling the spectra. |
| `interpolation` | `str` | none | The interpolation used in the TA spectrum. Allowed values can be found [here](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html) |
| `normalise_peak_height` | `bool` | True | Whether the y-axis of ESA spectra should be normalised such that the highest peak is at 1.0 |
| `peak_style` | `str` | bar | The style of drawing individual excitations in ESA spectra. Allowed values are *bar*, *gauss* and the combination *bar,gauss* |
| `energy_unit` | `str` | ev | The unit of energy in which the energies are stored. **If changed, no conversion will be performed.** |
| `ta_title` | `str` | [see](https://github.com/LinusBDittmer/dynamic-taxes/blob/master/dynamictaxes/default.config) | The title displayed atop the TA spectrum. |
| `slice_title` | `str` | [see](https://github.com/LinusBDittmer/dynamic-taxes/blob/master/dynamictaxes/default.config) | The title displayed atop a sliced spectrum. Note that the token `{wavelength}` will be replaced by the actual wavelength. |
| `avg_slice_title` | `str` | [see](https://github.com/LinusBDittmer/dynamic-taxes/blob/master/dynamictaxes/default.config) | The title displayed atop an averaged sliced spectrum. Note that the tokens `{wavelength}` and `{span}` will be replaced by their actual values. |
| `line_colour` | `str` | #a90000 | The line colour used in sliced and ESA spectra. |
| `linewidth` | `numeric` | 2.0 | The linewidth of sliced and ESA spectra. |
| `ta_width` | `numeric` | 8 | The width of a TA spectrum in inches. |
| `ta_height` | `numeric` | 6 | The height of a TA spectrum in inches. |
| `linegraph_width` | `numeric` | 8 | The width of a sliced or ESA spectrum in inches. |
| `linegraph_height` | `numeric` | 5 | The height of a sliced or ESA spectrum in inches. |

Note that in both the `default.config` file as well as a script file, _strings do not require apostrophes_. Each datatype is set via the following:

```
# Setting an Integer
set config dpi to 300
# Setting a Float
set config linewidth to 2.5
# Setting a Boolean
set config normalise_peak_height to False
# Setting a String
set config ta_title to This is a TA spectrum 	# no apostrophes!

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

