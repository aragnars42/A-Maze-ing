import sys
from typing import Any

REQUIRED_KEYS: list[str] = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT"
]


def parse() -> dict[str, Any]:
    """Doscstring"""

    if len(sys.argv) < 2:
        print("ERROR - No argument")
        sys.exit(1)

    name_fiche: str = sys.argv[1]
    try:
        with open(name_fiche, encoding="utf-8") as f:
            content: list[str] = f.readlines()
    except FileNotFoundError:
        print(f"ERROR - {name_fiche} Not found")
        sys.exit(1)

    config: dict[str, Any] = {}

    for i, line in enumerate(content, 1):
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if '=' not in line:
            print(f"ERROR - Line {i} invalid format")
            sys.exit(1)

        key, value = line.split("=", 1)
        key = key.strip().upper()
        value = value.strip()

        if not key or not value:
            print(f"ERROR - Line {i} empaty value or key")
            sys.exit(1)

        config[key] = value

    for key in REQUIRED_KEYS:
        if key not in config:
            sys.exit(1)

    config["ENTRY"] = config["ENTRY"].split(",")
    config["EXIT"] = config["EXIT"].split(",")

    try:
        config["WIDTH"] = int(config["WIDTH"])
        config["HEIGHT"] = int(config["HEIGHT"])
        config["ENTRY"][0] = int(config["ENTRY"][0])
        config["ENTRY"][1] = int(config["ENTRY"][1])
        config["EXIT"][0] = int(config["EXIT"][0])
        config["EXIT"][1] = int(config["EXIT"][1])
    except ValueError as e:
        print(f"ERROR -  {e}")
        sys.exit(1)

    if config["PERFECT"] == "True":
        config["PERFECT"] = True
    elif config["PERFECT"] == "False":
        config["PERFECT"] = False
    else:
        print("ERROR - Not True or False")
        sys.exit(1)

    if config["WIDTH"] <= 0:
        print("ERROR - Width cant be 0 or negative")
        sys.exit(1)
    if config["HEIGHT"] <= 0:
        print("ERROR - Height cant be 0 or negative")
        sys.exit(1)

    if (
        config["ENTRY"][0] >= config["WIDTH"]
        or config["ENTRY"][1] >= config["HEIGHT"]
    ):
        print("ERROR - Entry must be less than width")
        sys.exit(1)
    if (
        config["EXIT"][0] >= config["WIDTH"]
        or config["EXIT"][1] >= config["HEIGHT"]
    ):
        print("ERROR - Exit must be less than height")
        sys.exit(1)

    if config["ENTRY"][0] < 0 or config["ENTRY"][1] < 0:
        print("ERROR - Entry cant be negative")
        sys.exit(1)
    if config["EXIT"][0] < 0 or config["EXIT"][1] < 0:
        print("ERROR - Exit cant be negative")
        sys.exit(1)

    entry: tuple[int, int] = (config["ENTRY"][0], config["ENTRY"][1])
    exit: tuple[int, int] = (config["EXIT"][0], config["EXIT"][1])

    if entry == exit:
        print("ERROR- Entry and Exit cant be same")
        sys.exit(1)

    return config
