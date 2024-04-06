import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns 
import string
from utils import *
from constants import *
import datetime

def init_plt(subplots_0: int, subplots_f: int, w: int, h: int):
    fig, ax, = plt.subplots(subplots_0, subplots_f)
    fig.set_facecolor(color['background1'])
    fig.set_figwidth(w)
    fig.set_figheight(h)
    return (fig, ax)

def plot(indices: list, save_or_show: str=None):
    if len(indices) == 2:
        for i in indices:
            if (i[1] == 0 and (i[1] + 1) == 1):
                fig, ax = init_plt(subplots_0=1, subplots_f=2, w=17, h=7)
                break
            else:
                print("ERROR: Indices subplot out of bounds for some axis.")
                exit(-1)
    
    for index in indices:
        if (index[0] == 5 or index[0] == 6):
            x = []; y = [] 
            y = sorted(unique_items(column_items(index[0])))
            
            for n in range(1, 7):
                x.append(count_ocurrences(column_items(index[0]), n))
                
            print("histogram y: ", y, "size y: ", len(y))
            print("histogram x: ", x, "size x: ", len(x))
            make_histogram(ax=ax, column_index=index[0], x=x, y=y, indice_subplot=index[1], fig=fig)
            
        elif (index[0] == 7 or index[0] == 8 or index[0] == 2 or index[0] == 3 or index[0] == 4):
            x = []; y = [] 
            item_ocurrences = []
            split_all_items(x=x, alias=",", index=index[0], expections=[' etc;', ' faltas', ' provas'])
            y = unique_items(x) # labels
            
            if index[0] == 7:
                rm_multiples_duplicated_items(y=y, alias='complementares')
                rm_duplicated_item_by_key(y=y, key='Histórico acadêmico')
            
            if index[0] == 8:
                rm_duplicated_item_by_key(y=y, key='Calculadora de notas')
                rm_duplicated_item_by_key(y=y, key='Microhorário mais detalhado')
                y[0] = y[0] + ', provas, faltas, etc.'
                        
            for item in range(0, len(y)):
                item_ocurrences.append(check_item_equality(y, x, item))
                
            x = item_ocurrences
            if index[0] == 8:
                if y[1] == ' Mais objetividade e centralização das informações':
                    print("yes")
                    y[1] = 'Objetividade e centralização'
                    
            print("pie y: ", y, "size y: ", len(y))
            print("pie x: ", x, "size x: ", len(x))
            make_piechart(ax=ax, column_index=index[0], x=x, y=y, indice_subplot=index[1])
            
        elif (index[0] == 9):
            x = []; y = [] 
                
            x = unique_items(column_items(index=index[0]))
            x[1] = "Não"
            y = [count_ocurrences(column_items(index=index[0]), 'Sim'), count_ocurrences(column_items(index=index[0]), 'Não, prefiro usar no navegador mesmo')]
            
            print("bar y: ", y, "size y: ", len(y))
            print("bar x: ", x, "size x: ", len(x))
            make_bar(ax=ax, column_index=index[0], x=x, y=y, indice_subplot=index[1], orientation='h')
            
    plt.tight_layout()
    if save_or_show == 'save':
        plt.savefig(f"output/plot_{str(fig)}_{indices[0][0]}_{indices[1][0]}_{datetime.datetime.today().date()}.png")
    else:
        plt.show()
    
