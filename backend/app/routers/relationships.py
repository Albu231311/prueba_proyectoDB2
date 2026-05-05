from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.database import get_db
from app.models.schemas import (
    RatedRel, WatchedRel, ShouldWatchRel, LikesGenreRel,
    FollowsActorRel, FollowsDirectorRel, ActedInRel,
    CollaboratedWithRel, DirectedRel, InGenreRel,
    AvailableOnRel, PaysRel, RelPropertyUpdate, BulkPropertyUpdate
)

router = APIRouter(prefix="/relationships", tags=["Relationships"])
db = get_db()


# ════════════════════════════════════════════════════════════════
# RATED  (User -> Movie)
# ════════════════════════════════════════════════════════════════

@router.post("/rated", summary="Crear relación RATED (User -> Movie)")
def create_rated(rel: RatedRel):
    query = """
    MATCH (u:User {userId: $userId}), (m:Movie {movieId: $movieId})
    CREATE (u)-[r:RATED {rating: $rating, ratedAt: date($ratedAt), review: $review}]->(m)
    RETURN r
    """
    with db.session() as s:
        result = s.run(query, **rel.model_dump(mode="json"))
        if not result.single():
            raise HTTPException(status_code=404, detail="Usuario o película no encontrados")
        return {"message": "Relación RATED creada"}


