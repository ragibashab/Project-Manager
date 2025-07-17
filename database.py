import sqlite3

def create_database():
    """
    Creates the database and the leads table if they don't already exist.
    """
    conn = sqlite3.connect("leads.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY,
            name TEXT,
            company TEXT,
            email TEXT,
            url TEXT,
            industry TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_lead(lead):
    """
    Inserts a lead into the database.
    """
    conn = sqlite3.connect("leads.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO leads (name, company, email, url, industry)
        VALUES (?, ?, ?, ?, ?)
    """, (lead["name"], lead["company"], lead["email"], lead["url"], lead["industry"]))
    conn.commit()
    conn.close()

def get_all_leads():
    """
    Returns all leads from the database.
    """
    conn = sqlite3.connect("leads.db")
    c = conn.cursor()
    c.execute("SELECT * FROM leads")
    leads = c.fetchall()
    conn.close()
    return leads
