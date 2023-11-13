#Importação de bibliotecas

import statistics
from turtle import color

import matplotlib.pyplot as plt

import scipy.stats as stats

import pandas as pd

# Anexo da tabela do excel com os dados da rentabilidade dos 10 ativos analisados
tabela = r"C:\Users\gabip\OneDrive\Área de Trabalho\Programação\Tabela Rentabilidade dos Ativos.xlsx"

#Lista com os valores dos índices de mercados acumulados do ano dos dados coletados
índices_de_Mercado_2022={
   "CDI": 12.39,
   "Selic": 13.75,
   "IGPM": 5.45,
   "IPCA": 5.78,
}

print()
print("------------------------------------------------- Carteira de Títulos Públicos ------------------------------------------------------------")
print()

#Lista contendo os dados da rentabilidade de cada um dos 5 ativos públicos
dados=pd.read_excel(tabela,sheet_name="Títulos Públicos")

LFT =(dados.iloc[0:, 2]).tolist()

LTN=(dados.iloc[0:, 6]).tolist()

NTNB=(dados.iloc[0:, 10]).tolist()

NTNC=(dados.iloc[0:, 14]).tolist()

NTNF=(dados.iloc[0:, 18]).tolist()

listas = {"LFT": LFT, "LTN": LTN, "NTNB": NTNB, "NTNC": NTNC, "NTNF": NTNF}
títulos=["LFT","LTN","NTNB","NTNC","NTNF"]

# Lista com a taxa de retorno de cada ativo
taxas={"LFT": 13.75,
        "LTN": 10.83,
        "NTNB": 5.78,
        "NTNC": 16.91,
        "NTNF": 9.58,}

#Listas para armazenar cada tipo de dado estatístico das rentabilidades dos títulos.
médias=[]
variâncias=[] 
desvpads=[]
coevs=[]

def cálculos(): #Função para cálcular medidas estatísticas dos títulos.

  for x,y in listas.items():

    média=float(statistics.mean(y))
    médias.append(média)

    variância=float(statistics.variance(y))
    variâncias.append(variância)

    desvpad=float(variância**(1/2))
    desvpads.append(desvpad)

    coev=(desvpad/média)*100
    coevs.append(coev)

cálculos()

covcres=sorted(coevs)
#Função para colocar os coeficientes de variação em ordem crescente. 
# Assim, é possível identificar os dois ativos com menores coeficientes, que irão para a carteira.

menorcov=coevs.index(covcres[0])
menorcov2=coevs.index(covcres[1])

print("Os dois títulos que irão compor a carteira de títulos públicos são : ", títulos[menorcov],"e", títulos[menorcov2])

média1= médias[menorcov]
média2= médias[menorcov2]

#Funções para cálculo do índice de Sharpe:

w1=[] #Lista das proporções possíveis de aplicação no ativo.
for i in range(0,101):
      a=(i/100)
      w1.append(a)

mp=[] #Lista para armazenar os valores das médias do portifólio.
def médiaport():

    for a in w1:
     m=a*média1+(1-a)*média2 
     mp.append(m)

dadoscorrel1=listas[títulos[menorcov]]
dadoscorrel2=listas[títulos[menorcov2]]

correl=stats.pearsonr(dadoscorrel1,dadoscorrel2)
correl=correl[0] #Cálculo da correlação. Necessário para o cálculo da covariância.

def covariancia(): #Cálculo da covariância. Necessário para o cáculo da variância do portifólio.
       
       desvpads[menorcov]=float(desvpads[menorcov])
       desvpads[menorcov2]=float(desvpads[menorcov2])
       covariancia=desvpads[menorcov]*desvpads[menorcov2]*correl
       return covariancia

covar=covariancia()

vp=[] #Lista para armazenar os valores das variâncias do portifólio.
def variânciaport():

    variância1= variâncias[menorcov]
    variância2= variâncias[menorcov2]

    for a in w1:
     v=(a**2)*variância1+((1-a)**2)*variância2+2*a*(1-a)*covar
     vp.append(v)
     
dpp=[] #Lista para armazenar os valores dos desvios padrões do portifólio.
def desvpadport():
    
    for i in vp:
       d=i**(1/2)
       dpp.append(d)

dadossharpe=[] #Lista para armazenar os valores do índice de sharpe.
def sharpe():
   
   s1=[]
   for i in mp:
      s=(i-0.000353029)
      s1.append(s)

   for x,y in zip(s1,dpp):
      p=x/y
      dadossharpe.append(p)

#Exeção das funções 
médiaport()
variânciaport()
desvpadport()
sharpe()

