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

* **Batch Metrics key:** (GUI) Applies the specified logic of metrics key to the selected glyphs. *Vanilla required.*
* **Report Metrics Keys:** (GUI) Reports possibly wrong keys. It reports non-existent glyphs in the keys, glyphs using different keys in each layer, and nested keys. *Vanilla required.*
* **Generate ss20 for All-Glyph Access:** Writes OpenType ss20 feature for all glyphs in the font. Copy glyphs names with slashes and paste it to an OT-savvy application, and activate ss20 to see the glyphs.
* **Create .case alternate:** Duplicates selected glyphs but as components, giving them .case suffix and the sidebearings. Modified from Mekkablue's "Create .ssXX glyph from current layer" script.
* **Nudge-move by Numerical Value (GUI):** Nudge-moves selected nodes by the values specified in the window. *Vanilla required.*

## Outline Check
* **Report Glyphs with Acute-angled Node:** Reports glyphs that have nodes with very acute angle (default: less than 15 degrees).