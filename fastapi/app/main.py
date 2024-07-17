import socket
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Message": "Hello world from {}".format(socket.gethostname())}