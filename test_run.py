from yolo_benchmark import Benchmark

bench = Benchmark(
    models=[
        r"D:\python_package_benchmark_yolo\examples\yolov8n.pt",
        r"D:\python_package_benchmark_yolo\examples\yolov8s.pt"
    ],
    class_file="examples/classes.txt",
    device="cpu"
)

# ⏱️ run webcam for 10 seconds
# bench.run(0, duration=10)
# ⏱️ run video for 10 seconds
bench.run(r"D:\python_package_benchmark_yolo\examples\test_video.mp4", duration=10)