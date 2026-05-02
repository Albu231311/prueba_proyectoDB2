from fastapi import APIRouter
from app.database import get_db

router = APIRouter(prefix="/queries", tags=["Consultas Cypher"])
db = get_db()


# ════════════════════════════════════════════════════════════════
# CONSULTAS CYPHER (rúbrica: 4-6 consultas, cada integrante hace 2)
# ════════════════════════════════════════════════════════════════

@router.get("/recommendations/{userId}", summary="Q1 - Motor de recomendación por scoring de relaciones")
def get_recommendations(userId: int, limit: int = 10):
    """
    Recomienda películas usando un sistema de puntos basado en las relaciones del grafo:
    - +5 pts por cada director que el usuario sigue
    - +3 pts por cada género que le gusta al usuario
    - +2 pts por cada actor que el usuario sigue
    - +1 pt por rating alto de la película (avgRating >= 8.0)
    Solo recomienda películas disponibles en plataformas donde el usuario paga,
    y excluye películas que ya vio o calificó.
    Al final guarda la recomendación top como relación SHOULD_WATCH.
    """
    query = """
    MATCH (u:User {userId: $userId})
    MATCH (m:Movie)
    WHERE NOT (u)-[:WATCHED]->(m)
      AND NOT (u)-[:RATED]->(m)
      AND NOT (u)-[:SHOULD_WATCH]->(m)

    // Solo películas en plataformas donde paga
    MATCH (m)-[:AVAILABLE_ON]->(p:Platform)<-[:PAYS]-(u)

    WITH u, m, collect(DISTINCT p.name) AS platforms,

      // +5 pts por director seguido
      size([(u)-[:FOLLOWS]->(d:Director)<-[:DIRECTED]-(m) | d]) * 5 AS directorScore,

      // +3 pts por género que le gusta
      size([(u)-[:LIKES_GENRE]->(g:Genre)<-[:IN_GENRE]-(m) | g]) * 3 AS genreScore,

      // +2 pts por actor seguido
      size([(u)-[:FOLLOWS]->(a:Actor)-[:ACTED_IN]->(m) | a]) * 2 AS actorScore,

      // géneros y directores para el reason
      [(u)-[:LIKES_GENRE]->(g:Genre)<-[:IN_GENRE]-(m) | g.name] AS matchedGenres,
      [(u)-[:FOLLOWS]->(d:Director)<-[:DIRECTED]-(m) | d.name] AS matchedDirectors,
      [(u)-[:FOLLOWS]->(a:Actor)-[:ACTED_IN]->(m) | a.name] AS matchedActors

    WITH u, m, platforms, matchedGenres, matchedDirectors, matchedActors,
      directorScore + genreScore + actorScore +
      CASE WHEN m.avgRating >= 8.0 THEN 1 ELSE 0 END AS totalScore

    WHERE totalScore > 0

    RETURN m.movieId AS movieId,
           m.title AS title,
           m.year AS year,
           m.avgRating AS rating,
           m.tagline AS tagline,
           platforms,
           matchedGenres,
           matchedDirectors,
           matchedActors,
           totalScore
    ORDER BY totalScore DESC, m.avgRating DESC
    LIMIT $limit
    """
    with db.session() as s:
        result = s.run(query, userId=userId, limit=limit)
        recommendations = [dict(r) for r in result]

        # Guardar top recomendación como SHOULD_WATCH en el grafo
        if recommendations:
            top = recommendations[0]
            reason_parts = []
            if top["matchedDirectors"]:
                reason_parts.append(f"seguís a {', '.join(top['matchedDirectors'])}")
            if top["matchedGenres"]:
                reason_parts.append(f"te gusta {', '.join(top['matchedGenres'])}")
            if top["matchedActors"]:
                reason_parts.append(f"seguís a {', '.join(top['matchedActors'])}")
            reason = "Recomendado porque " + " y ".join(reason_parts)
            confidence = round(min(top["totalScore"] / 15.0, 1.0), 2)

            s.run("""
                MATCH (u:User {userId: $userId}), (m:Movie {movieId: $movieId})
                MERGE (u)-[r:SHOULD_WATCH]->(m)
                SET r.recommendedAt = date(toString(date())),
                    r.confidenceScore = $confidence,
                    r.reason = $reason
            """, userId=userId, movieId=top["movieId"],
                 confidence=confidence, reason=reason)

        return recommendations


@router.get("/top-rated-by-genre", summary="Q2 - Top películas por género con promedio de rating")
def top_rated_by_genre():
    """
    Agregación: promedio de rating, conteo de películas y conteo de ratings por género.
    """
    query = """
    MATCH (m:Movie)-[:IN_GENRE {isPrimary: true}]->(g:Genre)
    OPTIONAL MATCH ()-[r:RATED]->(m)
    RETURN g.name AS genre,
           count(DISTINCT m) AS totalMovies,
           round(avg(m.avgRating) * 100) / 100 AS avgRating,
           count(r) AS totalRatings
    ORDER BY avgRating DESC
    """
    with db.session() as s:
        result = s.run(query)
        return [dict(r) for r in result]


