import json
import re
import database


# Part (a) Visualization of disk blocks accessed by the query
# Function to get block content
def get_block_content(table_name, block_id):
    # Craft SQL query to get block content.
    query = f"SELECT * FROM {table_name} WHERE (ctid::text::point)[0] = {block_id};"
    results_table, column_names = get_query_results(query)
    return results_table, column_names


# Part (b) Visualizing different aspects of the QEP including buffer size, cost, etc
# Function to get query plan details
def get_qep_details(sql_query):
    detect_injection(sql_query)
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


if __name__ == "__main__":
    x = "SELECT nation.n_nationkey, nation.n_name, region.r_name AS region_name, nation.n_comment FROM public.nation JOIN public.region ON nation.n_regionkey = region.r_regionkey;"
    x = x.lower()
    print(get_block_content('orders', 0))
