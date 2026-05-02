"""
seed.py — Genera 5000+ nodos conectados en AuraDB
Ejecutar: python seed.py
"""

from neo4j import GraphDatabase
import random
from datetime import date, timedelta

# ─── CONEXIÓN ───────────────────────────────────────────────────
URI      = "neo4j://127.0.0.1:7687"
USER     = "neo4j"
PASSWORD = "Sportnicho1+"                              

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def run(query, **params):
    with driver.session() as s:
        s.run(query, **params)

def run_many(query, data):
    with driver.session() as s:
        s.run(query, data=data)

def rdate(start_year=2000, end_year=2024):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    return str(start + timedelta(days=random.randint(0, (end - start).days)))

# ─── DATOS BASE ─────────────────────────────────────────────────

GENRES = [
    {"genreId": 1,  "name": "Sci-Fi",       "description": "Ciencia ficción especulativa",          "isMainstream": True,  "subgenres": ["Cyberpunk","Space Opera","Biopunk"]},
    {"genreId": 2,  "name": "Thriller",      "description": "Suspenso con alta tensión narrativa",   "isMainstream": True,  "subgenres": ["Psychological","Crime","Tech"]},
    {"genreId": 3,  "name": "Drama",         "description": "Conflictos emocionales y humanos",       "isMainstream": True,  "subgenres": ["Romantic","Social","Biographical"]},
    {"genreId": 4,  "name": "Action",        "description": "Acción y aventura intensa",              "isMainstream": True,  "subgenres": ["Superhero","Martial Arts","Military"]},
    {"genreId": 5,  "name": "Horror",        "description": "Terror psicológico y sobrenatural",      "isMainstream": False, "subgenres": ["Psychological","Slasher","Supernatural"]},
    {"genreId": 6,  "name": "Comedy",        "description": "Humor y situaciones cómicas",            "isMainstream": True,  "subgenres": ["Romantic Comedy","Dark Comedy","Satire"]},
    {"genreId": 7,  "name": "Animation",     "description": "Películas animadas para todas las edades","isMainstream": True, "subgenres": ["3D","2D","Stop Motion"]},
    {"genreId": 8,  "name": "Documentary",   "description": "Narrativas basadas en hechos reales",    "isMainstream": False, "subgenres": ["Nature","Political","Crime"]},
    {"genreId": 9,  "name": "Romance",       "description": "Historias de amor y relaciones",         "isMainstream": True,  "subgenres": ["Historical","Contemporary","Tragic"]},
    {"genreId": 10, "name": "Fantasy",       "description": "Mundos mágicos y seres sobrenaturales",  "isMainstream": True,  "subgenres": ["Epic","Urban","Dark"]},
]

PLATFORMS = [
    {"platformId": 1, "name": "Netflix",   "country": "United States", "isPaid": True,  "monthlyCost": 15.99, "launchedAt": "2007-01-16"},
    {"platformId": 2, "name": "Max",       "country": "United States", "isPaid": True,  "monthlyCost": 15.99, "launchedAt": "2020-05-27"},
    {"platformId": 3, "name": "Disney+",   "country": "United States", "isPaid": True,  "monthlyCost": 10.99, "launchedAt": "2019-11-12"},
    {"platformId": 4, "name": "Amazon Prime","country": "United States","isPaid": True,  "monthlyCost": 8.99,  "launchedAt": "2011-02-22"},
    {"platformId": 5, "name": "Apple TV+", "country": "United States", "isPaid": True,  "monthlyCost": 9.99,  "launchedAt": "2019-11-01"},
    {"platformId": 6, "name": "Paramount+","country": "United States", "isPaid": True,  "monthlyCost": 7.99,  "launchedAt": "2021-03-04"},
    {"platformId": 7, "name": "Crunchyroll","country": "United States","isPaid": True,  "monthlyCost": 7.99,  "launchedAt": "2006-06-08"},
    {"platformId": 8, "name": "Mubi",      "country": "United Kingdom","isPaid": True,  "monthlyCost": 10.99, "launchedAt": "2007-01-01"},
]

