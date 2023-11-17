import tkinter as tk
from tkinter import scrolledtext, ttk
import tkinter.font as tkf
import pandas as pd
from pandastable import Table

from explore import get_qep_details, get_block_content, get_block_accessed_content

# Define tree globally
tree = None


# Function to initialise and open the application in a window
def open_application_window():
    print('Opening application')
    try:
        visualize()
    except Exception as error:
        show_message_popout(error)


def visualize():
    def on_mousewheel(event):
        qep_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Function to get user input on submit
    def on_submit_query_input():
        try:
            user_input = sql_query_entry.get("1.0", tk.END).strip()
            qep_details = get_qep_details(user_input)
            block_accessed_details, block_accessed_columns = get_block_accessed_content(user_input)
            ctid_data = pd.DataFrame(block_accessed_details, columns=block_accessed_columns)
            ctid_table = Table(ctid_table_frame, dataframe=ctid_data)
            ctid_table.show()
            qep_canvas.delete("all")

            # Enable the widget before clearing it and then disable it again
            node_details_text.config(state='normal')  # Enable the widget to clear
            node_details_text.delete('1.0', tk.END)  # Clear the node details text widget
            node_details_text.config(state='disabled')  # Disable the widget to prevent user from typing

            # Draw the QEP on the canvas, now passing the node_details_text to draw_nodes_recursively
            draw_nodes_recursively(qep_canvas, qep_details, 250, 50, node_details_text=node_details_text)

            # Set the scroll region after everything is drawn on the canvas
            qep_canvas.update_idletasks()  # This updates the layout so the bbox can be calculated correctly
            qep_canvas.config(scrollregion=qep_canvas.bbox("all"))
        except Exception as error:
            show_message_popout(error)

    # Main application window
    # Main layout frames using grid
    root = tk.Tk()
    # root.resizable(False, False)

    screen_width = root.winfo_screenwidth() - 100
    screen_height = root.winfo_screenheight() - 100

    root.geometry(f"{screen_width}x{screen_height}")

    root.title("Database Block Visualization")
    main_frame = tk.Frame(root)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # Row Config
    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_rowconfigure(2, weight=1)
    main_frame.grid_rowconfigure(4, weight=1)
    # Col Config
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)

    # Top frame for SQL query input
    top_frame = tk.Frame(main_frame)
    top_frame.grid(row=0, column=0, columnspan=4, sticky='ew')
    top_frame.grid_columnconfigure(0, weight=1)
    top_frame.grid_columnconfigure(1, weight=3)
    top_frame.grid_columnconfigure(2, weight=3)
    top_frame.grid_columnconfigure(3, weight=3)

    sql_query_label = tk.Label(top_frame, text="Enter SQL Query:")
    sql_query_label.grid(row=0, column=0)

    sql_query_entry = tk.Text(top_frame, height=4)
    sql_query_entry.grid(row=0, column=1, sticky='ew', padx=10, columnspan=3)

    submit_query_button = tk.Button(top_frame, text="Submit", command=on_submit_query_input)
    submit_query_button.grid(row=0, column=4, padx=10, sticky='w')

    # ctid table frame
    ctid_table_frame = tk.LabelFrame(main_frame, text="Block Accessed Information Table", width=400, height=100)
    ctid_table_frame.grid(row=1, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)

    # Block content frame
    block_content_frame = tk.LabelFrame(main_frame, text="Block Content", width=400, height=50)
    block_content_frame.grid(row=2, column=0, columnspan=4, sticky='ew')  # , padx=10, pady=10
    block_content_frame.grid_propagate(False)

    # Configure column weight to prevent expansion
    main_frame.columnconfigure(3, weight=0)  # Assuming the block_content_frame is in the fourth column

    # Create a sub-frame within the block content frame
    subframe_dropdown = tk.Frame(block_content_frame)
    subframe_dropdown.pack(side=tk.TOP, fill=tk.X, padx=10)

    # Create another subframe for the visualize button
    subframe_visualize = tk.Frame(block_content_frame)
    subframe_visualize.pack(side=tk.TOP, fill=tk.X, padx=10)

    # QEP frame with scrollbar
    qep_frame = tk.LabelFrame(main_frame, text="QEP")
    qep_frame.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)

    # Create the scrollbar first
    qep_scrollbar = tk.Scrollbar(qep_frame, orient="vertical")
    qep_scrollbar.pack(side="right", fill="y")

    # Create the canvas and attach the scrollbar to it
    qep_canvas = tk.Canvas(qep_frame, bg='white', yscrollcommand=qep_scrollbar.set)
    qep_canvas.pack(side="left", fill='both', expand=True)

    # Configure the scrollbar to control the yview of canvas
    qep_scrollbar.config(command=qep_canvas.yview)

    # Bind the mousewheel event to the on_mousewheel function
    qep_canvas.bind("<MouseWheel>", on_mousewheel)

    # Node details frame with scrolled text
    node_details_frame = tk.LabelFrame(main_frame, text="Node Details")
    node_details_frame.grid(row=3, column=1, columnspan=2, sticky='nsew', padx=10, pady=10)
    node_details_text = scrolledtext.ScrolledText(node_details_frame, wrap='word')
    node_details_text.pack(fill='both', expand=True)

    # Table selection dropdown
    table_names = ['customer', 'lineitem', 'nation', 'orders', 'part', 'partsupp', 'region', 'supplier']
    selected_table = tk.StringVar(root)
    selected_table.set(table_names[0])  # Default value
    # Label for the dropdown
    dropdown_label = tk.Label(subframe_dropdown, text="Select a table:")
    dropdown_label.pack(side=tk.LEFT)
    table_dropdown = ttk.Combobox(subframe_dropdown, values=table_names, textvariable=selected_table)
    # Pack the dropdown to fill 75% of the width
    table_dropdown.pack(side=tk.LEFT, fill=tk.X, expand=True)

    # Insert a spacer to center the elements
    spacer = tk.Frame(subframe_dropdown)
    spacer.pack(side=tk.LEFT, padx=(10, 0))  # Adjust padx as needed for spacing

    # Block ID entry
    block_id_label = tk.Label(subframe_dropdown, text="Enter Block ID:")
    block_id_label.pack(side=tk.LEFT)
    block_id_entry = tk.Entry(subframe_dropdown)
    block_id_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, pady=10)

    # Function to retrieve the selected table
    def get_table_name():
        selection = selected_table.get()
        print(selection)
        return selection

    # Function to retrieve the entered block ID value
    def capture_block_id():
        block_id_value = block_id_entry.get()
        print(block_id_value)
        return block_id_value

    # Define a function to clear all the items present in Treeview
    def clear_all():
        global tree
        if tree:
            for item in tree.get_children():
                tree.delete(item)

    def visualize_block_content():
        global tree
        # Call clear_all() before displaying new content
        clear_all()

        table_name = get_table_name()
        block_id = capture_block_id()
        block_content_table, column_names = get_block_content(table_name, block_id)
        display_table(block_content_table, column_names)

    def show_table_popout():
        try:
            table_name = get_table_name()
            block_id = capture_block_id()
            data, column_names = get_block_content(table_name, block_id)
            root1 = tk.Tk()
            # root1.resizable(False, False)
            root1.title("Table")
            screen_width = 1200
            screen_height = 800

            root1.geometry(f"{screen_width}x{screen_height}")
            # Create a Treeview widget
            tree = ttk.Treeview(root1)

            # Check the number of columns dynamically
            num_columns = len(data[0]) if data else 0  # Check the first row's length

            # Define columns
            tree["columns"] = list(range(num_columns))
            tree["show"] = "headings"

            # Add column headings
            for i, heading in enumerate([column_names[i] for i in range(num_columns)]):
                tree.heading(i, text=heading)
                # Adjust column widths based on content
                tree.column(i, width=tkf.Font().measure(heading))

            # Insert data rows
            for row in data:
                tree.insert("", "end", values=row)
                for i, value in enumerate(row):
                    # Measure the text in each cell and adjust column width if necessary
                    col_width = tkf.Font().measure(value)
                    if tree.column(i, width=None) < col_width:
                        tree.column(i, width=col_width)

            # Add a horizontal scrollbar
            hscrollbar = ttk.Scrollbar(root1, orient='horizontal', command=tree.xview)
            tree.configure(xscrollcommand=hscrollbar.set)
            hscrollbar.pack(side='bottom', fill='x')

            # Display Treeview
            tree.pack(fill='both', expand=True)

            root1.mainloop()
        except Exception as error:
            show_message_popout(error)



    def display_table(data, column_names):
        global tree, hscrollbar
        # Create a Frame to contain the Treeview
        tree_frame = tk.Frame(block_content_frame)
        tree_frame.pack(fill='both', expand=True)

        # Create a Treeview widget
        if not tree:
            tree = ttk.Treeview(tree_frame)
        else:
            clear_all()

        # Check the number of columns dynamically
        num_columns = len(data[0]) if data else 0  # Check the first row's length

        # Define columns
        tree["columns"] = list(range(num_columns))
        tree["show"] = "headings"

        # Add column headings
        for i, heading in enumerate([column_names[i] for i in range(num_columns)]):
            tree.heading(i, text=heading)
            # Adjust column widths based on content
            tree.column(i, width=tkf.Font().measure(heading))

        # Insert data rows
        for row in data:
            tree.insert("", "end", values=row)
            for i, value in enumerate(row):
                # Measure the text in each cell and adjust column width if necessary
                col_width = tkf.Font().measure(value)
                if tree.column(i, width=None) < col_width:
                    tree.column(i, width=col_width)

        # Add a horizontal scrollbar
        hscrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=tree.xview)
        tree.configure(xscrollcommand=hscrollbar.set)
        hscrollbar.pack(side='bottom', fill='x')

        # Display Treeview
        tree.pack(fill='both', expand=True)

        root.mainloop()

    # Visualize button
    visualize_button = tk.Button(subframe_visualize, text="Visualize", command=show_table_popout)
    visualize_button.pack(side=tk.BOTTOM, pady=(0, 5))

    root.mainloop()


