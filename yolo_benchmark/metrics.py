import time
import psutil
from collections import deque


class Metrics:
    def __init__(self, window_size=10):
        # 🔹 High precision timer
        self.start_time = time.perf_counter()
        self.prev_time = time.perf_counter()

        self.frame_count = 0
        self.current_fps = 0.0

        # 🔹 FPS smoothing
        self.fps_window = deque(maxlen=window_size)

        # 🔹 Process tracking
        self.process = psutil.Process()

    def update(self):
        self.frame_count += 1

        current_time = time.perf_counter()
        delta = current_time - self.prev_time

        if delta > 0:
            instant_fps = 1.0 / delta
            self.fps_window.append(instant_fps)

            # 🔹 Smoothed FPS
            self.current_fps = sum(self.fps_window) / len(self.fps_window)

        self.prev_time = current_time

    def get_fps(self):
        return self.current_fps

    def get_avg_fps(self):
        elapsed = time.perf_counter() - self.start_time
        return self.frame_count / elapsed if elapsed > 0 else 0

    def get_cpu(self):
        # 🔹 Process-specific CPU usage
        return self.process.cpu_percent(interval=None)

    def get_memory(self):
        # 🔹 Memory usage in MB
        return self.process.memory_info().rss / (1024 * 1024)