DIRECTORS = [
    {"directorId": 1,  "name": "Christopher Nolan",    "gender": "Male",   "birthDate": "1970-07-30", "nationality": "British-American"},
    {"directorId": 2,  "name": "Denis Villeneuve",      "gender": "Male",   "birthDate": "1967-10-03", "nationality": "Canadian"},
    {"directorId": 3,  "name": "David Fincher",         "gender": "Male",   "birthDate": "1962-08-28", "nationality": "American"},
    {"directorId": 4,  "name": "Greta Gerwig",          "gender": "Female", "birthDate": "1983-08-04", "nationality": "American"},
    {"directorId": 5,  "name": "Martin Scorsese",       "gender": "Male",   "birthDate": "1942-11-17", "nationality": "American"},
    {"directorId": 6,  "name": "Bong Joon-ho",          "gender": "Male",   "birthDate": "1969-09-14", "nationality": "South Korean"},
    {"directorId": 7,  "name": "Sofia Coppola",         "gender": "Female", "birthDate": "1971-05-14", "nationality": "American"},
    {"directorId": 8,  "name": "Ridley Scott",          "gender": "Male",   "birthDate": "1937-11-30", "nationality": "British"},
    {"directorId": 9,  "name": "Wes Anderson",          "gender": "Male",   "birthDate": "1969-05-01", "nationality": "American"},
    {"directorId": 10, "name": "Ava DuVernay",          "gender": "Female", "birthDate": "1972-08-24", "nationality": "American"},
    {"directorId": 11, "name": "Steven Spielberg",      "gender": "Male",   "birthDate": "1946-12-18", "nationality": "American"},
    {"directorId": 12, "name": "Quentin Tarantino",     "gender": "Male",   "birthDate": "1963-03-27", "nationality": "American"},
    {"directorId": 13, "name": "Jordan Peele",          "gender": "Male",   "birthDate": "1979-02-21", "nationality": "American"},
    {"directorId": 14, "name": "Alfonso Cuarón",        "gender": "Male",   "birthDate": "1961-11-28", "nationality": "Mexican"},
    {"directorId": 15, "name": "Park Chan-wook",        "gender": "Male",   "birthDate": "1963-08-23", "nationality": "South Korean"},
]

ACTORS = [
    {"actorId": 1,  "name": "Cillian Murphy",         "birthDate": "1976-05-25", "nationality": "Irish",           "isActive": True,  "oscars": 1},
    {"actorId": 2,  "name": "Timothée Chalamet",      "birthDate": "1995-12-27", "nationality": "American-French", "isActive": True,  "oscars": 0},
    {"actorId": 3,  "name": "Brad Pitt",               "birthDate": "1963-12-18", "nationality": "American",        "isActive": True,  "oscars": 1},
    {"actorId": 4,  "name": "Zendaya",                 "birthDate": "1996-09-01", "nationality": "American",        "isActive": True,  "oscars": 0},
    {"actorId": 5,  "name": "Leonardo DiCaprio",       "birthDate": "1974-11-11", "nationality": "American",        "isActive": True,  "oscars": 1},
    {"actorId": 6,  "name": "Meryl Streep",            "birthDate": "1949-06-22", "nationality": "American",        "isActive": True,  "oscars": 3},
    {"actorId": 7,  "name": "Margot Robbie",           "birthDate": "1990-07-02", "nationality": "Australian",      "isActive": True,  "oscars": 0},
    {"actorId": 8,  "name": "Ryan Gosling",            "birthDate": "1980-11-12", "nationality": "Canadian",        "isActive": True,  "oscars": 0},
    {"actorId": 9,  "name": "Viola Davis",             "birthDate": "1965-08-11", "nationality": "American",        "isActive": True,  "oscars": 1},
    {"actorId": 10, "name": "Tom Hanks",               "birthDate": "1956-07-09", "nationality": "American",        "isActive": True,  "oscars": 2},
    {"actorId": 11, "name": "Natalie Portman",         "birthDate": "1981-06-09", "nationality": "Israeli-American","isActive": True,  "oscars": 1},
    {"actorId": 12, "name": "Joaquin Phoenix",         "birthDate": "1974-10-28", "nationality": "American",        "isActive": True,  "oscars": 1},
    {"actorId": 13, "name": "Saoirse Ronan",           "birthDate": "1994-04-12", "nationality": "Irish-American",  "isActive": True,  "oscars": 0},
    {"actorId": 14, "name": "Adam Driver",             "birthDate": "1983-11-19", "nationality": "American",        "isActive": True,  "oscars": 0},
    {"actorId": 15, "name": "Florence Pugh",           "birthDate": "1996-01-03", "nationality": "British",         "isActive": True,  "oscars": 0},
    {"actorId": 16, "name": "Austin Butler",           "birthDate": "1991-08-17", "nationality": "American",        "isActive": True,  "oscars": 0},
    {"actorId": 17, "name": "Ana de Armas",            "birthDate": "1988-04-30", "nationality": "Cuban-Spanish",   "isActive": True,  "oscars": 0},
    {"actorId": 18, "name": "Paul Mescal",             "birthDate": "1996-02-02", "nationality": "Irish",           "isActive": True,  "oscars": 0},
    {"actorId": 19, "name": "Lupita Nyong'o",          "birthDate": "1983-03-01", "nationality": "Kenyan-Mexican",  "isActive": True,  "oscars": 1},
    {"actorId": 20, "name": "Oscar Isaac",             "birthDate": "1979-03-09", "nationality": "Guatemalan-American","isActive": True,"oscars": 0},
]

