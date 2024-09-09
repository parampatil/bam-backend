import sqlite3

def create_tables():
    conn = sqlite3.connect('bam.db')
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS users')
    # Create users table
    c.execute('''
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL UNIQUE,
        user_first_name TEXT NOT NULL,
        user_last_name TEXT NOT NULL,
        user_password TEXT NOT NULL,
        user_image TEXT,
        user_registration_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        user_access TEXT CHECK(user_access IN ('user', 'team', 'admin')) NOT NULL,
        university TEXT,
        collections_paper_ids TEXT
    )
    ''')

    c.execute('DROP TABLE IF EXISTS research_papers')

    # Create research papers table with paper_html and paper_css
    c.execute('''
    CREATE TABLE research_papers (
        paper_id INTEGER PRIMARY KEY AUTOINCREMENT,
        paper_created_by_user_id INTEGER,
        short_paper_title TEXT,
        short_description TEXT,
        preview_image TEXT,
        authors_ids TEXT,
        paper_pdf_link TEXT,
        paper_description TEXT,
        paper_html TEXT,         
        paper_css TEXT,            
        paper_publishDate TEXT,
        paper_editor JSON, 
        FOREIGN KEY (paper_created_by_user_id) REFERENCES users(user_id)
    )
''')


    # Verify the table structure
    c.execute('PRAGMA table_info(research_papers)')
    columns = c.fetchall()

    # Print the column details
    for column in columns:
        print(column)





    c.execute('DROP TABLE IF EXISTS authors')


    # Create authors table
    c.execute('''
    CREATE TABLE authors (
        author_id INTEGER PRIMARY KEY AUTOINCREMENT,
        author_first_name TEXT NOT NULL,
        author_last_name TEXT NOT NULL,
        author_image TEXT,
        author_website TEXT
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
    print("Database and tables created successfully.")
