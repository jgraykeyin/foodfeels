import tkinter as tk
from datetime import date
from tkinter.messagebox import showinfo

# Saving the current date, we'll sort our journal entries by the day they're recorded
current_date = date.today()

window = tk.Tk()
window.title("Food Feels")

def save_to_file():
    filename = "foodfeels_{}.txt".format(current_date.strftime("%Y%m%d"))
    file = open(filename, "w")
    items = food_list.get(0, tk.END)
    for i in items:
        file.write(i + "\n")
    file.close()
    save_label["text"] = "Saved to file {}".format(filename)


def toggle_dropdown_items(msg):

    entries = feels_dropdown['menu'].index('end')
    for i in range(entries + 1):
        feels_dropdown['menu'].entryconfig(i, state=msg)
    feels_selection.set(feels_list[0])
    feels_label["state"] = msg


def update_feels(msg):
    cur_item = food_list.curselection()
    feel = feels_selection.get()
    item = food_list.get(cur_item)
    if "::" in item:
        item_split = item.split("::")
        item = item_split[0]

    item_feel = "{} :: {}".format(item, feel)

    food_list.delete(cur_item)
    food_list.insert(cur_item, item_feel)
    toggle_dropdown_items("disable")


# Remove an item from the food list
def remove_list_item():
    food_list.delete((food_list.curselection()))
    item_remove_button["state"] = "disable"

    toggle_dropdown_items("disable")


# Function that triggers each time an item is selected
def list_item_selected(msg):
    item_remove_button["state"] = "normal"

    toggle_dropdown_items("normal")
    feels_selection.set(feels_list[0])


# Function to add items into our food list for the day
def add_food_item():
    item = food_input.get()

    if item != "":
        food_list.insert(tk.END, item)
        food_input.set("")

        food_list.selection_clear(0, tk.END)

        food_list.select_set(tk.END)
        list_item_selected(tk.END)
        food_list.event_generate("<<ListboxSelect>>")

    else:
        showinfo("Invalid Entry", "Please enter a food or drink item")


# Initialize input variables to handle our user inputs
food_input = tk.StringVar()
food_list_data = tk.StringVar()
feels_selection = tk.StringVar()


# Initialize our frames for the window
header_frame = tk.Frame(window)
item_input_frame = tk.LabelFrame(window, text="Your Food")
item_list_frame = tk.Frame(window)
feels_frame = tk.LabelFrame(window, text="Your Feels")
footer_frame = tk.Frame(window)


# Grid placements for our frames
header_frame.grid(row=0, column=0, padx=10, pady=10)
item_input_frame.grid(row=1, column=0, padx=10, pady=10, sticky="NS")
item_list_frame.grid(row=2, column=0, padx=10, pady=10)
feels_frame.grid(row=3, column=0, padx=10, pady=10, sticky="N")
footer_frame.grid(row=4, column=0, padx=10, pady=10)

# Elements for the header section
header_label = tk.Label(header_frame, text="Your food feels journal for {}".format(current_date))

# Elements for adding new items to your list
food_label = tk.Label(item_input_frame, text="Enter food or drink item: ")
food_entry = tk.Entry(item_input_frame, textvariable=food_input)
food_button = tk.Button(item_input_frame, text="Add Item", command=add_food_item, state="normal")

# Elements for displaying our list of items
food_list = tk.Listbox(item_list_frame, listvariable=food_list_data, selectmode="single", width=23)
food_list.bind("<<ListboxSelect>>", list_item_selected)
item_remove_button = tk.Button(item_list_frame, text="Remove Item", state="disable", command=remove_list_item)

# Elements for setting the feels for an item
feels_label = tk.Label(feels_frame, text="How did you feel after eating this?", state="disable")
feels_list = [' ','Terrible', 'Not Good', 'Okay', 'Wonderful']
feels_dropdown = tk.OptionMenu(feels_frame, feels_selection, *feels_list, command=update_feels)
feels_selection.set(feels_list[0])

entries = feels_dropdown['menu'].index('end')
for i in range(entries+1):
     feels_dropdown['menu'].entryconfig(i, state='disable')

# Elements for the footer frame
save_button = tk.Button(footer_frame, text="Save Current Day", command=save_to_file)
save_label = tk.Label(footer_frame, text="")

# Grid placements for the header
header_label.grid(row=0, column=0, padx=6, pady=6, sticky="W")

# Grid placements for the item_input_frame
food_label.grid(row=0, column=0, padx=6, pady=6, sticky="W")
food_entry.grid(row=1, column=0, padx=6, pady=6)
food_button.grid(row=2, column=0, sticky="E", padx=6, pady=6)

# Grid placements for the item_list_frame
food_list.grid(row=0, column=0, padx=6, pady=6)
item_remove_button.grid(row=1, column=0, sticky="E", padx=6, pady=6)

# Grid placements for the feelings inputs
feels_label.grid(row=0, column=0, padx=6, pady=6, sticky="W")
feels_dropdown.grid(row=1, column=0, padx=6, pady=6, sticky="WE")

# Grid placements for the footer items
save_button.grid(row=0, column=0, padx=6, pady=6)
save_label.grid(row=1, column=0, padx=6, pady=6)

window.mainloop()