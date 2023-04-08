from fastapi import FastAPI
from fastparser.parsers.article_parser.routing import parser
from fastapi.responses import FileResponse
import uvicorn


app = FastAPI()
app.mount("/parsers", parser)


@app.get("/")
def main_page() -> FileResponse:
    return FileResponse("python-hello-world.webp")


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
