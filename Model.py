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


class CleanModel(Model):
    """
    A model with some dirty floor and roombas to clean
    
    """

    def __init__(self,numberOfAgents,dirtPercentaje,width,height,maxSteps):
        self.numAgents = numberOfAgents
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True
        self.dirtPercentaje = int(dirtPercentaje*(width*height))
        self.maxSteps = maxSteps
        self.courrentSteps = 0

        #Data Collector
        self.datacollector = DataCollector(
            {
                "Clean": lambda m: self.count_type(m,"Clean"),
                "Dirty": lambda m: self.count_type(m,"Dirty")
            }
        )
        
        fList = []
        #Create Floor
        for (contents,x,y) in self.grid.coord_iter():
            f = Floor((x,y), self)
            self.grid.place_agent(f, (x,y))
            fList.append(f)
            self.schedule.add(f)
        
        #Change state to dirty floor
        dFloor = self.random.sample(list(fList),self.dirtPercentaje)
        
        for a in dFloor:
            a.state = "Dirty"

        #Create Agents

        for i in range(self.numAgents):
            a = Robot(i, self)
            self.schedule.add(a)

            #Add agent to grid
            self.grid.place_agent(a, (1,1))
    def step(self):
        print(f"Actual steps : {self.courrentSteps}, max {self.maxSteps}")
        if self.courrentSteps <= self.maxSteps:

            self.schedule.step()
            self.courrentSteps += 1
            
            self.datacollector.collect(self)
        else:
            print("Finish")
            self.running = False
    @staticmethod
    def count_type(model,floorCondition):
        

        count = 0
        for agent in model.schedule.agents:
            if type(agent) == Floor:
                if agent.state == floorCondition:
                    count+=1
            
        return count