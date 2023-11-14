import explore
from interface import run_gui  # Import the run_gui function from your interface.py file


def project():
    print("Project built and ran successfully!")


# Function to execute and visualize a SQL query.
def run_explore_b():
    sql_query = "SELECT nation.n_nationkey, nation.n_name, region.r_name AS region_name, nation.n_comment FROM public.nation JOIN public.region ON nation.n_regionkey = region.r_regionkey;"
    qep_details = explore.get_qep_details(sql_query)

    # Check for None before proceeding
    if qep_details:
        try:
            run_gui(qep_details)  # Pass the QEP details to the GUI
        except Exception as e:
            print(f"Failed to run GUI: {e}")
    else:
        print("Failed to get QEP details.")


if __name__ == "__main__":
    run_explore_b()
    project()
