import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="resume_screening",
        user="postgres",
        password="priyansh",  # change this
        host="localhost",
        port="5432"
    )

def insert_candidate_data(data):
    import psycopg2
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO candidates (
                filename, name, email, phone,
                matched_keywords, match_score, full_resume
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (email) DO UPDATE SET
                filename = EXCLUDED.filename,
                name = EXCLUDED.name,
                phone = EXCLUDED.phone,
                matched_keywords = EXCLUDED.matched_keywords,
                match_score = EXCLUDED.match_score,
                full_resume = EXCLUDED.full_resume;
        """, (
            data["filename"],
            data["name"],
            data["email"],
            data["phone"],
            data["matched_keywords"],
            data["match_score"],
            data["full_resume"]
        ))

        conn.commit()
        print("✅ Candidate inserted/updated.")

    except psycopg2.Error as e:
        print(f"❌ Error inserting candidate: {e}")

    finally:
        cur.close()
        conn.close()
