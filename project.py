import explore
import interface


def run_explore_a():
    sql_query = interface.get_user_input().lower()  # Convert user input to lowercase to ease parsing algorithm
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
    interface.visualise_blocks(tables_involved, result_table_with_block_info_only, stats_table)

    # except Exception as error:
    #     interface.show_message_popout(error)
    #     raise error


# Function to execute and visualize a SQL query.
def run_explore_b():
    sql_query = interface.get_user_input()
    # <<<<< TODO: for convenience only, remove before submission
    if not sql_query:
        sql_query = "SELECT nation.n_nationkey, nation.n_name, region.r_name AS region_name, nation.n_comment FROM public.nation JOIN public.region ON nation.n_regionkey = region.r_regionkey;"
    # >>>>>

    try:
        explore.detect_injection(sql_query)  # Prevent SQL injection to change data in database.
        qep_details = explore.get_qep_details(sql_query)
        interface.visualize_qep(qep_details)
    except Exception as error:
        interface.show_message_popout(error)


if __name__ == "__main__":
    run_explore_a()
    # run_explore_b()
