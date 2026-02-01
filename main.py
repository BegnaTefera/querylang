# main.py

from data import employees


def execute_select(table, columns):
    results = []
    for row in table:
        result_row = {}
        for col in columns:
            result_row[col] = row[col]
        results.append(result_row)
    return results


def main():
    query = "SELECT name, salary FROM employees"

    # very naive parsing (on purpose)
    select_part = query.split("FROM")[0]
    columns_part = select_part.replace("SELECT", "").strip()
    columns = [c.strip() for c in columns_part.split(",")]

    result = execute_select(employees, columns)

    for row in result:
        print(row)


if __name__ == "__main__":
    main()
 