# Actor+Director multi-label
ACTOR_DIRECTORS = [
    {"actorId": 21, "directorId": 16, "name": "Clint Eastwood", "gender": "Male",   "birthDate": "1930-05-31", "nationality": "American",   "isActive": False, "oscars": 1},
    {"actorId": 22, "directorId": 17, "name": "Ben Affleck",    "gender": "Male",   "birthDate": "1972-08-15", "nationality": "American",   "isActive": True,  "oscars": 1},
    {"actorId": 23, "directorId": 18, "name": "Olivia Wilde",   "gender": "Female", "birthDate": "1984-03-10", "nationality": "American",   "isActive": True,  "oscars": 0},
]

MOVIES = [
    {"movieId": 1,  "title": "Inception",             "year": 2010, "avgRating": 8.8, "duration": 148, "budget": 160000000.0, "languages": ["English","Japanese"],         "releaseDate": "2010-07-16", "tagline": "Your mind is the scene of the crime",        "directorId": 1,  "genreIds": [1,2],    "actorIds": [5,2]},
    {"movieId": 2,  "title": "Dune",                  "year": 2021, "avgRating": 8.0, "duration": 155, "budget": 165000000.0, "languages": ["English"],                     "releaseDate": "2021-10-22", "tagline": "Beyond fear, destiny awaits",                "directorId": 2,  "genreIds": [1,10],   "actorIds": [2,4,20]},
    {"movieId": 3,  "title": "Dune: Part Two",        "year": 2024, "avgRating": 8.5, "duration": 166, "budget": 190000000.0, "languages": ["English"],                     "releaseDate": "2024-03-01", "tagline": "Long live the fighters",                     "directorId": 2,  "genreIds": [1,10],   "actorIds": [2,4,20]},
    {"movieId": 4,  "title": "The Dark Knight",       "year": 2008, "avgRating": 9.0, "duration": 152, "budget": 185000000.0, "languages": ["English"],                     "releaseDate": "2008-07-18", "tagline": "Why so serious?",                            "directorId": 1,  "genreIds": [4,2],    "actorIds": [1]},
    {"movieId": 5,  "title": "Fight Club",            "year": 1999, "avgRating": 8.8, "duration": 139, "budget": 63000000.0,  "languages": ["English"],                     "releaseDate": "1999-10-15", "tagline": "Mischief. Mayhem. Soap.",                    "directorId": 3,  "genreIds": [2,3],    "actorIds": [3]},
    {"movieId": 6,  "title": "Barbie",                "year": 2023, "avgRating": 7.0, "duration": 114, "budget": 145000000.0, "languages": ["English"],                     "releaseDate": "2023-07-21", "tagline": "She's everything. He's just Ken.",           "directorId": 4,  "genreIds": [6,3],    "actorIds": [7,8]},
    {"movieId": 7,  "title": "Oppenheimer",           "year": 2023, "avgRating": 8.9, "duration": 180, "budget": 100000000.0, "languages": ["English"],                     "releaseDate": "2023-07-21", "tagline": "The world forever changes",                  "directorId": 1,  "genreIds": [3,2],    "actorIds": [1,8]},
    {"movieId": 8,  "title": "Parasite",              "year": 2019, "avgRating": 8.5, "duration": 132, "budget": 11400000.0,  "languages": ["Korean"],                      "releaseDate": "2019-10-11", "tagline": "Act like you own the place",                 "directorId": 6,  "genreIds": [2,3],    "actorIds": []},
    {"movieId": 9,  "title": "The Revenant",          "year": 2015, "avgRating": 8.0, "duration": 156, "budget": 135000000.0, "languages": ["English","Arikara"],            "releaseDate": "2015-12-25", "tagline": "Blood lost. Life found.",                    "directorId": 14, "genreIds": [4,3],    "actorIds": [5]},
    {"movieId": 10, "title": "Joker",                 "year": 2019, "avgRating": 8.4, "duration": 122, "budget": 55000000.0,  "languages": ["English"],                     "releaseDate": "2019-10-04", "tagline": "Put on a happy face",                        "directorId": 3,  "genreIds": [2,3],    "actorIds": [12]},
    {"movieId": 11, "title": "Gravity",               "year": 2013, "avgRating": 7.7, "duration": 91,  "budget": 100000000.0, "languages": ["English"],                     "releaseDate": "2013-10-04", "tagline": "Don't let go",                               "directorId": 14, "genreIds": [1,4],    "actorIds": [6]},
    {"movieId": 12, "title": "Her",                   "year": 2013, "avgRating": 8.0, "duration": 126, "budget": 23000000.0,  "languages": ["English"],                     "releaseDate": "2013-12-18", "tagline": "A love story for the digital age",           "directorId": 9,  "genreIds": [1,9],    "actorIds": [14]},
    {"movieId": 13, "title": "Little Women",          "year": 2019, "avgRating": 7.9, "duration": 135, "budget": 40000000.0,  "languages": ["English"],                     "releaseDate": "2019-12-25", "tagline": "Own your story",                             "directorId": 4,  "genreIds": [3,9],    "actorIds": [13,7,11]},
    {"movieId": 14, "title": "Blade Runner 2049",     "year": 2017, "avgRating": 8.0, "duration": 164, "budget": 150000000.0, "languages": ["English","Finnish"],            "releaseDate": "2017-10-06", "tagline": "The key to the future is finally unearthed","directorId": 2,  "genreIds": [1,2],    "actorIds": [8,17]},
    {"movieId": 15, "title": "Marriage Story",        "year": 2019, "avgRating": 7.9, "duration": 137, "budget": 18000000.0,  "languages": ["English"],                     "releaseDate": "2019-12-06", "tagline": "The story of a marriage",                    "directorId": 9,  "genreIds": [3,9],    "actorIds": [14,13]},
    {"movieId": 16, "title": "Midsommar",             "year": 2019, "avgRating": 7.1, "duration": 148, "budget": 9000000.0,   "languages": ["English","Swedish"],            "releaseDate": "2019-07-03", "tagline": "Let the festivities begin",                  "directorId": 13, "genreIds": [5,2],    "actorIds": [15]},
    {"movieId": 17, "title": "Get Out",               "year": 2017, "avgRating": 7.7, "duration": 104, "budget": 4500000.0,   "languages": ["English"],                     "releaseDate": "2017-02-24", "tagline": "Just because you're invited doesn't mean you're welcome","directorId": 13,"genreIds": [5,2],"actorIds": []},
    {"movieId": 18, "title": "Roma",                  "year": 2018, "avgRating": 7.7, "duration": 135, "budget": 15000000.0,  "languages": ["Spanish","Mixtec"],             "releaseDate": "2018-11-21", "tagline": "A love letter to Mexico City",               "directorId": 14, "genreIds": [3,8],    "actorIds": []},
    {"movieId": 19, "title": "Aftersun",              "year": 2022, "avgRating": 7.7, "duration": 101, "budget": 1000000.0,   "languages": ["English"],                     "releaseDate": "2022-10-21", "tagline": "Somewhere between memory and dream",         "directorId": 7,  "genreIds": [3],      "actorIds": [18]},
    {"movieId": 20, "title": "Alien: Romulus",        "year": 2024, "avgRating": 7.3, "duration": 119, "budget": 65000000.0,  "languages": ["English"],                     "releaseDate": "2024-08-16", "tagline": "Do not fear the dark",                       "directorId": 8,  "genreIds": [1,5],    "actorIds": []},
    {"movieId": 21, "title": "The Grand Budapest Hotel","year": 2014,"avgRating": 8.1,"duration": 99,  "budget": 25000000.0,  "languages": ["English","French","German"],    "releaseDate": "2014-03-28", "tagline": "Check in. Relax. Unwind.",                   "directorId": 9,  "genreIds": [6,3],    "actorIds": [10]},
    {"movieId": 22, "title": "Selma",                 "year": 2014, "avgRating": 7.5, "duration": 128, "budget": 20000000.0,  "languages": ["English"],                     "releaseDate": "2014-12-25", "tagline": "One dream can change the world",             "directorId": 10, "genreIds": [3,8],    "actorIds": [19]},
    {"movieId": 23, "title": "Gladiator II",          "year": 2024, "avgRating": 7.1, "duration": 148, "budget": 310000000.0, "languages": ["English"],                     "releaseDate": "2024-11-15", "tagline": "Unleash the might of Rome",                  "directorId": 8,  "genreIds": [4,3],    "actorIds": [18,20]},
    {"movieId": 24, "title": "Priscilla",             "year": 2023, "avgRating": 6.8, "duration": 113, "budget": 22000000.0,  "languages": ["English"],                     "releaseDate": "2023-10-27", "tagline": "The untold story",                           "directorId": 7,  "genreIds": [3,9],    "actorIds": [16]},
    {"movieId": 25, "title": "The Irishman",          "year": 2019, "avgRating": 7.8, "duration": 209, "budget": 159000000.0, "languages": ["English","Italian"],            "releaseDate": "2019-11-01", "tagline": "I heard you paint houses",                   "directorId": 5,  "genreIds": [2,3],    "actorIds": [3,10]},
    {"movieId": 26, "title": "Past Lives",            "year": 2023, "avgRating": 7.9, "duration": 106, "budget": 6000000.0,   "languages": ["English","Korean"],             "releaseDate": "2023-06-02", "tagline": "Some connections cannot be broken",          "directorId": 7,  "genreIds": [9,3],    "actorIds": []},
    {"movieId": 27, "title": "Poor Things",           "year": 2023, "avgRating": 8.0, "duration": 141, "budget": 35000000.0,  "languages": ["English"],                     "releaseDate": "2023-12-08", "tagline": "A woman returns from the dead",              "directorId": 14, "genreIds": [10,3],   "actorIds": [7,15]},
    {"movieId": 28, "title": "Arrival",               "year": 2016, "avgRating": 7.9, "duration": 116, "budget": 47000000.0,  "languages": ["English","French"],             "releaseDate": "2016-11-11", "tagline": "Why are they here?",                         "directorId": 2,  "genreIds": [1,3],    "actorIds": []},
    {"movieId": 29, "title": "Killers of the Flower Moon","year": 2023,"avgRating": 7.7,"duration": 206,"budget": 200000000.0,"languages": ["English","Osage"],             "releaseDate": "2023-10-20", "tagline": "When oil was discovered in Osage Nation",    "directorId": 5,  "genreIds": [3,2],    "actorIds": [5,9]},
    {"movieId": 30, "title": "Everything Everywhere All at Once","year": 2022,"avgRating": 7.8,"duration": 139,"budget": 14300000.0,"languages": ["English","Mandarin","Cantonese"],"releaseDate": "2022-03-25","tagline": "The universe is so much bigger than you realize","directorId": 13,"genreIds": [1,6,4],"actorIds": []}
]

