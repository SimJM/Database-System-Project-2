import tkinter as tk

from explore import get_qep_details


# Function to draw a node on the canvas
def draw_node(canvas, text, x, y):
    # Create a rectangle for the node
    node = canvas.create_rectangle(x, y, x + 150, y + 50, fill='white', outline='black')
    # Put the text inside the node
    canvas.create_text(x + 75, y + 25, text=text)
    return node


# Function to draw a line between two nodes
def draw_line(canvas, node1, node2):
    # Get the middle of the bottom edge of the first node
    x1, y1, x2, y2 = canvas.coords(node1)
    start_x = (x1 + x2) // 2
    start_y = y2

    # Get the middle of the top edge of the second node
    x3, y3, x4, y4 = canvas.coords(node2)
    end_x = (x3 + x4) // 2
    end_y = y3

    # Draw a line with an arrow at the end between the nodes
    canvas.create_line(start_x, start_y, end_x, end_y, arrow=tk.LAST)


# Function to recursively draw nodes and their children
# Function to recursively draw nodes and their children
def draw_nodes_recursively(canvas, plan, x, y, level=0, parent=None):
    # Check if 'Node Type' and 'Total Cost' keys exist
    node_type = plan.get('Node Type', 'Unknown Node')
    total_cost = plan.get('Total Cost', 'N/A')
    node_text = f"{node_type}\nCost={total_cost}"
    node = draw_node(canvas, node_text, x, y)
    if parent:
        draw_line(canvas, parent, node)

    # Assume each level has a fixed vertical distance, and horizontal distance is based on order
    vertical_distance = 100
    horizontal_distance = 150

    # Calculate the x offset for child nodes to avoid overlapping
    if 'Plans' in plan:
        num_children = len(plan['Plans'])
        child_offset = (num_children - 1) * horizontal_distance / 2

        for i, subplan in enumerate(plan['Plans']):
            # Position children horizontally based on their order
            child_x = x + (i * horizontal_distance) - child_offset
            # Increase the vertical position for the child nodes
            child_y = y + vertical_distance
            draw_nodes_recursively(canvas, subplan, child_x, child_y, level + 1, node)

def run_gui(qep_details):
    # Create the main window
    root = tk.Tk()
    root.title('QEP Visualization')

    # Create a canvas to draw the QEP diagram
    canvas = tk.Canvas(root, width=800, height=600, bg='white')
    canvas.pack(fill=tk.BOTH, expand=True)

    # Assuming qep_details is already the correct part of the plan
    draw_nodes_recursively(canvas, qep_details, 400, 50)

    # Start the Tkinter event loop
    root.mainloop()

if __name__ == "__main__":
    # Fetch the actual QEP details using your explore.py module
    sql_query = "SELECT * FROM public.orders WHERE o_orderkey > 50 AND o_orderkey < 300;"
    qep_details = get_qep_details(sql_query)

    if qep_details is not None:
        run_gui(qep_details)
    else:
        print("Failed to get QEP details.")