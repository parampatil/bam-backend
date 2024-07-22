import sqlite3

def create_tables():
    conn = sqlite3.connect('bam.db')
    c = conn.cursor()

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

    # Create research papers table
    c.execute('''
    CREATE TABLE research_papers (
        paper_id INTEGER PRIMARY KEY AUTOINCREMENT,
        paper_created_by_user_id INTEGER NOT NULL,
        short_paper_title TEXT NOT NULL,
        short_description TEXT NOT NULL,
        preview_image TEXT,
        authors_ids TEXT NOT NULL,
        paper_pdf_link TEXT NOT NULL,
        paper_description TEXT NOT NULL,
        FOREIGN KEY (paper_created_by_user_id) REFERENCES users(user_id)
    )
    ''')

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
