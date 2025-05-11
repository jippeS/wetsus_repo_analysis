#!/usr/bin/env python3
import sys
import os


def check(pathway):
    if not os.path.exists(pathway):
        os.makedirs(pathway, exist_ok=True)
        print(f"De map '{pathway}' is aangemaakt.")
    else:
        print(f"De map '{pathway}' bestaat al.")


def create_main_folder(widgets, clear_output, display):
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
    dropdown_widget, text_box_widget = folder_selector(root_folder, widgets, clear_output, display)
    return dropdown_widget, text_box_widget


def chosen_folder(dropdown_widget, text_box_widget):
    if dropdown_widget.value == "Choose":
        sys.exit(print("Please choose a folder"))

    if dropdown_widget.value == "new_project":
        if text_box_widget.value != "":
            chosen_item = text_box_widget.value
        else:
            chosen_item = "new_project"
    else:
        chosen_item = dropdown_widget.value
    # Stuff for multiple places
    folder_path = f"drive/MyDrive/Wetsus_data_analysis/{chosen_item}/qiime_analysis"
    return folder_path


def upload_files(files, shutil, folder_path):
    uploaded = files.upload()  # User selects a file to upload
    filename = list(uploaded.keys())[0]
    shutil.move(filename, os.path.join(folder_path, filename))
    print(f"File '{filename}' has been moved to '{folder_path}'")

def naming_convention(folder_path, widgets):
    folder_path2 = folder_path + "/"
    directory_names = [name for name in os.listdir(folder_path2) if os.path.isdir(os.path.join(folder_path2, name))]
    folder_name = ""
    for directory_name in directory_names:
        folder_name = directory_name
    folder_name = f"{folder_name}"[0:-1]
    outputdir = folder_path + "/output"
    cores = 2

    # Create an "input bar" at the top
    input_box = widgets.Text(
        value='',
        placeholder='Enter a name for the output files...',
        description='Name:',
        layout=widgets.Layout(width='50%')
    )

    output_box = widgets.Output()

    def handle_submit(sender):
        with output_box:
            output_box.clear_output()
            print(f"You entered: {sender.value}")
            # Add your logic here for processing the input
            # For example, sending commands to a Minecraft server

    input_box.on_submit(handle_submit)

    # Display it nicely at the top
    display(input_box, output_box)

    return input_box, cores, outputdir, folder_name

def create_names(input_box):
    name_convention = input_box.value
    metadata = name_convention + "@metadata.txt"
    name_convention_PairEndSequences = name_convention + "_PairEndSequences.qza"

    print(input_box.value)
    print(name_convention_PairEndSequences)

    return name_convention, metadata, name_convention_PairEndSequences