# Plataformas por película
MOVIE_PLATFORMS = {
    1:  [1, 4],   # Inception
    2:  [2],      # Dune
    3:  [2],      # Dune 2
    4:  [2, 4],   # Dark Knight
    5:  [1, 4],   # Fight Club
    6:  [2],      # Barbie
    7:  [4],      # Oppenheimer
    8:  [4, 1],   # Parasite
    9:  [1],      # The Revenant
    10: [2],      # Joker
    11: [3],      # Gravity
    12: [1, 4],   # Her
    13: [1],      # Little Women
    14: [3, 4],   # Blade Runner 2049
    15: [1],      # Marriage Story
    16: [3],      # Midsommar
    17: [2],      # Get Out
    18: [1],      # Roma
    19: [1],      # Aftersun
    20: [3],      # Alien Romulus
    21: [3, 4],   # Grand Budapest Hotel
    22: [4],      # Selma
    23: [2],      # Gladiator II
    24: [4],      # Priscilla
    25: [1],      # The Irishman
    26: [4],      # Past Lives
    27: [3],      # Poor Things
    28: [2],      # Arrival
    29: [4],      # Killers of the Flower Moon
    30: [4],      # Everything Everywhere
}

COUNTRIES   = ["Guatemala","México","Argentina","Colombia","Chile","Perú","España","Estados Unidos","Brasil","Ecuador"]
THEMES      = ["psicología","distopía","crimen","venganza","romance","aventura","familia","identidad","política","supervivencia","amistad","traición","redención","guerra","tecnología"]
DECADES     = ["1980s","1990s","2000s","2010s","2020s"]
GENRE_NAMES = [g["name"] for g in GENRES]
PLANS       = ["Basic","Standard","Premium"]

