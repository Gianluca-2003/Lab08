import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()
        self.nerc = None
        self.max_hours = None
        self.max_years = None

    def handleWorstCase(self, e):
        self._view._txtOut.controls.clear()
        # TO FILL
        if self.nerc is None:
            self._view.create_alert("Inserisci un NERC per prseguire")
            self._view.update_page()
            return
        self.max_years = float(self._view._txtYears.value)
        self.max_hours = float(self._view._txtHours.value)
        if self.max_years is None or self.max_hours is None:
            self._view.create_alert("Inserisci massimo anni e massimo ore per prseguire")
            self._view.update_page()
            return
        print(self.nerc)
        self._model.loadEvents(self._idMap[self.nerc])
        eventi, (ore, persone) = self._model.worstCase( self.nerc, self.max_years,self.max_hours)
        self._view._txtOut.controls.append(ft.Text(f"Ore totali: {ore}"))
        self._view._txtOut.controls.append(ft.Text(f"Persone coinvolte: {persone}"))
        for event in eventi:
            self._view._txtOut.controls.append(ft.Text(str(event)))
        self._view.update_page()


    def handleReadNerc(self, e):
        self.nerc = self._view._ddNerc.value
        print(self.nerc)




    def fillDD(self):
        nercList = self._model.listNerc
        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v
        print(self._idMap)

