from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from app.database import get_db
from app.models.schemas import (
    UserCreate, UserUpdate,
    MovieCreate, MovieUpdate,
    GenreCreate, GenreUpdate,
    ActorCreate, ActorUpdate,
    DirectorCreate, DirectorUpdate,
    ActorDirectorCreate,
    PlatformCreate, PlatformUpdate,
    BulkPropertyUpdate
)
from typing import List
import csv
import io

router = APIRouter(prefix="/nodes", tags=["Nodes"])
db = get_db()


# ════════════════════════════════════════════════════════════════
# USER
# ════════════════════════════════════════════════════════════════

@router.post("/users", summary="Crear usuario (1 label)")
def create_user(user: UserCreate):
    query = """
    CREATE (u:User {
        userId: $userId, name: $name, age: $age, country: $country,
        email: $email, createdAt: date($createdAt), isActive: $isActive,
        preferredGenres: $preferredGenres, preferredDecades: $preferredDecades,
        preferredThemes: $preferredThemes
    }) RETURN u
    """
    with db.session() as s:
        result = s.run(query, **user.model_dump(mode="json"))
        record = result.single()
        if not record:
            raise HTTPException(status_code=400, detail="Error al crear usuario")
        return dict(record["u"])


@router.get("/users", summary="Obtener todos los usuarios")
def get_users(country: str = None, isActive: bool = None, limit: int = 50):
    filters = []
    params = {"limit": limit}
    if country:
        filters.append("u.country = $country")
        params["country"] = country
    if isActive is not None:
        filters.append("u.isActive = $isActive")
        params["isActive"] = isActive
    where = ("WHERE " + " AND ".join(filters)) if filters else ""
    query = f"MATCH (u:User) {where} RETURN u LIMIT $limit"
    with db.session() as s:
        result = s.run(query, **params)
        return [dict(r["u"]) for r in result]


@router.patch("/users/bulk/update", summary="Actualizar propiedades en múltiples usuarios")
def bulk_update_users(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"u.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (u:User) WHERE u.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(u) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/users/bulk/delete", summary="Eliminar múltiples usuarios por país")
def bulk_delete_users(country: str):
    with db.session() as s:
        result = s.run(
            "MATCH (u:User {country: $country}) DETACH DELETE u RETURN count(u) as deleted",
            country=country
        )
        return {"deleted": result.single()["deleted"]}