# ─── SEED ───────────────────────────────────────────────────────

def clear_db():
    print("🗑  Limpiando base de datos...")
    with driver.session() as s:
        s.run("MATCH (n) DETACH DELETE n")
    print("   ✓ Limpieza completa")

def seed_genres():
    print("🎭 Creando géneros...")
    run_many("""
        UNWIND $data AS g
        CREATE (:Genre {
            genreId: g.genreId, name: g.name,
            description: g.description, isMainstream: g.isMainstream,
            subgenres: g.subgenres
        })
    """, data=GENRES)
    print(f"   ✓ {len(GENRES)} géneros")

def seed_platforms():
    print("📺 Creando plataformas...")
    run_many("""
        UNWIND $data AS p
        CREATE (:Platform {
            platformId: p.platformId, name: p.name, country: p.country,
            isPaid: p.isPaid, monthlyCost: p.monthlyCost,
            launchedAt: date(p.launchedAt)
        })
    """, data=PLATFORMS)
    print(f"   ✓ {len(PLATFORMS)} plataformas")

def seed_directors():
    print("🎬 Creando directores...")
    run_many("""
        UNWIND $data AS d
        CREATE (:Director {
            directorId: d.directorId, name: d.name, gender: d.gender,
            birthDate: date(d.birthDate), nationality: d.nationality
        })
    """, data=DIRECTORS)
    print(f"   ✓ {len(DIRECTORS)} directores")

