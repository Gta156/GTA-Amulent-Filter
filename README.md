# GTA Amulent Filter

**Version:** 3.0

**Amulet Editor Filter for Exporting Minecraft Builds as Optimized Commands**

![Filter Screenshot Placeholder - Consider adding a screenshot of the UI in Amulet Editor here]

## Description

The GTA Amulent Filter is an Amulet Editor filter designed to export selected Minecraft builds into a text file containing optimized Minecraft commands. This filter intelligently generates commands, using `fill` commands for linear blocks of the same type and `setblock` for individual blocks, resulting in a more efficient and concise command output for recreating your builds in Minecraft.

This filter is ideal for:

*   Exporting builds from Amulet Editor to use with Minecraft command blocks.
*   Sharing build structures in a text-based, command-line friendly format.
*   Quickly recreating structures in different Minecraft worlds or locations.
*   Optimizing command generation for large or repetitive structures, reducing the total number of commands and improving pasting speed.

## Features

*   **Relative Coordinate Commands:** Generates Minecraft commands using relative coordinates (`~`), allowing for easy placement of the build anywhere in your Minecraft world relative to your position.
*   **Adjustable Build Offset:**  Includes an in-editor UI to set X, Y, and Z offsets, allowing you to shift the position of the exported build when pasting into Minecraft.
*   **Air Block Inclusion Option:** Provides a checkbox to include air blocks in the exported commands, capturing the exact structure including empty spaces.
*   **Optimized Command Generation:**  Leverages `fill` commands for linear arrangements of identical blocks to minimize command count and improve efficiency.
*   **Text File Output:** Exports the generated Minecraft commands to a simple `.txt` file, ready to be copied and pasted directly into the Minecraft console or command blocks.
*   **User-Friendly Interface:** Simple and intuitive UI within Amulet Editor for easy configuration.

## How to Use

1.  **Installation:**
    *   Place the `GTA Filter.py` file into the `amulet_map_editor\plugins\operations` directory within your Amulet Editor installation.
    *   If the `operations` directory doesn't exist in your `plugins` directory, create it.
    *   Restart Amulet Editor.

2.  **Using the Filter in Amulet Editor:**
    *   Open your Minecraft world in Amulet Editor.
    *   Make a selection of the build you want to export using Amulet Editor's selection tools.
    *   Go to `Operation` -> `Filter`.
    *   Find and select `GTA's Amulent Filter 3.0` from the list of available filters.
    *   The GTA Amulent Filter UI will appear.

3.  **Filter UI Options:**
    *   **Top Buttons:**
        *   **Discord:** Opens a description box with a link to the Discord server (if applicable - update the script description accordingly).
        *   **Credits:** Opens a description box displaying credits for the filter.
        *   **Run Filter:**  Executes the filter and generates the command file.
    *   **Set Build Offset:**
        *   **X, Y, Z Inputs:**  Enter numerical values to offset the build's position when pasted into Minecraft. Default values are X: 1, Y: 0, Z: 1. Adjust these as needed for your desired placement.
    *   **Include Air Blocks Checkbox:** Check this box if you want to export air blocks as `setblock air` commands. Leave it unchecked to exclude air blocks from the output.
    *   **Description Box:** Displays information, credits, and filter status messages.

4.  **Running the Filter:**
    *   Click the "Run Filter" button.
    *   The filter will process your selection and generate a text file named `Filtered Build.txt` in your Downloads folder (or the configured `OUTPUT_DIRECTORY` in the script).
    *   The description box will update with the command count and the output file path.

5.  **Using the Output File in Minecraft:**
    *   Locate the `Filtered Build.txt` file in your Downloads folder.
    *   Open the file and copy all the commands.
    *   In your Minecraft world, you can paste these commands into:
        *   The chat window (for a small number of commands).
        *   A command block (for larger builds - you may need multiple command blocks or a function if the command count is very high).

## Configuration

*   **Output Directory:**
    *   By default, the output text file (`Filtered Build.txt`) is saved to your Downloads folder.
    *   You can change the `OUTPUT_DIRECTORY` variable in the `GTA Filter.py` script to specify a different output location.
    *   **To change the output directory:**
        1.  Open `GTA Filter.py` in a text editor.
        2.  Locate the line: `OUTPUT_DIRECTORY = os.path.join("C:\\Users", os.getlogin(), "Downloads")`
        3.  Modify the path within `os.path.join()` to your desired directory. For example, to save to a folder named "MinecraftBuilds" on your Desktop, you might change it to: `OUTPUT_DIRECTORY = os.path.join("C:\\Users", os.getlogin(), "Desktop", "MinecraftBuilds")`

*   **Build Offset:**
    *   The X, Y, and Z input fields in the filter UI allow you to adjust the offset of the exported build.  This is useful if you want to place the build slightly away from your current position in Minecraft when pasting the commands.

## Credits

*   **Developer:** GTA
*   **Special Thanks:** To the Amulet Team for creating Amulet Editor!

## Disclaimer

This filter is provided as-is, and the developer is not responsible for any issues arising from its use. Please back up your Minecraft worlds before using any external tools or filters.

---
