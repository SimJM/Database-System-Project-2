import explore
import interface


def project():
    print("Project built and ran successfully!")


# Function to execute and visualize a SQL query.
def run_explore_b():
    sql_query = interface.get_user_input()
    # <<<<< TODO: for convenience only, remove before submission
    if not sql_query:
        sql_query = "SELECT nation.n_nationkey, nation.n_name, region.r_name AS region_name, nation.n_comment FROM public.nation JOIN public.region ON nation.n_regionkey = region.r_regionkey;"
    # >>>>>

    try:
        qep_details = explore.get_qep_details(sql_query)
        interface.visualize_qep(qep_details)
    except Exception as error:
        interface.show_message_popout(error)


if __name__ == "__main__":
    run_explore_b()
    project()
