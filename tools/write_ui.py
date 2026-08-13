from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "src" / "AudioProfiles"


def write(rel: str, text: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\r\n", "\n"), encoding="utf-8")
    print("wrote", path)


def main() -> None:
    print("ready", ROOT)


if __name__ == "__main__":
    main()
