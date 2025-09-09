import csv
import os
from .streamUtils import openSerialConnection
from .livePlotter import singleLivePlotter

# === CONFIGURATION ===
OUTPUT_FILE = "data_stream.csv"

def create_csv_file():
    """Create CSV file with headers if it does not exist."""
    with open(OUTPUT_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Raw", "Temp"])

def append_to_csv(data_row):
    """Append a row of data to the CSV file."""
    with open(OUTPUT_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data_row)

def csvStream(graph = True):
    # Ensure CSV file exists
    if not os.path.exists(OUTPUT_FILE):
        create_csv_file()

    # Open serial connection
    ser = openSerialConnection()

    # Initialize live plotter for Value1, Value2,... in multiLivePlotter
    # Only a single label for singleLivePlotter
    if graph == True:
        plotter = singleLivePlotter(label="Value2")

    try:
        counter = 0
        while True:
            line = ser.readline().decode("utf-8").strip()
            # print(line)
            if line:
                values = line.split(",")

                # For simplicity, plot only the first numeric value (Value1)
                try:
                    val = [float(v) for v in values[:3]]
                except (ValueError, IndexError):
                    continue

                # Log to CSV
                row = [counter] + values
                append_to_csv(row)
                print(f"Logged: {row}")

                if graph == True:
                    plotter.update(counter, val[1]) # Feed complete list for multiLivePlotter 

                counter += 1

    except KeyboardInterrupt:
        print("\nStopping data stream.")
    finally:
        ser.close()
        plotter.finalize()