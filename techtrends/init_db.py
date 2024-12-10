import sqlite3
from datetime import datetime

# Connect to the database
connection = sqlite3.connect('database.db')

# Read and execute the schema SQL file
with open('schema.sql') as f:
    connection.executescript(f.read())

# Insert initial data into the posts table
cur = connection.cursor()

# Sample posts with 'created' timestamps
cur.execute("INSERT INTO posts (title, content, created) VALUES (?, ?, ?)",
            ('2020 CNCF Annual Report',
             'The Cloud Native Computing Foundation (CNCF) annual report for 2020 is now available.',
             datetime.utcnow())
            )

cur.execute("INSERT INTO posts (title, content, created) VALUES (?, ?, ?)",
            ('KubeCon + CloudNativeCon 2021',
             'The CNCF flagship conference gathers leading technologists.',
             datetime.utcnow())
            )

cur.execute("INSERT INTO posts (title, content, created) VALUES (?, ?, ?)",
            ('Kubernetes v1.20 Release Notes',
             'Kubernetes is an open source container orchestration engine.',
             datetime.utcnow())
            )

cur.execute("INSERT INTO posts (title, content, created) VALUES (?, ?, ?)",
            ('CNCF Cloud Native Interactive Landscape',
             'This landscape maps cloud native technologies.',
             datetime.utcnow())
            )

cur.execute("INSERT INTO posts (title, content, created) VALUES (?, ?, ?)",
            ('CNCF Cloud Native Definition v1.0',
             'Cloud native technologies empower organizations to build scalable apps.',
             datetime.utcnow())
            )

cur.execute("INSERT INTO posts (title, content, created) VALUES (?, ?, ?)",
            ('Kubernetes Certification',
             'CNCF and Linux Foundation offer Kubernetes certifications.',
             datetime.utcnow())
            )

# Commit changes and close the connection
connection.commit()
connection.close()
