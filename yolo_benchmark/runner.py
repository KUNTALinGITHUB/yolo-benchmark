import cv2
import pandas as pd
import time
from .metrics import Metrics
from .gui import DisplayGUI


class Runner:
    def __init__(self, models, source, class_names=None, model_names=None, duration=None, device="cpu"):
        self.models = models
        self.source = source
        self.class_names = class_names
        self.model_names = model_names if model_names else [f"Model_{i+1}" for i in range(len(models))]
        self.duration = duration
        self.device = device

        self.metrics = [Metrics() for _ in models]
        self.results = [[] for _ in models]

        # 🔹 Initialize GUI
        self.gui = DisplayGUI()

    def run(self):
        cap = cv2.VideoCapture(self.source)

        if not cap.isOpened():
            raise RuntimeError(f"Failed to open source: {self.source}")

        start_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # ⏱️ Stop after duration (if provided)
            if self.duration and (time.time() - start_time > self.duration):
                print("⏹️ Stopping after duration limit")
                break

            # 🔹 Resize for CPU performance
            frame = cv2.resize(frame, (640, 480))

            outputs = []

            for i, model in enumerate(self.models):
                result = model(frame, device=self.device, verbose=False)[0]

                # 🔹 Metrics
                self.metrics[i].update()
                fps = self.metrics[i].get_fps()
                cpu = self.metrics[i].get_cpu()

                annotated = result.plot()

                # 🔹 Overlay text
                cv2.putText(
                    annotated,
                    f"{self.model_names[i]} | FPS: {fps:.2f} | CPU: {cpu:.1f}%",
                    (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

                # 🔹 Process detections safely
                if result.boxes is not None:
                    for box in result.boxes:
                        cls_id = int(box.cls[0])

                        if self.class_names and cls_id < len(self.class_names):
                            cls_name = self.class_names[cls_id]
                        else:
                            cls_name = str(cls_id)

                        x1, y1 = int(box.xyxy[0][0]), int(box.xyxy[0][1])

                        cv2.putText(
                            annotated,
                            cls_name,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            (255, 255, 0),
                            1
                        )

                        # 🔹 Save CSV data
                        self.results[i].append({
                            "frame": self.metrics[i].frame_count,
                            "class_id": cls_id,
                            "class_name": cls_name,
                            "fps": fps,
                            "cpu": cpu
                        })

                outputs.append(annotated)

            # 🔹 Display GUI
            continue_loop = self.gui.show(outputs, self.model_names)
            if continue_loop is False:
                break

        cap.release()
        cv2.destroyAllWindows()
        self.save_csv()

    def save_csv(self):
        for i, data in enumerate(self.results):
            df = pd.DataFrame(data)

            filename = f"{self.model_names[i]}_results.csv"
            filename = filename.replace(".pt", "")

            df.to_csv(filename, index=False)

            if data:
                print(f"✅ CSV saved: {filename}")
            else:
                print(f"⚠️ No detections for {self.model_names[i]} (empty CSV)")