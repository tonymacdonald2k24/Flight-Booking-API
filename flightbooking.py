from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def first_flight():
    return {'message': 'Welcome abord!'}