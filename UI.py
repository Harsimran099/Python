from owlready2 import get_ontology
from tkinter import Tk, Label, Button, Listbox, Scrollbar, VERTICAL, RIGHT, Y, Frame, TOP, X, LEFT, BOTH
from tkinter import ttk

# Load the ontology
ontology_file = "Chemistry_ITS.owl"  # RDF/XML format
ontology = get_ontology(ontology_file).load()

# Global variable to track the selected category
selected_category = None

# Function to fetch top-level classes
def fetch_classes():
    global selected_category
    selected_category = "classes"  # Set the category to classes
    listbox.delete(0, "end")  # Clear the listbox
    for cls in ontology.classes():
        # Only show direct subclasses of Thing (top-level classes)
        if "Thing" in [str(parent.name) for parent in cls.is_a]:
            listbox.insert("end", f"Class: {cls.name}")

# Function to fetch subclasses only
def fetch_subclasses():
    global selected_category
    selected_category = "subclasses"  # Set the category to subclasses
    listbox.delete(0, "end")  # Clear the listbox
    for cls in ontology.classes():
        # Exclude direct subclasses of Thing (i.e., show only deeper subclasses)
        if "Thing" not in [str(parent.name) for parent in cls.is_a]:
            listbox.insert("end", f"Subclass: {cls.name}")

# Function to fetch individuals
def fetch_individuals():
    global selected_category
    selected_category = "individuals"  # Set the category to individuals
    listbox.delete(0, "end")  # Clear the listbox
    for individual in ontology.individuals():
        listbox.insert("end", f"Individual: {individual.name}")

# Function to fetch object properties
def fetch_object_properties():
    global selected_category
    selected_category = "object_properties"  # Set the category to object properties
    listbox.delete(0, "end")  # Clear the listbox
    for prop in ontology.object_properties():
        listbox.insert("end", f"Object Property: {prop.name}")

# Function to fetch data properties
def fetch_data_properties():
    global selected_category
    selected_category = "data_properties"  # Set the category to data properties
    listbox.delete(0, "end")  # Clear the listbox
    for prop in ontology.data_properties():
        listbox.insert("end", f"Data Property: {prop.name}")

# Function to display the properties of the selected individual
def show_individual_properties(event):
    if selected_category != "individuals":  # Only trigger if the category is individuals
        return

    selected_index = listbox.curselection()  # Get the selected item index
    if not selected_index:
        return  # If nothing is selected, do nothing
    
    selected_name = listbox.get(selected_index).split(": ")[1]  # Extract the name of the individual
    try:
        # Fetch the individual from the ontology
        individual = getattr(ontology, selected_name)

        # Create the information string
        info = f"Properties of {individual.name}:\n"
        
        # Get data properties
        for prop in individual.get_properties():
            values = getattr(individual, prop.name, [])
            for value in values:
                info += f"{prop.name}: {value}\n"
        
        # Update the result label with the individual properties
        result_label.config(text=info)
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")

# Build the enhanced UI
root = Tk()
root.title("Chemistry Ontology Viewer")
root.geometry("800x650")
root.configure(bg="#f2f2f2")  # Light gray background for better readability

# Header Label
header = Label(
    root,
    text="Chemistry Ontology Viewer",
    font=("Helvetica", 22, "bold"),
    fg="#E9EED9",
    bg="#85A98F",
    pady=20
)
header.pack(fill=X)

# Frame for buttons
button_frame = Frame(root, bg="#FFF4B7", pady=15)
button_frame.pack(fill=X, padx=10)

# Styled Buttons
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=6)

class_button = ttk.Button(
    button_frame, text="Show Classes", style="TButton", command=fetch_classes
)
class_button.pack(side=LEFT, padx=10)

subclass_button = ttk.Button(
    button_frame, text="Show Subclasses", style="TButton", command=fetch_subclasses
)
subclass_button.pack(side=LEFT, padx=10)

individual_button = ttk.Button(
    button_frame, text="Show Individuals", style="TButton", command=fetch_individuals
)
individual_button.pack(side=LEFT, padx=10)

object_prop_button = ttk.Button(
    button_frame, text="Show Object Properties", style="TButton", command=fetch_object_properties
)
object_prop_button.pack(side=LEFT, padx=10)

data_prop_button = ttk.Button(
    button_frame, text="Show Data Properties", style="TButton", command=fetch_data_properties
)
data_prop_button.pack(side=LEFT, padx=10)

# Frame for listbox
listbox_frame = Frame(root, bg="#f2f2f2")
listbox_frame.pack(fill=BOTH, expand=True, padx=15, pady=10)

# Scrollbar and Listbox
scrollbar = Scrollbar(listbox_frame, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

listbox = Listbox(
    listbox_frame,
    yscrollcommand=scrollbar.set,
    font=("Courier", 12),
    bg="#ffffff",  # White background for listbox
    fg="#333333",  # Dark gray text
    height=15,
    selectbackground="#608BC1",  # Blue color for selection
    selectforeground="white",
    borderwidth=2,
    relief="solid"  # Solid border for listbox
)
listbox.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.config(command=listbox.yview)

# Bind the click event to the Listbox (on individual click)
listbox.bind("<ButtonRelease-1>", show_individual_properties)

# Result Label for showing selected individual's properties
result_label = Label(root, text="", font=("Arial", 12), bg="#f2f2f2", anchor="w", justify="left")
result_label.pack(fill=BOTH, padx=15, pady=10)

# Footer Label
footer = Label(
    root,
    text="Ontology Viewer",
    font=("Arial", 10),
    bg="#85A98F",
    fg="white",
    pady=10
)
footer.pack(fill=X)

# Run the application
root.mainloop()