from fastapi import FastAPI
from FastParser.parsers.routing import parser
from fastapi.responses import FileResponse


app = FastAPI()
app.mount("/parsers", parser)


@app.get("/")
def main_page():
    return FileResponse("FastParser/python-hello-world.webp")
