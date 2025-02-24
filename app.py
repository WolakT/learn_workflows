from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def greet():
    return "hello"


@app.get("/dupa/{id}/jasia")
def greet_with_id(id: int):
    return f"Hello {id}"
