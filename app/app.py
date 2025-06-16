from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from psycopg2 import connect

app = FastAPI()

def connect_to_db():
    # Replace with your actual database connection details 
    return connect(
        host="db",
        port=5432,
        database="postgres",
        user="admin",
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