@router.patch("/rated/bulk/update", summary="Actualizar múltiples relaciones RATED")
def bulk_update_rated(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH ()-[r:RATED]->() WHERE r.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/rated/bulk/update", summary="Eliminar propiedades de múltiples RATED")
def bulk_delete_rated_properties(filter_property: str, filter_value: str, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH ()-[r:RATED]->()
    WHERE r.{filter_property} = $filter_value
       OR r.{filter_property} = toInteger($filter_value)
       OR r.{filter_property} = toFloat($filter_value)
    REMOVE {remove_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=filter_value)
        return {"updated": result.single()["updated"]}


@router.delete("/rated/bulk/delete", summary="Eliminar múltiples relaciones RATED por rating mínimo")
def bulk_delete_rated(max_rating: float):
    with db.session() as s:
        result = s.run("""
            MATCH ()-[r:RATED]->() WHERE r.rating <= $max_rating
            DELETE r RETURN count(r) as deleted
        """, max_rating=max_rating)
        return {"deleted": result.single()["deleted"]}


@router.patch("/rated/{userId}/{movieId}", summary="Actualizar propiedades de RATED")
def update_rated(userId: int, movieId: int, data: RelPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (u:User {{userId: $userId}})-[r:RATED]->(m:Movie {{movieId: $movieId}})
    SET {set_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, userId=userId, movieId=movieId, **data.properties)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Relación RATED actualizada"}


@router.delete("/rated/{userId}/{movieId}/properties", summary="Eliminar propiedades de 1 RATED")
def delete_rated_properties(userId: int, movieId: int, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH (u:User {{userId: $userId}})-[r:RATED]->(m:Movie {{movieId: $movieId}})
    REMOVE {remove_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, userId=userId, movieId=movieId)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Propiedades eliminadas de RATED"}


@router.delete("/rated/{userId}/{movieId}", summary="Eliminar relación RATED")
def delete_rated(userId: int, movieId: int):
    with db.session() as s:
        result = s.run("""
            MATCH (u:User {userId: $userId})-[r:RATED]->(m:Movie {movieId: $movieId})
            DELETE r RETURN count(r) as deleted
        """, userId=userId, movieId=movieId)
        return {"deleted": result.single()["deleted"]}


# ════════════════════════════════════════════════════════════════
# WATCHED  (User -> Movie)
# ════════════════════════════════════════════════════════════════

@router.post("/watched", summary="Crear relación WATCHED (User -> Movie)")
def create_watched(rel: WatchedRel):
    query = """
    MATCH (u:User {userId: $userId}), (m:Movie {movieId: $movieId})
    CREATE (u)-[r:WATCHED {
        watchedAt: date($watchedAt),
        completedPercent: $completedPercent,
        rewatched: $rewatched
    }]->(m)
    RETURN r
    """
    with db.session() as s:
        result = s.run(query, **rel.model_dump(mode="json"))
        if not result.single():
            raise HTTPException(status_code=404, detail="Usuario o película no encontrados")
        return {"message": "Relación WATCHED creada"}


@router.patch("/watched/bulk/update", summary="Actualizar múltiples relaciones WATCHED")
def bulk_update_watched(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH ()-[r:WATCHED]->() WHERE r.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/watched/bulk/properties", summary="Eliminar propiedades de múltiples WATCHED")
def bulk_delete_watched_properties(filter_property: str, filter_value: str, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH ()-[r:WATCHED]->()
    WHERE r.{filter_property} = $filter_value
       OR r.{filter_property} = toInteger($filter_value)
       OR r.{filter_property} = toFloat($filter_value)
    REMOVE {remove_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=filter_value)
        return {"updated": result.single()["updated"]}


@router.delete("/watched/bulk/delete", summary="Eliminar múltiples WATCHED incompletos")
def bulk_delete_watched_incomplete(max_percent: float):
    with db.session() as s:
        result = s.run("""
            MATCH ()-[r:WATCHED]->() WHERE r.completedPercent < $max_percent
            DELETE r RETURN count(r) as deleted
        """, max_percent=max_percent)
        return {"deleted": result.single()["deleted"]}


@router.patch("/watched/{userId}/{movieId}", summary="Actualizar relación WATCHED")
def update_watched(userId: int, movieId: int, data: RelPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (u:User {{userId: $userId}})-[r:WATCHED]->(m:Movie {{movieId: $movieId}})
    SET {set_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, userId=userId, movieId=movieId, **data.properties)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Relación WATCHED actualizada"}


@router.delete("/watched/{userId}/{movieId}/properties", summary="Eliminar propiedades de 1 WATCHED")
def delete_watched_properties(userId: int, movieId: int, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH (u:User {{userId: $userId}})-[r:WATCHED]->(m:Movie {{movieId: $movieId}})
    REMOVE {remove_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, userId=userId, movieId=movieId)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Propiedades eliminadas de WATCHED"}


@router.delete("/watched/{userId}/{movieId}", summary="Eliminar relación WATCHED")
def delete_watched(userId: int, movieId: int):
    with db.session() as s:
        result = s.run("""
            MATCH (u:User {userId: $userId})-[r:WATCHED]->(m:Movie {movieId: $movieId})
            DELETE r RETURN count(r) as deleted
        """, userId=userId, movieId=movieId)
        return {"deleted": result.single()["deleted"]}


# ════════════════════════════════════════════════════════════════
# SHOULD_WATCH  (User -> Movie)
# ════════════════════════════════════════════════════════════════

@router.post("/should-watch", summary="Crear relación SHOULD_WATCH (User -> Movie)")
def create_should_watch(rel: ShouldWatchRel):
    query = """
    MATCH (u:User {userId: $userId}), (m:Movie {movieId: $movieId})
    MERGE (u)-[r:SHOULD_WATCH]->(m)
    SET r.recommendedAt = date($recommendedAt),
        r.confidenceScore = $confidenceScore,
        r.reason = $reason
    RETURN r
    """
    with db.session() as s:
        result = s.run(query, **rel.model_dump(mode="json"))
        if not result.single():
            raise HTTPException(status_code=404, detail="Usuario o película no encontrados")
        return {"message": "Relación SHOULD_WATCH creada"}


@router.patch("/should-watch/bulk/update", summary="Actualizar múltiples SHOULD_WATCH")
def bulk_update_should_watch(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH ()-[r:SHOULD_WATCH]->() WHERE r.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/should-watch/bulk/properties", summary="Eliminar propiedades de múltiples SHOULD_WATCH")
def bulk_delete_should_watch_properties(filter_property: str, filter_value: str, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH ()-[r:SHOULD_WATCH]->()
    WHERE r.{filter_property} = $filter_value
       OR r.{filter_property} = toInteger($filter_value)
       OR r.{filter_property} = toFloat($filter_value)
    REMOVE {remove_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=filter_value)
        return {"updated": result.single()["updated"]}


@router.delete("/should-watch/bulk/delete", summary="Eliminar SHOULD_WATCH con baja confianza")
def bulk_delete_should_watch(min_confidence: float):
    with db.session() as s:
        result = s.run("""
            MATCH ()-[r:SHOULD_WATCH]->() WHERE r.confidenceScore < $min_confidence
            DELETE r RETURN count(r) as deleted
        """, min_confidence=min_confidence)
        return {"deleted": result.single()["deleted"]}


@router.patch("/should-watch/{userId}/{movieId}", summary="Actualizar relación SHOULD_WATCH")
def update_should_watch(userId: int, movieId: int, data: RelPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (u:User {{userId: $userId}})-[r:SHOULD_WATCH]->(m:Movie {{movieId: $movieId}})
    SET {set_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, userId=userId, movieId=movieId, **data.properties)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Relación SHOULD_WATCH actualizada"}


@router.delete("/should-watch/{userId}/{movieId}/properties", summary="Eliminar propiedades de 1 SHOULD_WATCH")
def delete_should_watch_properties(userId: int, movieId: int, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH (u:User {{userId: $userId}})-[r:SHOULD_WATCH]->(m:Movie {{movieId: $movieId}})
    REMOVE {remove_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, userId=userId, movieId=movieId)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Propiedades eliminadas de SHOULD_WATCH"}


@router.delete("/should-watch/{userId}/{movieId}", summary="Eliminar relación SHOULD_WATCH")
def delete_should_watch(userId: int, movieId: int):
    with db.session() as s:
        result = s.run("""
            MATCH (u:User {userId: $userId})-[r:SHOULD_WATCH]->(m:Movie {movieId: $movieId})
            DELETE r RETURN count(r) as deleted
        """, userId=userId, movieId=movieId)
        return {"deleted": result.single()["deleted"]}


# ════════════════════════════════════════════════════════════════
# LIKES_GENRE  (User -> Genre)
# ════════════════════════════════════════════════════════════════

@router.post("/likes-genre", summary="Crear relación LIKES_GENRE (User -> Genre)")
def create_likes_genre(rel: LikesGenreRel):
    query = """
    MATCH (u:User {userId: $userId}), (g:Genre {genreId: $genreId})
    CREATE (u)-[r:LIKES_GENRE {weight: $weight, since: date($since), explicit: $explicit}]->(g)
    RETURN r
    """
    with db.session() as s:
        result = s.run(query, **rel.model_dump(mode="json"))
        if not result.single():
            raise HTTPException(status_code=404, detail="Usuario o género no encontrados")
        return {"message": "Relación LIKES_GENRE creada"}


@router.patch("/likes-genre/bulk/update", summary="Actualizar múltiples LIKES_GENRE")
def bulk_update_likes_genre(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH ()-[r:LIKES_GENRE]->() WHERE r.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/likes-genre/bulk/properties", summary="Eliminar propiedades de múltiples LIKES_GENRE")
def bulk_delete_likes_genre_properties(filter_property: str, filter_value: str, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH ()-[r:LIKES_GENRE]->()
    WHERE r.{filter_property} = $filter_value
       OR r.{filter_property} = toInteger($filter_value)
       OR r.{filter_property} = toFloat($filter_value)
    REMOVE {remove_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=filter_value)
        return {"updated": result.single()["updated"]}


@router.delete("/likes-genre/bulk/delete", summary="Eliminar LIKES_GENRE con bajo peso")
def bulk_delete_likes_genre(max_weight: float):
    with db.session() as s:
        result = s.run("""
            MATCH ()-[r:LIKES_GENRE]->() WHERE r.weight < $max_weight
            DELETE r RETURN count(r) as deleted
        """, max_weight=max_weight)
        return {"deleted": result.single()["deleted"]}


@router.patch("/likes-genre/{userId}/{genreId}", summary="Actualizar LIKES_GENRE")
def update_likes_genre(userId: int, genreId: int, data: RelPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (u:User {{userId: $userId}})-[r:LIKES_GENRE]->(g:Genre {{genreId: $genreId}})
    SET {set_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, userId=userId, genreId=genreId, **data.properties)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Relación LIKES_GENRE actualizada"}


@router.delete("/likes-genre/{userId}/{genreId}/properties", summary="Eliminar propiedades de 1 LIKES_GENRE")
def delete_likes_genre_properties(userId: int, genreId: int, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH (u:User {{userId: $userId}})-[r:LIKES_GENRE]->(g:Genre {{genreId: $genreId}})
    REMOVE {remove_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, userId=userId, genreId=genreId)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Propiedades eliminadas de LIKES_GENRE"}


@router.delete("/likes-genre/{userId}/{genreId}", summary="Eliminar relación LIKES_GENRE")
def delete_likes_genre(userId: int, genreId: int):
    with db.session() as s:
        result = s.run("""
            MATCH (u:User {userId: $userId})-[r:LIKES_GENRE]->(g:Genre {genreId: $genreId})
            DELETE r RETURN count(r) as deleted
        """, userId=userId, genreId=genreId)
        return {"deleted": result.single()["deleted"]}


# ════════════════════════════════════════════════════════════════
# FOLLOWS ACTOR  (User -> Actor)
# ════════════════════════════════════════════════════════════════

@router.post("/follows/actor", summary="Crear relación FOLLOWS (User -> Actor)")
def create_follows_actor(rel: FollowsActorRel):
    query = """
    MATCH (u:User {userId: $userId}), (a:Actor {actorId: $actorId})
    CREATE (u)-[r:FOLLOWS {
        followedSince: date($followedSince),
        notificationsOn: $notificationsOn,
        interactionCount: $interactionCount
    }]->(a)
    RETURN r
    """
    with db.session() as s:
        result = s.run(query, **rel.model_dump(mode="json"))
        if not result.single():
            raise HTTPException(status_code=404, detail="Usuario o actor no encontrados")
        return {"message": "Relación FOLLOWS (Actor) creada"}


@router.patch("/follows/actor/bulk/update", summary="Actualizar múltiples FOLLOWS actor")
def bulk_update_follows_actor(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (u:User)-[r:FOLLOWS]->(a:Actor) WHERE r.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/follows/actor/bulk/properties", summary="Eliminar propiedades de múltiples FOLLOWS actor")
def bulk_delete_follows_actor_properties(filter_property: str, filter_value: str, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH (u:User)-[r:FOLLOWS]->(a:Actor)
    WHERE r.{filter_property} = $filter_value
       OR r.{filter_property} = toInteger($filter_value)
       OR r.{filter_property} = toFloat($filter_value)
    REMOVE {remove_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=filter_value)
        return {"updated": result.single()["updated"]}


@router.delete("/follows/actor/bulk/delete", summary="Eliminar múltiples FOLLOWS actor")
def bulk_delete_follows_actor(notificationsOn: bool):
    with db.session() as s:
        result = s.run("""
            MATCH (u:User)-[r:FOLLOWS]->(a:Actor) WHERE r.notificationsOn = $notificationsOn
            DELETE r RETURN count(r) as deleted
        """, notificationsOn=notificationsOn)
        return {"deleted": result.single()["deleted"]}


@router.patch("/follows/actor/{userId}/{actorId}", summary="Actualizar FOLLOWS (Actor)")
def update_follows_actor(userId: int, actorId: int, data: RelPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (u:User {{userId: $userId}})-[r:FOLLOWS]->(a:Actor {{actorId: $actorId}})
    SET {set_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, userId=userId, actorId=actorId, **data.properties)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Relación FOLLOWS (Actor) actualizada"}


@router.delete("/follows/actor/{userId}/{actorId}/properties", summary="Eliminar propiedades de 1 FOLLOWS actor")
def delete_follows_actor_properties(userId: int, actorId: int, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH (u:User {{userId: $userId}})-[r:FOLLOWS]->(a:Actor {{actorId: $actorId}})
    REMOVE {remove_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, userId=userId, actorId=actorId)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Propiedades eliminadas de FOLLOWS (Actor)"}


@router.delete("/follows/actor/{userId}/{actorId}", summary="Eliminar FOLLOWS (Actor)")
def delete_follows_actor(userId: int, actorId: int):
    with db.session() as s:
        result = s.run("""
            MATCH (u:User {userId: $userId})-[r:FOLLOWS]->(a:Actor {actorId: $actorId})
            DELETE r RETURN count(r) as deleted
        """, userId=userId, actorId=actorId)
        return {"deleted": result.single()["deleted"]}


# ════════════════════════════════════════════════════════════════
# FOLLOWS DIRECTOR  (User -> Director)
# ════════════════════════════════════════════════════════════════

@router.post("/follows/director", summary="Crear relación FOLLOWS (User -> Director)")
def create_follows_director(rel: FollowsDirectorRel):
    query = """
    MATCH (u:User {userId: $userId}), (d:Director {directorId: $directorId})
    CREATE (u)-[r:FOLLOWS {
        followedSince: date($followedSince),
        notificationsOn: $notificationsOn,
        interactionCount: $interactionCount
    }]->(d)
    RETURN r
    """
    with db.session() as s:
        result = s.run(query, **rel.model_dump(mode="json"))
        if not result.single():
            raise HTTPException(status_code=404, detail="Usuario o director no encontrados")
        return {"message": "Relación FOLLOWS (Director) creada"}


@router.patch("/follows/director/bulk/update", summary="Actualizar múltiples FOLLOWS director")
def bulk_update_follows_director(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (u:User)-[r:FOLLOWS]->(d:Director) WHERE r.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/follows/director/bulk/properties", summary="Eliminar propiedades de múltiples FOLLOWS director")
def bulk_delete_follows_director_properties(filter_property: str, filter_value: str, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH (u:User)-[r:FOLLOWS]->(d:Director)
    WHERE r.{filter_property} = $filter_value
       OR r.{filter_property} = toInteger($filter_value)
       OR r.{filter_property} = toFloat($filter_value)
    REMOVE {remove_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=filter_value)
        return {"updated": result.single()["updated"]}


@router.delete("/follows/director/bulk/delete", summary="Eliminar múltiples FOLLOWS director")
def bulk_delete_follows_director(notificationsOn: bool):
    with db.session() as s:
        result = s.run("""
            MATCH (u:User)-[r:FOLLOWS]->(d:Director) WHERE r.notificationsOn = $notificationsOn
            DELETE r RETURN count(r) as deleted
        """, notificationsOn=notificationsOn)
        return {"deleted": result.single()["deleted"]}


@router.patch("/follows/director/{userId}/{directorId}", summary="Actualizar FOLLOWS (Director)")
def update_follows_director(userId: int, directorId: int, data: RelPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (u:User {{userId: $userId}})-[r:FOLLOWS]->(d:Director {{directorId: $directorId}})
    SET {set_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, userId=userId, directorId=directorId, **data.properties)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Relación FOLLOWS (Director) actualizada"}


@router.delete("/follows/director/{userId}/{directorId}/properties", summary="Eliminar propiedades de 1 FOLLOWS director")
def delete_follows_director_properties(userId: int, directorId: int, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH (u:User {{userId: $userId}})-[r:FOLLOWS]->(d:Director {{directorId: $directorId}})
    REMOVE {remove_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, userId=userId, directorId=directorId)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Propiedades eliminadas de FOLLOWS (Director)"}


@router.delete("/follows/director/{userId}/{directorId}", summary="Eliminar FOLLOWS (Director)")
def delete_follows_director(userId: int, directorId: int):
    with db.session() as s:
        result = s.run("""
            MATCH (u:User {userId: $userId})-[r:FOLLOWS]->(d:Director {directorId: $directorId})
            DELETE r RETURN count(r) as deleted
        """, userId=userId, directorId=directorId)
        return {"deleted": result.single()["deleted"]}


# ════════════════════════════════════════════════════════════════
# ACTED_IN  (Actor -> Movie)
# ════════════════════════════════════════════════════════════════

@router.post("/acted-in", summary="Crear relación ACTED_IN (Actor -> Movie)")
def create_acted_in(rel: ActedInRel):
    query = """
    MATCH (a:Actor {actorId: $actorId}), (m:Movie {movieId: $movieId})
    CREATE (a)-[r:ACTED_IN {
        character: $character,
        isLead: $isLead,
        screenTimeMinutes: $screenTimeMinutes
    }]->(m)
    RETURN r
    """
    with db.session() as s:
        result = s.run(query, **rel.model_dump())
        if not result.single():
            raise HTTPException(status_code=404, detail="Actor o película no encontrados")
        return {"message": "Relación ACTED_IN creada"}


@router.patch("/acted-in/bulk/update", summary="Actualizar múltiples ACTED_IN")
def bulk_update_acted_in(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH ()-[r:ACTED_IN]->() WHERE r.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/acted-in/bulk/properties", summary="Eliminar propiedades de múltiples ACTED_IN")
def bulk_delete_acted_in_properties(filter_property: str, filter_value: str, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH ()-[r:ACTED_IN]->()
    WHERE r.{filter_property} = $filter_value
       OR r.{filter_property} = toInteger($filter_value)
       OR r.{filter_property} = toFloat($filter_value)
    REMOVE {remove_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=filter_value)
        return {"updated": result.single()["updated"]}


@router.delete("/acted-in/bulk/delete", summary="Eliminar múltiples ACTED_IN de extras")
def bulk_delete_acted_in_extras():
    with db.session() as s:
        result = s.run("""
            MATCH ()-[r:ACTED_IN]->() WHERE r.isLead = false AND r.screenTimeMinutes < 10
            DELETE r RETURN count(r) as deleted
        """)
        return {"deleted": result.single()["deleted"]}


@router.patch("/acted-in/{actorId}/{movieId}", summary="Actualizar ACTED_IN")
def update_acted_in(actorId: int, movieId: int, data: RelPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (a:Actor {{actorId: $actorId}})-[r:ACTED_IN]->(m:Movie {{movieId: $movieId}})
    SET {set_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, actorId=actorId, movieId=movieId, **data.properties)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Relación ACTED_IN actualizada"}


@router.delete("/acted-in/{actorId}/{movieId}/properties", summary="Eliminar propiedades de 1 ACTED_IN")
def delete_acted_in_properties(actorId: int, movieId: int, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH (a:Actor {{actorId: $actorId}})-[r:ACTED_IN]->(m:Movie {{movieId: $movieId}})
    REMOVE {remove_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, actorId=actorId, movieId=movieId)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Propiedades eliminadas de ACTED_IN"}


@router.delete("/acted-in/{actorId}/{movieId}", summary="Eliminar ACTED_IN")
def delete_acted_in(actorId: int, movieId: int):
    with db.session() as s:
        result = s.run("""
            MATCH (a:Actor {actorId: $actorId})-[r:ACTED_IN]->(m:Movie {movieId: $movieId})
            DELETE r RETURN count(r) as deleted
        """, actorId=actorId, movieId=movieId)
        return {"deleted": result.single()["deleted"]}


# ════════════════════════════════════════════════════════════════
# COLLABORATED_WITH  (Actor -> Director)
# ════════════════════════════════════════════════════════════════

@router.post("/collaborated-with", summary="Crear relación COLLABORATED_WITH (Actor -> Director)")
def create_collaborated_with(rel: CollaboratedWithRel):
    query = """
    MATCH (a:Actor {actorId: $actorId}), (d:Director {directorId: $directorId})
    CREATE (a)-[r:COLLABORATED_WITH {
        projectCount: $projectCount,
        firstProject: date($firstProject),
        lastProject: date($lastProject)
    }]->(d)
    RETURN r
    """
    with db.session() as s:
        result = s.run(query, **rel.model_dump(mode="json"))
        if not result.single():
            raise HTTPException(status_code=404, detail="Actor o director no encontrados")
        return {"message": "Relación COLLABORATED_WITH creada"}


@router.patch("/collaborated-with/bulk/update", summary="Actualizar múltiples COLLABORATED_WITH")
def bulk_update_collaborated_with(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH ()-[r:COLLABORATED_WITH]->() WHERE r.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/collaborated-with/bulk/properties", summary="Eliminar propiedades de múltiples COLLABORATED_WITH")
def bulk_delete_collaborated_with_properties(filter_property: str, filter_value: str, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH ()-[r:COLLABORATED_WITH]->()
    WHERE r.{filter_property} = $filter_value
       OR r.{filter_property} = toInteger($filter_value)
       OR r.{filter_property} = toFloat($filter_value)
    REMOVE {remove_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=filter_value)
        return {"updated": result.single()["updated"]}


@router.delete("/collaborated-with/bulk/delete", summary="Eliminar COLLABORATED_WITH de un solo proyecto")
def bulk_delete_collaborated_with_single():
    with db.session() as s:
        result = s.run("""
            MATCH ()-[r:COLLABORATED_WITH]->() WHERE r.projectCount = 1
            DELETE r RETURN count(r) as deleted
        """)
        return {"deleted": result.single()["deleted"]}


@router.patch("/collaborated-with/{actorId}/{directorId}", summary="Actualizar COLLABORATED_WITH")
def update_collaborated_with(actorId: int, directorId: int, data: RelPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (a:Actor {{actorId: $actorId}})-[r:COLLABORATED_WITH]->(d:Director {{directorId: $directorId}})
    SET {set_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, actorId=actorId, directorId=directorId, **data.properties)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "COLLABORATED_WITH actualizada"}


@router.delete("/collaborated-with/{actorId}/{directorId}/properties", summary="Eliminar propiedades de 1 COLLABORATED_WITH")
def delete_collaborated_with_properties(actorId: int, directorId: int, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH (a:Actor {{actorId: $actorId}})-[r:COLLABORATED_WITH]->(d:Director {{directorId: $directorId}})
    REMOVE {remove_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, actorId=actorId, directorId=directorId)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Propiedades eliminadas de COLLABORATED_WITH"}


@router.delete("/collaborated-with/{actorId}/{directorId}", summary="Eliminar COLLABORATED_WITH")
def delete_collaborated_with(actorId: int, directorId: int):
    with db.session() as s:
        result = s.run("""
            MATCH (a:Actor {actorId: $actorId})-[r:COLLABORATED_WITH]->(d:Director {directorId: $directorId})
            DELETE r RETURN count(r) as deleted
        """, actorId=actorId, directorId=directorId)
        return {"deleted": result.single()["deleted"]}


# ════════════════════════════════════════════════════════════════
# DIRECTED  (Director -> Movie)
# ════════════════════════════════════════════════════════════════

@router.post("/directed", summary="Crear relación DIRECTED (Director -> Movie)")
def create_directed(rel: DirectedRel):
    query = """
    MATCH (d:Director {directorId: $directorId}), (m:Movie {movieId: $movieId})
    CREATE (d)-[r:DIRECTED {
        fee: $fee,
        nominated: $nominated,
        startDate: date($startDate)
    }]->(m)
    RETURN r
    """
    with db.session() as s:
        result = s.run(query, **rel.model_dump(mode="json"))
        if not result.single():
            raise HTTPException(status_code=404, detail="Director o película no encontrados")
        return {"message": "Relación DIRECTED creada"}


@router.patch("/directed/bulk/update", summary="Actualizar múltiples DIRECTED")
def bulk_update_directed(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH ()-[r:DIRECTED]->() WHERE r.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/directed/bulk/properties", summary="Eliminar propiedades de múltiples DIRECTED")
def bulk_delete_directed_properties(filter_property: str, filter_value: str, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH ()-[r:DIRECTED]->()
    WHERE r.{filter_property} = $filter_value
       OR r.{filter_property} = toInteger($filter_value)
       OR r.{filter_property} = toFloat($filter_value)
    REMOVE {remove_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=filter_value)
        return {"updated": result.single()["updated"]}


@router.delete("/directed/bulk/delete", summary="Eliminar DIRECTED no nominados")
def bulk_delete_directed_not_nominated():
    with db.session() as s:
        result = s.run("""
            MATCH ()-[r:DIRECTED]->() WHERE r.nominated = false
            DELETE r RETURN count(r) as deleted
        """)
        return {"deleted": result.single()["deleted"]}


@router.patch("/directed/{directorId}/{movieId}", summary="Actualizar DIRECTED")
def update_directed(directorId: int, movieId: int, data: RelPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (d:Director {{directorId: $directorId}})-[r:DIRECTED]->(m:Movie {{movieId: $movieId}})
    SET {set_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, directorId=directorId, movieId=movieId, **data.properties)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Relación DIRECTED actualizada"}


@router.delete("/directed/{directorId}/{movieId}/properties", summary="Eliminar propiedades de 1 DIRECTED")
def delete_directed_properties(directorId: int, movieId: int, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH (d:Director {{directorId: $directorId}})-[r:DIRECTED]->(m:Movie {{movieId: $movieId}})
    REMOVE {remove_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, directorId=directorId, movieId=movieId)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Propiedades eliminadas de DIRECTED"}


@router.delete("/directed/{directorId}/{movieId}", summary="Eliminar DIRECTED")
def delete_directed(directorId: int, movieId: int):
    with db.session() as s:
        result = s.run("""
            MATCH (d:Director {directorId: $directorId})-[r:DIRECTED]->(m:Movie {movieId: $movieId})
            DELETE r RETURN count(r) as deleted
        """, directorId=directorId, movieId=movieId)
        return {"deleted": result.single()["deleted"]}


# ════════════════════════════════════════════════════════════════
# IN_GENRE  (Movie -> Genre)
# ════════════════════════════════════════════════════════════════

@router.post("/in-genre", summary="Crear relación IN_GENRE (Movie -> Genre)")
def create_in_genre(rel: InGenreRel):
    query = """
    MATCH (m:Movie {movieId: $movieId}), (g:Genre {genreId: $genreId})
    CREATE (m)-[r:IN_GENRE {
        isPrimary: $isPrimary,
        weight: $weight,
        addedAt: date($addedAt)
    }]->(g)
    RETURN r
    """
    with db.session() as s:
        result = s.run(query, **rel.model_dump(mode="json"))
        if not result.single():
            raise HTTPException(status_code=404, detail="Película o género no encontrados")
        return {"message": "Relación IN_GENRE creada"}


@router.patch("/in-genre/bulk/update", summary="Actualizar múltiples IN_GENRE")
def bulk_update_in_genre(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH ()-[r:IN_GENRE]->() WHERE r.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/in-genre/bulk/properties", summary="Eliminar propiedades de múltiples IN_GENRE")
def bulk_delete_in_genre_properties(filter_property: str, filter_value: str, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH ()-[r:IN_GENRE]->()
    WHERE r.{filter_property} = $filter_value
       OR r.{filter_property} = toInteger($filter_value)
       OR r.{filter_property} = toFloat($filter_value)
    REMOVE {remove_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=filter_value)
        return {"updated": result.single()["updated"]}


@router.delete("/in-genre/bulk/delete", summary="Eliminar IN_GENRE con bajo peso")
def bulk_delete_in_genre_low_weight(max_weight: float):
    with db.session() as s:
        result = s.run("""
            MATCH ()-[r:IN_GENRE]->() WHERE r.weight < $max_weight
            DELETE r RETURN count(r) as deleted
        """, max_weight=max_weight)
        return {"deleted": result.single()["deleted"]}


@router.patch("/in-genre/{movieId}/{genreId}", summary="Actualizar IN_GENRE")
def update_in_genre(movieId: int, genreId: int, data: RelPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (m:Movie {{movieId: $movieId}})-[r:IN_GENRE]->(g:Genre {{genreId: $genreId}})
    SET {set_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, movieId=movieId, genreId=genreId, **data.properties)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Relación IN_GENRE actualizada"}


@router.delete("/in-genre/{movieId}/{genreId}/properties", summary="Eliminar propiedades de 1 IN_GENRE")
def delete_in_genre_properties(movieId: int, genreId: int, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH (m:Movie {{movieId: $movieId}})-[r:IN_GENRE]->(g:Genre {{genreId: $genreId}})
    REMOVE {remove_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, movieId=movieId, genreId=genreId)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Propiedades eliminadas de IN_GENRE"}


@router.delete("/in-genre/{movieId}/{genreId}", summary="Eliminar IN_GENRE")
def delete_in_genre(movieId: int, genreId: int):
    with db.session() as s:
        result = s.run("""
            MATCH (m:Movie {movieId: $movieId})-[r:IN_GENRE]->(g:Genre {genreId: $genreId})
            DELETE r RETURN count(r) as deleted
        """, movieId=movieId, genreId=genreId)
        return {"deleted": result.single()["deleted"]}


# ════════════════════════════════════════════════════════════════
# AVAILABLE_ON  (Movie -> Platform)
# ════════════════════════════════════════════════════════════════

@router.post("/available-on", summary="Crear relación AVAILABLE_ON (Movie -> Platform)")
def create_available_on(rel: AvailableOnRel):
    query = """
    MATCH (m:Movie {movieId: $movieId}), (p:Platform {platformId: $platformId})
    CREATE (m)-[r:AVAILABLE_ON {
        addedAt: date($addedAt),
        region: $region,
        isExclusive: $isExclusive
    }]->(p)
    RETURN r
    """
    with db.session() as s:
        result = s.run(query, **rel.model_dump(mode="json"))
        if not result.single():
            raise HTTPException(status_code=404, detail="Película o plataforma no encontrados")
        return {"message": "Relación AVAILABLE_ON creada"}


@router.patch("/available-on/bulk/update", summary="Actualizar múltiples AVAILABLE_ON")
def bulk_update_available_on(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH ()-[r:AVAILABLE_ON]->() WHERE r.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/available-on/bulk/properties", summary="Eliminar propiedades de múltiples AVAILABLE_ON")
def bulk_delete_available_on_properties(filter_property: str, filter_value: str, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH ()-[r:AVAILABLE_ON]->()
    WHERE r.{filter_property} = $filter_value
       OR r.{filter_property} = toInteger($filter_value)
       OR r.{filter_property} = toFloat($filter_value)
    REMOVE {remove_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=filter_value)
        return {"updated": result.single()["updated"]}


@router.delete("/available-on/bulk/delete", summary="Eliminar AVAILABLE_ON por región")
def bulk_delete_available_on(region: str):
    with db.session() as s:
        result = s.run("""
            MATCH ()-[r:AVAILABLE_ON]->() WHERE r.region = $region
            DELETE r RETURN count(r) as deleted
        """, region=region)
        return {"deleted": result.single()["deleted"]}


@router.patch("/available-on/{movieId}/{platformId}", summary="Actualizar AVAILABLE_ON")
def update_available_on(movieId: int, platformId: int, data: RelPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (m:Movie {{movieId: $movieId}})-[r:AVAILABLE_ON]->(p:Platform {{platformId: $platformId}})
    SET {set_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, movieId=movieId, platformId=platformId, **data.properties)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Relación AVAILABLE_ON actualizada"}


@router.delete("/available-on/{movieId}/{platformId}/properties", summary="Eliminar propiedades de 1 AVAILABLE_ON")
def delete_available_on_properties(movieId: int, platformId: int, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH (m:Movie {{movieId: $movieId}})-[r:AVAILABLE_ON]->(p:Platform {{platformId: $platformId}})
    REMOVE {remove_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, movieId=movieId, platformId=platformId)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Propiedades eliminadas de AVAILABLE_ON"}


@router.delete("/available-on/{movieId}/{platformId}", summary="Eliminar AVAILABLE_ON")
def delete_available_on(movieId: int, platformId: int):
    with db.session() as s:
        result = s.run("""
            MATCH (m:Movie {movieId: $movieId})-[r:AVAILABLE_ON]->(p:Platform {platformId: $platformId})
            DELETE r RETURN count(r) as deleted
        """, movieId=movieId, platformId=platformId)
        return {"deleted": result.single()["deleted"]}

# ════════════════════════════════════════════════════════════════
# PAYS  (User -> Platform)
# ════════════════════════════════════════════════════════════════

@router.post("/pays", summary="Crear relación PAYS (User -> Platform)")
def create_pays(rel: PaysRel):
    query = """
    MATCH (u:User {userId: $userId}), (p:Platform {platformId: $platformId})
    CREATE (u)-[r:PAYS {
        subscribedSince: date($subscribedSince),
        plan: $plan,
        autoRenewal: $autoRenewal
    }]->(p)
    RETURN r
    """
    with db.session() as s:
        result = s.run(query, **rel.model_dump(mode="json"))
        if not result.single():
            raise HTTPException(status_code=404, detail="Usuario o plataforma no encontrados")
        return {"message": "Relación PAYS creada"}


@router.patch("/pays/bulk/update", summary="Actualizar múltiples PAYS")
def bulk_update_pays(data: BulkPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH ()-[r:PAYS]->() WHERE r.{data.filter_property} = $filter_value
    SET {set_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=data.filter_value, **data.properties)
        return {"updated": result.single()["updated"]}


@router.delete("/pays/bulk/properties", summary="Eliminar propiedades de múltiples PAYS")
def bulk_delete_pays_properties(filter_property: str, filter_value: str, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH ()-[r:PAYS]->()
    WHERE r.{filter_property} = $filter_value
       OR r.{filter_property} = toInteger($filter_value)
       OR r.{filter_property} = toFloat($filter_value)
    REMOVE {remove_clause} RETURN count(r) as updated
    """
    with db.session() as s:
        result = s.run(query, filter_value=filter_value)
        return {"updated": result.single()["updated"]}


@router.delete("/pays/bulk/delete", summary="Eliminar PAYS sin autorenovación")
def bulk_delete_pays_no_renewal():
    with db.session() as s:
        result = s.run("""
            MATCH ()-[r:PAYS]->() WHERE r.autoRenewal = false
            DELETE r RETURN count(r) as deleted
        """)
        return {"deleted": result.single()["deleted"]}


@router.patch("/pays/{userId}/{platformId}", summary="Actualizar PAYS")
def update_pays(userId: int, platformId: int, data: RelPropertyUpdate):
    set_clause = ", ".join([f"r.{k} = ${k}" for k in data.properties])
    query = f"""
    MATCH (u:User {{userId: $userId}})-[r:PAYS]->(p:Platform {{platformId: $platformId}})
    SET {set_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, userId=userId, platformId=platformId, **data.properties)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Relación PAYS actualizada"}


@router.delete("/pays/{userId}/{platformId}/properties", summary="Eliminar propiedades de 1 PAYS")
def delete_pays_properties(userId: int, platformId: int, properties: List[str] = Query(...)):
    remove_clause = ", ".join([f"r.{p}" for p in properties])
    query = f"""
    MATCH (u:User {{userId: $userId}})-[r:PAYS]->(p:Platform {{platformId: $platformId}})
    REMOVE {remove_clause} RETURN r
    """
    with db.session() as s:
        result = s.run(query, userId=userId, platformId=platformId)
        if not result.single():
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        return {"message": "Propiedades eliminadas de PAYS"}


@router.delete("/pays/{userId}/{platformId}", summary="Eliminar PAYS")
def delete_pays(userId: int, platformId: int):
    with db.session() as s:
        result = s.run("""
            MATCH (u:User {userId: $userId})-[r:PAYS]->(p:Platform {platformId: $platformId})
            DELETE r RETURN count(r) as deleted
        """, userId=userId, platformId=platformId)
        return {"deleted": result.single()["deleted"]}
