import pymysql
import dbconfig
import datetime

class DBHelper:
    def connect(self, database="crimemap"):
        return pymysql.connect(host="localhost",
                               user=dbconfig.db_user,
                               password=dbconfig.db_password,
                               db=database)
    def get_all_data(self):
        connection = self.connect()
        try:
            query = "SELECT latitude,longitude,date,category,description from crimes;"
            named_crimes = []
            with connection.cursor() as cursor:
                cursor.execute(query)
                for crime in cursor:
                    named_crime = {
                        'latitude': crime[0],
                        'longitude': crime[1],
                        'date': datetime.datetime.strftime(crime[2], '%y-%m-%d'),
                        'category': crime[3],
                        'description': crime[4]
                    }
                    named_crimes.append(named_crime)
            return named_crimes
        finally:
            connection.close()
    
    def add_input(self, category,date,latitude,longitude,description):
        connection = self.connect()
        try:
            query = "INSERT INTO crimes (category, date, latitude, longitude, description) VALUE (%s,%s,%s,%s,%s);"
            with connection.cursor() as cursor:
                cursor.execute(query, (category, date,latitude,longitude,description))
            connection.commit()
        finally:
            connection.close()

    def clear_all(self):
        connection = self.connect()
        try:
            query = "DELETE FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)
            connection.commit()
        finally:
            connection.close()