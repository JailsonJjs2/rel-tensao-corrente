import pandas as pd

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


pdf = canvas.Canvas('Rel_Fases_i.pdf',pagesize=A4)

def mm2p(milimetros):
    return milimetros / 0.352777


tabela = pd.read_csv('CurrentHarmonics.csv', sep=';', skiprows=2)

colunas = ['IHD2A']


def verificarCritico(coluna):
    hora = tabela.loc[(tabela[coluna] > 1.08)]['time'].unique()
    ia = tabela.loc[(tabela[coluna] > 1.08)][coluna].unique()
    cont = tabela[(tabela[coluna] > 1.08)][coluna].count()
    if cont > 0:
        return f'{cont} I max (A) {coluna}: {ia} Crítica(s), Horário(s): {hora}'


for coluna in colunas:
    resultadoC = verificarCritico(coluna)
    print(resultadoC)



