#   GTA
#   Amulent filter by Gta
#  Amulet Editor standard includes for an operation

import wx

from amulet.api.selection import SelectionGroup
from amulet.api.level import BaseLevel
from amulet.api.data_types import Dimension
from amulet.api.block import Block

from amulet_map_editor.programs.edit.api.operations import DefaultOperationUI

# Import Block and BlockEntity directly if needed for further processing
# from amulet.api.block_entity import BlockEntity

from random import randint
import os  # For working with file paths
TITLE = "GTA's Amulent Filter 3.0"

#  --- Configuration ---
OUTPUT_DIRECTORY = os.path.join("C:\\Users", os.getlogin(), "Downloads")

def get_unique_output_path(directory, filename):
    base, ext = os.path.splitext(filename)
    counter, unique_name = 1, filename
    while os.path.exists(os.path.join(directory, unique_name)):
        unique_name = f"{base} ({counter}){ext}"
        counter += 1
    return os.path.join(directory, unique_name)

#  --- End Configuration ---

class GTAFilterOperation(wx.Panel, DefaultOperationUI):
    def __init__(self, parent: wx.Window, canvas: "GTA", world: BaseLevel, options_path: str):
        super().__init__(parent)
        DefaultOperationUI.__init__(self, parent, canvas, world, options_path)

        # UI layout
        self._sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self._sizer)

        # Top buttons
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_buttons = [
            ("Discord", self._run_discord),
            ("Credits", self._run_credits),
            ("Run Filter", self._run_filter),
        ]
        for label, handler in top_buttons:
            button = wx.Button(self, label=label)
            button.Bind(wx.EVT_BUTTON, handler)
            button_sizer.Add(button, 0, wx.ALL, 5)
        self._sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        title_label = wx.StaticText(self, label="Set Build Offset:")
        font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_label.SetFont(font)
        self._sizer.Add(title_label, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        coordinate_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # X Input
        self.x_label = wx.StaticText(self, label="X:")
        self.x_input = wx.TextCtrl(self, size=(50, -1), value="1")
        coordinate_sizer.Add(self.x_label, 0, wx.ALL, 5)
        coordinate_sizer.Add(self.x_input, 0, wx.ALL, 5)

        # Y Input
        self.y_label = wx.StaticText(self, label="Y:")
        self.y_input = wx.TextCtrl(self, size=(50, -1), value="0")
        coordinate_sizer.Add(self.y_label, 0, wx.ALL, 5)
        coordinate_sizer.Add(self.y_input, 0, wx.ALL, 5)

        # Z Input
        self.z_label = wx.StaticText(self, label="Z:")
        self.z_input = wx.TextCtrl(self, size=(50, -1), value="1")
        coordinate_sizer.Add(self.z_label, 0, wx.ALL, 5)
        coordinate_sizer.Add(self.z_input, 0, wx.ALL, 5)

        self._sizer.Add(coordinate_sizer, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        # Air Blocks checkbox
        self.include_air_checkbox = wx.CheckBox(self, label="Include Air Blocks")
        self._sizer.Add(self.include_air_checkbox, 0, wx.ALIGN_CENTER | wx.TOP, 10)

        # Text box
        self._mode_description = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_BESTWRAP, size=(272, 150))
        self._mode_description.SetValue("GTA's Amulent Filter 3.0")
        self._sizer.Add(self._mode_description, 1, wx.EXPAND | wx.TOP | wx.RIGHT, 5)

        self.Layout()

    def _run_discord(self, _):
        self._mode_description.SetValue("Discord Black Light Builds:\n\nhttps://discord.gg/3pZvgq4XPq\nFor Exclusive Builds")

    def _run_credits(self, _):
        self._mode_description.SetValue("Credits:\n\nDeveloper: GTA\nSpecial Thanks To The Amulet Team! :D")

        self.groupedblocks = set()
        self.highestCoords = [-9999999, -9999999, -9999999]

    def checkAround(self, x, y, z, world: BaseLevel, dimension: Dimension, box, include_air):
        curgrouped = []
        alreadyChoseDir = False
        groupedblocks = self.groupedblocks

        try:
            block, _ = world.get_version_block(x, y, z, dimension, (world.level_wrapper.platform, world.level_wrapper.version))
        except Exception:
            return []
        if block is None:
            return []

        # Helper to get block safely
        def get_block(bx, by, bz):
            if box.min_x <= bx < box.max_x and box.min_y <= by < box.max_y and box.min_z <= bz < box.max_z:
                try:
                    b, _ = world.get_version_block(bx, by, bz, dimension, (world.level_wrapper.platform, world.level_wrapper.version))
                    return b
                except Exception:
                    return None
            return None

        if get_block(x + 1, y, z) == block and (x + 1, y, z) not in groupedblocks and not alreadyChoseDir:
            curgrouped = self.checkLinear(x, y, z, 1, 0, 0, world, dimension, box, block)
            alreadyChoseDir = True
        if get_block(x - 1, y, z) == block and (x - 1, y, z) not in groupedblocks and not alreadyChoseDir:
            curgrouped = self.checkLinear(x, y, z, -1, 0, 0, world, dimension, box, block)
            alreadyChoseDir = True
        if get_block(x, y + 1, z) == block and (x, y + 1, z) not in groupedblocks and not alreadyChoseDir:
            curgrouped = self.checkLinear(x, y, z, 0, 1, 0, world, dimension, box, block)
            alreadyChoseDir = True
        if get_block(x, y - 1, z) == block and (x, y - 1, z) not in groupedblocks and not alreadyChoseDir:
            curgrouped = self.checkLinear(x, y, z, 0, -1, 0, world, dimension, box, block)
            alreadyChoseDir = True
        if get_block(x, y, z + 1) == block and (x, y, z + 1) not in groupedblocks and not alreadyChoseDir:
            curgrouped = self.checkLinear(x, y, z, 0, 0, 1, world, dimension, box, block)
            alreadyChoseDir = True
        if get_block(x, y, z - 1) == block and (x, y, z - 1) not in groupedblocks and not alreadyChoseDir:
            curgrouped = self.checkLinear(x, y, z, 0, 0, -1, world, dimension, box, block)
            alreadyChoseDir = True

        return curgrouped

    def checkLinear(self, x, y, z, xdir, ydir, zdir, world: BaseLevel, dimension: Dimension, box, checkBlock):
        groupedblocks = self.groupedblocks
        groupStart = [x, y, z]
        groupEnd = [x, y, z]

        multfactor = 1
        extending = True

        while extending:
            nx, ny, nz = x + (xdir * multfactor), y + (ydir * multfactor), z + (zdir * multfactor)

            if box.min_x <= nx < box.max_x and box.min_y <= ny < box.max_y and box.min_z <= nz < box.max_z:
                try:
                    current_block, _ = world.get_version_block(nx, ny, nz, dimension, (world.level_wrapper.platform, world.level_wrapper.version))
                    if current_block == checkBlock:
                        groupEnd = [nx, ny, nz]
                        multfactor += 1
                        continue
                except Exception:
                    pass
            extending = False

        # Mark blocks as grouped
        min_x = min(groupStart[0], groupEnd[0])
        max_x = max(groupStart[0], groupEnd[0])
        min_y = min(groupStart[1], groupEnd[1])
        max_y = max(groupStart[1], groupEnd[1])
        min_z = min(groupStart[2], groupEnd[2])
        max_z = max(groupStart[2], groupEnd[2])

        for gx in range(min_x, max_x + 1):
            for gy in range(min_y, max_y + 1):
                for gz in range(min_z, max_z + 1):
                    groupedblocks.add((gx, gy, gz))

        if len(groupStart) == 3 and len(groupEnd) == 3:
            return [groupStart[0], groupStart[1], groupStart[2], groupEnd[0], groupEnd[1], groupEnd[2]]
        else:
            return []

    def findblocks(self, world: BaseLevel, dimension: Dimension, box, include_air):
        print(TITLE+" starting")

        output_path = get_unique_output_path(OUTPUT_DIRECTORY, "Filtered Build.txt")

        try:
            os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)  # Create the directory if it doesn't exist
        except OSError as e:
            print(f"Error creating output directory {OUTPUT_DIRECTORY}: {e}")
            return  # Stop if the directory cannot be created

        command_count = 0
        origin_x = box.min_x
        origin_y = box.min_y
        origin_z = box.min_z

        air_block = Block("minecraft", "air")
        self.groupedblocks = set()
        groupedblocks = self.groupedblocks

        def post_process_text(text):
                modified_lines = []  # Initialize the list
                inside_brackets = False
                i = 0
                while i < len(text):
                    char = text[i]
                    if char == '[':
                        modified_lines.append(char + '"')
                        inside_brackets = True
                    elif char == ']':
                        modified_lines.append(char)
                        inside_brackets = False
                    elif inside_brackets:
                        if char == '=':
                            modified_lines.append('"' + char)
                        elif char == ',':
                            modified_lines.append(char + '"')
                        elif char == '1' and i + 1 < len(text) and text[i + 1] == 'b':
                            modified_lines.append("true")
                            i += 1
                        elif char == '0' and i + 1 < len(text) and text[i + 1] == 'b':
                            modified_lines.append("false")
                            i += 1
                        else:
                            modified_lines.append(char)
                    else:
                        modified_lines.append(char)
                    i += 1
                modified_lines = ''.join(modified_lines).replace('""', '"').replace(':"', ':')
                return modified_lines


        with open(output_path, "w") as outfile:
            outfile.write("\n")

            for x in range(box.min_x, box.max_x):
                for y in range(box.min_y, box.max_y):
                    for z in range(box.min_z, box.max_z):
                        if (x, y, z) not in groupedblocks:
                            try:
                                block, _ = world.get_version_block(
                                    x, y, z, dimension, (world.level_wrapper.platform, world.level_wrapper.version)
                                )
                                if block is not None and (include_air or block != air_block):
                                    fill_coords = self.checkAround(x, y, z, world, dimension, box, include_air)
                                    if fill_coords:
                                        fx1, fy1, fz1, fx2, fy2, fz2 = fill_coords
                                        rel_fx1 = fx1 - origin_x
                                        rel_fy1 = fy1 - origin_y
                                        rel_fz1 = fz1 - origin_z
                                        rel_fx2 = fx2 - origin_x
                                        rel_fy2 = fy2 - origin_y
                                        rel_fz2 = fz2 - origin_z
                                        x_input = int(self.x_input.GetValue())  
                                        y_input = int(self.y_input.GetValue()) 
                                        z_input = int(self.z_input.GetValue())
                                        final_modified_text = post_process_text(f"fill ~{rel_fx1 + x_input} ~{rel_fy1 + y_input} ~{rel_fz1 + z_input} ~{rel_fx2 + x_input} ~{rel_fy2 + y_input} ~{rel_fz2 + z_input} {block}\n")
                                        outfile.write(final_modified_text)
                                        print(f"fill ~{rel_fx1 + x_input} ~{rel_fy1 + y_input } ~{rel_fz1 + z_input} ~{rel_fx2 + x_input} ~{rel_fy2 + y_input} ~{rel_fz2 + z_input} {block}")
                                        command_count += 1
                                    else:
                                        relative_x = x - origin_x
                                        relative_y = y - origin_y
                                        relative_z = z - origin_z
                                        x_input = int(self.x_input.GetValue())  
                                        y_input = int(self.y_input.GetValue()) 
                                        z_input = int(self.z_input.GetValue())
                                        final_modified_text = post_process_text(f"setblock ~{relative_x + x_input} ~{relative_y + y_input} ~{relative_z + z_input} {block}\n")
                                        outfile.write(final_modified_text)
                                        print(f"setblock ~{relative_x + x_input} ~{relative_y + y_input} ~{relative_z + z_input} {block}")
                                        command_count += 1
                                        groupedblocks.add((x,y,z)) # Mark as processed even if not part of fill
                                
                            except Exception as e:
                                print(f"Error getting block at {x}, {y}, {z}: {e}")

        print(f"Exported {command_count} relative block commands: \n{output_path}")
        print(TITLE+" Finished!")
        self._mode_description.SetValue("GTA's Amulent Filter 3.0" + f"\n\nCommand Count: {command_count} \n\nExported:\n\n{output_path}")

    def _run_filter(self, evt):
        if self.canvas.selection.selection_group:
            include_air = self.include_air_checkbox.GetValue()
            for box in self.canvas.selection.selection_group:
                self.findblocks(self.world, self.canvas.dimension, box, include_air)
        else:
            wx.MessageBox("Please make a selection before running the filter.", "Warning", wx.OK | wx.ICON_WARNING)

export = {"name": TITLE, "operation": GTAFilterOperation}