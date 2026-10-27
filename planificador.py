import math

from algoritmos import camino, dijkstra, mochila, vecino_mas_cercano, volumen_cm3

def distancia_km(a, b):
    lat1, lon1 = math.radians(a["lat"]), math.radians(a["lon"])
    lat2, lon2 = math.radians(b["lat"]), math.radians(b["lon"])
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return round(2 * 6371 * math.asin(math.sqrt(h)))  


def construir_grafo(aeropuertos, vuelos):
    grafo = {}
    for codigo in aeropuertos:
        grafo[codigo] = []
    for a, b in vuelos:
        km = distancia_km(aeropuertos[a], aeropuertos[b])
        grafo[a].append((b, km))
        grafo[b].append((a, km))
    return grafo


def planificar(aeropuertos, vuelos, avion, cajas, base, peso_max_caja):
    grafo = construir_grafo(aeropuertos, vuelos)

    distancias, anteriores = {}, {}
    for codigo in grafo:
        distancias[codigo], anteriores[codigo] = dijkstra(grafo, codigo)

    permitidas = []
    for caja in cajas:
        if caja["peso"] <= peso_max_caja:
            permitidas.append(caja)

    a_bordo = mochila(permitidas, avion["peso_max"], avion["volumen_max"] * 1_000_000)

    paradas = []
    for caja in a_bordo:
        if caja["destino"] not in paradas:
            paradas.append(caja["destino"])
    orden = vecino_mas_cercano(base, paradas, distancias)

    tramos = []
    if orden:
        recorrido = [base] + orden + [base]
        for i in range(len(recorrido) - 1):
            desde, hasta = recorrido[i], recorrido[i + 1]
            tramos.append({"desde": desde, "hasta": hasta, "km": distancias[desde][hasta],
                           "pasa_por": camino(anteriores[desde], hasta)})

    return {
        "a_bordo": a_bordo, "orden": orden, "tramos": tramos,
        "peso": sum(caja["peso"] for caja in a_bordo),
        "volumen": sum(volumen_cm3(caja) for caja in a_bordo) / 1_000_000,  # en m³
        "precio": sum(caja["precio"] for caja in a_bordo),
        "km": sum(tramo["km"] for tramo in tramos),
    }
