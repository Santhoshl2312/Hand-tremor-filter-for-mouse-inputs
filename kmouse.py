import numpy as np
import tkinter as tk
from collections import deque

class SmoothingApp:
    def __init__(self, root, alpha=0.1, buffer_size=5):
        self.root = root
        self.root.title("Brush Smoothing with EMA and Buffer")

        # Canvas setup
        self.canvas = tk.Canvas(root, bg="white", width=1920, height=1080)
        self.canvas.pack()

        # Mouse trajectory storage
        self.raw_points = []  # Raw mouse points
        self.smoothed_points = []  # Smoothed trajectory

        # EMA and buffer parameters
        self.alpha = alpha  # Smoothing factor for EMA
        self.buffer_size = buffer_size  # Size of buffer for moving average
        self.x_buffer = deque(maxlen=buffer_size)
        self.y_buffer = deque(maxlen=buffer_size)

        # Initial smoothed values
        self.prev_smoothed_x = None
        self.prev_smoothed_y = None

        # Tag to delete previous string line
        self.previous_string_tag = None

        # Bind events
        self.canvas.bind("<B1-Motion>", self.collect_and_smooth)
        self.canvas.bind("<ButtonPress-1>", self.reset_points)

    def collect_and_smooth(self, event):
        # Record raw points
        self.raw_points.append((event.x, event.y))

        # Initialize smoothing with the first raw point to avoid offset
        if self.prev_smoothed_x is None:
            self.prev_smoothed_x = event.x
            self.prev_smoothed_y = event.y

        # Add current x, y to buffer for moving average
        self.x_buffer.append(event.x)
        self.y_buffer.append(event.y)

        # Compute the moving average for smoothed x, y
        smooth_x = np.mean(self.x_buffer)
        smooth_y = np.mean(self.y_buffer)

        # Apply EMA to smooth the current point
        smooth_x = self.alpha * event.x + (1 - self.alpha) * self.prev_smoothed_x
        smooth_y = self.alpha * event.y + (1 - self.alpha) * self.prev_smoothed_y

        self.smoothed_points.append((smooth_x, smooth_y))

        # Update previous smoothed values
        self.prev_smoothed_x = smooth_x
        self.prev_smoothed_y = smooth_y

        # Draw raw line (light gray)
        '''if len(self.raw_points) > 1:
            x1, y1 = self.raw_points[-2]
            x2, y2 = self.raw_points[-1]
            self.canvas.create_line(x1, y1, x2, y2, fill="gray", width=1, tags="raw")'''

        # Draw smoothed line (blue)
        if len(self.smoothed_points) > 1:
            x1, y1 = self.smoothed_points[-2]
            x2, y2 = self.smoothed_points[-1]
            self.canvas.create_line(x1, y1, x2, y2, fill="blue", width=8, tags="smooth")

        # Delete previous "string" line if exists
        if self.previous_string_tag:
            self.canvas.delete(self.previous_string_tag)

        # Draw continuous line from smoothed point to current mouse position (like a string being pulled)
        self.previous_string_tag = self.canvas.create_line(smooth_x, smooth_y, event.x, event.y, fill="blue", width=2, tags="string")

    def reset_points(self, event):
        # Clear points and canvas
        self.raw_points = []
        self.smoothed_points = []
        self.prev_smoothed_x = None
        self.prev_smoothed_y = None
        self.x_buffer.clear()
        self.y_buffer.clear()
        self.canvas.delete("raw")
       # self.canvas.delete("smooth")
        self.canvas.delete("string")

if __name__ == "__main__":
    root = tk.Tk()
    app = SmoothingApp(root, alpha=0.01)
    root.mainloop()
