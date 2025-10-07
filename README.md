# Experimental Thermodynamics

This repository contains code, data and notebooks used to collect and visualise temperature data from small laboratory setups (PT100, thermistors, Arduino streams, etc.). The project is lightweight and aimed at recording serial data into CSV files and plotting live streams for quick experiments.

## Repository structure

Top-level layout:

- `data/` - raw CSV data collected from experiments. Several example datasets are included for calibration and testing.
- `notebooks/` - Jupyter notebooks used for analysis and demonstrations.
- `src/` - Python source code for streaming, plotting and serial utilities.

More detailed tree:

- data/
	- 00_thermo-calibration/
		- mixedBoiling0.csv
		- mixedBoiling1repro.csv
		- mixedCooling0.csv
		- mixedHeating0.csv
		- mixedHeating1.csv
		- pt100Ice0.csv
		- pt100Ice1.csv
		- pt100Ice2.csv
		- termIce0.csv
		- testIce0.csv

- notebooks/
	- 00_thermo-calibration.ipynb  # Notebook demonstrating calibration workflows and example analysis

- src/
	- __init__.py                  # Small package entry-point that calls the CSV stream runner
	- arduino/                     # Arduino sketches for devices used in experiments
		- LM35/
			- LM35.ino
		- mix/
			- mix.ino
		- PT100/
			- PT100.ino
	- dataStream/                  # Streaming and plotting utilities
		- csvStream.py               # Main CSV logging + live plotting loop (csvStream())
		- livePlotter.py             # Simple live plotting helpers (single/multi stream)
		- streamUtils.py             # Serial connection helper (uses pyserial)
		- settings.py                # Configure SERIAL_PORT, BAUD_RATE and OUTPUT_FILE here

## Key files and responsibilities

- `src/dataStream/settings.py`
	- Configuration constants. Update `SERIAL_PORT` to the device path of your USB serial (macOS example: `/dev/cu.usbmodem1201`) and `OUTPUT_FILE` to the desired CSV filename before running.

- `src/dataStream/streamUtils.py`
	- Wraps `serial.Serial(...)` (pyserial) and returns an open serial connection with a short timeout.

- `src/dataStream/csvStream.py`
	- The core loop reading lines from the serial device, parsing comma-separated values, appending rows to CSV and feeding the live plotters. Call `csvStream(graph=True)` to enable live plots.
	- The CSV file header created is `Timestamp, Raw, Temp` (the code appends rows beginning with a counter index followed by the raw values read).

- `src/dataStream/livePlotter.py`
	- Very small matplotlib-based live plotting utilities. `singleLivePlotter` plots a single series, `multiLivePlotter` can plot multiple labelled series.

- `src/__init__.py`
	- Imports and exposes `main()` which calls the CSV stream runner. You can launch the stream by importing the package and calling `src.main()`.

## Dependencies

You will need Python 3.8+ and the following packages:

- matplotlib
- pyserial

You can use `pixi` to install them.

## How to run

1. Edit `src/dataStream/settings.py` and set `SERIAL_PORT` to the correct device for your platform and device (macOS example: `/dev/cu.usbmodem1201`). Also set `OUTPUT_FILE` if you want a different CSV path.

2. From the repository root you can start the stream and live plots from Python:

```bash
# activate virtualenv first if used
python -c "import src; src.main()"
```

This will start reading lines from the serial port, append them to `OUTPUT_FILE`, and show live matplotlib plots. Use Ctrl+C to stop; the serial connection and plots are closed in the code's `finally` block.

Alternative (call csvStream directly from an interactive session):

```python
from src.dataStream.csvStream import csvStream
csvStream(graph=True)
```

If you don't want live plotting (headless logging), call `csvStream(graph=False)`.

## Data format

The code expects each serial line to be a comma-separated list of numeric values (floating point). It attempts to parse at least the first 6 values; invalid lines are ignored. The CSV rows written begin with a counter (an integer index) followed by the values emitted by the device.

## Notebooks

Open `notebooks/00_thermo-calibration.ipynb` in JupyterLab or Jupyter Notebook to inspect example analyses and calibration steps. The notebook uses CSVs from `data/00_thermo-calibration/`.

## Notes, caveats and edge cases

- Serial device availability: ensure you have permissions to access the serial device. On macOS you may need to allow terminal access to the USB device in System Settings or run Python from a session with appropriate permissions.
- Malformed serial lines are skipped; the parser expects numeric strings separated by commas.
- Live plotting with matplotlib requires a display environment; on headless machines disable plotting (graph=False) and just log to CSV.

## Next steps (suggested improvements)

- Add a `requirements.txt` and make a small CLI entrypoint in `src/__main__.py` for `python -m src` convenience.
- Add unit tests for CSV writing and parsing logic.