@router.get("/most-followed-actors", summary="Q3 - Actores más seguidos con películas")
def most_followed_actors():
    """
    Actores con más seguidores, cuántas películas tienen y su rating promedio.
    """
    query = """
    MATCH (u:User)-[:FOLLOWS]->(a:Actor)
    OPTIONAL MATCH (a)-[:ACTED_IN]->(m:Movie)
    RETURN a.name AS actor,
           a.nationality AS nationality,
           count(DISTINCT u) AS followers,
           count(DISTINCT m) AS movies,
           round(avg(m.avgRating) * 100) / 100 AS avgMovieRating
    ORDER BY followers DESC
    LIMIT 10
    """
    with db.session() as s:
        result = s.run(query)
        return [dict(r) for r in result]


@router.get("/platform-stats", summary="Q4 - Estadísticas por plataforma")
def platform_stats():
    """
    Cuántas películas tiene cada plataforma, cuántos usuarios pagan y rating promedio del catálogo.
    """
    query = """
    MATCH (p:Platform)
    OPTIONAL MATCH (m:Movie)-[:AVAILABLE_ON]->(p)
    OPTIONAL MATCH (u:User)-[:PAYS]->(p)
    RETURN p.name AS platform,
           p.monthlyCost AS monthlyCost,
           count(DISTINCT m) AS totalMovies,
           count(DISTINCT u) AS subscribers,
           round(avg(m.avgRating) * 100) / 100 AS avgCatalogRating
    ORDER BY subscribers DESC
    """
    with db.session() as s:
        result = s.run(query)
        return [dict(r) for r in result]


@router.get("/director-actor-network/{directorId}", summary="Q5 - Red de un director: actores y películas")
def director_network(directorId: int):
    """
    Para un director, muestra todas sus películas, los actores que trabajaron con él
    y cuántas veces han colaborado.
    """
    query = """
    MATCH (d:Director {directorId: $directorId})-[:DIRECTED]->(m:Movie)<-[:ACTED_IN]-(a:Actor)
    OPTIONAL MATCH (a)-[c:COLLABORATED_WITH]->(d)
    RETURN d.name AS director,
           m.title AS movie,
           m.year AS year,
           a.name AS actor,
           a.isActive AS actorActive,
           coalesce(c.projectCount, 0) AS totalCollabs
    ORDER BY m.year DESC
    """
    with db.session() as s:
        result = s.run(query, directorId=directorId)
        return [dict(r) for r in result]


@router.get("/user-activity/{userId}", summary="Q6 - Resumen de actividad de un usuario")
def user_activity(userId: int):
    """
    Cuántas películas vio, cuántas calificó, géneros favoritos y plataformas activas.
    """
    query = """
    MATCH (u:User {userId: $userId})
    OPTIONAL MATCH (u)-[w:WATCHED]->(mw:Movie)
    OPTIONAL MATCH (u)-[r:RATED]->(mr:Movie)
    OPTIONAL MATCH (u)-[:LIKES_GENRE]->(g:Genre)
    OPTIONAL MATCH (u)-[:PAYS]->(p:Platform)
    RETURN u.name AS user,
           u.country AS country,
           count(DISTINCT mw) AS moviesWatched,
           count(DISTINCT mr) AS moviesRated,
           round(avg(r.rating) * 100) / 100 AS avgRatingGiven,
           collect(DISTINCT g.name) AS favoriteGenres,
           collect(DISTINCT p.name) AS activePlatforms
    """
    with db.session() as s:
        result = s.run(query, userId=userId)
        record = result.single()
        if not record:
            return {"error": "Usuario no encontrado"}
        return dict(record)


# ════════════════════════════════════════════════════════════════
# FILTRADO Y AGREGACIONES EXTRA
# ════════════════════════════════════════════════════════════════

@router.get("/movies/filter", summary="Filtrar películas por múltiples criterios")
def filter_movies(
    min_year: int = None,
    max_year: int = None,
    min_rating: float = None,
    max_budget: float = None,
    language: str = None,
    limit: int = 20
):
    filters = []
    params = {"limit": limit}
    if min_year:
        filters.append("m.year >= $min_year")
        params["min_year"] = min_year
    if max_year:
        filters.append("m.year <= $max_year")
        params["max_year"] = max_year
    if min_rating:
        filters.append("m.avgRating >= $min_rating")
        params["min_rating"] = min_rating
    if max_budget:
        filters.append("m.budget <= $max_budget")
        params["max_budget"] = max_budget
    if language:
        filters.append("$language IN m.languages")
        params["language"] = language
    where = ("WHERE " + " AND ".join(filters)) if filters else ""
    query = f"""
    MATCH (m:Movie) {where}
    RETURN m ORDER BY m.avgRating DESC LIMIT $limit
    """
    with db.session() as s:
        result = s.run(query, **params)
        return [dict(r["m"]) for r in result]


