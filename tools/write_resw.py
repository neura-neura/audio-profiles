from pathlib import Path
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

root = Path(r"C:\Users\neura\repos\audio-device-switcher\src\AudioProfiles\Strings")

def convert(src: Path) -> None:
    tree = ET.parse(src)
    items = []
    for node in tree.getroot():
        name = node.attrib.get("name")
        if not name:
            continue
        items.append((name, "".join(node.itertext())))
    lines = [
        "<?xml version=\"1.0\" encoding=\"utf-8\"?>",
        "<root>",
        "  <resheader name=\"resmimetype\">",
        "    <value>text/microsoft-resx</value>",
        "  </resheader>",
        "  <resheader name=\"version\">",
        "    <value>2.0</value>",
        "  </resheader>",
        "  <resheader name=\"reader\">",
        "    <value>System.Resources.ResXResourceReader, System.Windows.Forms, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089</value>",
        "  </resheader>",
        "  <resheader name=\"writer\">",
        "    <value>System.Resources.ResXResourceWriter, System.Windows.Forms, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089</value>",
        "  </resheader>",
    ]
    for name, value in items:
        lines.append(f"  <data name=\"{escape(name)}\" xml:space=\"preserve\">")
        lines.append(f"    <value>{escape(value)}</value>")
        lines.append("  </data>")
    lines.append("</root>")
    lines.append("")
    src.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print("converted", src, "items", len(items))

for path in root.rglob("*.resw"):
    convert(path)
