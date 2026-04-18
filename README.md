# OpenHardwareBoard (OHB)

A web app for generating parametric 3D-printable hardware test boards for metric bolts (M2–M12). Enter your hardware dimensions, generate a board, and print it to verify fit before committing to a full design.

Every hole type includes a bolt slip-fit through-hole so you can test the bolt alongside the nut pocket in the same print.

## Inspiration

This project was inspired by [Alexandre Chappel's Hardware Design Boards](https://www.alch.shop/shop/p/hardware-design-boards) — a beautifully made physical reference board for hardware fit testing. My nuts and bolts didn't quite fit his board, so I built OHB to generate a fully parametric version sized to your exact hardware. If you want a polished, ready-to-go physical product, definitely check out his version.

## What It Generates

Each board includes the following hole types, all labeled with dimensions:

- **Hex nut pockets** — press fit and slip fit
- **Square nut pockets** — press fit, slip fit, and a vertical edge-insert slot
- **Counter bore** — standard and with washer clearance
- **Counter sunk** — with chamfered cone
- **Bolt slip fit** — simple clearance through-hole
- **Heat insert pocket** — for threaded heat-set inserts

Supports **multi-color export** — generates two separate STL files (base board + text/graphics layer) for multi-material printing.

## Calibration Test Pieces

Before printing the full board, use the **Calibration Test Pieces** tab to generate a small test piece with 5 holes in 0.1 mm increments. This lets you dial in the exact fit for your printer and hardware brand before committing to the full board.

## Requirements

- Python 3.10+
- [CadQuery](https://cadquery.readthedocs.io/) (installed via pip — see note below)

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/openhardwareboard.git
cd openhardwareboard

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

> **Note:** CadQuery and its dependencies are large (~500 MB). The install may take a few minutes.

## Running the App

```bash
python manage.py migrate
python manage.py runserver
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Usage

1. Select a bolt size preset (M2–M12) or enter your own measured values
2. Adjust any dimensions using calipers on your actual hardware
3. Choose an export mode (single color or multi-color)
4. Click **Generate Board**
5. Preview the board in the 3D viewer, then download the STL file(s)

> **Preset values are starting points only.** Every 3D printer and hardware brand is different. Always measure your hardware with calipers and use the calibration test pieces to verify fit before printing a full board.

## Export Modes

| Mode | Files | Use When |
|---|---|---|
| Single Color | 1 STL | Standard single-material printing |
| Multi-Color (raised text) | 2 STL | Filament swap at layer height for labels |
| Multi-Color (recessed text) | 2 STL | Text cut into board, second color fills it |

## Project Structure

```
board_designer/
  board_generator.py      # Core 3D model generation (CadQuery)
  test_piece_generator.py # Calibration test piece generation
  models.py               # Django model for board parameters
  forms.py                # Input forms and validation
  views.py                # Request handling and STL export
  validation.py           # Parameter validation logic
  holes.py                # Hole geometry functions
  lines.py                # Dimension line/arrow geometry
  outlines.py             # Feature outline geometry
  text.py                 # Text label geometry
hardware_board_generator/  # Django project settings
manage.py
requirements.txt
```

## Tech Stack

- **Django 5** — web framework
- **CadQuery 2.6** — parametric 3D CAD geometry, STL export
- **Three.js** — browser-based 3D STL preview
- **Bootstrap 5.3** — UI
