import sqlite3
from werkzeug.security import generate_password_hash
import json
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

    # Sample data for research papers (including paper_editor, paper_html, and paper_css)
    research_papers = [
        (1, 'Sample Paper 1', 'Sample 1 desc.', 'p1.jpg', '1', 'http://example.com/sample1.pdf', 'Full desc 1', 'HTML 1', 'CSS 1', '2024-01-01', json.dumps({
            'id': 1,
            'title': 'Sample 1',
            'date': '2024-01-01'
        })),
        
        (2, 'Sample Paper 2', 'Sample 2 desc.', 'p2.jpg', '2', 'http://example.com/sample2.pdf', 'Full desc 2', 'HTML 2', 'CSS 2', '2024-02-01', json.dumps({
            'id': 2,
            'title': 'Sample 2',
            'date': '2024-02-01'
        })),
        
        (3, 'Sample Paper 3', 'Sample 3 desc.', 'p3.jpg', '1,2', 'http://example.com/sample3.pdf', 'Full desc 3', 'HTML 3', 'CSS 3', '2024-03-01', json.dumps({
            'id': 3,
            'title': 'Sample 3',
            'date': '2024-03-01'
        }))
    ]

    c.executemany('''
        INSERT INTO research_papers (
            paper_created_by_user_id, 
            short_paper_title, 
            short_description, 
            preview_image, 
            authors_ids, 
            paper_pdf_link, 
            paper_description, 
            paper_html, 
            paper_css, 
            paper_publishDate, 
            paper_editor
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', research_papers)


    conn.commit()
    conn.close()

if __name__ == '__main__':
    populate_db()
    print("Sample data inserted successfully.")
