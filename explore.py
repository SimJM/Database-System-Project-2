import json
import re
import database


# Part (a) Visualization of disk blocks accessed by the query
# Function to craft sql query for block accessed.
# returns a sql_query
def craft_ctid_query(sql_query):
    sql_query = process_user_input(sql_query)
    sql_query = remove_group_having_aggregate(sql_query)

    temp = sql_query.split("from", 1)

    front = temp[0].strip().rstrip(',')
    back = temp[1].strip().rstrip(';')
    sql_query = f"{front} FROM {back}"

    # Split the string at the first occurrence of "SELECT"
    parts = re.split(r'\bSELECT\b', sql_query, maxsplit=1, flags=re.IGNORECASE)

    # Construct ctid columns into be added into query
    columns_to_add, renamed_columns_to_add = construct_ctid_column(sql_query)

    remaining_part = parts[1].strip()

    # Append new projection with the initial query
    query_with_ctid = f"SELECT {columns_to_add} FROM (SELECT {renamed_columns_to_add}, {remaining_part}) AS results_table"

    return query_with_ctid


def get_tables_involved(sql_query):
    result = []
    lower_case_query = sql_query.lower()  # Use lower() to make the comparison case-insensitive
    table_names = ['customer', 'lineitem', 'nation', 'orders', 'part', 'partsupp', 'region', 'supplier']
    for table_name in table_names:
        if table_name in lower_case_query:  # Check if table is used in the query
            result.append(f"{table_name} ctid")

    return result


# Function to craft SQL query to get statistics of query, for example block accessed and buffer hits.
# returns a sql_query
def craft_stats_query(sql_query):
    base_query = "SELECT relname, heap_blks_read, heap_blks_hit FROM pg_statio_all_tables"
    table_name_condition = construct_table_name_condition(sql_query)  # Construct conditions to be added into query
    stats_query = f"{base_query}  {table_name_condition}"  # Append base query with conditions
    return stats_query


# Function to craft SQL query to get block content.
# returns a sql_query
def craft_block_content_query(table_name, block_id):
    query = f"SELECT * FROM {table_name} WHERE (ctid::text::point)[0] = {block_id};"
    return query


# Part (b) Visualizing different aspects of the QEP including buffer size, cost, etc
# Function to get query plan details
def get_qep_details(sql_query):
    query_plan = generate_query_plan(sql_query)
    qep_details = extract_qep_details(query_plan)
    return qep_details


# Helper Functions
# Function to execute SQL query and get a table.
# returns a table
def get_query_results(sql_query):
    # Connect to the PgSQL database.
    conn = database.connect()
    cursor = conn.cursor()

    print(f"Executing SQL query: {sql_query}")
    cursor.execute(sql_query)
    column_names = [desc[0] for desc in cursor.description]
    results_table = cursor.fetchall()

    # Close the cursor and the database connection.
    cursor.close()
    conn.close()
    return results_table, column_names


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


# Function to parse user input and check for SQL injection
def process_user_input(input_query):
    detect_injection(input_query)  # Check for SQL injection
    block_sub_queries(input_query)   # Block queries with sub queries
    query = input_query.strip()  # Remove trailing spaces
    query = query.rstrip(';')  # Remove semicolon (if any) from query
    query = query.lower()  # Convert input to lowercase
    query = query.replace('\n', ' ').replace('\t', ' ')  # Replace tabs and next line with spaces
    query = re.sub(' +', ' ', query)  # Replace multiple spacing with single spacing
    return query


# Function to detect SQL injection
def detect_injection(sql_query):
    sql_query_upper = sql_query.upper()
    if "DELETE" in sql_query_upper:
        raise ValueError("DELETE statement is not allowed.")
    elif "UPDATE" in sql_query_upper:
        raise ValueError("UPDATE statement is not allowed.")
    elif "INSERT" in sql_query_upper:
        raise ValueError("INSERT statement is not allowed.")
    elif "CREATE" in sql_query_upper:
        raise ValueError("CREATE statement is not allowed.")
    elif "DROP" in sql_query_upper:
        raise ValueError("DROP statement is not allowed.")
    elif "ALTER" in sql_query_upper:
        raise ValueError("ALTER statement is not allowed.")
    elif "INDEX" in sql_query_upper:
        raise ValueError("INDEX statement is not allowed.")


# Function to block queries with sub queries as they are not supported by our program
def block_sub_queries(sql_query):
    sql_query_upper = sql_query.upper()
    num_of_sub_queries = sql_query_upper.count('SELECT')
    if num_of_sub_queries > 1:
        raise AssertionError("Sub queries are not allowed.")


# Function to remove GROUP BY clause, HAVING clause and aggregate functions
def remove_group_having_aggregate(sql_query):
    # Function to remove aggregate functions
    def remove_aggregate_functions(query):
        # Define a dictionary to map aggregate functions to their replacements
        substitutions = {
            "sum(": "(",
            "avg(": "(",
            "min(": "(",
            "max(": "(",
            "count(*)": "1",
            "count(": "(",
        }

        for old, new in substitutions.items():
            query = query.replace(old, new)

        return query

    # Remove aggregate functions
    sql_query = remove_aggregate_functions(sql_query)

    # Remove GROUP BY clause
    sql_query = re.sub(r'\bGROUP\s+BY\b[^;]+', '', sql_query, flags=re.IGNORECASE)

    # Remove HAVING clause
    sql_query = re.sub(r'\bHAVING\b[^;]+', '', sql_query, flags=re.IGNORECASE)

    return sql_query


# Function to construct ctid columns to add into query
def construct_ctid_column(query):
    result = ""
    result_with_rename = ""
    lower_case_query = query.lower()  # Use lower() to make the comparison case-insensitive
    table_names = ['customer', 'lineitem', 'nation', 'orders', 'part', 'partsupp', 'region', 'supplier']
    for table_name in table_names:
        if table_name in lower_case_query:  # Check if table is used in the query
            column_name = f"{table_name}_block_info"
            rename_column_name = f"{table_name}.ctid as {column_name}"
            if result_with_rename:
                # append comma, and new column name
                result = f"{result}, {column_name}"
                result_with_rename = f"{result_with_rename}, {rename_column_name}"
            else:
                result = column_name
                result_with_rename = rename_column_name

    return result, result_with_rename


# Function to construct relname conditions
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


if __name__ == "__main__":
    x = "SELECT nation.n_nationkey, nation.n_name, region.r_name AS region_name, nation.n_comment FROM public.nation JOIN public.region ON nation.n_regionkey = region.r_regionkey;"
    x = x.lower()
    print(craft_ctid_query(x))
    print(craft_stats_query(x))
    print(craft_block_content_query('orders', 0))
