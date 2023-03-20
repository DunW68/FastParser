from fastapi import FastAPI
from FastParser.parsers.routing import parser


app = FastAPI()
app.mount("/parsers", parser)


@app.get("/")
def main_page():
    return "Hello parser!"