# Function to draw a node on the canvas
def draw_node(canvas, text, x, y, node_data):
    node = canvas.create_rectangle(x, y, x + 100, y + 50, fill='white', outline='black')
    text_id = canvas.create_text(x + 50, y + 25, text=text)

    # Store node data as a tag for both the rectangle and text
    canvas.itemconfig(node, tags=('node', str(id(node_data))))
    canvas.itemconfig(text_id, tags=('node', str(id(node_data))))

    # Return both ids for event binding
    return node, text_id


# Function to draw a line from a child node pointing to its parent
def draw_line(canvas, child, parent):
    x1, y1, x2, y2 = canvas.coords(child)
    x3, y3, x4, y4 = canvas.coords(parent)

    # Calculate the start and end points for the line
    start_x = (x1 + x2) // 2
    start_y = y1
    end_x = (x3 + x4) // 2
    end_y = y4

    # Draw a line with an arrow at the end pointing to the parent node
    canvas.create_line(start_x, start_y, start_x, (start_y + end_y) // 2, end_x, (start_y + end_y) // 2, end_x, end_y,
                       arrow=tk.LAST)


def display_node_details(node_data, node_details_text):
    # Enable the widget to clear and insert the new text
    node_details_text.config(state='normal')

    # Clear previous items
    node_details_text.delete('1.0', tk.END)

    # Insert data to the text widget, each attribute on a new line
    for key, value in node_data.items():
        node_details_text.insert(tk.END, f"{key}: {value}\n")

    # Disable the widget to prevent user from typing
    node_details_text.config(state='disabled')


