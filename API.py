from fastapi import FastAPI
# from manager import Manager
from manager import Manager
app = FastAPI()

manager = Manager()


@app.get("/tweets")
def read_root():
    return manager.dal.get_all_documents()

@app.get("/tweets_tow_weapons")
def read_root():
    return manager.dal.get_all_documents()
