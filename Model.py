from mesa import DataCollector
from mesa import Model
from Agent import *
from mesa.time import RandomActivation
from mesa.space import MultiGrid

"""
Autor: Josué Bernardo Villegas Nuño 
Matricula: A01751694
Autor: Jose Miguel Garcia Gurtubay moreno
Matricula: A01373750
Robot limpiador
11 Octubre del 2022
"""

"""
Clase del modelo de limpiado
"""
class CleaningModel(Model):

    def __init__(self,numberOfAgents,dirtPercentaje,width,height,maxSteps):
        self.numAgents = numberOfAgents
        self.grid = MultiGrid(width, height, False)
        self.dirtPercentaje = int(dirtPercentaje*(width*height))
        self.schedule = RandomActivation(self)
        self.running = True
        
        self.maxSteps = maxSteps
        self.courrentSteps = 0

        #Data Collector
        self.datacollector = DataCollector(
            {
                "Limpio": lambda m: self.count_type(m,"Limpio"),
                "Sucio": lambda m: self.count_type(m,"Sucio")
            }
        )
        
        List = []
        #Create Superficie
        for (contents,x,y) in self.grid.coord_iter():
            punto = Superficie((x,y), self)
            self.grid.place_agent(punto, (x,y))
            List.append(punto)
            self.schedule.add(punto)
        
        #Change state to dirty floor
        sucioSuperficie = self.random.sample(list(List),self.dirtPercentaje)
        
        for i in sucioSuperficie:
            i.state = "Sucio"

        #Create Agents

        for i in range(self.numAgents):
            nuevoRo = Robot(i, self)
            self.schedule.add(nuevoRo)
            #Add agent to grid
            self.grid.place_agent(nuevoRo, (1,1))
  

    def step(self):
        print(f"N° de Step Actual: {self.courrentSteps}, Maximo N° de Steps: {self.maxSteps}")
        if self.courrentSteps <= self.maxSteps:
            self.schedule.step()
            self.courrentSteps += 1            
            self.datacollector.collect(self)
        else:
            print("Fin de los steps.")
            self.running = False

    @staticmethod
    def count_type(model,estadoSuelo):       
        contador = 0
        for agente in model.schedule.agents:
            if type(agente) == Superficie:
                if agente.state == estadoSuelo:
                    contador+=1           
        return contador