from fastapi import FastAPI

app = FastAPI()

@app.get("/v1/users/register")
def register():
    return '{"Hello": "World"}'