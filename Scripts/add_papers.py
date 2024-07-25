import sqlite3


def add_paper():
    conn = sqlite3.connect('../bam.db')
    c = conn.cursor()

    c.execute("DELETE from research_papers")

    # Sample data for research papers
    research_papers = [
        (1,
         'Are Vision Transformers More Data Hungry Than Newborn Visual Systems?',
         'Vision transformers (ViTs) are top-performing models on many computer vision benchmarks and can accurately predict human behavior on object recognition tasks. However, researchers question the value of using ViTs as models of biological learning because ViTs are thought to be more “data hungry” than brains, with ViTs requiring more training data to reach similar levels of performance.',
         'https://dummyimage.com/16:9x300&text=Research+Paper+1',
         '18,17,16',
         'https://static1.squarespace.com/static/639b62c102544464637767b3/t/64ebbc486a5337765f5b9cbe/1693170762344/Wood+%26+Wood+%282021%29_JEPG.pdf',
         '<p>This is the full description of sample paper 1.</p>'),
        (2,
         'A Simple Framework for Contrastive Learning of Visual Representations',
            'Contrastive learning has become a popular approach for learning visual representations. However, the design of contrastive learning frameworks is often complex and requires careful tuning of hyperparameters. In this paper, we propose a simple framework for contrastive learning that achieves state-of-the-art performance on a range of visual recognition tasks.',
            'https://dummyimage.com/16:9x300&text=Research+Paper+2',
            '16,17',
            'https://onlinelibrary.wiley.com/doi/pdf/10.1111/cogs.13021',
            '<p>This is the full description of sample paper 2.</p>'),
        (3,
            'A Simple Framework for Contrastive Learning of Visual Representations',
            'Contrastive learning has become a popular approach for learning visual representations. However, the design of contrastive learning frameworks is often complex and requires careful tuning of hyperparameters. In this paper, we propose a simple framework for contrastive learning that achieves state-of-the-art performance on a range of visual recognition tasks.',
            'https://dummyimage.com/16:9x300&text=Research+Paper+3',
            '19,16,17,18',
            'https://onlinelibrary.wiley.com/doi/pdf/10.1111/cogs.13021',
            '<p>This is the full description of sample paper 3.</p>')

    ]

    # Insert sample research papers
    c.executemany('''
    INSERT INTO research_papers (paper_created_by_user_id, short_paper_title, short_description, preview_image, authors_ids, paper_pdf_link, paper_description)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', research_papers)

    conn.commit()
    conn.close()


if __name__ == '__main__':
    add_paper()
    print("Sample data inserted successfully.")
