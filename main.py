from fastapi import FastAPI

from router.routes import router


app = FastAPI()


app.include_router(router)



@app.get("/")
def home():

    return {
        "message": "Website summarizer running"
    }