# ABOUT

Tosche's Python scripts for the [Glyphs font editor](http://glyphsapp.com/).


# INSTALLATION

Put the scripts into the *Scripts* folder which appears when you choose *Open Scripts Folder* from the *Scripts* menu.

For some scripts, you will also need to install Tal Leming's *Vanilla*. Here's how. Open Terminal and copy and paste each of the following lines and hit return. Notes: the second line (*curl*...) may take a while, the sudo line will prompt you for your password (type it and press Return, you will *not* see bullets):

    cd ~/Library/
    curl http://download.robofab.com/RoboFab_599_plusAllDependencies.zip > robofab.zip
    unzip -o robofab.zip -d Python_Installs
    rm robofab.zip
    cd Python_Installs/Vanilla/
    sudo python2.6 setup.py install

While we're at it, we can also install Robofab, DialogKit, and FontTools. You don't need those for my scripts though:

    cd ../Robofab/
    sudo python2.6 setup.py install
    cd ../DialogKit/
    sudo python2.6 install.py
    cd ../FontTools/
    sudo python2.6 setup.py install

And you are done. The installation should be effective immediately, but to be on the safe side, you may want to restart or log out and back in again.

# ABOUT THE SCRIPTS
*Metrics & Kerning*
*Path*
*Else*
* **Analyse Manuscript:** (GUI) Calculates the minimal character set required for the pasted text. Ideal for starting a font for specific text (e.g. book). *Vanilla required.*
* **Create .case alternate:** Duplicates selected glyphs but as components, giving them .case suffix and the sidebearings. Modified from Mekkablue's "Create .ssXX glyph from current layer" script.
* **Generate ss20 for All-Glyph Access:** Writes OpenType ss20 feature for all glyphs in the font. Copy glyphs names with slashes and paste it to an OT-savvy application, and activate ss20 to see the glyphs.
* **Guideline Locker:** (GUI) Locks selected guidelines and unlocks all global guidelines. *Vanilla required.*
* **Export Tagged Text with All Glyphs for InDesign:** Saves InDesign tagged text file that contains all glyphs for typesetting a specimen, using glyph ID. This is a better solution than generating ss20 feature.
* **Nudge-move by Numerical Value:** (GUI) Nudge-moves selected nodes by the values specified in the window. *Vanilla required.*
* **Regular Expression Glyph Renaming:** (GUI) Renames selected glyphs using regular expression, with case conversion options. You can use it as a normal renaming tool too. *Vanilla required.*
* **Transform Images with Proper Maths** (GUI) Batch scale and move images in selected layers, using the maths you learned at school. Based on mekkablue's Transform Images script. *Vanilla required.*
## Metrics & Kerning
* **Batch Metric keys:** (GUI) Applies the specified logic of metrics key to the selected glyphs. *Vanilla required.*
* **Copy Kerning Pairs:** (GUI) Copies kerning patterns to another. It supports pair-to-pair and preset group copying. *Vanilla required.*
* **Copy kerning to Greek & Cyrillic:** (GUI) Copies your Latin kerning to the common shapes of Greek and Cyrillic, including small caps, using predefined dictionary. Exceptions and absent glyphs are skipped. It's best used after finishing Latin kerning and before starting Cyrillic and Greek. *Vanilla required.*
* **MenuTitle: Display Unlocked Kerning Pairs** Shows unlocked kerning pairs (exceptions) in the edit view. String part done by Ben Jones, display part done by Toshi Omagari and Georg Seifert.
* **Kerning Exception** (GUI) Makes an kerning exception of the current pair. Note: Current glyph is considered the RIGHT side of the glyph. *Vanilla required.*
* **Permutation Text Generator:** (GUI) Outputs glyph permutation text for kerning. *Vanilla required.*
* **Rename Kerning Groups:** (GUI) Lets you rename kerning names and pairs associated with them. *Vanilla required.*
* **Report Metrics Keys:** (GUI) Reports possibly wrong keys. It reports non-existent glyphs in the keys, glyphs using different keys in each layer, and nested keys. *Vanilla required.*
* **Split Cross-Script Kerning:** Splits kerning groups of LGC (Latin, Greek, Cyrillic) and reconstructs kerning accordingly. Kern once, split later.
## Outline Check
* **Report Glyphs with Acute-angled Node:** Reports glyphs that have nodes with very acute angle (default: less than 15 degrees).
* **Sync Edit Views:** Refreshes the edit view contents of non-front files. Have multiple files open! *Vanilla required.*

# License

Copyright 2014 Toshi Omagari (@tosche_e).
Based on sample codes by Rainer Erich Scheichelbauer (@mekkablue).

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

See the License file included in this repository for further details.
