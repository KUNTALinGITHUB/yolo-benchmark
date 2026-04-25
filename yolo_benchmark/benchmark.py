from .model_loader import ModelLoader
from .runner import Runner
from .utils import load_classes
import os


class Benchmark:
    def __init__(self, models, class_file=None, device="cpu"):
        # 🔹 Validate models
        if not models:
            raise ValueError("At least one model must be provided")

        if len(models) > 3:
            raise ValueError("Maximum 3 models allowed")

        # 🔹 Validate model paths
        for path in models:
            if not os.path.exists(path):
                raise FileNotFoundError(f"Model file not found: {path}")

        # 🔹 Load models
        self.loader = ModelLoader(models, device=device)
        self.models = self.loader.get_models()

        # 🔹 Store model names (cleaned)
        self.model_names = [
            os.path.splitext(os.path.basename(m))[0] for m in models
        ]

        # 🔹 Store device
        self.device = device

        # 🔹 Load class names (optional)
        self.class_names = None
        if class_file:
            if not os.path.exists(class_file):
                raise FileNotFoundError(f"Class file not found: {class_file}")
            self.class_names = load_classes(class_file)

    def run(self, source, duration=None):
        # 🔹 Allow webcam (int input)
        if isinstance(source, str):
            if not os.path.exists(source):
                raise FileNotFoundError(f"Input source not found: {source}")

        elif not isinstance(source, int):
            raise ValueError("Source must be a file path or webcam index (int)")

        runner = Runner(
            models=self.models,
            source=source,
            class_names=self.class_names,
            model_names=self.model_names,
            device=self.device,
            duration=duration
        )

        runner.run()