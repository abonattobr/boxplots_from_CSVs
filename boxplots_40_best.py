import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import re
import os
import sys

# Configurando a paleta de cores do Seaborn
# sns.color_palette("pastel")
sns.set_palette("pastel")

# Configurações do Matplotlib para usar LaTeX globalmente
plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{siunitx}",
    "axes.linewidth": 0.25,
    "axes.edgecolor": (0.35,0.35,0.35),
    "axes.labelcolor": (0.35,0.35,0.35),
    "xtick.major.size": 1.5,
    "xtick.major.width": 0.25,
    "xtick.minor.size": 0.75,
    "xtick.minor.width": 0.25,
    "ytick.major.size": 1.5,
    "ytick.major.width": 0.25,
    "ytick.minor.size": 0.75,
    "ytick.minor.width": 0.25,
    "text.color": (0.35,0.35,0.35),
    "xtick.color": (0.35,0.35,0.35),
    "ytick.color": (0.35,0.35,0.35)
})

def format_title(var):
    if re.match(r'R\d+$', var):
        return rf"$R_{{{var[1:]}}} \, [\si{{\micro\meter}}]$"
    elif re.match(r'L\d+$', var):
        return rf"$L_{{{var[1:]}}} \, [\si{{\micro\meter}}]$"
    elif var == 'wpw':
        return r"$\omega_{p1}/\omega$"
    elif re.match(r'wp\d+w$', var):
        num = re.search(r'\d+', var).group()
        return fr"$\omega_{{p{num}}}/\omega$"
    elif var == 'zfoc':
        return r"$z_{foc} \, [\si{{\micro\meter}}]$"
    elif var == 'F_obj':
        return r"$F_{obj} \, [\si{{arb. unit.}}]$"
    elif var == 'E_median':
        return r"$\tilde{E}_{sel} \, [\si{{MeV}}]$"
    elif var == 'E_max':
        return r"$E_{max} \, [\si{{MeV}}]$"
    elif var == 'Q_tot':
        return r"$Q_{sel} \, [\si{{\pico\coulomb}}]$"
    else:
        return var

def set_axis_formatter(ax, var):
    if var == 'wpw' or re.match(r'wp\d+w$', var):
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
    else:
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

# Definir caminhos dos arquivos (substitua os caminhos pelos seus arquivos específicos)
caso1_path = "caso1_outputs.csv"
caso2_path = "caso2_outputs.csv"
caso3_path = "caso3_outputs.csv"

# Carregar os DataFrames
caso1_df = pd.read_csv(caso1_path, sep='\t')
caso2_df = pd.read_csv(caso2_path, sep='\t')
caso3_df = pd.read_csv(caso3_path, sep='\t')

# Definindo o fator de multiplicação para ter a carga em pC
Q_factor = 1000

# Multiplicando os valores de 'Q_tot' por Q_factor
caso1_df['Q_tot'] *= Q_factor
caso2_df['Q_tot'] *= Q_factor
caso3_df['Q_tot'] *= Q_factor

# Selecionar os 40 resultados com os maiores valores de 'F_obj'
caso1_top40 = caso1_df.nlargest(40, 'F_obj')
caso2_top40 = caso2_df.nlargest(40, 'F_obj')
caso3_top40 = caso3_df.nlargest(40, 'F_obj')

# Adicionar coluna 'Case'
caso1_top40['Case'] = '1'
caso2_top40['Case'] = '2'
caso3_top40['Case'] = '3'

# Concatenar os DataFrames
df = pd.concat([caso1_top40, caso2_top40, caso3_top40])

# Criação das visualizações
fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(0.5*7.2, 1.2*1.08))
var_names = ['F_obj', 'E_median', 'E_max', 'Q_tot']  # Adicione mais variáveis conforme necessário

for ax, var in zip(axes, var_names):
    sns.boxplot(x='Case', y=var, data=df,
                palette={'1': 'C3', '2': 'C0', '3': 'C2'},
                ax=ax, showfliers=True, whis=[5, 95],
                width=0.30, fliersize=0.5, linewidth=0.25)

    # Encontrando o valor máximo de F_obj para cada caso e plotando a linha tracejada
    print('Results from optimal simulations:')
    for i, case in enumerate(['1', '2', '3']):
        case_df = df[df['Case'] == case]
        max_f_obj_row = case_df[case_df['F_obj'] == case_df['F_obj'].max()].iloc[0]
        # Desenhar uma linha horizontal tracejada
        ax.hlines(max_f_obj_row[var], xmin=i-0.25, xmax=i+0.25, colors='red', linestyles='dashed', linewidth=0.5, zorder=1000)
        print('%s - %s = %s' %(case, var, max_f_obj_row[var]))


    ax.set_title(format_title(var), fontsize=8)
    set_axis_formatter(ax, var)
    ax.xaxis.get_major_formatter()._usetex = False
    ax.yaxis.get_major_formatter()._usetex = False
    ax.tick_params(axis='x', labelsize=7)
    ax.tick_params(axis='y', labelsize=7)
    ax.set_xlabel(None)
    ax.set_ylabel(None)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(2))
    ax.legend([], [], frameon=False)

# Desativando temporariamente o LaTeX para a fonte fina
with plt.rc_context({'text.usetex': False}):
    fig.text(0.5, 0.04, 'Case', ha='center', fontsize=7, fontweight='light')

plt.tight_layout()
plt.subplots_adjust(wspace=0.75*0.7, hspace=0.6, left=0.0675, right=0.95, top=0.8, bottom=1.5*0.15)
plt.savefig('boxplots_40_best.pdf')
# plt.show()
plt.close()