#A partir do maior índice de sharpe, é identificada a proporção do investimento que deve ser aplicada em cada ativo.
maiorsharpe=max(dadossharpe)
g=dadossharpe.index(maiorsharpe)
proporção1=w1[g]*100
proporção2=(1-w1[g])*100

print("O melhor investimento é alocar",proporção1,"% do seu dinheiro no título",menorcov,"e",proporção2,"% no título",menorcov2,".")

def retornos_esperados(): #Cálculo dos retornos esperados de cada ativo e do retorno total da carteira.

   ret1=taxas[títulos[menorcov]]*(proporção1/100)
   ret2=taxas[títulos[menorcov2]]*(proporção2/100)
   rettotal=ret1+ret2
   print("O retorno esperado de",menorcov,"é de",ret1,"%")
   print("O retorno esperado de",menorcov2,"é de",ret2,"%")
   print("O retorno total da carteira é de",rettotal,"%")
   return rettotal

rettotal=retornos_esperados() 

print()
print("Comparando com os índice do mercado, o retorno total dessa carteira é:")

#Loop para comparar o retorno total da carteira com índice de mercado listados anteriormente.
for x,y in índices_de_Mercado_2022.items():
   if rettotal>y:
      print("Maior do que o retorno do",x)
   elif rettotal<y:
      print("Menor do que o retorno do",x)
   else:
      print("Igual ao retorno do",x)

#Anexo de dados de uma rentabilidade do mercado para o cáculo do coeficiente beta da carteira.
dados=pd.read_excel(tabela,sheet_name="Dados IBOVESPA")

IBOVESPA =(dados.iloc[:, 2]).tolist()

#Ajuste do tamanho da lista para que seja possível calcular a correlção.
dadoscorrel1novo = dadoscorrel1[:-1]

dadoscorrel2novo = dadoscorrel2[:-1]

correl=stats.pearsonr(dadoscorrel1novo,IBOVESPA)
correl1=correl[0] #Cálculo da correlação. Necessário para o cálculo da covariância.

correl=stats.pearsonr(dadoscorrel2novo,IBOVESPA)
correl2=correl[0] #Cálculo da correlação. Necessário para o cálculo da covariância.

varIBOVESPA=float(statistics.variance(IBOVESPA))
desvpadIBOVESPA=float(varIBOVESPA**2)

def coeficiente_beta(): #Função para calcular o coeficiente beta.
   covariancia1=desvpadIBOVESPA*desvpads[menorcov]*correl1
   covariancia2=desvpadIBOVESPA*desvpads[menorcov2]*correl2
   b1=covariancia1/varIBOVESPA
   b2=covariancia2/varIBOVESPA
   bcarteira=b1*proporção1+b2*proporção2
   print()
   print("O coeficiente beta da carteira é",bcarteira )

   #Teste da volatilidade da carteira de acordo com o resultado do coeficiente.
   if bcarteira>1:
      print("Sua carteira é mais volátil do que o mercado.")
   elif bcarteira<1:
      print("Sua carteira é menos volátil que o mercado.")
   else:
      print("Sua carteira apresenta a mesma volatilidade do mercado.")

   return bcarteira

bcarteira=coeficiente_beta()

def índice_de_treynor(): #Função para calcular o índice de treynor.

   it= (rettotal*0.000353029)/bcarteira
   print()
   print("O índice de Treynor dessa carteira é",it)

   if it<0: #Teste sobre o retorno da carteira de acordo com o resultado do índice
      print("Essa carteira está gerando um retorno insuficiente em relação ao risco sistemático.")
   elif it>0:
      print("Essa carteira está gerando um retorno suficiente em relação ao risco sistemático.")
   else:
      print("Essa carteira está gerando um retorno que é exatamente o esperado para o nível de risco sistemático.")

índice_de_treynor()

#Montagem do gráfico para comparar o retorno da carteira com os índices de mercado.
valor1=[rettotal]
valor2=[índices_de_Mercado_2022["CDI"]]
valor3=[índices_de_Mercado_2022["Selic"]]
valor4=[índices_de_Mercado_2022["IGPM"]]
valor5=[índices_de_Mercado_2022["IPCA"]]

def gráfico1():
    categorias=["Carteira","CDI","SELIC","IGPM","IPCA"]
    valores=[valor1,valor2,valor3,valor4,valor5]
    cores=["red","green","pink","blue","orange"]

    largura_barra = 0.4

    #Loop para separar cada barra do gráfico.
    for i, (categoria, valor, cor) in enumerate(zip(categorias, valores, cores)):
        
        posicao = i * largura_barra
        plt.bar(posicao, valor, width=largura_barra, color=cor, label=f'{categoria}')

    plt.title("Carteira vs índices do Mercado")
    plt.xticks([i * largura_barra for i in range(len(categorias))], categorias)  #Loop para ajudar os nomes das barras no eixo x.
    plt.ylabel("Retorno(%)")
    plt.legend()
    plt.show()

