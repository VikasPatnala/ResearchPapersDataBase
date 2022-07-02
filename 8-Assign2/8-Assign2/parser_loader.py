import psycopg2


TITLE = "#*"
AUTHOR = "#@"
YEAR = "#t"
VENUE = "#c"
CITES = "#%"
INDEX = "#i"
ABSTRACT = "#!"

DB_HOST = "localhost"
DB_NAME = "new_DB"
DB_USER = "postgres"
DB_PASS = "root"

file = open("source.txt","r")
# To format the author names without the "."s and replace them with space instead
def formatstring(name):
	seperate = name.split(".")

	formatted = ""
	for word in seperate:
		formatted = formatted + word.strip() + " "

	return formatted		
#Opening a connection
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS,host=DB_HOST)

cur = conn.cursor()
#Dropping the tables if they already exists
cur.execute("DROP TABlE IF EXISTS Contribution cascade;")
cur.execute("DROP TABlE IF EXISTS Cites cascade;")
cur.execute("DROP TABLE IF EXISTS Venue cascade;")
cur.execute("DROP TABLE IF EXISTS paper cascade;")
cur.execute("DROP TABLE IF EXISTS Author cascade;")
conn.commit()
# Creating tables
cur.execute("""

	CREATE TABLE Venue
	(
	Venue_Name TEXT NOT NULL,
	PRIMARY KEY (Venue_Name)
	);
""")
conn.commit()
cur.execute("""
	CREATE TABLE IF NOT EXISTS Paper
	(
	Id INT NOT NULL,
	Title TEXT NOT NULL,
	Main_Author TEXT NOT NULL,
	year INT NOT NULL,
	abstract TEXT NOT NULL,
	Venue_Name TEXT,
	PRIMARY KEY (Id),
	FOREIGN KEY (Venue_Name) REFERENCES Venue(Venue_Name)
	);
""")
conn.commit()

cur.execute("""

	CREATE TABLE IF NOT EXISTS Author
	(
	Author_Name TEXT NOT NULL,
	PRIMARY KEY (Author_Name)
	);
""")
conn.commit()

cur.execute("""
	CREATE TABLE IF NOT EXISTS Contribution
	(
	  Id INT NOT NULL,
	  Contrib INT NOT NULL,
	  Author_Name TEXT NOT NULL,
	  PRIMARY KEY (Id, Author_Name),
	  FOREIGN KEY (Id) REFERENCES Paper(Id),
	  FOREIGN KEY (Author_Name) REFERENCES Author(Author_Name)
	);
""")
conn.commit()

cur.execute("""
	CREATE TABLE IF NOT EXISTS Cites
	(
	Id_1 INT NOT NULL,
	CitesId_2 INT NOT NULL,
	PRIMARY KEY (Id_1, CitesId_2),
	FOREIGN KEY (Id_1) REFERENCES Paper(Id),
	FOREIGN KEY (CitesId_2) REFERENCES Paper(Id)
	);
	"""
)
conn.commit()

#Reading input
s = file.readline()

title = ""
authors = []
abstract = ""
paperid = ""
year = ""
venue = ""
cites = []
while s !="":
	code = s[0:2]
	info = s[2:-1]
	if s!="\n":
		if code == TITLE:
			title = info
		elif code == AUTHOR:
			authors = info.split(",")
		elif code == ABSTRACT:
			abstract = info
		elif code == INDEX:
			paperid = s[6:]
		elif code == CITES:
			cites.append(info)
		elif code == VENUE:
			venue = info
		elif code == YEAR:
			year = info
	elif s == "\n":
		if(paperid!=""):
			no_rep_authors = []
			for author in authors:
				if author not in no_rep_authors:
					author = formatstring(author)
					no_rep_authors.append(author.strip())
			# If the primary key is being repeated then we do not add using ON CONFLICT DO NOTHING
			for author in no_rep_authors:
				if author!='':	
					cur.execute("INSERT INTO author (Author_Name) VALUES(%s) ON CONFLICT DO NOTHING",[(author)])	
				else:
					cur.execute("INSERT INTO author (Author_Name) VALUES(%s) ON CONFLICT DO NOTHING",["(Not Found)"]) 
			if venue == "" or venue == "\n":
				if no_rep_authors[0]!="":
					cur.execute("INSERT INTO paper (ID,Title,Abstract,Main_Author,Year,Venue_Name) VALUES(%s,%s,%s,%s,%s,NULL) ",(int(paperid),title,abstract,no_rep_authors[0],int(year)))
				else:
					cur.execute("INSERT INTO paper (ID,Title,Abstract,Main_Author,Year,Venue_Name) VALUES(%s,%s,%s,%s,%s,NULL) ",(int(paperid),title,abstract,"(Not Found)",int(year)))

			else:
				cur.execute("INSERT INTO Venue (Venue_Name) VALUES (%s) ON CONFLICT DO NOTHING",[venue])
				if no_rep_authors[0]!="":
					cur.execute("INSERT INTO paper (ID,Title,Abstract,Main_Author,Year,Venue_Name) VALUES(%s,%s,%s,%s,%s,%s) ",(int(paperid),title,abstract,no_rep_authors[0],int(year),venue))
				else:
					cur.execute("INSERT INTO paper (ID,Title,Abstract,Main_Author,Year,Venue_Name) VALUES(%s,%s,%s,%s,%s,%s) ",(int(paperid),title,abstract,"(Not Found)",int(year),venue))
		
		title = ""
		authors = []
		abstract = ""
		paperid = ""
		year = ""
		venue = ""
		cites = []

	s = file.readline()

conn.commit()
# Again reading and parsing the file
# So we can fill foreign keys 
# For example in cites some paper may reference another paper which ias not already added, so first we add all the papers,
# then citations
file.seek(0)
s = file.readline()

title = ""
authors = []
abstract = ""
paperid = ""
year = ""
venue = ""
cites = []
while s !="":
	code = s[0:2]
	info = s[2:-1]
	if s!="\n":
		if code == TITLE:
			title = info
		elif code == AUTHOR:
			authors = info.split(",")
		elif code == ABSTRACT:
			abstract = info
		elif code == INDEX:
			paperid = s[6:]
		elif code == CITES:
			cites.append(info)
		elif code == VENUE:
			venue = info
		elif code == YEAR:
			year = info
	elif s == "\n":
		if(paperid!=""):
			# For no repetitions in authors for a paper
			no_rep_authors = []
			for author in authors:
				if author not in no_rep_authors:
					author = formatstring(author)
					no_rep_authors.append(author.strip())

			for author in no_rep_authors:
				if author!="":
					cur.execute("INSERT INTO contribution (Id,contrib,Author_name) VALUES(%s,%s,%s) ON CONFLICT DO NOTHING",(int(paperid),no_rep_authors.index(author),author))	

			# Checking no repetitions in cites
			no_rep_cites = []	
			for cite in cites:
				if cite not in no_rep_cites:
					no_rep_cites.append(cite)
		
			for cite in no_rep_cites:
				# A paper cannot cite itself
				if cite != "" and cite!=paperid:
					cur.execute("INSERT INTO Cites (Id_1,CitesId_2) VALUES(%s,%s) ON CONFLICT DO NOTHING",(int(paperid),int(cite)))
		title = ""
		authors = []
		abstract = ""
		paperid = ""
		year = ""
		venue = ""
		cites = []
			
	s = file.readline()

conn.commit()

# Closing the connection
conn.close()

