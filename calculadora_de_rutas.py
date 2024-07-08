
alto = 10
ancho = 10
movimientos_posibles = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def estimacion_g(valor_g):
    return valor_g + 1  # Costo uniforme de moverse a un nodo adyacente

def estimacion_h(nodo_actual, nodo_meta):
    return abs(nodo_actual[0] - nodo_meta[0]) + abs(nodo_actual[1] - nodo_meta[1])

def estimacion_f(valor_g, valor_h):
    return valor_g + valor_h

def crear_mapa(alto, ancho):
    return [[0 for _ in range(ancho)] for _ in range(alto)]

def mostrar_mapa(mapa):
    for fila in mapa:
        print(" ".join(map(str, fila)))

def es_valido(nodo, mapa):
    x, y = nodo
    # Considera inválido si está fuera del rango o es un obstáculo (valor 1 o 2)
    return 0 <= x < len(mapa) and 0 <= y < len(mapa[0]) and mapa[x][y] == 0

def algoritmo_A_estrella(mapa, inicio, meta):
    lista_nodos_abiertos = []
    lista_nodos_cerrados = set()
    pila_nodo_padre = {}

    valor_g_inicial = 0
    nodo_actual = (inicio, valor_g_inicial)
    lista_nodos_abiertos.append(nodo_actual)
    pila_nodo_padre[inicio] = None

    while lista_nodos_abiertos:
        lista_nodos_abiertos.sort(key=lambda nodo: nodo[1])
        nodo_actual, valor_g = lista_nodos_abiertos.pop(0)

        if nodo_actual == meta:
            camino = []
            while nodo_actual is not None:
                camino.append(nodo_actual)
                nodo_actual = pila_nodo_padre[nodo_actual]
            return camino[::-1]  # Ruta desde inicio hasta meta

        lista_nodos_cerrados.add(nodo_actual)

        for mov in movimientos_posibles:
            nodo_adyacente = (nodo_actual[0] + mov[0], nodo_actual[1] + mov[1])

            if nodo_adyacente in lista_nodos_cerrados or not es_valido(nodo_adyacente, mapa):
                continue

            valor_g_adyacente = estimacion_g(valor_g)
            valor_h = estimacion_h(nodo_adyacente, meta)
            f = estimacion_f(valor_g_adyacente, valor_h)

            if nodo_adyacente not in [nodo for nodo, _ in lista_nodos_abiertos]:
                lista_nodos_abiertos.append((nodo_adyacente, f))
                pila_nodo_padre[nodo_adyacente] = nodo_actual
            else:
                for i, (coord, viejo_f) in enumerate(lista_nodos_abiertos):
                    if coord == nodo_adyacente and f < viejo_f:
                        lista_nodos_abiertos[i] = (nodo_adyacente, f)
                        lista_nodos_abiertos.sort(key=lambda nodo: nodo[1])
                        pila_nodo_padre[nodo_adyacente] = nodo_actual

    return None

def main():
    mapa = crear_mapa(alto, ancho)

    # Solicitar obstáculos
    num_obstaculos = int(input("Ingrese el número de obstáculos: "))
    for _ in range(num_obstaculos):
        x = int(input("Ingrese la coordenada x del obstáculo: "))
        y = int(input("Ingrese la coordenada y del obstáculo: "))
        tipo_obstaculo = int(input("Ingrese el tipo de obstáculo (1 o 2): "))
        mapa[x][y] = tipo_obstaculo

    # Mostrar el mapa inicial
    print("Mapa inicial:")
    mostrar_mapa(mapa)

    # Solicitar puntos de inicio y meta
    inicio_x = int(input("Ingrese la coordenada x del punto de inicio: "))
    inicio_y = int(input("Ingrese la coordenada y del punto de inicio: "))
    inicio = (inicio_x, inicio_y)

    meta_x = int(input("Ingrese la coordenada x del punto de llegada: "))
    meta_y = int(input("Ingrese la coordenada y del punto de llegada: "))
    meta = (meta_x, meta_y)

    # Ejecutar el algoritmo A*
    camino = algoritmo_A_estrella(mapa, inicio, meta)

    if camino:
        # Marcar el camino en el mapa
        for (x, y) in camino:
            if (x, y) != inicio and (x, y) != meta:
                mapa[x][y] = 'c'

        # Marcar inicio y meta en el mapa
        mapa[inicio_x][inicio_y] = 'I'
        mapa[meta_x][meta_y] = 'M'

        # Mostrar el mapa con la ruta resuelta
        print("Mapa con la ruta resuelta:")
        mostrar_mapa(mapa)
    else:
        print("No se encontró una ruta desde el inicio hasta la meta.")

if __name__ == "__main__":
    main()
