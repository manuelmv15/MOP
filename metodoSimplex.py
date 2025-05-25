import numpy as np

def construir_tabla_simplex(A, b, c):
    m, n = A.shape
    A_ext = np.hstack((A, np.eye(m)))
    c_ext = np.hstack((-c, np.zeros(m)))
    tabla = np.zeros((m + 1, n + m + 1))
    tabla[:-1, :-1] = A_ext
    tabla[:-1, -1] = b
    tabla[-1, :-1] = c_ext
    return tabla

def simplex(tabla):
    while True:
        z = tabla[-1, :-1]
        if np.all(z >= 0):
            break
        col_piv = np.argmin(z)
        columna = tabla[:-1, col_piv]
        resultado = tabla[:-1, -1]

        with np.errstate(divide='ignore', invalid='ignore'):
            razones = np.where(columna > 0, resultado / columna, np.inf)
        fila_piv = np.argmin(razones)

        if razones[fila_piv] == np.inf:
            raise Exception("Problema no acotado")

        tabla[fila_piv, :] /= tabla[fila_piv, col_piv]

        for i in range(tabla.shape[0]):
            if i != fila_piv:
                tabla[i, :] -= tabla[i, col_piv] * tabla[fila_piv, :]

    return tabla

def mostrar_solucion(tabla, num_vars):
    solucion = np.zeros(num_vars)
    for i in range(num_vars):
        columna = tabla[:, i]
        if list(columna[:-1]).count(0) == len(columna) - 2 and list(columna[:-1]).count(1) == 1:
            fila = np.where(columna[:-1] == 1)[0][0]
            solucion[i] = tabla[fila, -1]

    print("\nSolución óptima:")
    for i, val in enumerate(solucion):
        print(f"x{i+1} = {val}")
    print(f"Valor máximo de Z = {tabla[-1, -1]}")

def main():
    m = int(input("Ingrese el número de restricciones: "))
    n = int(input("Ingrese el número de variables: "))

    A = []
    b = []

    print("\nIngrese los coeficientes de las restricciones:")
    for i in range(m):
        fila = list(map(float, input(f"Coeficientes de la restricción {i+1} (separados por espacio): ").split()))
        A.append(fila[:n])
        b_val = float(input(f"Valor del lado derecho b[{i+1}]: "))
        b.append(b_val)

    print("\nIngrese los coeficientes de la función objetivo Z = c1*x1 + c2*x2 + ...")
    c = list(map(float, input("Coeficientes c (separados por espacio): ").split()))

    A = np.array(A)
    b = np.array(b)
    c = np.array(c)

    tabla = construir_tabla_simplex(A, b, c)
    print("\nTabla inicial:")
    print(tabla)

    tabla_final = simplex(tabla)
    print("\nTabla final:")
    print(tabla_final)

    mostrar_solucion(tabla_final, len(c))

if __name__ == "__main__":
    main()
