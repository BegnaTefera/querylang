# main.py

from data import employees


# ------------------ PARSING ------------------

def parse_query(query):
    query = " ".join(query.split())  # normalize whitespace

    select_part, rest = query.split("FROM")
    select_part = select_part.replace("SELECT", "").strip()

    where_part = None
    group_by_part = None

    if "GROUP BY" in rest:
        rest, group_by_part = rest.split("GROUP BY")
        group_by_part = group_by_part.strip()

    if "WHERE" in rest:
        from_part, where_part = rest.split("WHERE")
        where_part = where_part.strip()
    else:
        from_part = rest

    columns = [c.strip() for c in select_part.split(",")]
    table_name = from_part.strip()

    return {
        "columns": columns,
        "table": table_name,
        "where": where_part,
        "group_by": group_by_part,
    }


# ------------------ WHERE ------------------

def apply_where(rows, condition):
    if not condition:
        return rows

    column, value = condition.split("=")
    column = column.strip()
    value = value.strip().strip("'")

    return [row for row in rows if str(row[column]) == value]


# ------------------ GROUP BY + AGGREGATION ------------------

def apply_group_by(rows, group_col, select_cols):
    groups = {}

    for row in rows:
        key = row[group_col]
        groups.setdefault(key, []).append(row)

    results = []

    for key, group_rows in groups.items():
        result = {group_col: key}

        for col in select_cols:
            if col.startswith("COUNT"):
                result[col] = len(group_rows)

            elif col.startswith("SUM"):
                field = col[col.find("(")+1:col.find(")")]
                result[col] = sum(r[field] for r in group_rows)

            elif col.startswith("AVG"):
                field = col[col.find("(")+1:col.find(")")]
                result[col] = sum(r[field] for r in group_rows) / len(group_rows)

        results.append(result)

    return results


# ------------------ EXECUTION ------------------

def execute_query(query, data):
    parsed = parse_query(query)
    rows = data

    rows = apply_where(rows, parsed["where"])

    if parsed["group_by"]:
        return apply_group_by(rows, parsed["group_by"], parsed["columns"])

    # Simple SELECT
    results = []
    for row in rows:
        result = {}
        for col in parsed["columns"]:
            result[col] = row[col]
        results.append(result)

    return results


# ------------------ MAIN ------------------

def main():
    query = """
    SELECT dept, COUNT(id), AVG(salary)
    FROM employees
    WHERE dept = 'IT'
    GROUP BY dept
    """

    result = execute_query(query, employees)

    print("Query Result:")
    for row in result:
        print(row)


if __name__ == "__main__":
    main()
