import sqlite3

conn = sqlite3.connect('bam.db')
c = conn.cursor()

# Drop column paper_description from research_papers table
# c.execute('''
# ALTER TABLE research_papers
# DROP COLUMN paper_description
# ''')

# add publication column to research_papers table to store publication name as string. This column can be empty

c.execute('''
ALTER TABLE research_papers
ADD COLUMN paper_publication TEXT
''')

# close the connection
conn.commit()
conn.close()

