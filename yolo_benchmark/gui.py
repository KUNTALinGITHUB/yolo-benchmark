import cv2


class DisplayGUI:
    def __init__(self, window_name="YOLO Benchmark", window_size=(1200, 800)):
        self.window_name = window_name
        self.window_size = window_size

        # 🔹 Create resizable window
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, *self.window_size)

    def show(self, frames, model_names):
        """
        Display frames in grid layout (1, 2, or 3 models)
        """

        if not frames:
            return True

        # 🔹 Ensure all frames same size
        base_h, base_w = frames[0].shape[:2]
        resized_frames = [cv2.resize(f, (base_w, base_h)) for f in frames]

        labeled_frames = []
        for i, frame in enumerate(resized_frames):
            labeled = frame.copy()

            label = model_names[i] if i < len(model_names) else f"Model {i+1}"

            # 🔹 Draw background box for readability
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(labeled, (5, 5), (5 + w + 10, 5 + h + 10), (0, 0, 0), -1)

            cv2.putText(
                labeled,
                label,
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2
            )

            labeled_frames.append(labeled)

        # 🔹 Layout handling
        if len(labeled_frames) == 1:
            display_frame = labeled_frames[0]

        elif len(labeled_frames) == 2:
            display_frame = cv2.hconcat(labeled_frames)

        elif len(labeled_frames) == 3:
            top = cv2.hconcat(labeled_frames[:2])
            bottom = labeled_frames[2]

            bottom = cv2.resize(bottom, (top.shape[1], top.shape[0]))
            display_frame = cv2.vconcat([top, bottom])

        else:
            raise ValueError("Maximum 3 models supported")

        # 🔹 Show window
        cv2.imshow(self.window_name, display_frame)

        # 🔹 Exit on ESC
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            return False

        return True