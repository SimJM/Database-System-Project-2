import json
import database


# Part (a) Visualization of disk blocks accessed by the query
# Function to execute SQL query and get a table.
def get_query_results(sql_query):
    # Connect to the PgSQL database.
    conn = database.connect()
    cursor = conn.cursor()

    print(f"Executing SQL query: {sql_query}")
    cursor.execute(sql_query)
    results_table = cursor.fetchall()

    # Close the cursor and the database connection.
    cursor.close()
    conn.close()
    return results_table


# Function to craft sql query for block accessed.
def craft_ctid_query(sql_query):
    # Function to add ctid
    def construct_ctid_column(query):
        result = ""
        lower_case_query = query.lower()  # Use lower() to make the comparison case-insensitive
        table_names = ['customer', 'lineitem', 'nation', 'orders', 'part', 'partsupp', 'region', 'supplier']
        for table_name in table_names:
            if table_name in lower_case_query:  # Check if table is used in the query
                column_name = f"{table_name}.ctid as {table_name}_block_info"
                if result:
                    result = f"{result}, {column_name}"  # append comma, and new column name
                else:
                    result = column_name

        return result

    parts = sql_query.split("FROM", 1)                   # Split the string at the first occurrence of "FROM"
    columns_to_add = construct_ctid_column(sql_query)    # Construct ctid columns into be added into query

    remaining_part = f"FROM {parts[1].strip()}"
    query_with_ctid = f"SELECT {columns_to_add} {remaining_part}"  # Append new projection with the initial query

    return query_with_ctid


# Function to craft SQL query to get statistics of query, for example block accessed and buffer hits.
def craft_stats_query(sql_query):
    def construct_table_name_condition(query):
        result = ""
        lower_case_query = query.lower()  # Use lower() to make the comparison case-insensitive
        table_names = ['customer', 'lineitem', 'nation', 'orders', 'part', 'partsupp', 'region', 'supplier']
        for table_name in table_names:
            if table_name in lower_case_query:  # Check if table is used in the query
                if result:
                    result = f"{result} OR relname = '{table_name}'"  # Append comma and new condition
                else:
                    result = f"WHERE relname = '{table_name}'"

        return result

    base_query = "SELECT relname, heap_blks_read, heap_blks_hit FROM pg_statio_all_tables"
    table_name_condition = construct_table_name_condition(sql_query)  # Construct conditions into be added into query
    stats_query = f"{base_query}  {table_name_condition}"             # Append base query with conditions
    return stats_query


# Function to craft SQL query to get block content.
def craft_block_content_query(table_name, block_id):
    query = f"SELECT * FROM {table_name} WHERE (ctid::text::point)[0] = {block_id}"
    return query


# Part (b) Visualizing different aspects of the QEP including buffer size, cost, etc
# Function to get query plan details
def get_qep_details(sql_query):
    query_plan = generate_query_plan(sql_query)
    qep_details = extract_qep_details(query_plan)
    return qep_details


# Function to execute and visualize a SQL query.
def generate_query_plan(sql_query):
    # Connect to the PgSQL database.
    conn = database.connect()
    cursor = conn.cursor()

    print(f"Generating QEP for query: {sql_query}")
    # Execute the SQL query and retrieve the query execution plan (QEP) in JSON format.
    cursor.execute(f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {sql_query}")
    query_plan = cursor.fetchall()
    print(json.dumps(query_plan, indent=4))

    # Close the cursor and the database connection.
    cursor.close()
    conn.close()

    return query_plan


# Function to extract relevant information from the query plan.
def extract_qep_details(query_plan):
    if query_plan is None:
        return None  # Return None if query_plan is None

    query_plan_json = query_plan[0][0][0];
    aspects = query_plan_json.get("Plan", {})
    aspects["Planning Time"] = query_plan_json.get("Planning Time", 0)
    aspects["Execution Time"] = query_plan_json.get("Execution Time", 0)
    return aspects;


# Function to detect SQL injection
def detect_injection(sql_query):
    if "DELETE" in sql_query.upper():
        raise ValueError("DELETE statement is not allowed.")
    elif "UPDATE" in sql_query.upper():
        raise ValueError("UPDATE statement is not allowed.")
    elif "INSERT" in sql_query.upper():
        raise ValueError("INSERT statement is not allowed.")
    elif "CREATE" in sql_query.upper():
        raise ValueError("CREATE statement is not allowed.")
    elif "DROP" in sql_query.upper():
        raise ValueError("DROP statement is not allowed.")
    elif "ALTER" in sql_query.upper():
        raise ValueError("ALTER statement is not allowed.")
    else:
        print("SQL query is valid.")


if __name__ == "__main__":
    input_query = "SELECT nation.n_nationkey, nation.n_name, region.r_name AS region_name, nation.n_comment FROM public.nation JOIN public.region ON nation.n_regionkey = region.r_regionkey;"
    print(craft_ctid_query(input_query))
    print(craft_stats_query(input_query))
    print(craft_block_content_query('orders', 0))
