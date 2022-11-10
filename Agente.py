from mesa import Agent, Model, time, space

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

    # 2 Funcion Step 
    def step(self):
        similar = 0
        # 3 Calcular numero similar de vecinos

        for neighbor in self.model.grid.neighbor_iter(self.pos):
            if neighbor.type == self.type:
                similar += 1

        # 4 Mover a una posicion random si no esta conentento
        if similar < self.model.homophily:
            self.model.grid.move_to_empty(self)
        else:
            self.model.happy += 1
        
    class Robot(Model):
        def __init__(self, width=20, height=20, density=0.8, minority_pc=0.2, homophily=8):
        
            self.width = width
            self.height = height
            self.density = density
            self.minority_pc = minority_pc
            self.homophily = homophily

            self.schedule =time.RandomActivation(self)
            self.grid = space.SingleGrid(width, height, torus=True)

            self.happy = 0
            self.datacollector = DataCollector(
                {"happy": "happy"},  # Model-level count of happy agents
                # For testing purposes, agent's individual x and y
                {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]},
            )

            # Set up agents
            # We use a grid iterator that returns
            # the coordinates of a cell as well as
            # its contents. (coord_iter)
            for cell in self.grid.coord_iter():
                x = cell[1]
                y = cell[2]
                if self.random.random() < self.density:
                    if self.random.random() < self.minority_pc:
                        agent_type = 1
                    else:
                        agent_type = 0

                    agent = CleanRobot((x, y), self, agent_type)
                    self.grid.place_agent(agent, (x, y))
                    self.schedule.add(agent)

            self.running = True
            self.datacollector.collect(self)

        def step(self):
            
            self.happy = 0  # Reset counter of happy agents
            self.schedule.step()
            # collect data
            self.datacollector.collect(self)

            if self.happy == self.schedule.get_agent_count():
                self.running = False