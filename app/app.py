from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from psycopg2 import connect
import os
from fastapi.responses import JSONResponse
app = FastAPI()

print(os.getenv("ENV"))
if os.getenv("ENV") == 'DEV':
    DB_HOST = "localhost"
    PG_USER = os.getenv("PG_USER")
elif os.getenv("ENV") == 'TEST':
    DB_HOST = "db"
    PG_USER = "admin"
else:
    DB_HOST = "db"
    PG_USER = "admin"

def connect_to_db():
    # Replace with your actual database connection details 
    return connect(
        host=DB_HOST,
        port=5432,
        database="postgres",
        user=PG_USER,
        password="postgres"
    )

@app.get("/", response_class=HTMLResponse)
def get_root():
    return '''
    <html>
        <head>
            <title>Basic App</title>
        </head>
        <body>
        <h1>Welcome to the Basic App</h1>
        <p>This is a simple FastAPI application, created by EntropyScourge, for the purposes of demonstrating a simple CI/CD pipeline.</p>
        <p><a href="/posts">View Posts</a></p>
    '''

@app.get("/posts", response_class=HTMLResponse)
def get_posts():
    connection = connect_to_db()
    cursor = connection.cursor()
    cursor.execute("SELECT title, content FROM posts;")
    posts = cursor.fetchall()
    post_html = '<br>'.join(['<h2>{}</h2> <p>{}</p>'.format(title, content) for title, content in posts])
    cursor.close()
    connection.close()

    return '''
    <html>
        <head>
            <title>Posts</title>
        </head>
        <body>
        <h1>Posts</h1>
        <p>{posts}</p>
        <p><a href="/">Back to Home</a></p>
    '''.format(posts=post_html)

@app.get("/health", response_class=JSONResponse)
def health_check():
    try:
        connection = connect_to_db()
        connection.close()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}