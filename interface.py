import matplotlib.pyplot as plt


# Function to visualize QEP details.
def visualize_qep(aspects):
    display_label, display_values = generate_display_aspects(aspects)
    create_and_display_chart(display_label, display_values)


# Function to process data to be displayed.
def generate_display_aspects(aspects):
    labels = list(aspects.keys())
    display_label = []
    display_values = []

    for label in labels:
        # Only display fields that are integer or float
        if isinstance(aspects[label], bool):
            continue
        elif isinstance(aspects[label], (int, float)):
            # Only Display values that are non-zero
            if aspects[label] != 0:
                # Add units for labels associated with time
                if "Cost" in label or "Time" in label:
                    display_label.append(f"{label} (ms)")
                else:
                    display_label.append(label)
                display_values.append(aspects[label])
        else:
            continue
    return display_label, display_values


# Function to plot and display chart
def create_and_display_chart(display_label, display_values):
    assert (len(display_label) == len(display_values))
    # Initialise chart
    plt.figure(figsize=(10, 6))
    plt.xlabel("QEP Aspects")
    plt.ylabel("Values (Logarithmic Scale)")
    plt.title("Query Execution Plan Aspects")
    plt.xticks(rotation=45, ha="right")

    # Plot chart
    bars = plt.bar(display_label, display_values, color='skyblue')
    plt.yscale("log")  # Add logarithmic scale to the y-axis

    # Add text labels for each bar
    for bar, value in zip(bars, display_values):
        plt.text(bar.get_x() + bar.get_width() / 2 - 0.15, value, str(value), ha='center', va='bottom')

    plt.tight_layout()
    plt.show()
