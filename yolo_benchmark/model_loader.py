from ultralytics import YOLO
import os


class ModelLoader:
    def __init__(self, model_paths, device="cpu"):
        if not model_paths:
            raise ValueError("Model list cannot be empty")

        if len(model_paths) > 3:
            raise ValueError("Maximum 3 models allowed")

        self.models = []
        self.model_names = []
        self.device = self._validate_device(device)

        for path in model_paths:
            # 🔹 Validate path
            if not os.path.exists(path):
                raise FileNotFoundError(f"Model file not found: {path}")

            try:
                model = YOLO(path)

                # 🔹 Store model
                self.models.append(model)

                # 🔹 Clean model name (remove .pt)
                name = os.path.splitext(os.path.basename(path))[0]
                self.model_names.append(name)

            except Exception as e:
                raise RuntimeError(f"Failed to load model '{path}': {str(e)}")

    def _validate_device(self, device):
        """
        Validate and fallback device if needed
        """
        if device == "cuda":
            try:
                import torch
                if not torch.cuda.is_available():
                    print("⚠️ CUDA not available, switching to CPU")
                    return "cpu"
            except ImportError:
                print("⚠️ PyTorch not found, switching to CPU")
                return "cpu"

        return device

    def get_models(self):
        return self.models

    def get_model_names(self):
        return self.model_names

    def get_device(self):
        return self.device