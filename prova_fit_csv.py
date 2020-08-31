import math
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

import csv
import pandas as pd
url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/dpc-covid19-ita-andamento-nazionale.csv'


# apri foglio csv
file_dati = pd.read_csv(url, error_bad_lines=False)
print("L'ultima data diponibile è:",str(file_dati['data'][int(file_dati['data'].count())-1])[:10])
print("L'ultima data corrisponde a:",file_dati['data'].count())

# inizializza variabili per raccogliere dati
xdata =[]
ydata = []
# prende i giorni dalla colonna 1 e i dat dalla colonna 2, partendo dalla seconda riga
# def get_data(giorno):
#     range_giorno= 'A'+str(giorno+1)
#     range_dati = 'b'+ str(giorno+1)

#     for row in sheet_ranges['A2':range_giorno]:
#         for cell in row:
#             xdata.append(cell.value)

#     for row in sheet_ranges['B2':range_dati]:
#         for cell in row:
#             ydata.append(cell.value)

def get_data(giorno, argomento):

    i=0
    while i < giorno:
        ydata.append(file_dati[argomento][i])
        i = i+1




# messaggio di benvenuto
print("Benvenuto: selezionare il giorno fino a cui cercare il fit!")
# chiede fino a che giorno calcolare
giorno_input = int(input("fino a che giorno:"))
print('Ottimo: ora selezionare cosa si vuole fittare:')
print('scrivere "totale_casi" per i casi totali, "deceduti" per i deceduti')
argomento = str(input('Che dati devo fittare?'))

# costruisci le due liste di dati
get_data(giorno_input, argomento)
j=1

while j<= giorno_input:
    xdata.append(j)
    j=j+1

newydata = []


# funzione con cui cercare il fit
def f(x,a,b,c,d):
    #y = (a*math.atan2((b*x-c),1))+d
    #y= a*math.e**(b*x-c)+d
    y= a*(1+b*math.e**(-x/c))/(1+d*math.e**(-x/c))
    return y

# fit vero e proprio
popt, pcov = curve_fit(f,xdata,ydata)


# asse x per plottare la funzione "continua"
x_1 = np.linspace(0, giorno_input, 200)

# ciclo per ottenere  ìle y della funzione "continua"
i=0
while i <200:
    newydata.append(f(x_1[i],popt[0],popt[1],popt[2],popt[3]))
    i= i+1

print('In Italia ci saranno',str(int(popt[0])),'contagiati.')

#plot vero e proprio
plt.legend("fit")
plt.ylim(top=ydata[-1]*100/98)
plot_funzione, = plt.plot(x_1,newydata, 'y-')
plot_dati, = plt.plot(xdata,ydata, 'r+')
plot_dati.set_label('Dati')
plot_funzione.set_label('Funzione logistica del fit')
plt.legend()
if argomento == 'totale_casi':
    plt.title('Casi Totali')
elif argomento == 'deceduti':
    plt.title('Deceduti')
plt.show()
