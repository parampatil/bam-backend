import sqlite3

conn = sqlite3.connect('bam.db')
c = conn.cursor()

# Drop column paper_description from research_papers table
c.execute('''
ALTER TABLE research_papers
DROP COLUMN paper_description
''')

# close the connection
conn.commit()
conn.close()