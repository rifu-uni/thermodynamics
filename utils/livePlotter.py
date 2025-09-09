import matplotlib.pyplot as plt

class multiLivePlotter:
    def __init__(self, labels, max_points=50):
        """
        Initialize the live plotter.
        labels: list of labels for each data stream, e.g. ["Value1", "Value2"]
        max_points: how many recent points to keep on the plot
        """
        self.labels = labels
        self.max_points = max_points
        self.x_data = []
        self.y_data = {label: [] for label in labels}

        plt.ion()
        self.fig, self.ax = plt.subplots()

    def update(self, timestamp, values):
        """
        Update the plot with new data.
        timestamp: string (x-axis value, e.g. time)
        values: list of floats, same length as self.labels
        """
        self.x_data.append(timestamp)
        for label, val in zip(self.labels, values):
            self.y_data[label].append(val)

        # Keep only the last max_points
        if len(self.x_data) > self.max_points:
            self.x_data.pop(0)
            for label in self.labels:
                self.y_data[label].pop(0)

        # Clear and redraw
        self.ax.clear()
        for label in self.labels:
            self.ax.plot(self.x_data, self.y_data[label], marker="o", label=label)

        self.ax.set_title("Live Data Stream")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Values")
        self.ax.tick_params(axis="x", rotation=45)
        self.ax.legend()
        plt.tight_layout()
        plt.pause(0.01)

    def finalize(self):
        """Stop interactive mode and keep the final plot open."""
        plt.ioff()
        plt.show()

class singleLivePlotter:
    def __init__(self, label, max_points=50):
        """
        Initialize live plotter.
        label: the single data stream to plot (e.g. "Value2")
        max_points: number of recent points to keep on the plot
        """
        self.label = label
        self.max_points = max_points
        self.x_data = []
        self.y_data = []

        plt.ion()
        self.fig, self.ax = plt.subplots()

    def update(self, timestamp, value):
        """
        Update the plot with new data.
        timestamp: string (x-axis, e.g. time)
        value: float (the value corresponding to self.label)
        """
        self.x_data.append(timestamp)
        self.y_data.append(value)

        # Keep only the last max_points
        if len(self.x_data) > self.max_points:
            self.x_data.pop(0)
            self.y_data.pop(0)

        # Clear and redraw
        self.ax.clear()
        self.ax.plot(self.x_data, self.y_data, marker="o", label=self.label)

        self.ax.set_title(f"Live Data Stream: {self.label}")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Value")
        self.ax.tick_params(axis="x", rotation=45)
        self.ax.legend()
        plt.tight_layout()
        plt.pause(0.01)

    def finalize(self):
        """Stop interactive mode and keep the final plot open."""
        plt.ioff()
        plt.show()