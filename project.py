import explore
import interface


def project():
    print("Project built and ran successfully!")


# Function to execute and visualize a SQL query.
def run_explore_b():
    # sql_query = input('Please enter a sql query: ')
    sql_query = "SELECT * FROM public.orders WHERE o_orderkey > 50 AND o_orderkey < 300;"

    qep_details = explore.get_qep_details(sql_query)
    interface.visualize_qep(qep_details)


if __name__ == "__main__":
    run_explore_b()
    project()
