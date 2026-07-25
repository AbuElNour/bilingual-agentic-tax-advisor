from pathlib import Path
from xml.etree import ElementTree


def main() -> None:
    files = sorted(Path("force-app").rglob("*.xml"))
    if not files:
        raise SystemExit("No metadata files found")
    for path in files:
        ElementTree.parse(path)
    apex = list(Path("force-app").rglob("*.cls"))
    if not apex:
        raise SystemExit("No Apex files found")
    print(f"Validated {len(files)} XML metadata files and {len(apex)} Apex files")


if __name__ == "__main__":
    main()

