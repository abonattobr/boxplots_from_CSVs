import numpy as np
import matplotlib.pyplot as plt

# Definindo o intervalo de x com 1000 pontos entre -50 e 50
x = np.linspace(-3, 3, 1000)

# Calculando y = sin(x)
y = np.cos(x)

# Cores Tableau
tableau_red = '#d62728'
tableau_green = '#2ca02c'

# Criando o gráfico
plt.figure(figsize=(10, 5))

# Plotando y = sin(x) com a cor Tableau Red e linha sólida
plt.plot(x, np.cos(x)*np.cos(20.*x), lw=1.25, color='k', label='a')
plt.plot(x, 0.5*np.cos(x)*np.cos(20.*x), lw=1.25,color='red', label='b')
plt.plot(x, 0.5*np.cos(x)*np.cos(20.*x), lw=1.25, ls=':', color='k', label='c')
plt.plot(x, 0.5*np.cos(x)*np.cos(20.*x), lw=1.25, ls='dashdot',color='blue', label='d')

plt.legend(frameon='False')

# Ajustando os limites do eixo y para -1.3 até 1.3
plt.ylim(-1.3, 1.3)

# Adicionando título e rótulos aos eixos
# plt.title('Gráfico de sin(x) e 1.03*sin(x)')
plt.xlabel('x')
plt.ylabel('y')

# Removendo linhas de grade
plt.grid(False)

plt.savefig('plot1.pdf')

# Mostrar o gráfico
plt.show()
