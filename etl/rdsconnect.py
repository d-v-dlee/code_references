# DBConnect object. Use with context manager ('with' keyword)

import pymysql

class RDSConnect:
    def __init__(self, database):
        if database == "db_name":
            self.RDS_data = {
                "host": "host_name",
                "user": "root",
                "pass": "password",
                "db"  : "database_name"
            }
        elif database == "db_name2":
            self.RDS_data = {
                "host": "db_name",
                "user": "admin",
                "pass": "password",
                "db"  : "database_name"
            }
        else:
            raise Exception("Database required! db_name, db_name2 or db_name3'")

    def __enter__(self):
        self.db = pymysql.connect(self.RDS_data["host"],
                                  self.RDS_data["user"],
                                  self.RDS_data["pass"],
                                  self.RDS_data["db"])

        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


    def get(self, table, amount="all"):
        sql = "SELECT * FROM {}".format(table)

        with self.db.cursor() as cursor:
            cursor.execute(sql)

            if amount == "many":
                # Really just in case we need later. Use with a generator.
                data = cursor.fetchmany(size=10)
            elif amount == "all":
                data = cursor.fetchall()
            else:
                raise Exception("Amount is required!")
        return data
    

    def put(self, patientMap):
        try:
            with self.db.cursor() as cursor:
                for patient in patientMap:
                    sql = "INSERT INTO userinfo_uuid_map(user_id, uuid) \
                             VALUES({}, '{}')".format(patient[0], patient[1])
                    cursor.execute(sql)

            self.db.commit()
            return True
        except Exception as e:
            print("Exception: {}\nRolling back!".format(e))
            self.db.rollback()
            return False

