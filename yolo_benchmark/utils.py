import os


def load_classes(class_file):
    # 🔹 Check file exists
    if not os.path.exists(class_file):
        raise FileNotFoundError(f"Class file not found: {class_file}")

    classes = []

    try:
        with open(class_file, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()

                # 🔹 Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue

                # 🔹 Handle "0 person" format
                parts = line.split()
                if len(parts) > 1 and parts[0].isdigit():
                    name = " ".join(parts[1:])
                else:
                    name = line

                classes.append(name)

    except Exception as e:
        raise RuntimeError(f"Error reading class file '{class_file}': {str(e)}")

    # 🔹 Validate content
    if not classes:
        raise ValueError(f"Class file '{class_file}' is empty or invalid")

    return classes