@router.delete("/users/bulk/properties", summary="Eliminar propiedades de múltiples usuarios")
def bulk_delete_user_properties(filter_property: str, filter_value: str, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"u.{p}" for p in properties])
    query = f"""
    MATCH (u:User)
    WHERE u.{filter_property} = $filter_value
       OR u.{filter_property} = toInteger($filter_value)
       OR u.{filter_property} = toFloat($filter_value)
    REMOVE {remove_clause}
    RETURN count(u) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=filter_value)
        return {"updated": result.single()["updated"]}



@router.get("/users/{userId}", summary="Obtener un usuario por ID")
def get_user(userId: int):
    with db.session() as s:
        result = s.run("MATCH (u:User {userId: $userId}) RETURN u", userId=userId)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return dict(record["u"])


@router.patch("/users/{userId}", summary="Actualizar propiedades de un usuario")
def update_user(userId: int, data: UserUpdate):
    updates = {k: v for k, v in data.model_dump(mode="json").items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No hay propiedades para actualizar")
    set_clause = ", ".join([f"u.{k} = ${k}" for k in updates])
    query = f"MATCH (u:User {{userId: $userId}}) SET {set_clause} RETURN u"
    with db.session() as s:
        result = s.run(query, userId=userId, **updates)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return dict(record["u"])




@router.delete("/users/{userId}", summary="Eliminar un usuario")
def delete_user(userId: int):
    with db.session() as s:
        result = s.run(
            "MATCH (u:User {userId: $userId}) DETACH DELETE u RETURN count(u) as deleted",
            userId=userId
        )
        return {"deleted": result.single()["deleted"]}


    
    

@router.delete("/users/{userId}/properties", summary="Eliminar propiedades de 1 usuario")
def delete_user_properties(userId: int, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"u.{p}" for p in properties])
    query = f"MATCH (u:User {{userId: $userId}}) REMOVE {remove_clause} RETURN u"
    with db.session() as s:
        result = s.run(query, userId=userId)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return dict(record["u"])


# ════════════════════════════════════════════════════════════════
# MOVIE
# ════════════════════════════════════════════════════════════════

@router.post("/movies", summary="Crear película (1 label)")
def create_movie(movie: MovieCreate):
    query = """
    CREATE (m:Movie {
        movieId: $movieId, title: $title, year: $year, avgRating: $avgRating,
        duration: $duration, budget: $budget, languages: $languages,
        releaseDate: date($releaseDate), tagline: $tagline
    }) RETURN m
    """
    with db.session() as s:
        result = s.run(query, **movie.model_dump(mode="json"))
        record = result.single()
        if not record:
            raise HTTPException(status_code=400, detail="Error al crear película")
        return dict(record["m"])


@router.get("/movies", summary="Obtener todas las películas con filtros")
def get_movies(year: int = None, min_rating: float = None, limit: int = 50):
    filters = []
    params = {"limit": limit}
    if year:
        filters.append("m.year = $year")
        params["year"] = year
    if min_rating:
        filters.append("m.avgRating >= $min_rating")
        params["min_rating"] = min_rating
    where = ("WHERE " + " AND ".join(filters)) if filters else ""
    query = f"MATCH (m:Movie) {where} RETURN m LIMIT $limit"
    with db.session() as s:
        result = s.run(query, **params)
        return [dict(r["m"]) for r in result]


@router.patch("/movies/bulk/update", summary="Actualizar propiedades en múltiples películas")
def bulk_update_movies(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"m.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (m:Movie) WHERE m.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(m) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/movies/bulk/delete", summary="Eliminar múltiples películas por año")
def bulk_delete_movies(year: int):
    with db.session() as s:
        result = s.run(
            "MATCH (m:Movie {year: $year}) DETACH DELETE m RETURN count(m) as deleted",
            year=year
        )
        return {"deleted": result.single()["deleted"]}



@router.get("/movies/{movieId}", summary="Obtener una película por ID")
def get_movie(movieId: int):
    with db.session() as s:
        result = s.run("MATCH (m:Movie {movieId: $movieId}) RETURN m", movieId=movieId)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Película no encontrada")
        return dict(record["m"])


@router.patch("/movies/{movieId}", summary="Actualizar propiedades de una película")
def update_movie(movieId: int, data: MovieUpdate):
    updates = {k: v for k, v in data.model_dump(mode="json").items() if v is not None}
    if not updates:
        raise HTTPException(status_code=400, detail="No hay propiedades para actualizar")
    set_clause = ", ".join([f"m.{k} = ${k}" for k in updates])
    query = f"MATCH (m:Movie {{movieId: $movieId}}) SET {set_clause} RETURN m"
    with db.session() as s:
        result = s.run(query, movieId=movieId, **updates)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Película no encontrada")
        return dict(record["m"])




@router.delete("/movies/{movieId}", summary="Eliminar una película")
def delete_movie(movieId: int):
    with db.session() as s:
        result = s.run(
            "MATCH (m:Movie {movieId: $movieId}) DETACH DELETE m RETURN count(m) as deleted",
            movieId=movieId
        )
        return {"deleted": result.single()["deleted"]}




# ════════════════════════════════════════════════════════════════
# GENRE
# ════════════════════════════════════════════════════════════════

@router.post("/genres", summary="Crear género (1 label)")
def create_genre(genre: GenreCreate):
    query = """
    CREATE (g:Genre {
        genreId: $genreId, name: $name, description: $description,
        isMainstream: $isMainstream, subgenres: $subgenres
    }) RETURN g
    """
    with db.session() as s:
        result = s.run(query, **genre.model_dump())
        return dict(result.single()["g"])


@router.get("/genres", summary="Obtener todos los géneros")
def get_genres(isMainstream: bool = None):
    params = {}
    where = ""
    if isMainstream is not None:
        where = "WHERE g.isMainstream = $isMainstream"
        params["isMainstream"] = isMainstream
    with db.session() as s:
        result = s.run(f"MATCH (g:Genre) {where} RETURN g", **params)
        return [dict(r["g"]) for r in result]


@router.get("/genres/{genreId}", summary="Obtener un género por ID")
def get_genre(genreId: int):
    with db.session() as s:
        result = s.run("MATCH (g:Genre {genreId: $genreId}) RETURN g", genreId=genreId)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Género no encontrado")
        return dict(record["g"])


@router.patch("/genres/{genreId}", summary="Actualizar un género")
def update_genre(genreId: int, data: GenreUpdate):
    updates = {k: v for k, v in data.model_dump().items() if v is not None}
    set_clause = ", ".join([f"g.{k} = ${k}" for k in updates])
    query = f"MATCH (g:Genre {{genreId: $genreId}}) SET {set_clause} RETURN g"
    with db.session() as s:
        result = s.run(query, genreId=genreId, **updates)
        return dict(result.single()["g"])


@router.delete("/genres/{genreId}", summary="Eliminar un género")
def delete_genre(genreId: int):
    with db.session() as s:
        result = s.run(
            "MATCH (g:Genre {genreId: $genreId}) DETACH DELETE g RETURN count(g) as deleted",
            genreId=genreId
        )
        return {"deleted": result.single()["deleted"]}


# ════════════════════════════════════════════════════════════════
# ACTOR
# ════════════════════════════════════════════════════════════════

@router.post("/actors", summary="Crear actor (1 label)")
def create_actor(actor: ActorCreate):
    query = """
    CREATE (a:Actor {
        actorId: $actorId, name: $name, birthDate: date($birthDate),
        nationality: $nationality, isActive: $isActive, oscars: $oscars
    }) RETURN a
    """
    with db.session() as s:
        result = s.run(query, **actor.model_dump(mode="json"))
        return dict(result.single()["a"])


@router.get("/actors", summary="Obtener actores con filtros")
def get_actors(nationality: str = None, isActive: bool = None, limit: int = 50):
    filters = []
    params = {"limit": limit}
    if nationality:
        filters.append("a.nationality = $nationality")
        params["nationality"] = nationality
    if isActive is not None:
        filters.append("a.isActive = $isActive")
        params["isActive"] = isActive
    where = ("WHERE " + " AND ".join(filters)) if filters else ""
    with db.session() as s:
        result = s.run(f"MATCH (a:Actor) {where} RETURN a LIMIT $limit", **params)
        return [dict(r["a"]) for r in result]


@router.patch("/actors/bulk/update", summary="Actualizar múltiples actores")
def bulk_update_actors(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"a.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (a:Actor) WHERE a.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(a) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/actors/bulk/delete", summary="Eliminar múltiples actores por nacionalidad")
def bulk_delete_actors(nationality: str):
    with db.session() as s:
        result = s.run(
            "MATCH (a:Actor {nationality: $nationality}) DETACH DELETE a RETURN count(a) as deleted",
            nationality=nationality
        )
        return {"deleted": result.single()["deleted"]}



@router.get("/actors/{actorId}", summary="Obtener un actor por ID")
def get_actor(actorId: int):
    with db.session() as s:
        result = s.run("MATCH (a:Actor {actorId: $actorId}) RETURN a", actorId=actorId)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Actor no encontrado")
        return dict(record["a"])


@router.patch("/actors/{actorId}", summary="Actualizar un actor")
def update_actor(actorId: int, data: ActorUpdate):
    updates = {k: v for k, v in data.model_dump(mode="json").items() if v is not None}
    set_clause = ", ".join([f"a.{k} = ${k}" for k in updates])
    query = f"MATCH (a:Actor {{actorId: $actorId}}) SET {set_clause} RETURN a"
    with db.session() as s:
        result = s.run(query, actorId=actorId, **updates)
        return dict(result.single()["a"])



@router.delete("/actors/{actorId}", summary="Eliminar un actor")
def delete_actor(actorId: int):
    with db.session() as s:
        result = s.run(
            "MATCH (a:Actor {actorId: $actorId}) DETACH DELETE a RETURN count(a) as deleted",
            actorId=actorId
        )
        return {"deleted": result.single()["deleted"]}





# ════════════════════════════════════════════════════════════════
# DIRECTOR
# ════════════════════════════════════════════════════════════════

@router.post("/directors", summary="Crear director (1 label)")
def create_director(director: DirectorCreate):
    query = """
    CREATE (d:Director {
        directorId: $directorId, name: $name, gender: $gender,
        birthDate: date($birthDate), nationality: $nationality
    }) RETURN d
    """
    with db.session() as s:
        result = s.run(query, **director.model_dump(mode="json"))
        return dict(result.single()["d"])


@router.get("/directors", summary="Obtener directores con filtros")
def get_directors(nationality: str = None, limit: int = 50):
    params = {"limit": limit}
    where = ""
    if nationality:
        where = "WHERE d.nationality = $nationality"
        params["nationality"] = nationality
    with db.session() as s:
        result = s.run(f"MATCH (d:Director) {where} RETURN d LIMIT $limit", **params)
        return [dict(r["d"]) for r in result]


@router.patch("/directors/bulk/update", summary="Actualizar múltiples directores")
def bulk_update_directors(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"d.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (d:Director) WHERE d.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(d) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/directors/bulk/delete", summary="Eliminar múltiples directores por nacionalidad")
def bulk_delete_directors(nationality: str):
    with db.session() as s:
        result = s.run(
            "MATCH (d:Director {nationality: $nationality}) DETACH DELETE d RETURN count(d) as deleted",
            nationality=nationality
        )
        return {"deleted": result.single()["deleted"]}



@router.get("/directors/{directorId}", summary="Obtener un director por ID")
def get_director(directorId: int):
    with db.session() as s:
        result = s.run("MATCH (d:Director {directorId: $directorId}) RETURN d", directorId=directorId)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Director no encontrado")
        return dict(record["d"])


@router.patch("/directors/{directorId}", summary="Actualizar un director")
def update_director(directorId: int, data: DirectorUpdate):
    updates = {k: v for k, v in data.model_dump(mode="json").items() if v is not None}
    set_clause = ", ".join([f"d.{k} = ${k}" for k in updates])
    query = f"MATCH (d:Director {{directorId: $directorId}}) SET {set_clause} RETURN d"
    with db.session() as s:
        result = s.run(query, directorId=directorId, **updates)
        return dict(result.single()["d"])




@router.delete("/directors/{directorId}", summary="Eliminar un director")
def delete_director(directorId: int):
    with db.session() as s:
        result = s.run(
            "MATCH (d:Director {directorId: $directorId}) DETACH DELETE d RETURN count(d) as deleted",
            directorId=directorId
        )
        return {"deleted": result.single()["deleted"]}





# ════════════════════════════════════════════════════════════════
# ACTOR + DIRECTOR (multi-label)
# ════════════════════════════════════════════════════════════════

@router.post("/actor-directors", summary="Crear nodo Actor+Director (2 labels)")
def create_actor_director(person: ActorDirectorCreate):
    query = """
    CREATE (p:Actor:Director {
        actorId: $actorId, directorId: $directorId, name: $name,
        gender: $gender, birthDate: date($birthDate),
        nationality: $nationality, isActive: $isActive, oscars: $oscars
    }) RETURN p
    """
    with db.session() as s:
        result = s.run(query, **person.model_dump(mode="json"))
        return dict(result.single()["p"])


@router.get("/actor-directors", summary="Obtener todos los nodos Actor+Director")
def get_actor_directors():
    with db.session() as s:
        result = s.run("MATCH (p:Actor:Director) RETURN p")
        return [dict(r["p"]) for r in result]


# ════════════════════════════════════════════════════════════════
# PLATFORM
# ════════════════════════════════════════════════════════════════

@router.post("/platforms", summary="Crear plataforma (1 label)")
def create_platform(platform: PlatformCreate):
    query = """
    CREATE (p:Platform {
        platformId: $platformId, name: $name, country: $country,
        isPaid: $isPaid, monthlyCost: $monthlyCost, launchedAt: date($launchedAt)
    }) RETURN p
    """
    with db.session() as s:
        result = s.run(query, **platform.model_dump(mode="json"))
        return dict(result.single()["p"])


@router.get("/platforms", summary="Obtener todas las plataformas")
def get_platforms(isPaid: bool = None):
    params = {}
    where = ""
    if isPaid is not None:
        where = "WHERE p.isPaid = $isPaid"
        params["isPaid"] = isPaid
    with db.session() as s:
        result = s.run(f"MATCH (p:Platform) {where} RETURN p", **params)
        return [dict(r["p"]) for r in result]


@router.get("/platforms/{platformId}", summary="Obtener una plataforma por ID")
def get_platform(platformId: int):
    with db.session() as s:
        result = s.run("MATCH (p:Platform {platformId: $platformId}) RETURN p", platformId=platformId)
        record = result.single()
        if not record:
            raise HTTPException(status_code=404, detail="Plataforma no encontrada")
        return dict(record["p"])


@router.patch("/platforms/{platformId}", summary="Actualizar una plataforma")
def update_platform(platformId: int, data: PlatformUpdate):
    updates = {k: v for k, v in data.model_dump(mode="json").items() if v is not None}
    set_clause = ", ".join([f"p.{k} = ${k}" for k in updates])
    query = f"MATCH (p:Platform {{platformId: $platformId}}) SET {set_clause} RETURN p"
    with db.session() as s:
        result = s.run(query, platformId=platformId, **updates)
        return dict(result.single()["p"])


@router.delete("/platforms/{platformId}", summary="Eliminar una plataforma")
def delete_platform(platformId: int):
    with db.session() as s:
        result = s.run(
            "MATCH (p:Platform {platformId: $platformId}) DETACH DELETE p RETURN count(p) as deleted",
            platformId=platformId
        )
        return {"deleted": result.single()["deleted"]}


# ════════════════════════════════════════════════════════════════
# CARGA CSV
# ════════════════════════════════════════════════════════════════

@router.post("/csv/movies", summary="Cargar películas desde CSV")
async def load_movies_csv(file: UploadFile = File(...)):
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
    created = 0
    with db.session() as s:
        for row in reader:
            s.run("""
                MERGE (m:Movie {movieId: toInteger($movieId)})
                SET m.title = $title,
                    m.year = toInteger($year),
                    m.avgRating = toFloat($avgRating),
                    m.duration = toInteger($duration),
                    m.budget = toFloat($budget),
                    m.languages = split($languages, '|'),
                    m.releaseDate = date($releaseDate),
                    m.tagline = $tagline
            """, **row)
            created += 1
    return {"loaded": created}


@router.post("/csv/users", summary="Cargar usuarios desde CSV")
async def load_users_csv(file: UploadFile = File(...)):
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
    created = 0
    with db.session() as s:
        for row in reader:
            s.run("""
                MERGE (u:User {userId: toInteger($userId)})
                SET u.name = $name,
                    u.age = toInteger($age),
                    u.country = $country,
                    u.email = $email,
                    u.createdAt = date($createdAt),
                    u.isActive = ($isActive = 'true'),
                    u.preferredGenres = split($preferredGenres, '|'),
                    u.preferredDecades = split($preferredDecades, '|'),
                    u.preferredThemes = split($preferredThemes, '|')
            """, **row)
            created += 1
    return {"loaded": created}


@router.post("/csv/actors", summary="Cargar actores desde CSV")
async def load_actors_csv(file: UploadFile = File(...)):
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
    created = 0
    with db.session() as s:
        for row in reader:
            s.run("""
                MERGE (a:Actor {actorId: toInteger($actorId)})
                SET a.name = $name,
                    a.birthDate = date($birthDate),
                    a.nationality = $nationality,
                    a.isActive = ($isActive = 'true'),
                    a.oscars = toInteger($oscars)
            """, **row)
            created += 1
    return {"loaded": created}


@router.post("/csv/movies-with-director", summary="Cargar películas con director desde CSV")
async def load_movies_with_director_csv(file: UploadFile = File(...)):
    content = await file.read()
    reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
    created = 0
    with db.session() as s:
        for row in reader:
            s.run("""
                // Crear o actualizar Movie
                MERGE (m:Movie {movieId: toInteger($movieId)})
                SET m.title = $title,
                    m.year = toInteger($year),
                    m.avgRating = toFloat($avgRating),
                    m.duration = toInteger($duration),
                    m.budget = toFloat($budget),
                    m.languages = split($languages, '|'),
                    m.releaseDate = date($releaseDate),
                    m.tagline = $tagline

                // Crear o actualizar Director
                MERGE (d:Director {directorId: toInteger($directorId)})
                SET d.name = $directorName,
                    d.gender = $directorGender,
                    d.birthDate = date($directorBirthDate),
                    d.nationality = $directorNationality

                // Crear relación DIRECTED
                MERGE (d)-[r:DIRECTED]->(m)
                SET r.fee = toFloat($fee),
                    r.nominated = ($nominated = 'true'),
                    r.startDate = date($startDate)
            """, **row)
            created += 1
    return {"loaded": created}