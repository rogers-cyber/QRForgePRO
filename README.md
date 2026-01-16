# QRForge PRO v2.0.0 – Professional QR Code Design & Export Studio (Full Source Code)

QRForge PRO v2.0.0 is a professional Python desktop application for **designing, customizing, and exporting high-quality QR codes** for print and digital use.  
This repository contains the **full source code**, allowing you to customize QR generation logic, styling options, canvas behavior, export formats, and UI theming for personal or commercial design workflows.

------------------------------------------------------------
🌟 FEATURES
------------------------------------------------------------

- 📦 Multi-Type QR Generation — Text, URL, and Wi-Fi QR codes
- 🔗 URL Shortening — Optional TinyURL shortening for compact QR codes
- 🎨 Color Customization — Custom fill and background colors
- 🪟 Transparent Background — Ideal for overlays and design workflows
- 🖱️ Interactive Canvas — Drag, move, rotate, and scale QR codes
- 🔄 Rotation Control — Hold **ALT + Drag** to rotate QR items freely
- 🖼️ Multi-QR Workspace — Design multiple QR codes on a single canvas
- 🧭 Zoom & Pan — Mouse wheel zoom with smooth transformations
- 🌗 Dark / Light Theme Support — Toggle modern UI themes
- 🖨️ Print-Ready Export — High-resolution PNG, SVG (vector), and PDF
- 📄 One-QR-Per-Page PDF — Automatic page scaling for professional printing
- 🎯 Designer-Friendly — Large infinite canvas with bounding-box exports
- 🧩 Fully Customizable — Modify UI, QR logic, export behavior, or styling

------------------------------------------------------------
🚀 INSTALLATION
------------------------------------------------------------

1. Clone or download this repository:


```
git clone https://github.com/rogers-cyber/QRForgePRO.git
cd QRForgePRO
```

2. Install required Python packages:

```
pip install qrcode pillow requests PySide6
```

3. Run the application:

```
python QRForgePRO.py
```

4. Optional: Build a standalone executable using PyInstaller:

```
pyinstaller --onefile --windowed QRForgePRO.py
```


------------------------------------------------------------
💡 USAGE
------------------------------------------------------------

1. Select QR Mode:
   - **Text** — Plain text or custom payloads
   - **URL** — Web links (optional shortening)
   - **Wi-Fi** — SSID, password, and encryption type

2. Customize Design:
   - Choose **Fill Color**
   - Choose **Background Color**
   - Enable **Transparent Background** if needed

3. Add QR Code:
   - Click ➕ **Add QR**
   - The QR appears centered on the canvas

4. Edit on Canvas:
   - Drag to move
   - Scroll to zoom
   - Hold **ALT + Drag** to rotate

5. Export:
   - 🖼️ **PNG** — Transparent or solid background
   - 🧩 **SVG** — Fully vector, scalable design
   - 📄 **PDF** — Print-ready, one QR per page

6. Theme & Info:
   - Toggle 🌗 **Theme**
   - View ℹ **About** information

------------------------------------------------------------
⚙️ CONFIGURATION OPTIONS
------------------------------------------------------------

Option                    Description
------------------------- --------------------------------------------------
QR Mode                   Text, URL, or Wi-Fi QR generation
URL Shortening            Optional TinyURL compression
Fill Color                Foreground QR color
Background Color          QR background color
Transparent Background    Export with alpha channel
Canvas Interaction        Drag, zoom, rotate QR items
Theme Toggle              Switch between dark and light UI
Export PNG                Raster image export
Export SVG                Vector-based scalable export
Export PDF                Print-ready PDF (A4, 300 DPI)

------------------------------------------------------------
📦 OUTPUT FORMATS
------------------------------------------------------------

- **PNG** — High-resolution raster image (supports transparency)
- **SVG** — Fully scalable vector QR for professional design tools
- **PDF** — Print-optimized pages with automatic scaling

------------------------------------------------------------
📦 DEPENDENCIES
------------------------------------------------------------

- Python 3.10+
- PySide6 — Qt-based professional GUI framework
- qrcode — QR code generation engine
- Pillow (PIL) — Image handling and RGBA processing
- requests — URL shortening API access
- Qt SVG / PDF — Vector and print export support

------------------------------------------------------------
📝 NOTES
------------------------------------------------------------

- SVG exports are fully vector and suitable for Illustrator, Inkscape, or Figma
- Transparent background is recommended for logo overlays
- PDF export places each QR on a separate A4 page at 300 DPI
- Multiple QR codes can coexist on the same canvas
- Full source code is modular and easy to extend
- Ideal for designers, print shops, and automation workflows

------------------------------------------------------------
👤 ABOUT
------------------------------------------------------------

QRForge PRO v2.0.0 is developed and maintained by **Mate Technologies**, delivering professional Python-based creative and productivity tools.

Website: https://matetools.gumroad.com

------------------------------------------------------------
📜 LICENSE
------------------------------------------------------------

Distributed as commercial source code.  
You may use it for personal or commercial projects.  
Redistribution, resale, or rebranding as a competing product is **not allowed**.
