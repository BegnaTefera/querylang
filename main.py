# main.py

from data import employees, departments


# ------------------ PARSER ------------------

def normalize(q):
    return " ".join(q.replace("\n", " ").split())


def parse_query(query):
    query = normalize(query)

    select_part, rest = query.split("FROM")
    select_cols = [c.strip() for c in select_part.replace("SELECT", "").split(",")]

    join_part = None
    where_part = None
    group_by = None

    if "GROUP BY" in rest:
        rest, group_by = rest.split("GROUP BY")
        group_by = group_by.strip()

    if "WHERE" in rest:
        rest, where_part = rest.split("WHERE")
        where_part = where_part.strip()

    if "JOIN" in rest:
        from_part, join_part = rest.split("JOIN")
        from_table = from_part.strip()

        join_table, on_part = join_part.split("ON")
        join_table = join_table.strip()
        on_left, on_right = [x.strip() for x in on_part.split("=")]

        join_part = {
            "table": join_table,
            "left": on_left,
            "right": on_right,
        }
    else:
        from_table = rest.strip()

    return {
        "select": select_cols,
        "from": from_table,
        "join": join_part,
        "where": where_part,
        "group_by": group_by,
    }


# ------------------ WHERE ------------------

def apply_where(rows, condition):
    if not condition:
        return rows

    if "IN (" in condition:
        col, subquery = condition.split("IN")
        col = col.strip()
        subquery = subquery.strip()[1:-1]
        values = execute_query(subquery)
        values = {list(v.values())[0] for v in values}
        return [r for r in rows if r[col] in values]

    col, value = condition.split("=")
    value = value.strip().strip("'")
    return [r for r in rows if str(r[col.strip()]) == value]


# ------------------ JOIN ------------------

def apply_join(left_rows, right_rows, left_key, right_key):
    result = []
    for l in left_rows:
        for r in right_rows:
            if l[left_key.split(".")[1]] == r[right_key.split(".")[1]]:
                merged = {}
                for k, v in l.items():
                    merged[f"employees.{k}"] = v
                for k, v in r.items():
                    merged[f"departments.{k}"] = v
                result.append(merged)
    return result


# ------------------ GROUP BY ------------------

def apply_group_by(rows, group_col, select_cols):
    groups = {}
    for r in rows:
        groups.setdefault(r[group_col], []).append(r)

    results = []
    for key, group in groups.items():
        row = {group_col: key}
        for col in select_cols:
            if col.startswith("COUNT"):
                row[col] = len(group)
            elif col.startswith("SUM"):
                field = col[col.find("(")+1:col.find(")")]
                row[col] = sum(r[field] for r in group)
            elif col.startswith("AVG"):
                field = col[col.find("(")+1:col.find(")")]
                row[col] = sum(r[field] for r in group) / len(group)
        results.append(row)

    return results


# ------------------ EXECUTION ------------------

def execute_query(query):
    q = parse_query(query)

    tables = {
        "employees": employees,
        "departments": departments,
    }

    rows = tables[q["from"]]

    if q["join"]:
        right_rows = tables[q["join"]["table"]]
        rows = apply_join(
            rows,
            right_rows,
            q["join"]["left"],
            q["join"]["right"],
        )

    rows = apply_where(rows, q["where"])

    if q["group_by"]:
        return apply_group_by(rows, q["group_by"], q["select"])

    result = []
    for r in rows:
        row = {}
        for c in q["select"]:
            row[c] = r[c]
        result.append(row)

    return result


# ------------------ MAIN ------------------

def main():
    query = """
    SELECT employees.name, departments.name
    FROM employees JOIN departments
    ON employees.dept = departments.id
    """

    for row in execute_query(query):
        print(row)


if __name__ == "__main__":
    main()
