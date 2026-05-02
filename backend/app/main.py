from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import nodes, relationships, queries

app = FastAPI(
    title="CineGraph API",
    description="Backend para sistema de recomendación de películas con Neo4j — CC3089 Base de Datos 2",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(nodes.router)
app.include_router(relationships.router)
app.include_router(queries.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "CineGraph API corriendo"}


@app.get("/health", tags=["Health"])
def health():
    from app.database import get_db
    try:
        with get_db().session() as s:
            s.run("RETURN 1")
        return {"status": "ok", "neo4j": "conectado"}
    except Exception as e:
        return {"status": "error", "neo4j": str(e)}