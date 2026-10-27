
INFINITO = float("inf")

def volumen_cm3(caja):
    return caja["alto"] * caja["ancho"] * caja["profundidad"]


def mochila(cajas, peso_max, volumen_max):
    memoria = {}

    def mejor(i, peso_libre, volumen_libre):
        if i == len(cajas):  
            return 0, []
        if (i, peso_libre, volumen_libre) in memoria:
            return memoria[(i, peso_libre, volumen_libre)]

        caja = cajas[i]

        mejor_precio, mejores_cajas = mejor(i + 1, peso_libre, volumen_libre)

        if caja["peso"] <= peso_libre and volumen_cm3(caja) <= volumen_libre:
            precio, elegidas = mejor(i + 1, peso_libre - caja["peso"], volumen_libre - volumen_cm3(caja))
            if caja["precio"] + precio > mejor_precio:
                mejor_precio, mejores_cajas = caja["precio"] + precio, [caja] + elegidas

        memoria[(i, peso_libre, volumen_libre)] = (mejor_precio, mejores_cajas)
        return mejor_precio, mejores_cajas

    precio, elegidas = mejor(0, peso_max, volumen_max)
    return elegidas



def dijkstra(grafo, origen):
    distancias = {}
    anterior = {}
    for aeropuerto in grafo:
        distancias[aeropuerto] = INFINITO  
        anterior[aeropuerto] = None
    distancias[origen] = 0
    pendientes = list(grafo)

    while pendientes:
        actual = pendientes[0]
        for aeropuerto in pendientes:
            if distancias[aeropuerto] < distancias[actual]:
                actual = aeropuerto
        pendientes.remove(actual)

        for vecino, km in grafo[actual]:
            if distancias[actual] + km < distancias[vecino]:
                distancias[vecino] = distancias[actual] + km
                anterior[vecino] = actual

    return distancias, anterior


def camino(anterior, destino):
    ruta = []
    while destino is not None:
        ruta.insert(0, destino)
        destino = anterior[destino]
    return ruta


def vecino_mas_cercano(origen, paradas, distancias):
    actual = origen
    pendientes = list(paradas)
    orden = []
    while pendientes:
        mas_cercano = pendientes[0]
        for parada in pendientes:
            if distancias[actual][parada] < distancias[actual][mas_cercano]:
                mas_cercano = parada
        orden.append(mas_cercano)
        pendientes.remove(mas_cercano)
        actual = mas_cercano
    return orden
