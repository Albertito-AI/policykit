"""Create two original, clearly fictional PDFs using only the standard library.

Run from the repository root: python examples/esg/make_demo.py NEW_DIRECTORY
No existing file is overwritten. These fixtures are not real company reports.
"""

from pathlib import Path
import sys


REPORTS = {
    "fictional_2024.pdf": [
        ["FICTIONAL REGNAV TRAINING COMPANY", "Sustainability disclosure exercise: reporting year 2024", "This is original fictional training data, not a real company report.", "Scope 1 emissions: 100 tCO2e.", "Scope 2 emissions: 200 tCO2e.", "Boundary: Facility A. Method: Activity data multiplied by supplied factors.", "Energy use was 800 MWh. Water withdrawal was 1000 cubic metres.", "The board plans to train 40 employees by 31 December 2025."],
        ["FICTIONAL GOVERNANCE AND ASSURANCE", "The sustainability committee reviews the emissions inventory.", "Limited assurance covers Scope 1 and Scope 2 emissions for Facility A only.", "Other report content is outside the selected-indicator engagement.", "Target: reduce energy use after checking comparable reporting boundaries.", "Source date: fictional year-end 2024."],
    ],
    "fictional_2025.pdf": [
        ["FICTIONAL REGNAV TRAINING COMPANY", "Sustainability disclosure exercise: reporting year 2025", "This is original fictional training data, not a real company report.", "Scope 1 emissions: 110 tCO2e.", "Scope 2 emissions: 180 tCO2e.", "The 2024 Scope 1 comparative is restated to 120 tCO2e.", "Boundary: Facilities A and B. Method changed after adding Facility B.", "The original 2024 Scope 1 figure was 100 tCO2e."],
        ["FICTIONAL PLANS AND GOVERNANCE", "Management reports that 30 employees attended training.", "Attendance records were not included in the supplied report.", "The earlier plan was to train 40 employees by 31 December 2025.", "The committee reviewed the changed reporting boundary.", "Energy use was 780 MWh. Water withdrawal was 950 cubic metres.", "Waste recycling programmes continued. No outcome evidence was supplied."],
        ["FICTIONAL SELECTED-INDICATOR ASSURANCE", "Limited assurance covers Scope 1 emissions for Facility A only.", "Scope 2, Scope 3 and the remaining report content are excluded.", "The assurance statement does not cover all entities in the group.", "This is a fictional scope statement for a software demonstration."],
    ],
}


def pdf_bytes(pages):
    objects = [b"<< /Type /Catalog /Pages 2 0 R >>", b"", b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"]
    kids = []
    for lines in pages:
        page_id = len(objects) + 1
        stream_id = page_id + 1
        kids.append(f"{page_id} 0 R")
        objects.append(f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 3 0 R >> >> /Contents {stream_id} 0 R >>".encode())
        commands = ["BT", "/F1 10 Tf", "44 748 Td", "18 TL"]
        for line in lines:
            text = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
            commands.append(f"({text}) Tj T*")
        commands.append("ET")
        stream = ("\n".join(commands) + "\n").encode("ascii")
        objects.append(f"<< /Length {len(stream)} >>\nstream\n".encode() + stream + b"endstream")
    objects[1] = f"<< /Type /Pages /Kids [{' '.join(kids)}] /Count {len(pages)} >>".encode()
    result = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(result))
        result.extend(f"{i} 0 obj\n".encode() + obj + b"\nendobj\n")
    start = len(result)
    result.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        result.extend(f"{offset:010d} 00000 n \n".encode())
    result.extend(f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{start}\n%%EOF\n".encode())
    return bytes(result)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python examples/esg/make_demo.py NEW_DIRECTORY")
    directory = Path(sys.argv[1])
    directory.mkdir(parents=False, exist_ok=False)
    for name, pages in REPORTS.items():
        with (directory / name).open("xb") as handle:
            handle.write(pdf_bytes(pages))
    print(directory.resolve())


if __name__ == "__main__":
    main()
