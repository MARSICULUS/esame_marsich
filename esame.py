class ExamException(Exception):
    pass

""" 
Classe CSVFile
Serve per leggere una classe CSV file

---attributi---
self.name -> nome del file
self.title -> intestazione del file
self.righe -> numero di righe del file
self.can_read -> se il file esiste ed è leggibile(non vuoto)

---metodi---
__init__
    inizializza tutte gli attributi

__str__
    rappresentazione del file
    titolo, intestazione e numero di righe

__conta_righe__
    conta quante righe ci sono in un file
    non conta righe vuote

get_data
    ritorna una lista di liste, le liste più piccole contengono le righe nelle quali ogni elemento rappresenta una colonna

get_dates
    converte la lista di liste di get_data in una lista di liste, dove le date sono effettivamente l'oggetto datatime
"""
class CSVFile:

    def __init__(self, nome_file):

        #NOME del file
        #Controlo Se il nome è una stringa che finisce per .csv
        if type(nome_file) == str and nome_file[-4:] == '.csv':
            t_input = True
        else:
            t_input = False

        #setto il nome
        self.name = nome_file

        #CHECK:
        #esistenza file, tipo file, file vuoto
        
        #se il tipo del file è corretto
        if not t_input:
            raise ExamException('Errore: il tipo del file non è .csv')

        #controllo se il file esiste
        try:
            my_file = open(self.name, 'r')
            my_file.close()
        except Exception:
            raise ExamException('Errore: il file non può essere aperto (inesistente)')

        #controllo se il file non è vuoto
        if self.__conta_righe__() < 1:
            raise ExamException('Errore: il file è vuoto')
        

        #TITOLO e RIGHE
        #Quando il file si può leggere controllo se non è vuoto
        #Apro il file e prendo il titolo
        my_file = open(self.name, 'r')
        titolo = my_file.readline().strip('\n')
        my_file.close()
        self.title = titolo
        self.righe = self.__conta_righe__()

             
    #Presentazione del file
    def __str__(self):
        return '[----------]\n{}\n    {}\n    numero righe: {}\n'.format(self.name, self.title, self.righe)
             

    def __conta_righe__(self):
        my_file = open(self.name, 'r')

        #Creo una lista di 1 per ogni riga non vuota a partire dalla seconda
        lst = [1 for i, line in enumerate(my_file) if i > 0 and line != '\n']

        my_file.close()
        return sum(lst)

    def get_data(self):

        #Prendo tutti i dati così come sono tranne le righe vuote
        #Apro il file
        my_file = open(self.name, 'r')
            
        #creo una lista vuota (all data)
        all_data = []

        #Prendo tutte le righe e le metto nella lista
        for i, line in enumerate(my_file):
                #divido la riga per ogni colonna
                l = line.strip('\n')
                l = l.split(',')
                #salvo la linea
                all_data.append(l)

        my_file.close()

        return all_data

class CSVTimeSeriesFile(CSVFIle, nome_file):
    #cosa deve fare

    #prende il get data del super
    #converte le prime due colonnne in numeri e li aggiunge in una nuova lista
    #    (le colonne dopo non mi innteressano)

    old_data = super().get_data(nome_file)
    floaty_data = []

    for lista in old_data:
        for i, item in enumerate(lista):
            linea = []
            if i === 0:
                linea.append(item)
                try:
                    floaty_item = float(item)
                    floaty_data.append(floaty_item)
                    
    

#================
# CORPO DEL PROGRAMMA
#====================

file = CSVFile('shampoo_sales.csv')
print(file)
print(file.get_data())