def make_bar(ax: any, column_index: int, x: list, y: list, indice_subplot: int, orientation: str='vertical'):
    title = df.columns[column_index]
    if orientation == 'h': # horizontal bar chart
        ax[indice_subplot].barh(x, y, height=0.6,color=(color_chart['color1'], 
                                            color_chart['color2'], 
                                            color_chart['color3'],
                                            color_chart['color4'], 
                                            color_chart['color5'], 
                                            color_chart['color6']), 
                                            ec="black")
        ax[indice_subplot].axvline(y[0], color='r', label=l10n['max_yes_count'], linewidth=0.6)
        ax[indice_subplot].axvline(y[1], color='b', label=l10n['max_no_count'], linewidth=0.6)

        inds=range(len(column_items(index=column_index)))
        ax[indice_subplot].grid(axis='y', color=color['soft_black'], linewidth = 0.3)
        # ax[indice_subplot].set_axisbelow(True)
        ax[indice_subplot].set_xticks([ind+0.0 for ind in inds])
        ax[indice_subplot].set_xlabel(l10n['votes_quantity'], fontdict=font['label'])
    else:
        barplot = ax[indice_subplot].bar(np.arange(len(x)), y, color=(color_chart['color1'], 
                                                                        color_chart['color2'], 
                                                                        color_chart['color3'],
                                                                        color_chart['color4'], 
                                                                        color_chart['color5'], 
                                                                        color_chart['color6']), 
                                                                        ec="black")
        ax[indice_subplot].set_xlabel(l10n['values_ocurrences'], fontdict=font['label'])
        ax[indice_subplot].set_ylabel(l10n['votes_quantity'], fontdict=font['label'])
        ax[indice_subplot].bar_label(barplot, labels=x, label_type="edge", padding=3, fontsize=12)

    ax[indice_subplot].set_title(title, fontdict=font['title'])
    ax[indice_subplot].legend()
    ax[indice_subplot].set_facecolor(color['background2'])

    
def make_histogram(ax: any, column_index: int, x: list, y: list, indice_subplot: list, fig=None, linebreakers=None):
    if linebreakers:
        title = config_strlabel(df.columns[column_index])
    else:
        title = df.columns[column_index]            
    bins = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    votes_count = column_items(column_index)
    x = votes_count
    median_votes_count = sum(column_items(column_index)) / len(column_items(column_index))
    
    print(votes_count)
    N, bins, patches = ax[indice_subplot].hist(x, bins=bins, edgecolor='black') # need to declare this varibales N, bins, patches to color the data
    patches[1].set_facecolor(color_chart['color1'])
    patches[2].set_facecolor(color_chart['color1'])
    patches[5].set_facecolor(color_chart['color1'])
    
    patches[0].set_facecolor(color_chart['color2'])
    patches[6].set_facecolor(color_chart['color2'])
    
    patches[3].set_facecolor(color_chart['color5'])
    patches[4].set_facecolor(color_chart['color6'])

    ax[indice_subplot].axvline(median_votes_count, color='r', label=l10n['votes_ocurrences_median'], linewidth=2)
    ax[indice_subplot].set_xlabel(l10n['values_ocurrences'] + '\n\n' + l10n[f'column{column_index}_description'], fontdict=font['label'])
    ax[indice_subplot].set_ylabel(l10n['votes_quantity'], fontdict=font['label'])
    ax[indice_subplot].legend()
    ax[indice_subplot].grid(axis='y', color=color['soft_black'])
    ax[indice_subplot].set_title(title, fontdict=font['title'])
    #ax[fig_index].text(fig.get_figwidth() / 2, fig.get_figheight() / 2, 'function', horizontalalignment='center', verticalalignment='center')

def make_piechart(ax: any, column_index: int, x: list, y: list, indice_subplot: int, fig=None, linebreakers=None):
    if linebreakers:
        title = config_strlabel(df.columns[column_index])
    else:
        title = df.columns[column_index]
    colors_pie = [v for v in color_chart.values()]
    
    max_value = max(x)
    for i in x:
        if i == max_value:
            if column_index == 7:
                explode = (0, 0, 0, 0.1, 0, 0, 0) # tuples are immutable
            elif column_index == 8:
                explode = (0.1, 0, 0, 0)
            elif column_index == 2 or column_index == 4:
                explode = (0.1, 0, 0)
            elif column_index == 3:
                explode = (0.1, 0)

    ax[indice_subplot].set_title(title, fontdict=font['title'])
    ax[indice_subplot].pie(x, labels=y, autopct="%.2f%%", shadow=False, colors=colors_pie, explode=explode)
    ax[indice_subplot].axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle
    ax[indice_subplot].set_xlabel(l10n[f'column{column_index}_description'], fontdict=font['label'])

if __name__ == "__main__":
    # About projet
    #plot(indices=[[5, 0], [7, 1]], save_or_show='save')
    plot(indices=[[6, 0], [8, 1]], save_or_show='save')
    #plot(indices=[[9, 0], [9, 1]], save_or_show='save')
    
    # About user
    #plot(indices=[[2, 0], [3, 1]], save_or_show='save')
    #plot(indices=[[4, 0], [4, 1]], save_or_show='save')