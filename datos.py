BASE = "BOG"          
PESO_MAX_CAJA = 1200  

AEROPUERTOS = {
    "BOG": {"ciudad": "Bogota",           "pais": "Colombia",       "lat": 4.70,   "lon": -74.15},
    "PTY": {"ciudad": "Ciudad de Panama", "pais": "Panama",         "lat": 9.07,   "lon": -79.38},
    "MIA": {"ciudad": "Miami",            "pais": "Estados Unidos", "lat": 25.79,  "lon": -80.29},
    "MEX": {"ciudad": "Ciudad de Mexico", "pais": "Mexico",         "lat": 19.44,  "lon": -99.07},
    "LIM": {"ciudad": "Lima",             "pais": "Peru",           "lat": -12.02, "lon": -77.11},
    "SCL": {"ciudad": "Santiago",         "pais": "Chile",          "lat": -33.39, "lon": -70.79},
}

VUELOS = [("BOG", "PTY"), ("BOG", "MIA"), ("BOG", "LIM"), ("PTY", "MIA"), ("PTY", "MEX"), ("MIA", "MEX"), ("LIM", "SCL")]

AVION = {"nombre": "SebasAirLines", "peso_max": 3000, "volumen_max": 6}

CAJAS = [
    {"nombre": "Vacunas",             "destino": "PTY", "alto": 80,  "ancho": 60,  "profundidad": 60,  "peso": 180, "precio": 13600000},
    {"nombre": "Flores",              "destino": "MIA", "alto": 120, "ancho": 100, "profundidad": 80,  "peso": 520, "precio": 6400000},
    {"nombre": "Repuestos de avion",  "destino": "MEX", "alto": 150, "ancho": 100, "profundidad": 100, "peso": 640, "precio": 10800000},
    {"nombre": "Cafe",                "destino": "MIA", "alto": 120, "ancho": 80,  "profundidad": 90,  "peso": 450, "precio": 5200000},
    {"nombre": "Equipos medicos",     "destino": "LIM", "alto": 120, "ancho": 100, "profundidad": 90,  "peso": 390, "precio": 10000000},
    {"nombre": "Esmeraldas",          "destino": "SCL", "alto": 40,  "ancho": 30,  "profundidad": 30,  "peso": 35,  "precio": 16800000},
    {"nombre": "Autopartes",          "destino": "MEX", "alto": 150, "ancho": 120, "profundidad": 90,  "peso": 950, "precio": 8800000},
    {"nombre": "Telefonos celulares", "destino": "LIM", "alto": 100, "ancho": 80,  "profundidad": 60,  "peso": 310, "precio": 13200000},
]
