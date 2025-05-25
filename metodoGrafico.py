from matplotlib import pyplot as plt
import numpy as np

# Función para ingresar restricciones desde consola (simulada aquí con input())
def ingresar_restricciones():
    print("Ingrese la cantidad de restricciones:")
    n = int(input())

    print("Ingrese la cantidad de variables:")
    m = int(input())

    restricciones = []
    for i in range(n):
        print(f"\nRestricción {i + 1}:")
        coef = []
        for j in range(m):
            coef.append(float(input(f"Ingrese coeficiente de x{j + 1}: ")))
        simbolo = input("Ingrese el símbolo (<=, >=, =): ").strip()
        lado_derecho = float(input("Ingrese el lado derecho: "))
        restricciones.append((coef, simbolo, lado_derecho))

    print("\nIngrese los coeficientes de la función objetivo Z = c1*x1 + c2*x2 + ...:")
    z = [float(input(f"Coeficiente de x{i + 1}: ")) for i in range(m)]

    return restricciones, z


restricciones, z = ingresar_restricciones()

# Graficar
x = np.linspace(0, 10, 400)
plt.figure(figsize=(8, 6))

# Dibujar restricciones
for coef, simbolo, b in restricciones:
    if coef[1] != 0:
        y = (b - coef[0] * x) / coef[1]
        plt.plot(x, y, label=f'{coef[0]}x1 + {coef[1]}x2 {simbolo} {b}')
    else:
        # x constante
        plt.axvline(x=b / coef[0], linestyle='--', label=f'{coef[0]}x1 {simbolo} {b}')

# Región factible aproximada (solo para el ejemplo)
x1_vals = np.linspace(0, 5, 200)
x2_1 = 4 - x1_vals
x2_2 = np.full_like(x1_vals, 3)
x2_3 = np.full_like(x1_vals, np.nan)
x2_3[x1_vals <= 2] = np.minimum(x2_1[x1_vals <= 2], x2_2[x1_vals <= 2])

plt.fill_between(x1_vals, 0, x2_3, color='gray', alpha=0.3, label='Región factible')

# Vértices del ejemplo para calcular Z
vertices = np.array([[0, 0], [0, 3], [1, 3], [2, 2], [2, 0]])
Z = z[0] * vertices[:, 0] + z[1] * vertices[:, 1]

for i, (xv, yv) in enumerate(vertices):
    plt.plot(xv, yv, 'ro')
    plt.text(xv + 0.1, yv, f'Z={Z[i]:.0f}')

plt.xlim(0, 5)
plt.ylim(0, 5)
plt.xlabel('$x_1$')
plt.ylabel('$x_2$')
plt.title('Método Gráfico - Entrada por Consola')
plt.legend()
plt.grid(True)
plt.show()
