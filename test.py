import explore


def read_sql_query(file_path):
    with open(file_path, 'r') as file:
        return file.read()


if __name__ == "__main__":

    test_file_numbers = 22
    count_passed = 0
    count_failed = 0
    no_of_queries_with_sub_queries = 0
    for i in range(test_file_numbers):
        try:
            file_number = i + 1
            path = f"test_queries/{file_number}.sql"
            query = read_sql_query(path)
            query = explore.process_user_input(query)

            query = explore.craft_ctid_query(query)
            # query = explore.craft_stats_query(query)

            explore.get_query_results(query)
            count_passed += 1
            print(f"\033[32mSuccess! {file_number}.sql\033[0m")
        except AssertionError as error:
            count_passed += 1
            no_of_queries_with_sub_queries += 1
            print(f"\033[38;5;208mSuccess! {file_number}.sql\033[0m")
        except:
            count_failed += 1
            print(f"\033[91mFailed! {file_number}.sql\033[0m")

    print(f"Test passed: {count_passed}, Test failed: {count_failed}")
    print(f"Number of queries with sub queries: {no_of_queries_with_sub_queries}")
