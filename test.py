import pymysql
import pandas as pd

# Connect to the database
conn = pymysql.connect(host='localhost', user='root', password='0000', db='dbProject')
curs = conn.cursor(pymysql.cursors.DictCursor)

# Read Excel file
df = pd.read_excel('movieList.xls', skiprows=4)

df = df.fillna({
    '영화명': '',
    '영화명(영문)': '',
    '제작연도': 0,
    '제작국가': '',
    '유형': '',
    '장르': '',
    '제작상태': '',
    '감독': '',
    '제작사': ''
})
df['영화명(영문)'] = df['영화명(영문)'].str[:100]
df['감독'] = df['감독'].str[:100]

# Create Movies table if it doesn't exist
curs.execute("CREATE TABLE IF NOT EXISTS Movies (id INT PRIMARY KEY AUTO_INCREMENT, movie_name VARCHAR(100), movie_name_eng TEXT, production_year INT, production_country VARCHAR(50), movie_type VARCHAR(50), production_status VARCHAR(20), production_company VARCHAR(100))")

# Create Directors table if it doesn't exist
curs.execute("CREATE TABLE IF NOT EXISTS Directors (id INT PRIMARY KEY AUTO_INCREMENT, director_name VARCHAR(100))")

# Create Movies_Directors relationship table if it doesn't exist
curs.execute("CREATE TABLE IF NOT EXISTS Movies_Directors (movie_id INT, director_id INT, FOREIGN KEY (movie_id) REFERENCES Movies(id), FOREIGN KEY (director_id) REFERENCES Directors(id), PRIMARY KEY (movie_id, director_id))")

# Create Genres ID-dependent table if it doesn't exist
curs.execute("CREATE TABLE IF NOT EXISTS Genres (movie_id INT, genre VARCHAR(100), FOREIGN KEY (movie_id) REFERENCES Movies(id), PRIMARY KEY (movie_id, genre))")

# Insert data into Movies table
for index, row in df.iterrows():
    movie_name = row['영화명']
    movie_name_eng = row['영화명(영문)']
    production_year = row['제작연도']
    production_country = row['제작국가']
    movie_type = row['유형']
    production_status = row['제작상태']
    production_company = row['제작사']

    curs.execute("INSERT INTO Movies (movie_name, movie_name_eng, production_year, production_country, movie_type, production_status, production_company) VALUES (%s, %s, %s, %s, %s, %s, %s)", (movie_name, movie_name_eng, production_year, production_country, movie_type, production_status, production_company))
    conn.commit()

# Insert data into Directors table
directors_set = set()
for index, row in df.iterrows():
    director_name = row['감독']
    if pd.notnull(director_name):
        if director_name not in directors_set:
            curs.execute("INSERT INTO Directors (director_name) VALUES (%s)", director_name)
            directors_set.add(director_name)
            conn.commit()

# Insert data into Genres relationship table
for index, row in df.iterrows():
    movie_name = row['영화명']
    genre = row['장르']
    
    if pd.notnull(genre):
        genres = genre.split(',')
        curs.execute("SELECT id FROM Movies WHERE movie_name = %s", movie_name)
        movie_id = curs.fetchone()['id']
        for genre_name in genres:
            genre_name = genre_name.strip()
            curs.execute("SELECT COUNT(*) AS count FROM Genres WHERE movie_id = %s AND genre = %s", (movie_id, genre_name))
            result = curs.fetchone()
            if result['count'] == 0:  # If the entry doesn't exist, insert it
                curs.execute("INSERT INTO Genres (movie_id, genre) VALUES (%s, %s)", (movie_id, genre_name))
                conn.commit()

# Insert data into Movies_Directors relationship table
for index, row in df.iterrows():
    movie_name = row['영화명']
    director = row['감독']
    
    if pd.notnull(director):
        directors = director.split(',')
        curs.execute("SELECT id FROM Movies WHERE movie_name = %s", movie_name)
        movie_id = curs.fetchone()['id']
        for director_name in directors:
            director_name = director_name.strip()
            curs.execute("SELECT id FROM Directors WHERE director_name = %s", director_name)
            result = curs.fetchone()
            if result is None:  # If the director does not exist, insert them
                curs.execute("INSERT INTO Directors (director_name) VALUES (%s)", (director_name,))
                conn.commit()
                curs.execute("SELECT id FROM Directors WHERE director_name = %s", director_name)
                result = curs.fetchone()
            director_id = result['id']
            curs.execute("SELECT COUNT(*) AS count FROM Movies_Directors WHERE movie_id = %s AND director_id = %s", (movie_id, director_id))
            result = curs.fetchone()
            if result['count'] == 0:  # If the entry doesn't exist, insert it
                curs.execute("INSERT INTO Movies_Directors (movie_id, director_id) VALUES (%s, %s)", (movie_id, director_id))
                conn.commit()


# Close cursor and connection
curs.close()
conn.close()
