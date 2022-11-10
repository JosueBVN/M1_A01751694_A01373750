from mesa import Agent, Model 

# Debido a que necesitamos un solo agente por celda elegimos `SingleGrid` que fuerza un solo objeto por celda.
from mesa.space import SingleGrid
#
from mesa.datacollection import DataCollector

# Con `SimultaneousActivation` hacemos que todos los agentes se activen de manera simultanea.
from mesa.time import SimultaneousActivation
import numpy as np

class CleanRobot(Agent):
    
    def __init__(self,pos, model, agent_type):

        super().__init__(pos, model)
        self.pos = pos
        self.type = agent_type

    # 2 Step function
    def step(self):
        similar = 0
        # 3 Calculate the number of similar neighbours
        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type == self.type:
                similar += 1

        # 4 Move to a random empty location if unhappy
        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1
        
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                if self.random.random() < self.minority_pc:
                    agent_type = 1
                else:
                    agent_type = 0

                agent = CleanRobot((x, y), self, agent_type)
                self.grid.position_agent(agent, (x, y))
                self.schedule.add(agent)

            
