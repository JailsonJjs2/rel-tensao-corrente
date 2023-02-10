import pandas as pd

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


pdf = canvas.Canvas('Rel_Fases.pdf',pagesize=A4)

def mm2p(milimetros):
    return milimetros / 0.352777


tabela = pd.read_csv('DataSheet01.csv', sep=';', skiprows=2)

colunas = ['UA', 'UB', 'UC']

## T CRITICA ##
def verificarCritico(coluna):
    hora = tabela.loc[(tabela[coluna] < 110).any() or (tabela[coluna] > 135), 'Time'].unique()
    tensao = tabela.loc[(tabela[coluna] < 110).any() or (tabela[coluna] > 135), coluna].unique()
    cont = tabela[(tabela[coluna] < 110) | (tabela[coluna] > 135)][coluna].count()
    if cont > 0:
        #print(cont, f'Tensão(ões) {coluna}: {tensao} Crítica(s), Horário(s): {hora}')
        return f'{cont} Tensão(ões) {coluna}: {tensao} Crítica(s), Horário(s): {hora}'
    else:
        #print(cont, f'Tensão {coluna}: {tensao} Crítica')
        return f'{cont} Tensão {coluna}: {tensao} Crítica'
for coluna in colunas:
    verificarCritico(coluna)

## T PRECARIA ##
def verificarPrecario(coluna):
    hora = tabela.loc[(tabela[coluna] < 117).any() or (tabela[coluna] >= 133), 'Time'].unique()
    tensao = tabela.loc[(tabela[coluna] < 117).any() or (tabela[coluna] >= 133), coluna].unique()
    cont = tabela[(tabela[coluna] < 117) | (tabela[coluna] >= 133)][coluna].count()
    if cont > 0:
        #print(cont, f'Tensão(ões) {coluna}: {tensao} Precária(s), Horário(s): {hora}')
        return f'{cont} Tensão(ões) {coluna}: {tensao} Precária(s), Horário(s): {hora}'
    else:
        #print(cont, f'Tensão {coluna}: {tensao} Crítica')
        return f'{cont} Tensão {coluna}: {tensao} Crítica'
for coluna in colunas:
    verificarPrecario(coluna)

## T ADEQUADA ##
if ( ( (tabela['UA'] >= 117).any() and (tabela['UA'] < 133).any() ) and
        ( (tabela['UB'] >= 117).any() and (tabela['UB'] < 133).any() ) and
        ( (tabela['UC'] >= 117).any() and (tabela['UC'] < 133).any() )):
    contA = len(tabela[(tabela['UA'] >= 117) & (tabela['UA'] < 133)])
    print('Total Tensão(ões) A:', contA, 'Adequadas')
    contB = len(tabela[(tabela['UB'] >= 117) & (tabela['UB'] < 133)])
    print('Total Tensão(ões) B:', contB, 'Adequadas')
    contC = len(tabela[(tabela['UC'] >= 117) & (tabela['UC'] < 133)])
    print('Total Tensão(ões) C:', contC, 'Adequadas')

eixo = 285

for coluna in colunas:
    resultadoC = verificarCritico(coluna)
    pdf.drawString(mm2p(10), mm2p(eixo), resultadoC)
    eixo -= 8

pdf.translate(0, -mm2p(10))

for coluna in colunas:
    resultadoP = verificarPrecario(coluna)
    pdf.drawString(mm2p(10), mm2p(eixo), resultadoP)
    eixo -= 8

pdf.translate(0, -mm2p(10))

pdf.drawString(30, 670, f'Total Tensão(ões) A: {contA} Adequadas')
pdf.drawString(30, 640, f'Total Tensão(ões) B: {contB} Adequadas')
pdf.drawString(30, 610, f'Total Tensão(ões) C: {contC} Adequadas')
pdf.save()
