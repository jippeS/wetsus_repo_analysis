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
    check(folder_path)
    return folder_path


def upload_files(files, shutil, folder_path):
    uploaded = files.upload()  # User selects a file to upload
    filename = list(uploaded.keys())[0]
    shutil.move(filename, os.path.join(folder_path, filename))
    print(f"File '{filename}' has been moved to '{folder_path}'")

def naming_convention(folder_path, widgets):
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

    return input_box, cores, outputdir

def create_names(input_box):
    name_convention = input_box.value
    metadata = name_convention + "@metadata.txt"
    name_convention_PairEndSequences = name_convention + "_PairEndSequences.qza"

    print(input_box.value)
    print(name_convention_PairEndSequences)

    return name_convention, metadata, name_convention_PairEndSequences

def return_primers():
    """
    # https://lutzonilab.org/16s-ribosomal-dna/ : 27F, 8F, , 515F, 1492R
    # https://earthmicrobiome.org/protocols-and-standards/16s/ : 515F-Y, 806R
    # https://www.researchgate.net/publication/382628589_The_formation_of_sulfur_metabolites_during_in_vitro_gastrointestinal_digestion_of_fish_white_and_red_meat_is_affected_by_the_addition_of_fructo-oligosaccharides/fulltext/66a63fc375fcd863e5e28168/The-formation-of-sulfur-metabolites-during-in-vitro-gastrointestinal-digestion-of-fish-white-and-red-meat-is-affected-by-the-addition-of-fructo-oligosaccharides.pdf : 341F
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC4865482/ : 799F, 1193R
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC4040986/ : 926F
    # https://www.researchgate.net/publication/315754509_Comparative_Evaluation_of_Four_Bacteria-Specific_Primer_Pairs_for_16S_rRNA_Gene_Surveys : 785R
    # https://pmc.ncbi.nlm.nih.gov/articles/PMC4228914/ : 1387R
    :return:
    """
    forward_primers = {
        "27F": "AGAGTTTGATCMTGGCTCAG",
        "8F": "AGAGTTTGATCCTGGCTCAG",
        "341F": "CCTACGGGNGGCWGCAG",
        "515F": "GTGCCAGCMGCCGCGGTAA",
        "515F-Y": "GTGYCAGCMGCCGCGGTAA",
        "799F": "AACMGGATTAGATACCCKG",
        "926F": "AAACTYAAAKGAATTGRCGG"}

    reverse_primers = {
        "1492R": "GGTTACCTTGTTACGACTT",
        "785R": "GACTACHVGGGTATCTAATCC",
        "806R": "GGACTACHVGGGTWTCTAAT",
        "926R": "CCGYCAATTYMTTTRAGTTT",
        "1193R": "ACGTCATCCCCACCTTCC",
        "1387R": "GGGCGGWGTGTACAAGGC"}

    return forward_primers, reverse_primers


def create_first_dropdown_primers(widgets):
    forward_primers, reverse_primers = return_primers()
    def create_dropdown_with_new_project(dictionary, label):
        options = list(dictionary.keys())
        options.insert(0, "new_primer")
        options.insert(0, "Choose")
        return widgets.Dropdown(options=options, description=label)

    def create_name_and_sequence_inputs(label_prefix):
        name_input = widgets.Text(
            placeholder='Primer name',
            description=f'{label_prefix} Name:',
            layout=widgets.Layout(width='50%')
        )
        sequence_input = widgets.Text(
            placeholder='Primer sequence',
            description=f'{label_prefix} Seq:',
            layout=widgets.Layout(width='50%')
        )
        return name_input, sequence_input

    dic_1 = {"forward_dropdown": create_dropdown_with_new_project(forward_primers, "Forward:"),
             "forward_name_input": (create_name_and_sequence_inputs("Forward"))[0],
             "forward_seq_input": (create_name_and_sequence_inputs("Forward"))[1],
             "reverse_dropdown": create_dropdown_with_new_project(reverse_primers, "Reverse:"),
             "reverse_name_input": (create_name_and_sequence_inputs("Reverse"))[0],
             "reverse_seq_input": (create_name_and_sequence_inputs("Reverse"))[1], "forward_output": widgets.Output(),
             "reverse_output": widgets.Output()}
    # Widgets for forward primers

    # Widgets for reverse primers

    # Output areas for conditional input

    return dic_1

def primer_dropdown(dic_1, display, clear_output):
    forward_output = dic_1["forward_output"]
    forward_name_input = dic_1["forward_name_input"]
    forward_seq_input = dic_1["forward_seq_input"]
    forward_dropdown = dic_1["forward_dropdown"]

    reverse_output = dic_1["reverse_output"]
    reverse_name_input = dic_1["reverse_name_input"]
    reverse_seq_input = dic_1["reverse_seq_input"]
    reverse_dropdown = dic_1["reverse_dropdown"]

    def on_forward_change(change):
        with forward_output:
            clear_output()
            if change["new"] == "new_primer":
                display(forward_name_input, forward_seq_input)

    def on_reverse_change(change):
        with reverse_output:
            clear_output()
            if change["new"] == "new_primer":
                display(reverse_name_input, reverse_seq_input)

    # Attach observers
    forward_dropdown.observe(on_forward_change, names='value')
    reverse_dropdown.observe(on_reverse_change, names='value')

    # Display all widgets
    display(forward_dropdown, forward_output)
    display(reverse_dropdown, reverse_output)

    dic_primer_output = {"forward_dropdown": forward_dropdown, "forward_name_input": forward_name_input,
                         "forward_seq_input": forward_seq_input, "reverse_dropdown": reverse_dropdown,
                         "reverse_name_input": reverse_name_input, "reverse_seq_input": reverse_seq_input}

    return dic_primer_output

def check_string(String_value, input_name, input_seq):
  if String_value == "Choose":
    sys.exit(print("Please choose a primer"))

  if String_value == "new_primer":
    if input_name.value == "":
      sys.exit(print("Please enter a name"))
    if input_seq.value == "":
      sys.exit(print("Please enter a sequence"))

def finalize_primers(dic_primer_output):

    forward_primers, reverse_primers = return_primers()

    forward_dropdown = dic_primer_output["forward_dropdown"]
    forward_name_input = dic_primer_output["forward_name_input"]
    forward_seq_input = dic_primer_output["forward_seq_input"]
    reverse_dropdown = dic_primer_output["reverse_dropdown"]
    reverse_name_input = dic_primer_output["reverse_name_input"]
    reverse_seq_input = dic_primer_output["reverse_seq_input"]

    check_string(forward_dropdown.value, forward_name_input, forward_seq_input)
    check_string(reverse_dropdown.value, reverse_name_input, reverse_seq_input)

    if forward_dropdown.value == "Choose" or reverse_dropdown.value == "Choose" or forward_seq_input == None or forward_name_input == None:
        sys.exit(print("Please choose a primer"))

    if forward_dropdown.value == "new_primer":
        forward_primer = forward_name_input.value
        forward_primer_seq = forward_seq_input.value.upper()
    else:
        forward_primer = forward_dropdown.value
        forward_primer_seq = forward_primers[forward_dropdown.value]

    if reverse_dropdown.value == "new_primer":
        reverse_primer = reverse_name_input.value
        reverse_primer_seq = reverse_seq_input.value.upper()
    else:
        reverse_primer = reverse_dropdown.value
        reverse_primer_seq = reverse_primers[reverse_dropdown.value]

    print(f"Chosen forward primer: {forward_primer}: {forward_primer_seq}")
    print(f"Chosen reverse primer: {reverse_primer}: {reverse_primer_seq}")

    return forward_primer_seq, reverse_primer_seq