import tkinter as tk
from tkinter import scrolledtext, ttk
import pandas as pd
from pandastable import Table

import explore


# Function to initialise and open the application in a window
def open_application_window():
    print('Opening application')
    run_explore_a()


def visualise_blocks(tables_involved, table1, table2):
    # Main application window
    # Main layout frames using grid
    root = tk.Tk()
    root.title("Database Block Visualization")
    main_frame = tk.Frame(root)
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_rowconfigure(2, weight=1)
    # Configure two columns with equal weight for the QEP and Node Details
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(2, weight=1)
    main_frame.grid_columnconfigure(3, weight=1)
    main_frame.grid_columnconfigure(4, weight=1)
    main_frame.grid_columnconfigure(5, weight=1)

    # Top frame for SQL query input
    top_frame = tk.Frame(main_frame)
    top_frame.grid(row=0, column=0, columnspan=4, sticky='ew')
    top_frame.grid_columnconfigure(0, weight=1)

    sql_query_label = tk.Label(top_frame, text="Enter SQL Query:")
    sql_query_label.grid(row=0, column=0, padx=10)

    sql_query_entry = tk.Entry(top_frame)
    sql_query_entry.grid(row=0, column=1, sticky='ew', padx=10, columnspan=2)

    submit_query_button = tk.Button(top_frame, text="Submit")
    submit_query_button.grid(row=0, column=3, padx=10)

    # ctid table frame
    ctid_table_frame = tk.LabelFrame(main_frame, text="ctid Table")
    ctid_table_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=10, pady=10)
    ctid_data = pd.DataFrame(table1, columns=tables_involved)
    ctid_table = Table(ctid_table_frame, dataframe=ctid_data)
    ctid_table.show()

    # Stats table frame
    stats_table_frame = tk.LabelFrame(main_frame, text="stats_table")
    stats_table_frame.grid(row=1, column=2, columnspan=2, sticky='nsew', padx=10, pady=10)
    stats_data = pd.DataFrame(table2,
                              columns=['Relation Name', 'Number of Blocks Accessed', 'Number of Buffer Hits'])
    stats_table = Table(stats_table_frame, dataframe=stats_data)
    stats_table.show()

    # Block content frame
    block_content_frame = tk.LabelFrame(main_frame, text="Block Content")
    block_content_frame.grid(row=1, column=4, columnspan=2, sticky='nsew', padx=10, pady=10)
    block_content_text = tk.Text(block_content_frame)
    block_content_text.pack(fill='both', expand=True)

    # QEP frame
    qep_frame = tk.LabelFrame(main_frame, text="QEP")
    qep_frame.grid(row=2, column=0, columnspan=3, sticky='nsew', padx=10, pady=10)
    qep_text = tk.Text(qep_frame)
    qep_text.pack(fill='both', expand=True)

    # Node details frame
    node_details_frame = tk.LabelFrame(main_frame, text="Node Details")
    node_details_frame.grid(row=2, column=3, columnspan=3, sticky='nsew', padx=10, pady=10)
    node_details_text = tk.Text(node_details_frame)
    node_details_text.pack(fill='both', expand=True)

    # Table selection dropdown
    table_names = ['customer', 'lineitem', 'nation', 'orders', 'part', 'partsupp', 'region', 'supplier']
    selected_table = tk.StringVar(root)
    selected_table.set(table_names[0])  # Default value
    table_dropdown = ttk.Combobox(root, values=table_names, textvariable=selected_table)
    table_dropdown.pack(fill='x', pady=5)

    # Block ID entry
    block_id_label = tk.Label(root, text="Enter Block ID:")
    block_id_label.pack()
    block_id_entry = tk.Entry(root)
    block_id_entry.pack(fill='x')

    table_name = 'orders'
    block_id = 0  # TODO: take in user input to get block_id
    query_for_block_content = explore.craft_block_content_query(table_name, block_id)
    block_content_table = explore.get_query_results(query_for_block_content)

    # Visualize button
    visualize_button = tk.Button(root, text="Visualize",
                                 command=lambda: block_content_table)
    visualize_button.pack(pady=5)

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


