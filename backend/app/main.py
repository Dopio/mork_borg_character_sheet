from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.endpoints.characters import router as characters_router
from core.database import engine, Base


app = FastAPI(
    title="MÖRK BORG Character Sheet API",
    description="API для создания и управления персонажами MÖRK BORG",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(characters_router)


@app.get("/")
async def root():
    return {
        "message": "⚔️ MÖRK BORG Character Sheet API ⚔️",
        "docs": "/docs"
    }


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
