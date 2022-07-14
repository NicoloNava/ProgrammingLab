
class ExamException(Exception):
    pass
class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name
    def get_data(self):
        # Inizializzo una lista vuota per salvare i valori
        values = []
        # Apro e leggo il file, linea per linea
        try:
            my_file = open(self.name, 'r')

        except FileNotFoundError: #se non esiste il file alzo un eccezione

            raise ExamException("Nome del file errato")
        last_epoch=-1
        for line in my_file:
            # Faccio lo split di ogni riga sulla virgola
            elements = line.split(',')
            # Se ho almeno 2 elementi sulla riga splittata sulla virgola
            if len(elements) >= 2:
                # Setto la data e il valore
                '''
                    se il secondo elemento della riga splittata sulla virgola
                    non è convertibile in int , smetto di processare questa riga
                '''
                try:
                    elements[0] = int(elements[0])

                except ValueError:

                    continue
                '''
                    se il secondo elemento della riga splittata sulla virgola
                    non è convertibile in float, smetto di processare questa riga
                '''
                try:
                    elements[1] = float(elements[1])

                except ValueError:

                    continue
                """
                 se la data di questo elemento non è ordinata in ordine cronologico rispetto a quella dell'
                 elemento precedente azo un eccezione
                """

                if last_epoch > elements[0]:
                    raise ExamException("ci sono valori non ordinati ")


                """
                 se la data di questo elemento  è uguale  a quella dell'
                 elemento precedente azo un eccezione
                """
                if last_epoch == elements[0]:
                    raise ExamException("ci sono valori consecutivi duplicati ")
                # Aggiungo alla lista dei valori questo valore
                values.append(elements)
                last_epoch=elements[0]

        my_file.close()

        #se la lista di valori è vuota alzo un eccezione

        if len(values)==0:
            raise ExamException("Tutti i valori non sono formattati correttamente o file vuoto")
        return values
def compute_daily_max_difference(time_series):
    """
     inizializzo la lista di valori in aoutput, la data da cui la lista in input parte,
     i flag di "prima iterazione", e il contatore di valori trovati per quello specifico giorno
    """
    values = []

    day_start_epoch_last=time_series[0][0] - (time_series[0][0] % 86400)
    highest_value_current_day=0
    lowest_value_current_day=0
    first_highest = True
    first_lowest = True
    count_values_in_c_day=0
    #itero sugli elementi della lista in input
    for item in time_series:
        #leggo e salvo la epoch e il valore della temperatura
        epoch=item[0]
        value=item[1]
        #calcolo a che giornata appartiene la epoch letta
        day_start_epoch = epoch - (epoch % 86400)
        """
         se il valore della temperatura è maggiore del piu' alto trovato 
         fino ad ora in questa giornata aggiorno il valore piu' alto
        """
        if value > highest_value_current_day or first_highest == True:
            highest_value_current_day=value
            first_highest = False
        """
          vice versa col valore piu' basso
        """
        if value < lowest_value_current_day or first_lowest == True:
            lowest_value_current_day=value
            first_lowest = False
        """
        se la giornata è cambiata rispetto a quella in cui eravamo
         nell'iterazione precedente, o siamo arrivati all'ultimo elemento della lista
        preparo i valori per il nuovo giorno e aggiungo l'escursione massima alla lista di output
        """
        if day_start_epoch_last != day_start_epoch or item==time_series[-1]:
            #se è l'ultimo elemento è un caso particolare
            if item==time_series[-1]:
                # se appartiene allo stesso giorno calcolo l'escursione e aggiungo uno al contatore
                if day_start_epoch_last == day_start_epoch:
                    excursion = highest_value_current_day - lowest_value_current_day
                    count_values_in_c_day += 1
                # se è l'ultimo elemento ed appartiene ad una giornata nuova l'escursione è necessariamente None
                else:
                    #appendi il valore trovato prima di quest ultima iterazione
                    values.append(excursion)
                    excursion=None

            #se abbiamo solo un valore in questa giornata
            if count_values_in_c_day==1:
                excursion=None

            highest_value_current_day=value

            lowest_value_current_day=value

            day_start_epoch_last=day_start_epoch
            count_values_in_c_day=0
            values.append(excursion)
        count_values_in_c_day += 1
        excursion = highest_value_current_day - lowest_value_current_day
    return values
time_series_file = CSVTimeSeriesFile(name='data.csv')
time_series = time_series_file.get_data()

print(compute_daily_max_difference(time_series))
