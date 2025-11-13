from fastapi import FastAPI
from database import Base, engine
from routers import auth, users, admin

Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "is work /docs"}