def display_node_details(node_data, canvas):
    # Ensure the details frame is visible when displaying node details
    canvas.detail_frame.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

    # Clear previous items
    for item in canvas.detail_frame.winfo_children():
        item.destroy()

    # Create a scrollbar for the Listbox
    scrollbar = tk.Scrollbar(canvas.detail_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a Listbox and attach the scrollbar
    details_listbox = tk.Listbox(canvas.detail_frame, yscrollcommand=scrollbar.set, width=50)
    details_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Configure the scrollbar to scroll through the Listbox content
    scrollbar.config(command=details_listbox.yview)

    # Insert data to the Listbox, each attribute on a new line
    for key, value in node_data.items():
        details_listbox.insert(tk.END, f"{key}: {value}")


def draw_nodes_recursively(canvas, plan, x, y, level=0, parent=None):
    # Check for the existence of 'Relation Name' and include it in the node text if it's a leaf node
    relation_name = plan.get('Relation Name', '')
    node_type = plan.get('Node Type', 'Unknown Node')
    total_cost = plan.get('Total Cost', 'N/A')
    node_text = f"{node_type}\nCost={total_cost}"
    if relation_name and not plan.get('Plans'):  # If there is a relation name and no child plans, get the relation
        node_text += f"\nRelation: {relation_name}"

    # node_data pass to the draw_node
    node_data = {k: v for k, v in plan.items() if k not in ['Plans']}
    node, text_id = draw_node(canvas, node_text, x, y, node_data)

    # Bind the click to both the rectangle and text
    for item in (node, text_id):
        canvas.tag_bind(item, '<Button-1>', lambda event, nd=node_data: display_node_details(nd, canvas))

    if parent:
        draw_line(canvas, node, parent)

    vertical_distance = 100
    horizontal_distance = 150

    if 'Plans' in plan:
        num_children = len(plan['Plans'])
        child_offset = (num_children - 1) * horizontal_distance // 2
        for i, sub_plan in enumerate(plan['Plans']):
            child_x = x + (i * horizontal_distance) - child_offset
            child_y = y + (vertical_distance * (level + 1))
            draw_nodes_recursively(canvas, sub_plan, child_x, child_y, level + 1, node)


def visualize_qep(qep_details):
    root = tk.Tk()
    root.title('QEP Visualization')

    # Create a frame for the canvas and details table
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(frame, width=600, height=600, bg='white')
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    canvas.detail_frame = tk.Frame(frame, width=200)

    draw_nodes_recursively(canvas, qep_details, 250, 50)

    root.mainloop()


# Function to display window to take in user input
def get_user_input():
    def on_submit():
        text = entry.get("1.0", tk.END).strip()
        result_label.config(text=f"You entered: {text}")
        root.quit()  # To exit the main loop
        return text

    root = tk.Tk()
    root.title("User SQL Input")

    label = tk.Label(root, text="Enter a SQL query:")
    label.pack()

    entry = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
    entry.pack(expand=True, fill="both")

    result_label = tk.Label(root, text="")
    result_label.pack()

    submit_button = tk.Button(root, text="Submit", command=on_submit)
    submit_button.pack()

    center_window(root, 400, 300)
    root.mainloop()

    # After the user submits the input, call the callback to get the user input
    user_input = on_submit()
    return user_input


# Function to display message
def show_message_popout(message):
    def dismiss():
        root.quit()  # To exit the main loop

    root = tk.Tk()
    root.title("Message")

    label = tk.Label(root, text=message)
    label.pack()

    submit_button = tk.Button(root, text="Dismiss", command=dismiss)
    submit_button.pack()

    center_window(root, 400, 200)
    root.mainloop()


# Function to center the window when pop out
def center_window(root, width, height):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    root.geometry(f"{width}x{height}+{x}+{y}")


def run_explore_a():
    sql_query = get_user_input().lower()  # Convert user input to lowercase to ease parsing algorithm
    # <<<<< TODO: for convenience only, remove before submission
    if not sql_query:
        sql_query = "SELECT nation.n_nationkey, nation.n_name, region.r_name AS region_name, nation.n_comment FROM public.nation JOIN public.region ON nation.n_regionkey = region.r_regionkey;"
    # >>>>>

    #try:
    explore.detect_injection(sql_query)  # Prevent SQL injection to change data in database.
    tables_involved = explore.get_tables_involved(sql_query)

    query_with_ctid = explore.craft_ctid_query(sql_query)
    result_table_with_block_info_only = explore.get_query_results(query_with_ctid)

    query_for_stats = explore.craft_stats_query(sql_query)
    stats_table = explore.get_query_results(query_for_stats)

    # table_name = 'orders'
    # block_id = 0  # TODO: take in user input to get block_id
    # query_for_block_content = explore.craft_block_content_query(table_name, block_id)
    # block_content_table = explore.get_query_results(query_for_block_content)
    # TODO: visualize block_content_table
    visualise_blocks(tables_involved, result_table_with_block_info_only, stats_table)

    # except Exception as error:
    #     interface.show_message_popout(error)
    #     raise error


# Function to execute and visualize a SQL query.
def run_explore_b():
    sql_query = get_user_input()
    # <<<<< TODO: for convenience only, remove before submission
    if not sql_query:
        sql_query = "SELECT nation.n_nationkey, nation.n_name, region.r_name AS region_name, nation.n_comment FROM public.nation JOIN public.region ON nation.n_regionkey = region.r_regionkey;"
    # >>>>>

    try:
        explore.detect_injection(sql_query)  # Prevent SQL injection to change data in database.
        qep_details = explore.get_qep_details(sql_query)
        visualize_qep(qep_details)
    except Exception as error:
        show_message_popout(error)