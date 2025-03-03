from fastapi import FastAPI

app = FastAPI()

@app.get("/ok")
def read_root():
    return {"message": "Everything is OK"}

@app.get("/hello")
async def hello_endpoint(name: str = 'World'):
    return {"message": f"Hello, {name}"}