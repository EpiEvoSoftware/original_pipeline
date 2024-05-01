"""
This module is where we put the helpers that are used by multiple other modules.
"""

from PIL import Image, ImageTk
import traceback
import os, sys
import tkinter as tk
import json
from tkinter import filedialog


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text="widget info"):
        self.waittime = 500
        self.wraplength = 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20

        self.tw = tk.Toplevel(self.widget)

        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(
            self.tw,
            text=self.text,
            justify="left",
            background="#ffffff",
            relief="solid",
            borderwidth=1,
            wraplength=self.wraplength,
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


def read_txt(filename):
    try:
        with open(filename, "r") as file:
            print("success")
        #     lines = file.readlines()
        # # Process each line
        # for line in lines:
        #     # Assuming your data is comma-separated, split the line into parts
        #     parts = line.split(',')
        #     # Now you can process each part as needed
        #     print(parts)
    except FileNotFoundError:
        print("The directory does not exist.")
    except PermissionError:
        print("You don't have permission to access this directory.")
    except Exception as e:
        print(f"An error occurred: {e}")


def list_files(directory):
    """
    Prints out all the files in the specified directory.

    :param directory: The path to the directory to list files from.
    """
    try:
        for item in os.listdir(directory):
            full_path = os.path.join(directory, item)
            if os.path.isfile(full_path):
                print(item)
    except FileNotFoundError:
        print("The directory does not exist.")
    except PermissionError:
        print("You don't have permission to access this directory.")
    except Exception as e:
        print(f"An error occurred: {e}")


def data_for_file(filename):
    """
    Returns the 2-dimensional table for the given CSV file.

    CSV files should have a header with attributes.  The header COMMENTS is ignored.
    All other attributes are kept and should have numeric values.

    Parameter filename: The file to parse
    Precondition: filename is a name of a CSV file.
    """
    raise NotImplementedError("todo implement")


def list_csv(directory, suffix=None):
    """
    Returns the list of CSV files in a directory.

    The optional suffix attribute is used to separate 2d CSV files from other,
    more general files.

    Parameter directory: The directory path
    Precondition: directory is a string and valid path name

    Parameter suffix: The suffix BEFORE the .csv extension.
    Precondition: suffix is a string
    """
    raise NotImplementedError("todo implement")


def edit_params(dir):
    # Step 1: Read the file into a dictionary
    params = {}

    with open("params.config", "r") as file:
        for line in file:
            key, value = line.strip().split(":", 1)
            params[key] = value.strip()

    # Step 2: Edit or update the dictionary
    params["host_size"] = "2000"  # Example: updating host_size
    params["Infection_rate"] = "0.04"  # Example: updating Infection_rate
    params["new_param"] = "new_value"  # Example: adding a new parameter

    # Step 3: Write the updated dictionary back to the file
    with open("params.config", "w") as file:
        for key, value in params.items():
            file.write(f"{key}:{value}\n")


def go_to_next_tab(tab_parent):
    current_tab_index = tab_parent.index(tab_parent.select())
    next_tab_index = (current_tab_index + 1) % tab_parent.index("end")
    tab_parent.select(next_tab_index)


def load_config_as_dict(config_path):
    with open(config_path, "r") as file:
        return json.load(file)


def save_config(config_path, config):
    with open(config_path, "w") as file:
        json.dump(config, file, indent=4)


def update_nested_dict(d, keys, value):
    """
    Update a nested dictionary of arbitrary depth
    """
    if len(keys) == 1:
        d[keys[0]] = value
    else:
        update_nested_dict(d[keys[0]], keys[1:], value)


def update_list_int_params(
    entry, keys_path, config_path, prev_val=None, instance_name=""
):
    try:
        stripped_entry = entry.get().strip()
        cleaned_input = stripped_entry.strip("[]").strip()

        if cleaned_input == "":
            new_parsed = []
        elif cleaned_input.isdigit():
            new_parsed = [int(float(cleaned_input))]
        elif "," in stripped_entry:
            new_parsed = [int(float(item.strip())) for item in cleaned_input.split(",")]
        else:
            raise ValueError("Invalid input format.")

        config = load_config_as_dict(config_path)
        update_nested_dict(config, keys_path, new_parsed)
        save_config(config_path, config)

        # if new_parsed != prev_val:
        # setattr(self, keys_path[-1], new_parsed)
        # messagebox.showinfo("Success", "Updated successfully")
        tk.messagebox.showinfo("Success", "Updated successfully")
    except ValueError:  # This catches cases where conversion to integer fails
        tk.messagebox.showerror(
            "Update Error", "Please enter a valid list of numbers, separated by commas."
        )
    except Exception as e:  # General error handling (e.g., file operation failures)
        tk.messagebox.showerror("Update Error", str(e))


def update_list_int_params_v2(
    entry, keys_path, config_path, error_messages, render_text_short
):
    try:
        stripped_entry = entry.get().strip()
        cleaned_input = stripped_entry.strip("[]").strip()

        if cleaned_input == "":
            new_parsed = []
        elif cleaned_input.isdigit():
            new_parsed = [int(float(cleaned_input))]
        elif "," in stripped_entry:
            new_parsed = [int(float(item.strip())) for item in cleaned_input.split(",")]
        else:
            new_parsed = []
            error_messages.append(f"{render_text_short}: Invalid input format.")

        config = load_config_as_dict(config_path)
        update_nested_dict(config, keys_path, new_parsed)
        save_config(config_path, config)

        # if new_parsed != prev_val:
        # setattr(self, keys_path[-1], new_parsed)
        # messagebox.showinfo("Success", "Updated successfully")
    except ValueError:  # This catches cases where conversion to integer fails
        error_messages.append(
            f"{render_text_short}: Please enter a valid list of numbers, separated by commas."
        )
    except Exception as e:  # General error handling (e.g., file operation failures)
        error_messages.append(f"{render_text_short + ": Update Error, " + str(e)}")


string_to_bool_mapping = {"yes": True, "no": False, "Yes": True, "No": False}

bool_to_string_mapping = {True: "Yes", False: "No"}


def next_button(tab_index, tab_parent, parent, next_tab_fx):
    def next_tab():
        match update():
            case 1:
                return

        go_to_next_tab(tab_index, tab_parent)

    next_button = tk.ttk.Button(parent, text="Next", command=next_tab_fx)
    next_button.pack()


def render_next_button(tab_index, tab_parent, parent, update=None):
    def next_tab():
        match update():
            case 1:
                return

        go_to_next_tab(tab_index, tab_parent)

    next_button = tk.ttk.Button(parent, text="Next", command=next_tab)
    next_button.pack()


def go_to_next_tab(tab_index, tab_parent):
    current_tab_index = tab_index
    next_tab_index = (current_tab_index + 1) % tab_parent.index("end")
    tab_parent.tab(next_tab_index, state="normal")
    tab_parent.select(next_tab_index)


minwidth = 100


def validate_input(P):
    if P.strip() in ["e", ".", ""]:
        return True
    return P.isdigit()


def choose_ref_path(self, title, config_path, var, filetypes=None):
    filetypes = (  # don't need to check if its genome file: or use python package jaehee said
        (
            "Genome files",
            ("*.fasta", "*.fa", "*.gb", "*.gtf", "*.vcf", "*.bam", "*.sam", "*.fna"),
        ),
        ("All files", "*.*"),
    )
    # chosen_file = filedialog.askopenfilename(title="Select a Genome Reference File", filetypes=filetypes)
    chosen_file = filedialog.askopenfilename(title="Select a Genome Reference File")
    if chosen_file:
        var = chosen_file
        # self.ref_path_label.config(text=self.ref_path)
        config = load_config_as_dict(config_path)
        config["GenomeElement"]["ref_path"] = var
        save_config(config_path, config)


def no_validate_update(var, config_path, keys_path, mapping=None):
    if mapping:
        var_get = mapping[var.get()]
    else:
        var_get = var.get()
    config = load_config_as_dict(config_path)
    update_nested_dict(config, keys_path, var_get)
    save_config(config_path, config)


def no_validate_update_val(val, config_path, keys_path):
    config = load_config_as_dict(config_path)
    update_nested_dict(config, keys_path, val)
    save_config(config_path, config)


def get_dict_val(d, keys):
    for key in keys:
        d = d[key]
    return d


val_to_render_ui_wf_epi_mapping = {
    "user_input": "User Input",
    "SLiM_burnin_WF": "Burn-in by a Wright-Fisher Model",
    "SLiM_burnin_epi": "Burn-in by an Epidemiological Model",
}

render_to_val_ui_wf_epi_mapping = {
    value: key for key, value in val_to_render_ui_wf_epi_mapping.items()
}

ui_wf_epi_values = list(val_to_render_ui_wf_epi_mapping.values())
# ui_wf_epi_values = list(val_to_render_ui_wf_epi_mapping.keys())


def derender_components(components: set):
    grid_configs = {}
    for component in components:
        grid_configs[component] = component.grid_info()
        component.grid_forget()

    return grid_configs


def rerender_components(components: set, grid_configs: dict = {}):
    for component in components:
        grid_info = grid_configs.get(component, {})
        component.grid(**grid_info)


string_to_network_mode = {
    "ER": "Erdős–Rényi",
    "BA": "Barabási-Albert",
    "RP": "Random Partition",
}


network_model_to_string = {
    "Erdős–Rényi": "ER",
    "Barabási-Albert": "BA",
    "Random Partition": "RP",
}

graph_values = list(network_model_to_string.keys())

val_to_render_generate_genetic_architecture_method = {
    "user_input": "User Input",
    "randomly_generate": "Random Generation from the GFF file",
}

render_to_val_generate_genetic_architecture_method = {
    value: key
    for key, value in val_to_render_generate_genetic_architecture_method.items()
}

generate_genetic_architecture_method_values = list(
    val_to_render_generate_genetic_architecture_method.values()
)


def render_path_select(
    keys_path, config_path, render_text, control_frame, column, frow
):
    """
    Renders a path select component in the GUI.
    depreciated, replace with EasyPathSelect
    """

    def update():
        chosen_file = filedialog.askopenfilename(title="Select a File")
        if chosen_file:
            no_validate_update_val(chosen_file, config_path, keys_path)
            value_label.config(text=chosen_file)

    dict_var = get_dict_val(load_config_as_dict(config_path), keys_path)
    label = tk.ttk.Label(control_frame, text=render_text, style="Bold.TLabel")

    if dict_var == "":
        value_label = tk.ttk.Label(
            control_frame, text="None selected", foreground="black"
        )
    else:
        value_label = tk.ttk.Label(control_frame, text=dict_var, foreground="black")

    button = tk.Button(control_frame, text="Choose File", command=update)

    if frow is None or column is None:
        label.grid()
        value_label.grid()
        button.grid()
    else:
        label.grid(row=frow, column=column, sticky="w", pady=5)
        value_label.grid(row=frow + 1, column=column, sticky="w", pady=5)
        button.grid(row=frow + 2, column=column, sticky="e", pady=5)

    local_components = {label, value_label, button}
    grid_layout = derender_components(local_components)
    rerender_components(local_components, grid_layout)

    def updater():
        return None

    def rerenderer():
        rerender_components(local_components, grid_layout)

    def derenderer():
        derender_components(local_components)

    controls = {"updater": updater, "rerenderer": rerenderer, "derenderer": derenderer}

    return controls


def update_numerical_input(
    entry, keys_path, config_path, error_messages, render_text_short, is_int
):
    try:
        # print("entry.get()",  entry.get())
        new_val = int(float(entry.get()))
        config = load_config_as_dict(config_path)
        update_nested_dict(config, keys_path, new_val)
        save_config(config_path, config)
    except ValueError:  # This catches cases where conversion to integer fails
        if is_int:
            valtype = "integer"
        else:
            valtype = "numerical"
        error_messages.append(
            f"{render_text_short}: Please enter a valid {valtype} value."
        )
    except Exception as e:  # General error handling (e.g., file operation failures)
        error_messages.append(f"{render_text_short + ": Update Error, " + str(e)}")


def render_numerical_input(
    keys_path, config_path, render_text, control_frame, column, frow, internal_type
):
    """
    depreciated
    """
    dict_var = get_dict_val(load_config_as_dict(config_path), keys_path)
    label = tk.ttk.Label(control_frame, text=render_text, style="Bold.TLabel")
    entry = tk.ttk.Entry(control_frame, foreground="black")
    entry.insert(0, str(dict_var))

    if frow is None or column is None:
        label.grid()
        entry.grid()
    else:
        label.grid(row=frow, column=column, sticky="w", pady=5)
        entry.grid(row=frow + 1, column=column, sticky="w", pady=5)

    local_components = {entry, label}
    grid_layout = derender_components(local_components)
    rerender_components(local_components, grid_layout)

    if internal_type == "list":

        def updater(error_messages, render_text_short):
            update_list_int_params_v2(
                entry, keys_path, config_path, error_messages, render_text_short
            )
    elif internal_type == "integer":

        def updater(error_messages, render_text_short):
            update_numerical_input(
                entry, keys_path, config_path, error_messages, render_text_short, True
            )
    elif internal_type == "numerical":

        def updater(error_messages, render_text_short):
            update_numerical_input(
                entry, keys_path, config_path, error_messages, render_text_short, False
            )
    else:
        raise ValueError("Invalid internal type.")

    def rerenderer():
        rerender_components(local_components, grid_layout)

    def derenderer():
        derender_components(local_components)

    controls = {"updater": updater, "rerenderer": rerenderer, "derenderer": derenderer}

    return controls


def render_rb(
    keys_path,
    config_path,
    render_text,
    control_frame,
    column,
    frow,
    rerenderer,
    derenderer,
):
    """
    depreciated
    """

    def update():
        no_validate_update(var, config_path, keys_path)
        if var.get():
            rerenderer()
            # print("use_genetic_model_local: ", dict_var)
            # self.use_method_grid_configs = derender_components(self.use_method_components)
            # self.user_input_grid_configs = derender_components(self.user_input_components)
            # self.wf_grid_configs = derender_components(self.wf_components)
            # self.epi_grid_configs = derender_components(self.epi_components)
        else:
            derenderer()
            # print("use_genetic_model_local: ", dict_var)
            # rerender_components(self.use_method_components, self.use_method_grid_configs)
            # rerender_components(self.user_input_components, self.user_input_grid_configs)
            # keys_path = ['SeedsConfiguration', 'method']
            # use_method_local = get_dict_val(load_config_as_dict(self.config_path), keys_path)
            # match use_method_local:
            #     case "user_input":
            #         rerender_components(self.user_input_components, self.user_input_grid_configs)
            #     case "SLiM_burnin_WF":
            #         rerender_components(self.wf_components, self.wf_grid_configs)
            #     case "SLiM_burnin_epi":
            #         rerender_components(self.epi_components, self.epi_grid_configs)

    dict_var = get_dict_val(load_config_as_dict(config_path), keys_path)
    var = tk.BooleanVar(value=dict_var)
    label = tk.ttk.Label(control_frame, text=render_text, style="Bold.TLabel")
    rb_true = tk.ttk.Radiobutton(
        control_frame, text="Yes", variable=var, value=True, command=update
    )
    rb_false = tk.ttk.Radiobutton(
        control_frame, text="No", variable=var, value=False, command=update
    )
    if frow is None or column is None:
        label.grid()
        rb_true.grid()
        rb_false.grid()
    else:
        label.grid(row=frow, column=column, sticky="w", pady=5)
        rb_true.grid(row=frow + 1, column=column, sticky="w", pady=5)
        rb_false.grid(row=frow + 2, column=column, sticky="w", pady=5)

    local_components = {label, rb_true, rb_false}
    grid_layout = derender_components(local_components)
    rerender_components(local_components, grid_layout)

    def local_rerenderer():
        rerender_components(local_components, grid_layout)

    def local_derenderer():
        derender_components(local_components)

    controls = {
        "updater": None,
        "rerenderer": local_rerenderer,
        "derenderer": local_derenderer,
    }

    return controls


class EasyWidgetBase:
    def __init__(self):
        self.local_components = set()
        self.grid_layout = None

    def rerender_itself(self):
        rerender_components(self.local_components, self.grid_layout)

    def derender_itself(self):
        derender_components(self.local_components)

    def set_to_rerender(self, to_rerender):
        self.to_rerender = to_rerender

    def set_to_derender(self, to_derender):
        self.to_derender = to_derender

    def update(self, error_messages):
        pass


class EasyTitle(EasyWidgetBase):
    def __init__(
        self, render_text, control_frame, column, frow, hide, columnspan=1, sticky="we"
    ) -> None:
        super().__init__()
        self.render_text = render_text
        self.label = tk.ttk.Label(
            control_frame, text=self.render_text, style="Title.TLabel"
        )
        if frow is None or column is None:
            self.label.grid()
        else:
            self.label.grid(
                row=frow, column=column, columnspan=columnspan, sticky=sticky, pady=5
            )

        self.local_components = {self.label}
        self.grid_layout = derender_components(self.local_components)
        if not hide:
            rerender_components(self.local_components, self.grid_layout)


class EasyLabel(EasyWidgetBase):
    def __init__(
        self, render_text, control_frame, column, frow, hide, columnspan=1, sticky="w"
    ) -> None:
        super().__init__()
        self.render_text = render_text
        self.label = tk.ttk.Label(
            control_frame, text=self.render_text, style="Bold.TLabel"
        )
        if frow is None or column is None:
            self.label.grid()
        else:
            self.label.grid(
                row=frow, column=column, columnspan=columnspan, sticky=sticky, pady=5
            )

        self.local_components = {self.label}
        self.grid_layout = derender_components(self.local_components)
        if not hide:
            rerender_components(self.local_components, self.grid_layout)


class EasyButton(EasyWidgetBase):
    def __init__(
        self, render_text, control_frame, column, frow, command, hide, sticky="e"
    ) -> None:
        super().__init__()
        self.render_text = render_text
        self.button = tk.Button(control_frame, text=self.render_text, command=command)
        if frow is None or column is None:
            self.button.grid()
        else:
            self.button.grid(row=frow, column=column, sticky=sticky, pady=5)

        self.local_components = {self.button}
        self.grid_layout = derender_components(self.local_components)
        if not hide:
            rerender_components(self.local_components, self.grid_layout)


class EasyEntry(EasyWidgetBase):
    """
    replaces render_numerical_input
    """

    def __init__(
        self,
        keys_path,
        config_path,
        render_text,
        render_text_short,
        control_frame,
        column,
        frow,
        validate_for,
        hide,
        columnspan,
    ) -> None:
        super().__init__()
        self.keys_path = keys_path
        self.config_path = config_path
        self.render_text_short = render_text_short
        self.validate_for = validate_for
        dict_var = get_dict_val(load_config_as_dict(config_path), keys_path)
        label = tk.ttk.Label(control_frame, text=render_text, style="Bold.TLabel")
        self.entry = tk.ttk.Entry(control_frame, foreground="black")
        self.entry.insert(0, str(dict_var))

        if frow is None or column is None:
            label.grid()
            self.entry.grid()
        else:
            label.grid(
                row=frow, column=column, columnspan=columnspan, sticky="w", pady=5
            )
            self.entry.grid(
                row=frow + 1, column=column, columnspan=columnspan, sticky="w", pady=5
            )

        self.local_components = {self.entry, label}
        self.grid_layout = derender_components(self.local_components)
        if not hide:
            rerender_components(self.local_components, self.grid_layout)

    def update(self, error_messages):
        match self.validate_for:
            case "list":
                update_list_int_params_v2(
                    self.entry,
                    self.keys_path,
                    self.config_path,
                    error_messages,
                    self.render_text_short,
                )
            case "integer":
                update_numerical_input(
                    self.entry,
                    self.keys_path,
                    self.config_path,
                    error_messages,
                    self.render_text_short,
                    True,
                )
            case "numerical":
                update_numerical_input(
                    self.entry,
                    self.keys_path,
                    self.config_path,
                    error_messages,
                    self.render_text_short,
                    False,
                )
            case _:
                raise ValueError("Invalid internal type.")


class EasyRadioButton(EasyWidgetBase):
    """
    replaces render_rb
    """

    def __init__(
        self,
        keys_path,
        config_path,
        render_text,
        render_text_short,
        control_frame,
        column,
        frow,
        hide,
        to_rerender,
        to_derender,
        columnspan,
        radiobuttonselected,
    ) -> None:
        super().__init__()
        self.keys_path = keys_path
        self.config_path = config_path
        self.render_text_short = render_text_short
        self.to_rerender = to_rerender
        self.to_derender = to_derender
        self.radiobuttonselected = radiobuttonselected

        dict_var = get_dict_val(load_config_as_dict(config_path), keys_path)
        self.var = tk.BooleanVar(value=dict_var)
        label = tk.ttk.Label(control_frame, text=render_text, style="Bold.TLabel")
        self.rb_true = tk.ttk.Radiobutton(
            control_frame,
            text="Yes",
            variable=self.var,
            value=True,
            command=self._updater,
        )
        self.rb_false = tk.ttk.Radiobutton(
            control_frame,
            text="No",
            variable=self.var,
            value=False,
            command=self._updater,
        )
        if frow is None or column is None:
            label.grid()
            self.rb_true.grid()
            self.rb_false.grid()
        else:
            label.grid(
                row=frow, column=column, columnspan=columnspan, sticky="w", pady=5
            )
            self.rb_true.grid(row=frow + 1, column=column, sticky="w", pady=5)
            self.rb_false.grid(row=frow + 2, column=column, sticky="w", pady=5)

        self.local_components = {label, self.rb_true, self.rb_false}
        self.grid_layout = derender_components(self.local_components)
        if not hide:
            rerender_components(self.local_components, self.grid_layout)

    def _updater(self):
        self.radiobuttonselected(self.var, self.to_rerender, self.to_derender)
        # if self.to_derender is not None:
        #     self.to_derender()
        # if self.to_rerender is not None:
        #     self.to_rerender()

    def update_rb_false_text(self, new_text):
        """Updates the text of the rb_false radiobutton."""
        self.rb_false.config(text=new_text)


class EasyPathSelector(EasyWidgetBase):
    def __init__(
        self,
        keys_path,
        config_path,
        render_text,
        control_frame,
        column,
        hide,
        frow,
        columnspan,
        filetype=None,
        tooltip="",
    ):
        """
        Replaces render_path_select
        """
        super().__init__()
        self.filetype = filetype
        self.keys_path = keys_path
        self.config_path = config_path

        dict_var = get_dict_val(load_config_as_dict(config_path), keys_path)
        label = tk.ttk.Label(control_frame, text=render_text, style="Bold.TLabel")
        CreateToolTip(label, tooltip)

        if dict_var == "":
            self.value_label = tk.ttk.Label(
                control_frame, text="None selected", foreground="black"
            )
        else:
            self.value_label = tk.ttk.Label(
                control_frame, text=dict_var, foreground="black"
            )

        button = tk.Button(control_frame, text="Choose File", command=self._update)

        if frow is None or column is None:
            label.grid()
            self.value_label.grid()
            button.grid()
        else:
            label.grid(
                row=frow, column=column, columnspan=columnspan, sticky="w", pady=5
            )
            self.value_label.grid(
                row=frow + 1, column=column, columnspan=columnspan, sticky="w", pady=5
            )
            button.grid(
                row=frow + 2, column=column, columnspan=columnspan, sticky="e", pady=5
            )

        self.local_components = {label, self.value_label, button}
        self.grid_layout = derender_components(self.local_components)
        if not hide:
            rerender_components(self.local_components, self.grid_layout)

    def _update(self):
        if self.filetype is None:
            chosen_file = filedialog.askopenfilename(title="Select a File")
        else:
            chosen_file = filedialog.askopenfilename(
                title="Select a File", filetypes=self.filetype
            )

        if chosen_file:
            no_validate_update_val(chosen_file, self.config_path, self.keys_path)
            self.value_label.config(text=chosen_file)


class EasyCombobox(EasyWidgetBase):
    def __init__(
        self,
        keys_path,
        config_path,
        render_text,
        control_frame,
        column,
        frow,
        combobox_values,
        to_rerender,
        to_derender,
        comboboxselected,
        hide,
        width,
        columnnspan,
        val_to_ui_mapping=None,
    ):
        super().__init__()
        self.keys_path = keys_path
        self.config_path = config_path
        self.control_frame = control_frame
        self.to_derender = to_derender
        self.to_rerender = to_rerender
        self.val_to_ui_mapping = val_to_ui_mapping
        self.comboboxselected = comboboxselected

        self.label = tk.ttk.Label(
            self.control_frame, text=render_text, style="Bold.TLabel"
        )
        dict_var = get_dict_val(load_config_as_dict(config_path), keys_path)

        if val_to_ui_mapping is None:
            var_val = dict_var
        else:
            var_val = val_to_ui_mapping.get(dict_var, "")
            # print("var_val", var_val)

        self.var = tk.StringVar(value=var_val)
        self.combobox = tk.ttk.Combobox(
            self.control_frame,
            textvariable=self.var,
            values=combobox_values,
            state="readonly",
            width=width,
        )
        self.combobox.bind("<<ComboboxSelected>>", self._updater)

        if frow is None or column is None:
            self.label.grid()
            self.combobox.grid()
        else:
            self.label.grid(
                row=frow, column=column, columnspan=columnnspan, sticky="w", pady=5
            )
            self.combobox.grid(
                row=frow + 1, column=column, columnspan=columnnspan, sticky="w", pady=5
            )

        self.local_components = {self.label, self.combobox}
        self.grid_layout = derender_components(self.local_components)
        if not hide:
            rerender_components(self.local_components, self.grid_layout)

    def _updater(self, event):
        self.comboboxselected(self.var, self.to_rerender, self.to_derender)
        self.comboboxselected(self.var, self.to_rerender, self.to_derender)


class GroupControls:
    def __init__(self, items=None):
        self.items = items if items is not None else []

    def add(self, item):
        if isinstance(item, EasyWidgetBase) or isinstance(item, GroupControls):
            self.items.append(item)
        # elif isinstance(item, list):
        #     for subitem in item:
        #         self.add(subitem)
        else:
            raise ValueError(
                "Item must be an instance of EasyWidgetBase or GroupControls"
            )

    def rerender_itself(self):
        for item in self.items:
            item.rerender_itself()

    def derender_itself(self):
        for item in self.items:
            item.derender_itself()

    def to_rerender(self):
        for item in self.items:
            item.to_rerender()

    def to_derender(self):
        for item in self.items:
            # print("group control derending", item)
            item.to_derender()


class TabBase2:
    def __init__(
        self, parent, tab_parent, config_path, tab_title, tab_index, hide=False
    ):
        self.visible_components = set()
        self.init_val(config_path)
        self.init_tab(parent, tab_parent, tab_title, tab_index, hide)
        self.load_page()
        render_next_button(
            self.tab_index, self.tab_parent, self.parent, self.global_update
        )

    def init_val(self, config_path):
        pass

    def load_page(self):
        pass

    def global_update(self):
        users_validation_messages = []

        for component in self.visible_components:
            component.update(users_validation_messages)

        match len(users_validation_messages):
            case 0:
                #        tk.messagebox.showinfo("Update Successful", "Parameters Updated.")
                return 0
            case _:
                error_message_str = "\n\n".join(users_validation_messages)
                tk.messagebox.showerror("Update Error", error_message_str)
                return 1

    def global_update_no_success_message(self):
        users_validation_messages = []

        for component in self.visible_components:
            component.update(users_validation_messages)

        match len(users_validation_messages):
            case 0:
                return 0
            case _:
                error_message_str = "\n\n".join(users_validation_messages)
                tk.messagebox.showerror("Update Error", error_message_str)
                return 1

    def init_tab(self, parent, tab_parent, tab_title, tab_index, hide):
        self.parent = parent
        self.tab_parent = tab_parent
        self.tab_index = tab_index
        self.tab_parent.add(parent, text=tab_title)
        if hide:
            self.tab_parent.tab(self.tab_index, state="disabled")
        self.control_frame = tk.ttk.Frame(self.parent, width=300)
        self.control_frame.pack(padx=10, pady=10)


class TabBase:
    def __init__(
        self,
        parent,
        tab_parent,
        config_path,
        tab_title,
        tab_index,
        hide=False,
        render_nb=True,
    ):
        self.render_nb = render_nb
        self.visible_components = set()
        self.init_val(config_path)
        self.init_tab(parent, tab_parent, tab_title, tab_index, hide)
        self.load_page()
        if self.render_nb:
            render_next_button(
                self.tab_index, self.tab_parent, self.parent, self.global_update
            )

    def init_val(self, config_path):
        pass

    def load_page(self):
        pass

    def global_update(self):
        users_validation_messages = []

        for component in self.visible_components:
            component.update(users_validation_messages)

        match len(users_validation_messages):
            case 0:
                # tk.messagebox.showinfo("Update Successful", "Parameters Updated.")
                return 0
            case _:
                error_message_str = "\n\n".join(users_validation_messages)
                tk.messagebox.showerror("Update Error", error_message_str)
                return 1

    def global_update_no_success_message(self):
        users_validation_messages = []

        for component in self.visible_components:
            component.update(users_validation_messages)

        match len(users_validation_messages):
            case 0:
                return 0
            case _:
                error_message_str = "\n\n".join(users_validation_messages)
                tk.messagebox.showerror("Update Error", error_message_str)
                return 1

    def init_tab(self, parent, tab_parent, tab_title, tab_index, hide):
        self.parent = parent
        self.tab_parent = tab_parent
        self.tab_index = tab_index
        self.tab_parent.add(parent, text=tab_title)
        if hide:
            self.tab_parent.tab(self.tab_index, state="disabled")
        self.control_frame = tk.ttk.Frame(self.parent, width=300)
        self.control_frame.pack(padx=10, pady=10)


class EasyImage(EasyWidgetBase):
    def __init__(
        self,
        image_path,
        desired_width,
        desired_height,
        hide,
        control_frame,
        frow,
        column,
        columnspan,
        rowspan,
    ):
        with Image.open(image_path) as img:
            img = img.resize((desired_width, desired_height))
            self.photo = ImageTk.PhotoImage(img)
            image_label = tk.Label(control_frame, image=self.photo)

            if frow is None or column is None:
                image_label.grid()
            else:
                image_label.grid(
                    column=column,
                    row=frow,
                    columnspan=columnspan,
                    rowspan=rowspan,
                    sticky="nsew",
                )

            self.local_components = {image_label}
            self.grid_layout = derender_components(self.local_components)
            if not hide:
                rerender_components(self.local_components, self.grid_layout)
