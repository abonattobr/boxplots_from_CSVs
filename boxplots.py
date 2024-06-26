import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import re

sns.color_palette("pastel")

# Configurando matplotlib para usar LaTeX globalmente
plt.rcParams.update({
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{siunitx}",
})

def format_title(variable):
    if re.match(r'R\d+$', variable):
        return rf"$R_{{{variable[1:]}}} \, [\si{{\micro\meter}}]$"
    elif re.match(r'L\d+$', variable):
        return rf"$L_{{{variable[1:]}}} \, [\si{{\micro\meter}}]$"
    elif re.match(r'wp\d+w$', variable) or variable == 'wpw':
        return rf"$\omega_{{p{variable[2] if variable != 'wpw' else ''}}}/\omega$"
    elif variable == 'zfoc':
        return r"$z_{foc}$"
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
    fig, axes = plt.subplots(num_rows, num_columns, figsize=(fig_width / 2, fig_height))

    for i, variable in enumerate(sorted([col for col in data if col not in ['Unnamed: 0', 'iteracao', 'Fobj', 'Group']])):
        ax = axes.flatten()[i] if num_rows > 1 or num_columns > 1 else axes
        sns.boxplot(x=['40 best'] * len(best_40) + ['40 last'] * len(last_40), 
                    y=pd.concat([best_40[variable], last_40[variable]]), 
                    ax=ax, linewidth=0.5, palette={'40 best': 'C0', '40 last': 'C3'}, 
                    showfliers=True, whis=[5, 95], width=0.5)

        for patch in ax.artists:
            r, g, b, a = patch.get_facecolor()
            patch.set_facecolor((r, g, b, .3))

        ax.axhline(y=best_40[variable].loc[best_40['Fobj'].idxmax()], color='C7', linewidth=1., dashes=[4,3])
        
        ax.set_title(format_title(variable), fontsize=14)
        set_axis_formatter(ax, variable)  # Ajustando o formatador do eixo Y
        
        # Desabilitando uso de LaTeX nos labels após plotar
        ax.xaxis.get_major_formatter()._usetex = False
        ax.yaxis.get_major_formatter()._usetex = False

        ax.tick_params(axis='x', labelsize=12)
        ax.tick_params(axis='y', labelsize=12)
        
        # ax.set_xlabel('Grupo', fontsize=10)
        # ax.set_ylabel('Valor', fontsize=10)
        ax.set_xlabel(None)
        ax.set_ylabel(None)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Configurando para mostrar menos tick labels no eixo y
        ax.yaxis.set_major_locator(ticker.MaxNLocator(5))
        
        ax.legend([], [], frameon=False)

    plt.tight_layout()
    plt.savefig(f'{case_filename.split(".")[0]}_final_boxplots.pdf')
    plt.close()

# Gerando e salvando os gráficos formatados para cada caso
generate_final_subplot_boxplots('completo_caso1.csv', 1, 5, 20, 6)
generate_final_subplot_boxplots('completo_caso2.csv', 2, 4, 20, 12)
generate_final_subplot_boxplots('completo_caso3.csv', 2, 4, 20, 12)
