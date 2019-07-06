# ABOUT

Toshi Omagari's Python scripts for the [Glyphs font editor](http://glyphsapp.com/). They are primarily written for the newest versions (or supposed to be).


# INSTALLATION

Put the scripts into the *Scripts* folder which appears when you choose *Open Scripts Folder* from the *Scripts* menu. After installation, either choose Refresh Script Menu (Option+Shift+Command+Y) or restart the application.

For some scripts, you will also need to install Tal Leming's *Vanilla* and may need to install other modules. In Glyphs 2, you can install them from Preferences > Addons.

# ABOUT THE SCRIPTS
### Metrics & Kerning
* **Batch Metric keys:** (GUI) Applies the specified logic of metrics key to the selected glyphs. *Vanilla required.*
* **Copy Kerning Pairs:** (GUI) Copies kerning patterns to another. It supports pair-to-pair and preset group copying. *Vanilla required.*
* **Copy kerning to Greek & Cyrillic:** (GUI) Copies your Latin kerning to the common shapes of Greek and Cyrillic, including small caps, using predefined dictionary. Exceptions and absent glyphs are skipped. It's best used after finishing Latin kerning and before starting Cyrillic and Greek. *Vanilla required.*
* **Display Unlocked Kerning Pairs:** Shows unlocked kerning pairs (exceptions) in the edit view. String part done by Ben Jones, display part done by Toshi Omagari and Georg Seifert.
* **Kerning Exception:** (GUI) Makes an kerning exception of the current pair. Note: Current glyph is considered the RIGHT side of the glyph. *Vanilla required.*
* **Permutation Text Generator:** (GUI) Outputs glyph permutation text for kerning. *Vanilla required.*
* **Rename Kerning Groups:** (GUI) Lets you rename kerning names and pairs associated with them. *Vanilla required.*
* **Report Metrics Keys:** (GUI) Reports possibly wrong keys. It reports non-existent glyphs in the keys, glyphs using different keys in each layer, and nested keys. *Vanilla required.*
* **Set Kerning Groups (Lat-Grk-Cyr):** (GUI) Sets kerning groups. Groups Latin Greek and Cyrillic together. I advise you use Split Lat-Grk-Cyr Kerning script later. *Vanilla required.*
* **Split Lat-Grk-Cyr Kerning:** Splits kerning groups of LGC (Latin, Greek, Cyrillic) and reconstructs kerning accordingly. Kern once, split later.

### Path
* **Delete Diagonal Nodes Between Extremes:** Good for cleaning TTF curve. It removes Diagonal Node Between Extremes, after placing the current outline in the background.
* **Nudge-move by Numerical Value:** (GUI) Nudge-moves selected nodes by the values specified in the window. *Vanilla required.*
* **Report Compatibility by Numbers:** Outputs path count, node count, anchor count etc. of selected glyphs in the Macro Window.
* **Report Glyphs with Acute-angled Node:** Reports glyphs that have nodes with very acute angle (default: less than 15 degrees).
* **Un-Round Corners:** Removes corners of outlines of the selected letters (current master only).

### Else
* **Analyse Manuscript:** (GUI) Calculates the minimal character set required for the pasted text. Ideal for starting a font for specific text (e.g. book). *Vanilla required.*
* **Create .case alternate:** Duplicates selected glyphs but as components, giving them .case suffix and the sidebearings. Modified from Mekkablue's "Create .ssXX glyph from current layer" script.
* **Duplicate Glyph with Component:** Duplicates selected glyphs but as components, giving them 001 suffix or above depending on availability.
* **Export Glyph Annotations as PDF:** Generates Glyphs annotations as PDF on Desktop.
* **Export InDesign Tagged Text with All Glyphs:** (GUI) Saves InDesign tagged text file that contains all glyphs for typesetting a specimen, using glyph ID.
* **Guideline Locker:** (GUI) Locks selected guidelines and unlocks all global guidelines. *Vanilla required.*
* **Instance Slider:** (GUI) Lets you define interpolation values of instances more graphically, using sliders and preview. *Vanilla and Robofab required.*
* **Search Glyph In Class Features:** Searches glyphs in OpenType classes and features if they are used.*
* **Sync Edit Views:** Refreshes the edit view contents of non-front files. Have multiple files open! *Vanilla required.*
* **Transform Images with Proper Maths:** (GUI) Batch scale and move images in selected layers, using the maths you learned at school. Based on mekkablue's Transform Images script. *Vanilla required.*

# License

Copyright 2016 Toshi Omagari (@tosche_e).
Based on sample codes by Rainer Erich Scheichelbauer (@mekkablue).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
