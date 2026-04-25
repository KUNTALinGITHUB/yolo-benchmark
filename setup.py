from setuptools import setup, find_packages

setup(
    name="yolo_benchmark",
    version="0.1.0",
    author="Kuntal Pal",
    author_email="kuntal.pal7550@gmail.com",
    description="A real-time YOLO model benchmarking tool for comparing performance (FPS, detection, CSV export) across multiple models.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KUNTALinGITHUB/yolo-benchmark",  # update this
    packages=find_packages(),
    install_requires=[
        "ultralytics",
        "opencv-python",
        "pandas",
        "numpy",
        "psutil"
    ],
    python_requires=">=3.8",
    keywords=[
        "yolo",
        "object detection",
        "benchmark",
        "computer vision",
        "opencv",
        "ai",
        "deep learning"
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",  # change if needed
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    include_package_data=True,
    zip_safe=False,
)