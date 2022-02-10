class ExamException(Exception):
    pass

""" 
Classe CSVFile
Serve per leggere una classe CSV file

---attributi---
self.name -> nome del file

---metodi---
__init__
    inizializza tutte gli attributi

__str__
    rappresentazione del file
    titolo, intestazione e numero di righe

get_data
    ritorna una lista di liste, le liste più piccole contengono le righe nelle quali ogni elemento rappresenta una colonna
"""
class CSVFile:

    def __init__(self, name):

        #NOME del file
        #Controlo Se il nome è una stringa che finisce per .csv
        if type(name) == str and name[-4:] == '.csv':
            t_input = True
        else:
            t_input = False

        #setto il nome
        self.name = name
        
        #se il tipo del file è corretto
        if not t_input:
            raise ExamException('Errore: il tipo del file non è .csv')

    #Presentazione del file
    def __str__(self):
        return '[----------]\n{}\n[----------]'.format(self.name)

    
    def get_data(self):

        #controllo se il file esiste
        try:
            my_file = open(self.name, 'r')
            my_file.close()
        except Exception:
            raise ExamException('Errore: il file non può essere aperto (inesistente)')

        #provo ad aprirlo
        my_file = open(self.name, 'r')
        #Controllo non sia vuoto
        vuoto = [1 for line in my_file if line != '\n' ]
        my_file.close()
        #Se il file è vuoto raiso un Exception
        if sum(vuoto) < 1:
            raise ExamException('Errore: il file passato è vuoto')

        #Prendo tutti i dati così come sono tranne le righe vuote
        #Apro il file
        my_file = open(self.name, 'r')
            
        #creo una lista vuota (all data)
        all_data = []

        #Prendo tutte le righe e le metto nella lista
        for line in my_file:            
            #divido la riga per ogni colonna
            l = line.strip('\n')
            l = l.split(',')
            #salvo la linea
            if l[0] != '':
                all_data.append(l)

        my_file.close()

        return all_data

class CSVTimeSeriesFile(CSVFile):
    #cosa deve fare

    #devo alzare eccesioni quando: (funzione)
    #quando la serie temporale non è ordinata o ci sono dei doppioni

    #gestione errori
    #un valore intero o non positivo non va considerato
    #linee incomplete
    #testo

    

    #prende il get data del super
    #converte le prime due colonnne in numeri e li aggiunge in una nuova lista
    #    (le colonne dopo non mi innteressano)
    def get_data(self):
        old_data = super().get_data()

        floaty_data = []
    
        for lista in old_data:
            linea = []
            for i, item in enumerate(lista):
                if i == 0:
                    linea.append(item)
                if i == 1:
                    try:
                        floaty_item = int(item)
                        if floaty_item < 0:
                            raise Exception
                        linea.append(floaty_item)
                    except:
                        linea.append(None)

            if linea[0] == 'date':
                pass
            else:
                floaty_data.append(linea)

        if not self.__time_check__(floaty_data):
            raise ExamException('Errore: ordine temporale sbagliato')
                        
        return floaty_data

    def __time_check__(self, dati):

        tutto_a_posto = True

        #considero solo le date (le righe con None o testo non vanno considerate)
        only_date =[]
        for lista in dati:
            only_date.append(lista[0])

        right_data = []
        for item in only_date:
            try:
                l = item.split('-')
                if len(l) != 2:
                    raise Exception
                l[0] = int(l[0])
                l[1] = int(l[1])
                right_data.append(l)
            except:
                pass

        mese = 1
        anno = right_data[0][0]
        for item in right_data:
            if item[0] != anno:
                tutto_a_posto = False
            if item[1] != mese:
                tutto_a_posto = False
            if mese == 12:
                mese = 1
                anno = anno + 1
            else:
                mese = mese + 1

        return tutto_a_posto

def compute_avg_monthly_difference(time_series, first_year, last_year):

    #potrei fare almeno il time check
    #e qualche altro check
    if not isinstance(first_year, str) or not isinstance(first_year, str):
        raise ExamException('Errore: le date inserite non sono stringhe')

    
    try:
        first_year = int(first_year)
        last_year = int(last_year)
    except:
        raise ExamException('errore: le date non sono del tipo giusto')

    if last_year < first_year:
        raise ExamException('Errore:  non si può tornare indietro nel tempo')
    
    #prima considero gli anni giusti
        #converto i get data in [anno, mese, passegieri]

    modified_data = []
    for item in time_series:
        l = item[0].split('-')
        l.append(item[1])
        modified_data.append(l)

    data = []
    for item in modified_data:
        linea = []
        for i in range(2):
            linea.append(int(item[i]))
        linea.append(item[2])
        data.append(linea)

    wanted_data = []

    for item in data:
        if item[0] >= first_year and item[0] <= last_year:
            wanted_data.append(item[2])

    nice_data = []

    for i in range(0, len(wanted_data), 12):
        nice_data.append(wanted_data[i:i+12])



    difference_year = last_year - first_year + 1
    result = [0,0,0,0,0,0,0,0,0,0,0,0]    

    for i in range(12):
        for j, item in enumerate(nice_data):
            if j + 1 < difference_year:
                if item[i] != None and nice_data[j + 1][i] != None:
                    result[i] = result [i] + abs(item[i] - nice_data[j + 1][i])

            
    real_result = []

    for item in result:
        if item != 0:
            real_result.append(item /( difference_year - 1))
        else:
            real_result.append(item)
        
    
    '''
    for i, item in enuemrate(data):
        if item[0] >= first_year and item[0] <= last_year:
            if item[2] != None:
                result[item[1] - 1] = result[item[1] - 1] +  
    
    '''
    
    '''

    for item in data:
        if item[0] >= first_year and item[0] <= last_year:
            print(item)
            if item[2] != None:
                result[item[1] - 1] = result[item[1] - 1] + item[2]

    print(result)
    print('---------')
    
    real_result = []

    for item in result:
        if item != 0:
            real_result.append(item / difference_year)
        else:
            real_result.append(item)

'''
    return real_result
    #dovrei avere una lista come la volgio io (ci sono dei null nei dati dei passeggieri)

    #faccio un altra funzione per cercare il dato dei passeggieri dato un anno e un giorno

    #faccio un ciclo for che va da 0 a 11
    #ogni ciclo dato il mese si trovano tutti i mesi e si sommano
    
    #only_passengers =[]

    #for item in time_series:
     #   only_passengers.append
    
    
#====================
# CORPO DEL PROGRAMMA
#====================

file = CSVTimeSeriesFile(name = 'file_vuoto.csv')
#print(file.get_data())
print(compute_avg_monthly_difference(file.get_data(), '1950', '1952'))


#cose ancora da fare:
'''
Lasciarsi temmpo per consegnare
commenti almeno i titoli e descrizioni delle funzioni
altri check nella funzione

se gli anni da considerare non esistono

capire cosa fare se manca una data (nel time check e nel cuore del programma); se è fuori ordine va alzata un' eccezzione ma se manca penso che si possa calcolare comunque
'''