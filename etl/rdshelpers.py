import pymysql
from rdsconnect import RDSConnect

def insert_into_user_table(table_name, patient_list, cursor):
    """
    function for writing data into new table

    inputs
    -----
    table_name: table name of SQL table to write into
    patient_list: list of pt dictionaries
    cursor: mysql cursor
    """
    
    for d_ in new_list_of_dicts:
        placeholder = ", ".join(["%s"] * len(d_)
        stmt = "insert into `{table}` ({columns}) values ({values});".format(table=table_name, 
                                                            columns=",".join(d_.keys()), values=placeholder)
        cursor.execute(stmt, list(d_.values()))