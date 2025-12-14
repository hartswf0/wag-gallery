# WAG Gold Gallery & Castle Architect

This repository contains the tools for the **WAG Gold** project: a premium LDraw visualization gallery and a procedural castle generation system.

## 🏰 WAG Castle Architect (`wag-castle-arch.html`)

A powerful, browser-based procedural generation tool for creating LDraw (`.mpd`) castle scenes.

### Key Features
*   **Procedural Generation**: Instantly generates **Small (32x32)**, **Medium (48x48)**, and **Large (64x64)** castle layouts.
*   **Intelligent Parsing**: Paste raw LDraw/MPD code for custom units or scatter props. The tool parses the geometry and "inlines" it into the final model—no broken sub-file references.
*   **Cinematic Camera**: Includes a pre-programmed **MENTO** camera track:
    1.  Orbit Front → Right → Back → Left
    2.  Swoop In to Courtyard
    3.  Gatekeeper Hero Shot
*   **Production Ready**: Outputs a single, flat `.mpd` file compatible with any LDraw viewer (Bricksmith, LeoCAD) and the **Grecian Urn** web viewer.

### How to Use
1.  **Launch**: Open `wag-castle-arch.html` in your browser (via local server recommended).
2.  **Configure**:
    *   **Architecture**: Set sizes and wall height.
    *   **Gate & Hero**: Customize the gate geometry or hero unit.
    *   **Forces**: Paste MPD code for **Invaders** and **Defenders**.
    *   **Scatter**: Paste a "Location/Production" MPD to procedurally scatter its props (trees, crates, lamps) in the courtyard.
3.  **Generate**: Click **GENERATE SYSTEMS**.
4.  **Export**: Select a size tab (Small/Medium/Large), then click **Copy** or **Download**.
5.  **Visualize**: Paste the code into the [Grecian Urn Viewer](https://hartswf0.github.io/tractor-dce-gyo/grecian-urn.html) to see it rendered with lighting and camera animation.

---

## 🖼️ WAG Gold Gallery (`wag-gold-gallery.html`)

A premium, dark-mode slideshow viewer for presenting generated LDraw scenes.

### Key Features
*   **Slideshow Mode**: Seamless navigation between scenes using Arrow keys or UI buttons.
*   **Metadata Display**: Shows filename, author, part count, and description for each scene.
*   **Export Tools**:
    *   **Download PNG**: Capture high-res screenshots of the current view.
    *   **Download MPD**: Get the source file for any slide.
*   **MENTO Integration**: correctly handles `!MENTO` comments for lighting and camera setup instructions if processed by a compatible renderer.

### Workflows

#### Setting Up the Gallery
1.  Place your `.mpd` files in the `scenes/` directory (or root).
2.  **Generate Manifest**: Run `python3 generate_manifest.py` to index the new files. This is required for GitHub Pages.
3.  Open `wag-gold-gallery.html` to view.

#### "Production Set" Workflow
1.  Build a "palette" of props (trees, crates, walls) in a single LDraw file.
2.  Label them with comments like `0 // PROP - Tree`.
3.  Copy the content of this file.
4.  Paste it into the **Scatter MPD** field in **Castle Architect**.
5.  The Architect will extract these items and procedurally populate your castle courtyard.

---

## 🛠️ Local Development

To run the tools locally (avoids CORS issues):

```bash
# Start a Python HTTP server
python3 -m http.server 8090
```

Then visit:
*   [http://localhost:8090/wag-castle-arch.html](http://localhost:8090/wag-castle-arch.html)
*   [http://localhost:8090/wag-gold-gallery.html](http://localhost:8090/wag-gold-gallery.html)