def draw_nodes_recursively(canvas, plan, x, y, node_details_text, level=0, parent=None):
    # Check for the existence of 'Relation Name' and include it in the node text if it's a leaf node
    relation_name = plan.get('Relation Name', '')
    node_type = plan.get('Node Type', 'Unknown Node')
    total_cost = plan.get('Total Cost', 'N/A')
    node_text = f"{node_type}\nCost={total_cost}"
    if relation_name and not plan.get('Plans'):  # If there is a relation name and no child plans
        node_text += f"\nRelation: {relation_name}"

    # node_data passed to the draw_node
    node_data = {k: v for k, v in plan.items() if k not in ['Plans']}
    node, text_id = draw_node(canvas, node_text, x, y, node_data)

    # Bind the click to both the rectangle and text, passing the node_details_text widget
    for item in (node, text_id):
        canvas.tag_bind(item, '<Button-1>', lambda event, nd=node_data: display_node_details(nd, node_details_text))

    if parent:
        draw_line(canvas, node, parent)

    vertical_distance = 100
    horizontal_distance = 150

    if 'Plans' in plan:
        num_children = len(plan['Plans'])
        child_offset = (num_children - 1) * horizontal_distance // 2
        for i, sub_plan in enumerate(plan['Plans']):
            child_x = x + (i * horizontal_distance) - child_offset
            # Child y is now calculated as a constant offset from the parent y, not based on level
            child_y = y + vertical_distance
            draw_nodes_recursively(canvas, sub_plan, child_x, child_y, node_details_text, level + 1, node)


# Function to display message
def show_message_popout(message):

    root = tk.Tk()
    root.title("Message")

    label = tk.Label(root, text=message)
    label.pack()

    center_window(root, 400, 200)
    root.mainloop()


# Function to center the window when pop out
def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    root.geometry(f"{width}x{height}+{x}+{y}")