gráfico1()

print()
print("------------------------------------------------- Carteira de Títulos Privados ------------------------------------------------------------")
print()

#Lista contendo os dados da rentabilidade de cada um dos 5 ativos privados
dados=pd.read_excel(tabela,sheet_name="Títulos Privados")

LCAMA9=(dados.iloc[0:, 2]).tolist()

CMGD27=(dados.iloc[0:, 6]).tolist()

UNDAC3=(dados.iloc[0:, 10]).tolist()

RDORB7=(dados.iloc[0:, 14]).tolist()

BSA315=(dados.iloc[0:, 18]).tolist()

listas = {"LCAMA9": LCAMA9, "CMGD27": CMGD27, "UNDAC3": UNDAC3, "RDORB7": RDORB7, "BSA315": BSA315}
títulos=["LCAMA9","CMGD27","UNDAC3","RDORB7","BSA315"]

# Lista com a taxa de retorno de cada ativo
taxas={"LCAMA9":14.78,
       "CMGD27":9.88,
       "UNDAC3":13.87,
       "RDORB7":13.63,
       "BSA315":13.55,
       }

#Listas para armazenar cada tipo de dado estatístico das rentabilidades dos títulos.
médias=[]
variâncias=[] 
desvpads=[]
coevs=[]

cálculos() #Função para cálcular medidas estatísticas dos títulos.

covcres=sorted(coevs)
#Função para colocar os coeficientes de variação em ordem crescente. 
# Assim, é possível identificar os dois ativos com menores coeficientes, que irão para a carteira.

menorcov=coevs.index(covcres[0])
menorcov2=coevs.index(covcres[1])

print("Os dois títulos que irão compor a carteira de títulos públicos são : ", títulos[menorcov],"e", títulos[menorcov2])

média1= médias[menorcov]
média2= médias[menorcov2]

dadoscorrel1=listas[títulos[menorcov]]
dadoscorrel2=listas[títulos[menorcov2]]

média1= médias[menorcov]
média2= médias[menorcov2]

#Funções para cálculo do índice de Sharpe:

w1=[] #Lista das proporções possíveis de aplicação no ativo.
for i in range(0,101):
      a=(i/100)
      w1.append(a)

mp=[] #Lista das médias do portifólio.

correl=stats.pearsonr(dadoscorrel1,dadoscorrel2)
correl=correl[0] #Cálculo da correlação. Necessário para o cálculo da covariância.

covar=covariancia()

vp=[] #Lista das variãncias do portifólio.
dpp=[] #Lista dos desvios padrões do portifólio
dadossharpe=[] #Lista dos resultados dos índices de sharpe.

#Exeção das funções 
médiaport()
variânciaport()
desvpadport()
sharpe()

#A partir do maior índice de sharpe, é identificada a proporção do investimento que deve ser aplicada em cada ativo.
maiorsharpe=max(dadossharpe)
g=dadossharpe.index(maiorsharpe)
proporção1=w1[g]*100
proporção2=(1-w1[g])*100

print("O melhor investimento é alocar",proporção1,"% do seu dinheiro no título",menorcov,"e",proporção2,"% no título",menorcov2,".")

rettotal=retornos_esperados()

print()
print("Comparando com os índice do mercado, o retorno total dessa carteira é:")

for x,y in índices_de_Mercado_2022.items():
   if rettotal>y:
      print("Maior do que o retorno do",x)
   elif rettotal<y:
      print("Menor do que o retorno do",x)
   else:
      print("Igual ao retorno do",x)

dados=pd.read_excel(tabela,sheet_name="Dados IBOVESPA")

IBOVESPA =(dados.iloc[:, 2]).tolist()

dadoscorrel1novo = dadoscorrel1[:-1]

dadoscorrel2novo = dadoscorrel2[:-1]

correl=stats.pearsonr(dadoscorrel1novo,IBOVESPA)
correl1=correl[0] #Cálculo da correlação. Necessário para o cálculo da covariância.

correl=stats.pearsonr(dadoscorrel2novo,IBOVESPA)
correl2=correl[0] #Cálculo da correlação. Necessário para o cálculo da covariância.

varIBOVESPA=float(statistics.variance(IBOVESPA))
desvpadIBOVESPA=float(varIBOVESPA**2)

bcarteira=coeficiente_beta()

índice_de_treynor()

valor1=[rettotal]
valor2=[índices_de_Mercado_2022["CDI"]]
valor3=[índices_de_Mercado_2022["Selic"]]
valor4=[índices_de_Mercado_2022["IGPM"]]
valor5=[índices_de_Mercado_2022["IPCA"]]

gráfico1()