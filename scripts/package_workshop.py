#!/usr/bin/env python3
import sys
import os

def create_main_folder(widgets, clear_output, display):
    def check(pathway):
        if not os.path.exists(pathway):
            os.makedirs(pathway, exist_ok=True)
            print(f"De map '{pathway}' is aangemaakt.")
        else:
            print(f"De map '{pathway}' bestaat al.")

    root_folder = "drive/MyDrive/Wetsus_data_analysis"
    check(root_folder)

    # Create dropdown + dynamic text input
    def folder_selector(base_dir, widgets, clear_output, display):
        folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f)) and not f.startswith(".ipynb")]
        folders.insert(0, "new_project")
        folders.insert(0, "Choose")

        dropdown = widgets.Dropdown(options=folders, description="Folder:")
        text_box = widgets.Text(
            value='',
            placeholder='Type new project name...',
            description='Input:',
            layout=widgets.Layout(width='50%')
        )
        output = widgets.Output()

        def on_dropdown_change(change):
            with output:
                clear_output()
                if change["new"] == "new_project":
                    display(text_box)

        dropdown.observe(on_dropdown_change, names='value')

        display(dropdown, output)
        return dropdown, text_box

    # Use the selector
    dropdown_widget, text_box_widget = folder_selector(root_folder, widgets)
    return dropdown_widget, text_box_widget