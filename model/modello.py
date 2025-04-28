from database.DAO import DAO
from model.powerOutages import Event


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self.ore_tot = 0
        self.persone_tot = 0





    def worstCase(self, nerc, maxY, maxH):
        # TO FILL
        self._solBest = []
        self.ore_tot = 0
        self.persone_tot = 0
        self.ricorsione([], maxY, maxH,0)
        print(self._solBest)
        print("Ore totali:",self.ore_tot)
        print("Persone totali:", self.persone_tot)
        return self._solBest, (self.ore_tot, self.persone_tot)

    def isValidConAnni(self, parziale, maxY, event : Event):
        #se len di parziale è <= 2 lo aggiungoe return True
        if len(parziale) <= 2:
            return True

        #trovo il piu giovane
        giovane = min(parziale+[event], key=lambda e: e.date_event_began)
        vecchio = max(parziale+[event], key=lambda e: e.date_event_began)
        # Prendo solo la differenza di anni
        diff_anni = vecchio.date_event_began.year - giovane.date_event_began.year
        if diff_anni > maxY:
            return False
        return True

    def calcolaOre(self, parziale):
        ore_tot = 0
        for event in parziale:
            delta = event.date_event_finished - event.date_event_began
            ore_evento = delta.total_seconds() / 3600
            ore_tot += ore_evento
        return ore_tot

    def calcolaPersoneCoivolte(self, parziale):
        n_persone = 0
        for event in parziale:
            n_persone += event.customers_affected
        return n_persone



    def ricorsione(self, parziale, maxY, maxH,pos):
        # TO FILL

        #condizione terminale raggiungo il massimo numero di ore
        if self.calcolaOre(parziale) <= maxH:
            #print(parziale)
            if self.calcolaPersoneCoivolte(parziale) > self.calcolaPersoneCoivolte(self._solBest):
                self._solBest = list(parziale)
                self.ore_tot = self.calcolaOre(self._solBest)
                self.persone_tot = self.calcolaPersoneCoivolte(self._solBest)



            #for event in self._listEvents:
        for i in range(pos, len(self._listEvents)):
                #vado a mettere un controllo su gli anni
            event = self._listEvents[i]
            if self.isValidConAnni(parziale, maxY, event):
                parziale.append(event)
                self.ricorsione(parziale, maxY, maxH,i+1)
                parziale.pop()




    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)
        #print(self._listEvents)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()
        #print(self._listNerc)


    @property
    def listNerc(self):
        return self._listNerc

if __name__ == "__main__":
    my_model = Model()
    my_model.loadNerc()
    my_model.loadEvents(my_model.listNerc[1])
    my_model.worstCase(my_model.listNerc[1], 2, 50)

