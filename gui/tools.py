"""
This module is where we put the helpers that are used by multiple other modules.
"""
import traceback
import os, sys
import tkinter as tk
import json
from tkinter import filedialog

class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """
    def __init__(self, widget, text='widget info'):
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
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

def read_txt(filename):
    try:
        with open(filename, 'r') as file:
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


def list_csv(directory,suffix=None):
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

    with open('params.config', 'r') as file:
        for line in file:
            key, value = line.strip().split(':', 1)
            params[key] = value.strip()

    # Step 2: Edit or update the dictionary
    params['host_size'] = '2000'  # Example: updating host_size
    params['Infection_rate'] = '0.04'  # Example: updating Infection_rate
    params['new_param'] = 'new_value'  # Example: adding a new parameter

    # Step 3: Write the updated dictionary back to the file
    with open('params.config', 'w') as file:
        for key, value in params.items():
            file.write(f"{key}:{value}\n")


def go_to_next_tab(tab_parent):
    current_tab_index = tab_parent.index(tab_parent.select())
    next_tab_index = (current_tab_index + 1) % tab_parent.index("end")
    tab_parent.select(next_tab_index)

def load_config_as_dict(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def save_config(config_path, config):
    with open(config_path, 'w') as file:
        json.dump(config, file, indent=4)

def update_nested_dict(d, keys, value):
    """
    Update a nested dictionary of arbitrary depth
    """
    if len(keys) == 1:
        d[keys[0]] = value
    else:
        update_nested_dict(d[keys[0]], keys[1:], value)

def update_list_int_params(entry, keys_path, config_path, prev_val = None, instance_name = ""):
    try:
        stripped_entry = entry.get().strip()
        cleaned_input = stripped_entry.strip("[]").strip()
        
        if cleaned_input == "":
            new_parsed = []
        elif cleaned_input.isdigit():
            new_parsed = [int(float(cleaned_input))]
        elif "," in stripped_entry:
            new_parsed = [int(float(item.strip())) for item in cleaned_input.split(',')]
        else:
            raise ValueError("Invalid input format.")
        
        config = load_config_as_dict(config_path)
        update_nested_dict(config, keys_path, new_parsed)
        save_config(config_path, config)

        # if new_parsed != prev_val:
            # setattr(self, keys_path[-1], new_parsed)
            # messagebox.showinfo("Success", "Updated successfully") 
        tk.messagebox.showinfo("Success", "Updated successfully") 
    except ValueError: # This catches cases where conversion to integer fails
        tk.messagebox.showerror("Update Error", "Please enter a valid list of numbers, separated by commas.")
    except Exception as e: # General error handling (e.g., file operation failures)
        tk.messagebox.showerror("Update Error", str(e))


string_to_bool_mapping = {
    "yes": True,
    "no": False,
    "Yes": True,
    "No": False
}

bool_to_string_mapping = {
    True: "Yes",
    False: "No"
}


def render_next_button(tab_index, tab_parent, parent, update = None):
    def next_tab():
        match update():
            case 1:
                return

        go_to_next_tab(tab_index, tab_parent)

            
    next_button = tk.ttk.Button(parent, text="Next",  command=next_tab)
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

def choose_ref_path(self, title, config_path, var, filetypes = None):  
    filetypes = ( #don't need to check if its genome file: or use python package jaehee said
        ("Genome files", ("*.fasta", "*.fa", "*.gb", "*.gtf", "*.vcf", "*.bam", "*.sam", "*.fna")),
        ("All files", "*.*")
    )
    # chosen_file = filedialog.askopenfilename(title="Select a Genome Reference File", filetypes=filetypes)
    chosen_file = filedialog.askopenfilename(title="Select a Genome Reference File")
    if chosen_file:  
        var = chosen_file
        # self.ref_path_label.config(text=self.ref_path) 
        config = load_config_as_dict(config_path)
        config['GenomeElement']['ref_path'] = var
        save_config(config_path, config)