def seed_actor_directors():
    print("🎭 Creando Actor+Director (multi-label)...")
    run_many("""
        UNWIND $data AS p
        CREATE (:Actor:Director {
            actorId: p.actorId, directorId: p.directorId,
            name: p.name, gender: p.gender,
            birthDate: date(p.birthDate), nationality: p.nationality,
            isActive: p.isActive, oscars: p.oscars
        })
    """, data=ACTOR_DIRECTORS)
    print(f"   ✓ {len(ACTOR_DIRECTORS)} actor+director")

def seed_actors():
    print("🎭 Creando actores...")
    run_many("""
        UNWIND $data AS a
        CREATE (:Actor {
            actorId: a.actorId, name: a.name,
            birthDate: date(a.birthDate), nationality: a.nationality,
            isActive: a.isActive, oscars: a.oscars
        })
    """, data=ACTORS)
    print(f"   ✓ {len(ACTORS)} actores")

def seed_movies():
    print("🎥 Creando películas...")
    movies_clean = [{k: v for k, v in m.items() if k not in ("directorId","genreIds","actorIds")} for m in MOVIES]
    run_many("""
        UNWIND $data AS m
        CREATE (:Movie {
            movieId: m.movieId, title: m.title, year: m.year,
            avgRating: m.avgRating, duration: m.duration, budget: m.budget,
            languages: m.languages, releaseDate: date(m.releaseDate),
            tagline: m.tagline
        })
    """, data=movies_clean)
    print(f"   ✓ {len(MOVIES)} películas")

def seed_movie_relationships():
    print("🔗 Creando relaciones de películas...")
    with driver.session() as s:
        for m in MOVIES:
            mid = m["movieId"]
            # Director -> Movie
            s.run("""
                MATCH (d:Director {directorId: $did}), (m:Movie {movieId: $mid})
                CREATE (d)-[:DIRECTED {fee: $fee, nominated: $nom, startDate: date($sd)}]->(m)
            """, did=m["directorId"], mid=mid,
                 fee=round(random.uniform(2000000, 20000000), 2),
                 nom=random.choice([True, False]),
                 sd=rdate(m["year"]-2, m["year"]-1))

            # Movie -> Genre
            for i, gid in enumerate(m["genreIds"]):
                s.run("""
                    MATCH (m:Movie {movieId: $mid}), (g:Genre {genreId: $gid})
                    CREATE (m)-[:IN_GENRE {isPrimary: $primary, weight: $w, addedAt: date($ad)}]->(g)
                """, mid=mid, gid=gid,
                     primary=(i == 0),
                     w=round(random.uniform(0.5, 1.0), 2),
                     ad=m["releaseDate"])

            # Actor -> Movie
            for aid in m["actorIds"]:
                s.run("""
                    MATCH (a:Actor {actorId: $aid}), (m:Movie {movieId: $mid})
                    CREATE (a)-[:ACTED_IN {character: $char, isLead: $lead, screenTimeMinutes: $st}]->(m)
                """, aid=aid, mid=mid,
                     char=f"Character_{aid}_{mid}",
                     lead=random.choice([True, False]),
                     st=random.randint(20, 150))

            # Movie -> Platform
            for pid in MOVIE_PLATFORMS.get(mid, []):
                s.run("""
                    MATCH (m:Movie {movieId: $mid}), (p:Platform {platformId: $pid})
                    CREATE (m)-[:AVAILABLE_ON {addedAt: date($ad), region: $region, isExclusive: $excl}]->(p)
                """, mid=mid, pid=pid,
                     ad=rdate(m["year"], 2024),
                     region=random.choice(["Global","Latinoamérica","North America","Europe"]),
                     excl=random.choice([True, False]))

    print("   ✓ Relaciones de películas creadas")

