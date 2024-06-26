import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import re
import os
import sys

sns.color_palette("pastel")

# plt.style.use(os.path.join(os.getcwd(), 'onehalf_golden.mplstyle'))

# Configurando matplotlib para usar LaTeX globalmente
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

def format_title(variable):
    if re.match(r'R\d+$', variable):
        return rf"$R_{{{variable[1:]}}} \, [\si{{\micro\meter}}]$"
    elif re.match(r'L\d+$', variable):
        return rf"$L_{{{variable[1:]}}} \, [\si{{\micro\meter}}]$"
    elif variable == 'wpw':
        return r"$\omega_{p1}/\omega$"
    elif re.match(r'wp\d+w$', variable):
        num = re.search(r'\d+', variable).group()
        return fr"$\omega_{{p{num}}}/\omega$"
    elif variable == 'zfoc':
        return r"$z_{foc} \, [\si{{\micro\meter}}]$"
    else:
        return variable


def set_axis_formatter(ax, variable):
    # Definindo o número de casas decimais conforme a variável
    if variable == 'wpw' or re.match(r'wp\d+w$', variable):
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%.3f'))
    else:
        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

def generate_final_subplot_boxplots(case_filename, num_rows, num_columns, fig_width, fig_height):
    data = pd.read_csv(case_filename)
    best_40 = data.sort_values(by='Fobj', ascending=False).head(40)
    last_40 = data.tail(40)

    # Encontrando os limites de dados para 'wpw'
    # data_wpw = pd.concat([best_40['wpw'], last_40['wpw']])
    # lower_bound, upper_bound = np.percentile(data_wpw, [1.175, 100.])

    fig, axes = plt.subplots(num_rows, num_columns, figsize=(fig_width / 2, fig_height))

    if 'caso1' in case_filename:
        var_order = ['zfoc', 'wpw', 'R1', 'L1', 'R2']
    else:  # Casos 2 e 3
        var_order = ['zfoc', 'wp1w', 'wp2w', 'R1', 'L1', 'R2', 'L2', 'R3']

    for i, variable in enumerate(var_order):
        ax = axes.flatten()[i]
        sns.boxplot(x=['best'] * len(best_40) + ['last'] * len(last_40), 
                    y=pd.concat([best_40[variable], last_40[variable]]), 
                    ax=ax, linewidth=0.25, palette={'best': 'C0', 'last': 'C3'},
                    showfliers=False, whis=[5, 95], width=0.25, fliersize=0.5)

        for patch in ax.artists:
            r, g, b, a = patch.get_facecolor()
            patch.set_facecolor((r, g, b, .3))

        ax.axhline(y=best_40[variable].loc[best_40['Fobj'].idxmax()], color='red', linewidth=0.5, dashes=[4, 3])
        
        ax.set_title(format_title(variable), fontsize=8)
        set_axis_formatter(ax, variable)

        # Ajustar a escala do wpw (caso 1 apenas)
        # if variable == 'wpw':
        #     ax.set_ylim(lower_bound, None)

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

    plt.tight_layout()

    # Aplicando ajustes de espaçamento específicos para cada caso
    if 'caso1' in case_filename:
        plt.subplots_adjust(wspace=0.7, hspace=0.6, left=0.0675, right=0.95, top=0.8, bottom=0.15)
    else:  # Casos 2 e 3
        plt.subplots_adjust(wspace=0.7, hspace=0.6, left=0.0675, right=0.95, top=0.9, bottom=0.1)

    plt.savefig(f'{case_filename.split(".")[0]}_boxplots.pdf')
    plt.close()

# Gerando e salvando os gráficos formatados para cada caso
generate_final_subplot_boxplots('completo_caso1.csv', 1, 5, 7.2, 1.08)
generate_final_subplot_boxplots('completo_caso2.csv', 2, 4, 7.2, 2.16)
generate_final_subplot_boxplots('completo_caso3.csv', 2, 4, 7.2, 2.16)
