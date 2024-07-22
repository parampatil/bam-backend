import sqlite3
from werkzeug.security import generate_password_hash

def populate_db():
    conn = sqlite3.connect('bam.db')
    c = conn.cursor()

    # Sample data for users
    users = [
        ('john.doe@example.com', 'John', 'Doe', generate_password_hash('password1', method='pbkdf2:sha256'), 'image1.jpg', 'user', 'Harvard University', '1,2'),
        ('jane.smith@example.com', 'Jane', 'Smith', generate_password_hash('password2', method='pbkdf2:sha256'), 'image2.jpg', 'team', 'Stanford University', '2,3'),
        ('bob.jones@example.com', 'Bob', 'Jones', generate_password_hash('password3', method='pbkdf2:sha256'), 'image3.jpg', 'admin', 'MIT', '1,3')
    ]
    
    # Insert sample users
    c.executemany('''
    INSERT INTO users (user_email, user_first_name, user_last_name, user_password, user_image, user_access, university, collections_paper_ids)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', users)

    # Sample data for authors
    authors = [
        ('Alice', 'Johnson', 'alice.jpg', 'http://alicejohnson.com'),
        ('David', 'Brown', 'david.jpg', 'http://davidbrown.com')
    ]
    
    # Insert sample authors
    c.executemany('''
    INSERT INTO authors (author_first_name, author_last_name, author_image, author_website)
    VALUES (?, ?, ?, ?)
    ''', authors)

    # Sample data for research papers
    research_papers = [
        (1, 'Sample Paper 1', 'This is a sample paper 1.', 'paper1.jpg', '1', 'http://example.com/sample1.pdf', '<p>This is the full description of sample paper 1.</p>'),
        (2, 'Sample Paper 2', 'This is a sample paper 2.', 'paper2.jpg', '2', 'http://example.com/sample2.pdf', '<p>This is the full description of sample paper 2.</p>'),
        (3, 'Sample Paper 3', 'This is a sample paper 3.', 'paper3.jpg', '1,2', 'http://example.com/sample3.pdf', '<p>This is the full description of sample paper 3.</p>')
    ]

    # Insert sample research papers
    c.executemany('''
    INSERT INTO research_papers (paper_created_by_user_id, short_paper_title, short_description, preview_image, authors_ids, paper_pdf_link, paper_description)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', research_papers)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    populate_db()
    print("Sample data inserted successfully.")