def seed_collaborated_with():
    print("🤝 Creando colaboraciones actor-director...")
    seen = set()
    with driver.session() as s:
        for m in MOVIES:
            did = m["directorId"]
            for aid in m["actorIds"]:
                key = (aid, did)
                if key not in seen:
                    seen.add(key)
                    s.run("""
                        MATCH (a:Actor {actorId: $aid}), (d:Director {directorId: $did})
                        CREATE (a)-[:COLLABORATED_WITH {
                            projectCount: $pc, firstProject: date($fp), lastProject: date($lp)
                        }]->(d)
                    """, aid=aid, did=did,
                         pc=random.randint(1, 4),
                         fp=rdate(2000, 2015),
                         lp=rdate(2016, 2024))
    print(f"   ✓ {len(seen)} colaboraciones")

def seed_users():
    print("👤 Creando 4900 usuarios...")
    BATCH = 500
    uid = 100
    created = 0
    while created < 4900:
        batch = []
        for _ in range(min(BATCH, 4900 - created)):
            genres_sample  = random.sample(GENRE_NAMES, random.randint(2, 4))
            decades_sample = random.sample(DECADES, random.randint(1, 3))
            themes_sample  = random.sample(THEMES, random.randint(2, 4))
            batch.append({
                "userId":           uid,
                "name":             f"User_{uid}",
                "age":              random.randint(16, 65),
                "country":          random.choice(COUNTRIES),
                "email":            f"user{uid}@cinegraph.com",
                "createdAt":        rdate(2020, 2024),
                "isActive":         random.choice([True, True, True, False]),
                "preferredGenres":  genres_sample,
                "preferredDecades": decades_sample,
                "preferredThemes":  themes_sample,
            })
            uid += 1
            created += 1
        run_many("""
            UNWIND $data AS u
            CREATE (:User {
                userId: u.userId, name: u.name, age: u.age,
                country: u.country, email: u.email,
                createdAt: date(u.createdAt), isActive: u.isActive,
                preferredGenres: u.preferredGenres,
                preferredDecades: u.preferredDecades,
                preferredThemes: u.preferredThemes
            })
        """, data=batch)
        print(f"   ... {created}/4900")
    print("   ✓ 4900 usuarios")

