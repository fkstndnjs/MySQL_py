import pymysql

# Connect to the database
conn = pymysql.connect(host='localhost', user='root', password='0000', db='dbProject')
curs = conn.cursor(pymysql.cursors.DictCursor)

# Initialize the search criteria with empty values
search_criteria = {
    "movie_name": "",
    "production_year": "",
    "production_country": "",
    "genre": "",
    "director_name": ""
}

# Function to get user input and build the search criteria
def get_user_input():
    for key in search_criteria.keys():
        search_criteria[key] = input(f"Enter {key} (Press Enter to skip): ")

# Function to build the SQL query based on the user input
def build_sql_query():
    base_query = "SELECT * FROM Movies m JOIN Genres g ON m.id = g.movie_id JOIN Movies_Directors md ON m.id = md.movie_id JOIN Directors d ON d.id = md.director_id WHERE 1=1"
    if search_criteria["movie_name"] != "":
        base_query += f' AND m.movie_name LIKE "%{search_criteria["movie_name"]}%"'
    if search_criteria["production_year"] != "":
        base_query += f' AND m.production_year = {search_criteria["production_year"]}'
    if search_criteria["production_country"] != "":
        base_query += f' AND m.production_country LIKE "%{search_criteria["production_country"]}%"'
    if search_criteria["genre"] != "":
        base_query += f' AND g.genre LIKE "%{search_criteria["genre"]}%"'
    if search_criteria["director_name"] != "":
        base_query += f' AND d.director_name LIKE "%{search_criteria["director_name"]}%"'
    return base_query

# Function to execute the SQL query and print the results
def execute_sql_query():
    curs.execute(build_sql_query())
    rows = curs.fetchall()
    for row in rows:
        print(row)

# Get user input
get_user_input()

# Execute the SQL query and print the results
execute_sql_query()

# Close cursor and connection
curs.close()
conn.close()

