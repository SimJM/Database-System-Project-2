import json
import database


# Part (a) Visualization of disk blocks accessed by the query
# Function to execute and get a table.
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