def seed_user_relationships():
    print("🔗 Creando relaciones de usuarios...")
    movie_ids    = [m["movieId"] for m in MOVIES]
    genre_ids    = [g["genreId"] for g in GENRES]
    platform_ids = [p["platformId"] for p in PLATFORMS]
    actor_ids    = [a["actorId"] for a in ACTORS]
    director_ids = [d["directorId"] for d in DIRECTORS]

    BATCH = 200
    uid_start = 100
    uid_end   = 4999
    total = uid_end - uid_start + 1
    processed = 0

    for uid in range(uid_start, uid_end + 1):
        with driver.session() as s:
            # PAYS → 1-2 plataformas
            pays_platforms = random.sample(platform_ids, random.randint(1, 2))
            for pid in pays_platforms:
                s.run("""
                    MATCH (u:User {userId:$uid}),(p:Platform {platformId:$pid})
                    CREATE (u)-[:PAYS {subscribedSince:date($sd), plan:$plan, autoRenewal:$ar}]->(p)
                """, uid=uid, pid=pid,
                     sd=rdate(2019,2024),
                     plan=random.choice(PLANS),
                     ar=random.choice([True,True,False]))

            # LIKES_GENRE → 2-4 géneros
            for gid in random.sample(genre_ids, random.randint(2,4)):
                s.run("""
                    MATCH (u:User {userId:$uid}),(g:Genre {genreId:$gid})
                    CREATE (u)-[:LIKES_GENRE {weight:$w, since:date($sd), explicit:$ex}]->(g)
                """, uid=uid, gid=gid,
                     w=round(random.uniform(0.3,1.0),2),
                     sd=rdate(2018,2024),
                     ex=random.choice([True,False]))

            # FOLLOWS actor → 1-3
            for aid in random.sample(actor_ids, random.randint(1,3)):
                s.run("""
                    MATCH (u:User {userId:$uid}),(a:Actor {actorId:$aid})
                    CREATE (u)-[:FOLLOWS {followedSince:date($fs), notificationsOn:$no, interactionCount:$ic}]->(a)
                """, uid=uid, aid=aid,
                     fs=rdate(2018,2024),
                     no=random.choice([True,False]),
                     ic=random.randint(0,50))

            # FOLLOWS director → 1-2
            for did in random.sample(director_ids, random.randint(1,2)):
                s.run("""
                    MATCH (u:User {userId:$uid}),(d:Director {directorId:$did})
                    CREATE (u)-[:FOLLOWS {followedSince:date($fs), notificationsOn:$no, interactionCount:$ic}]->(d)
                """, uid=uid, did=did,
                     fs=rdate(2018,2024),
                     no=random.choice([True,False]),
                     ic=random.randint(0,50))

            # WATCHED → 3-8 películas disponibles en sus plataformas
            available_movies = [
                mid for mid, pids in MOVIE_PLATFORMS.items()
                if any(p in pays_platforms for p in pids)
            ]
            if not available_movies:
                available_movies = movie_ids
            watched = random.sample(available_movies, min(random.randint(3,8), len(available_movies)))
            for mid in watched:
                s.run("""
                    MATCH (u:User {userId:$uid}),(m:Movie {movieId:$mid})
                    CREATE (u)-[:WATCHED {watchedAt:date($wa), completedPercent:$cp, rewatched:$rw}]->(m)
                """, uid=uid, mid=mid,
                     wa=rdate(2019,2024),
                     cp=round(random.uniform(40.0,100.0),1),
                     rw=random.choice([True,False,False]))

            # RATED → subconjunto de lo que vio
            rated = random.sample(watched, min(random.randint(1,4), len(watched)))
            for mid in rated:
                s.run("""
                    MATCH (u:User {userId:$uid}),(m:Movie {movieId:$mid})
                    CREATE (u)-[:RATED {rating:$r, ratedAt:date($ra), review:$rv}]->(m)
                """, uid=uid, mid=mid,
                     r=round(random.uniform(5.0,10.0),1),
                     ra=rdate(2019,2024),
                     rv=random.choice([
                         "Excelente película","La recomiendo mucho","Muy entretenida",
                         "Buena pero no la mejor","Me dejó pensando","Obra maestra",
                         "Algo lenta pero vale la pena","Increíble actuación","La vi dos veces",
                         "No era lo que esperaba pero me gustó"
                     ]))

        processed += 1
        if processed % 500 == 0:
            print(f"   ... {processed}/{total} usuarios relacionados")

    print("   ✓ Relaciones de usuarios creadas")

def verify():
    print("\n📊 Verificando nodos totales...")
    with driver.session() as s:
        r = s.run("MATCH (n) RETURN count(n) AS total").single()
        print(f"   Total nodos: {r['total']}")
        for label in ["User","Movie","Genre","Actor","Director","Platform"]:
            c = s.run(f"MATCH (n:{label}) RETURN count(n) AS c").single()
            print(f"   {label}: {c['c']}")
        rels = s.run("MATCH ()-[r]->() RETURN count(r) AS total").single()
        print(f"   Total relaciones: {rels['total']}")

if __name__ == "__main__":
    print("🚀 Iniciando seed de CineGraph...\n")
    clear_db()
    seed_genres()
    seed_platforms()
    seed_directors()
    seed_actors()
    seed_actor_directors()
    seed_movies()
    seed_movie_relationships()
    seed_collaborated_with()
    seed_users()
    seed_user_relationships()
    verify()
    driver.close()
    print("\n✅ Seed completo!")