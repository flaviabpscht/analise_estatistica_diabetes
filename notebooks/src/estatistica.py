from scipy.stats import(
    levene,  
    mannwhitneyu, 
    ttest_ind, 
)
from collections import namedtuple

def remove_outliers(dados, largura_bigodes=1.5):
    """ Retorna outliers de uma coluna ou aaray
    Espera uma coluna categórica.

    Parameters
    ----------
   dados: pd.DataFtame[coluna], np.array
        Colunas ou arrays
    largura_bigode:
    padrão 1.5, mas pode ser alterado
    Returns 
    --------
    Float
        Valores que são considerados outliers de acordo com os parâmetros informados
        """
    q1 = dados.quantile (0.25)
    q3 = dados.quantile(0.75)
    iqr = q3-q1
    return dados[(dados>=q1-largura_bigodes *iqr) & (dados<=q3+largura_bigodes *iqr)]
    


    
def analise_levene(dataframe, alfa=0.05, centro='mean'):
    """#parâmetro center=
#median (mediana)é recomendada para a distribuição que tem algum tipo de assimetria (não normal)
#mean (media(é recomendada para distribui9ções simétricas (menos distorções)
#trimed é recomendada para caldas que tem um alongamento (uma calda muito longa)"""
    print('Teste de Levene')
    estatistica_levene, valor_p_levene= levene(
        *[dataframe[coluna] for coluna in dataframe.columns],
        center=centro,
        nan_policy="omit"
    )
    
    print(f'{ estatistica_levene= :.3f}')
    
    if valor_p_levene > alfa:
        print(f'Variâncias iguais (valor p:{valor_p_levene:.3f}). Hipótese nula válida')
    else:
        print(f' Ao menos uma variância é diferente (valor p:{valor_p_levene:.3f}). Hipótese nula pode ser desconsiderada')


def analise_ttest_ind(
    dataframe,
    alfa=0.05,
    variancias_iguais=True,
    alternativa="two-sided",
):
    #distribuição paramétrica
    print('Teste T amostras independentes')
    estatistica_ttest, valor_p_ttest = ttest_ind(
        *[dataframe[coluna] for coluna in dataframe.columns], 
        equal_var=variancias_iguais,
        alternative=alternativa,
        nan_policy="omit"
    )
        
    print(f"{estatistica_ttest= :.3f}")
    if valor_p_ttest > alfa:
        print(f"Não rejeita a hipótese nula (valor p: {valor_p_ttest:.3f})")
    else:
        print(f"Rejeita a hipótese nula (valor p: {valor_p_ttest:.3f})")

def analise_mannwhitneyu(
    dataframe,
    alfa=0.05,
    alternativa='two-sided',
        
):
    #distribuição paramétrica
    print('Teste Mannwhitneyu')
    estatistica_mannwhitneyu, valor_p_mannwhitneyu =  mannwhitneyu (
        *[dataframe[coluna] for coluna in dataframe.columns], 
        nan_policy='omit',
        alternative= alternativa
    )
        
    print(f"{estatistica_mannwhitneyu =:.3f}")
    if valor_p_mannwhitneyu > alfa:
        print(f"Não rejeita a hipótese nula (valor p: {valor_p_mannwhitneyu:.3f})")
    else:
        print(f"Rejeita a hipótese nula (valor p: {valor_p_mannwhitneyu:.3f})")

#distribuição não paramétrica (Anormal) três ou mais amostras emparelhadas


def histogramas_variaveis_categoricas(dataframe, 
                                      lista_colunas,
                                      coluna_alvo,
                                      linhas=4,
                                      colunas=4, 
                                      tamanho=(14, 16), 
                                      titulo="Análise variáveis categóricas",
                                      legenda = "Variável Alvo"
                                     ):

    fig, axs = plt.subplots(nrows=linhas, ncols=colunas, figsize=tamanho, sharey=True)
    
    for i, coluna in enumerate(lista_colunas):
        h = sns.histplot(x=coluna, 
                         hue=coluna_alvo, 
                         data=dataframe, 
                         multiple='fill', 
                         ax=axs.flat[i], 
                         stat='percent',
                         shrink=0.8)
        h.tick_params(axis='x', labelrotation=45)
        h.grid(False)
    
        h.yaxis.set_major_formatter(PercentFormatter(1))
        h.set_ylabel('')
    
        for bar in h.containers:
            h.bar_label(bar, label_type='center', labels=[f'{b.get_height():.1%}' for b in bar], color='white', weight='bold', fontsize=11)
    
        legend = h.get_legend()
        legend.remove()
    
    labels = [text.get_text() for text in legend.get_texts()]
    
    fig.legend(handles=legend.legend_handles, labels=labels, loc='upper center', ncols=2, title=legenda, bbox_to_anchor=(0.5, 0.965))
    fig.suptitle(titulo, fontsize=16)
    
    fig.align_labels()
    
    plt.subplots_adjust(wspace=0.4, hspace=0.3, top=0.9)
    
    plt.show()


def histogramas_variaveis_categoricas_nao_binarias(dataframe, 
                                      lista_colunas,
                                      coluna_alvo,
                                      linhas=4,
                                      colunas=1, 
                                      tamanho=(12, 16), 
                                      titulo="Análise variáveis categóricas",
                                      legenda = "Variável Alvo"
                                     ):

    fig, axs = plt.subplots(nrows=linhas, ncols=colunas, figsize=tamanho)
    
    for i, coluna in enumerate(lista_colunas):
        h = sns.histplot(x=coluna, 
                         hue=coluna_alvo, 
                         data=dataframe, 
                         multiple='fill', 
                         ax=axs.flat[i], 
                         stat='percent',
                         shrink=0.8)
        h.tick_params(axis='x', labelrotation=45)
        h.grid(False)
    
        h.yaxis.set_major_formatter(PercentFormatter(1))
        h.set_ylabel('')
    
        for bar in h.containers:
            h.bar_label(bar, label_type='center', labels=[f'{b.get_height():.1%}' for b in bar], color='white', weight='bold', fontsize=11)
    
        legend = h.get_legend()
        legend.remove()
    
    labels = [text.get_text() for text in legend.get_texts()]
    
    fig.legend(handles=legend.legend_handles, labels=labels, loc='upper center', ncols=2, title=legenda, bbox_to_anchor=(0.5, 0.965))
    fig.suptitle(titulo, fontsize=16)
    
    fig.align_labels()
    
    plt.subplots_adjust(wspace=0.1, hspace=0.7, top=0.925)
    
    plt.show()

