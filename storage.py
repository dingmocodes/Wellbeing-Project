import sqlite3

con = sqlite3.connect("prev_responses")
cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS responses
                        (response text, ai_resopnse text, prompt text)''')

# not currently used