import os
from google.cloud import bigquery


def authenticate(file: str):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = file


def get_table_sample(project_id: str, schema_name: str, table_name: str, nrows: int):
    client = bigquery.Client(project_id)
    sql_call = f"SELECT * FROM {schema_name}.{table_name} WHERE RAND() < {nrows}/(SELECT COUNT(*) FROM {schema_name}.{table_name})"
    query_job = client.query(sql_call)
    return query_job.to_dataframe()


def get_num_null(project_id: str, schema_name: str, table_name: str):
    # Query excludes columns with 0 null rows
    client = bigquery.Client(project_id)
    res = client.query(f"""
        SELECT col_name, COUNT(1) nulls_count
        FROM `{schema_name}.{table_name}` t, UNNEST(REGEXP_EXTRACT_ALL(TO_JSON_STRING(t), r'"(\w+)":null')) col_name
        GROUP BY col_name
        """)
    return {row[0]: row[1] for row in res.result()}


def get_table_data_types(project_id: str, schema_name: str, table_name: str):
    client = bigquery.Client(project_id)
    sql_call = f"SELECT column_name, data_type FROM {schema_name}.INFORMATION_SCHEMA.COLUMNS WHERE table_name='{table_name}'"
    res = client.query(sql_call)
    return {row[0]: row[1] for row in res.result()}


def metrics_numeric(client, schema_name: str, table_name: str, col_name: str, data_type: str):
    res = client.query(f"""
        SELECT COUNT(DISTINCT {col_name}) unique, 
        MIN({col_name}) min, 
        MAX({col_name}) max, 
        COUNTIF({col_name} IS NULL) null_count
        FROM `{schema_name}.{table_name}`
        """)
    for row in res.result():
        return {"data_type": data_type, "unique": row[0], "min": row[1], "max": row[2], "num_null": row[3]}


def metrics_string(client, schema_name: str, table_name: str, col_name: str, data_type: str):
    res = client.query(f"""
        SELECT COUNT(DISTINCT {col_name}), 
        COUNTIF({col_name} IS NULL) null_count
        FROM `{schema_name}.{table_name}`    
        """)
    for row in res.result():
        return {"data_type": data_type, "unique": row[0], "num_null": row[1]}


def metrics_date(client, schema_name: str, table_name: str, col_name: str, data_type: str):
    res = client.query(f"""
        SELECT COUNT(DISTINCT {col_name}), 
        MIN({col_name}), 
        MAX({col_name}), 
        COUNTIF({col_name} IS NULL) null_count
        FROM `{schema_name}.{table_name}`    
        """)
    for row in res.result():
        return {"data_type": data_type, "unique:": row[0], "min": row[1], "max": row[2], "num_null": row[3]}


def column_metrics(client, schema_name: str, table_name: str, column_name: str, data_type: str):
    if data_type == "STRING":
        return metrics_string(client, schema_name, table_name, column_name, data_type)
    elif data_type == "DATE":
        return metrics_date(client, schema_name, table_name, column_name, data_type)
    elif data_type == "FLOAT64" or data_type == "INT64":
        return metrics_numeric(client, schema_name, table_name, column_name, data_type)
    else:
        return {"data_type": data_type}


def table_metrics(project_id: str, schema_name: str, table_name: str):
    out = {}
    client = bigquery.Client(project_id)
    data_types = get_table_data_types(project_id, schema_name, table_name)
    for col, data_type in data_types.items():
        out[col] = column_metrics(client, schema_name, table_name, col, data_type)
    return out
