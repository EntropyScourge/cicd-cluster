from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from psycopg2 import connect

app = FastAPI()

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
    connection = connect(
        dbname="postgresdb",
        user="admin",
        password="adminpassword",
        host="postgres",
        port="5432"
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts;")
    posts = cursor.fetchall()
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
    '''.format(posts=posts)