@router.get("/aggregations/overview", summary="Resumen general del grafo")
def graph_overview():
    query = """
    MATCH (u:User) WITH count(u) AS users
    MATCH (m:Movie) WITH users, count(m) AS movies
    MATCH (a:Actor) WITH users, movies, count(a) AS actors
    MATCH (d:Director) WITH users, movies, actors, count(d) AS directors
    MATCH (g:Genre) WITH users, movies, actors, directors, count(g) AS genres
    MATCH (p:Platform) WITH users, movies, actors, directors, genres, count(p) AS platforms
    RETURN users, movies, actors, directors, genres, platforms
    """
    with db.session() as s:
        result = s.run(query)
        record = result.single()
        return dict(record) if record else {}
    
    

# ════════════════════════════════════════════════════════════════
# GDS - ALGORITMOS DE DATA SCIENCE
# ════════════════════════════════════════════════════════════════

@router.post("/gds/project", summary="GDS - Proyectar grafo en memoria")
def project_graph():
    with db.session() as s:
        s.run("CALL gds.graph.drop('cinegraph', false) YIELD graphName RETURN graphName")
        result = s.run("""
            CALL gds.graph.project(
              'cinegraph',
              ['User', 'Movie', 'Genre', 'Actor', 'Director', 'Platform'],
              {
                WATCHED:      { orientation: 'NATURAL' },
                RATED:        { orientation: 'NATURAL' },
                LIKES_GENRE:  { orientation: 'NATURAL' },
                FOLLOWS:      { orientation: 'NATURAL' },
                ACTED_IN:     { orientation: 'NATURAL' },
                DIRECTED:     { orientation: 'NATURAL' },
                IN_GENRE:     { orientation: 'NATURAL' },
                AVAILABLE_ON: { orientation: 'NATURAL' },
                PAYS:         { orientation: 'NATURAL' }
              }
            )
            YIELD graphName, nodeCount, relationshipCount
        """)
        record = result.single()
        return {
            "graph": record["graphName"],
            "nodes": record["nodeCount"],
            "relationships": record["relationshipCount"]
        }


@router.get("/gds/recommendations/pagerank/{userId}",
            summary="GDS - Recomendaciones por Personalized PageRank")
def gds_pagerank(userId: int, limit: int = 10):
    """
    Corre Personalized PageRank desde el usuario, filtra solo películas
    disponibles en plataformas donde paga y que no haya visto ni calificado,
    y guarda la top recomendación como SHOULD_WATCH.
    """
    query = """
    MATCH (u:User {userId: $userId})

    CALL gds.pageRank.stream('cinegraph', {
      maxIterations: 30,
      dampingFactor: 0.85,
      sourceNodes: [u]
    })
    YIELD nodeId, score

    WITH gds.util.asNode(nodeId) AS movie, score, u
    WHERE movie:Movie AND score > 0

    // Filtrar vistas, calificadas y ya recomendadas
    WITH movie, score, u
    WHERE NOT (u)-[:WATCHED]->(movie)
      AND NOT (u)-[:RATED]->(movie)
      AND NOT (u)-[:SHOULD_WATCH]->(movie)

    // Filtrar solo plataformas donde el usuario paga
    MATCH (movie)-[:AVAILABLE_ON]->(p:Platform)<-[:PAYS]-(u)

    WITH movie, score, u, collect(DISTINCT p.name) AS availableOn
    WHERE size(availableOn) > 0

    // Info adicional
    WITH movie, score, u, availableOn,
         [(movie)-[:IN_GENRE]->(g:Genre) | g.name] AS genres,
         [(d:Director)-[:DIRECTED]->(movie) | d.name] AS directors,
         [(a:Actor)-[:ACTED_IN]->(movie) | a.name][..3] AS topActors

    RETURN movie.movieId   AS movieId,
           movie.title     AS title,
           movie.year      AS year,
           movie.avgRating AS avgRating,
           movie.tagline   AS tagline,
           round(score * 1000) / 1000 AS score,
           genres,
           directors,
           topActors,
           availableOn
    ORDER BY score DESC, movie.avgRating DESC
    LIMIT $limit
    """
    with db.session() as s:
        result = s.run(query, userId=userId, limit=limit)
        recommendations = [dict(r) for r in result]

        if recommendations:
            for rec in recommendations:
                reason_parts = []
                if rec["directors"]:
                    reason_parts.append(f"dirigida por {', '.join(rec['directors'])}")
                if rec["genres"]:
                    reason_parts.append(f"géneros: {', '.join(rec['genres'][:2])}")
                if rec["availableOn"]:
                    reason_parts.append(f"disponible en {', '.join(rec['availableOn'])}")
                reason = "Recomendado por PageRank: " + " · ".join(reason_parts)
                confidence = round(min(rec["score"] * 50, 1.0), 2)

                s.run("""
                    MATCH (u:User {userId: $userId}), (m:Movie {movieId: $movieId})
                    MERGE (u)-[r:SHOULD_WATCH]->(m)
                    SET r.recommendedAt = date(toString(date())),
                        r.confidenceScore = $confidence,
                        r.reason = $reason
                """, userId=userId,
                    movieId=rec["movieId"],
                    confidence=confidence,
                    reason=reason)

        return recommendations