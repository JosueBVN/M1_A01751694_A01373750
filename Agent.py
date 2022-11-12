from mesa import Agent

"""
Autor: Josué Bernardo Villegas Nuño 
Matricula: A01751694
Autor: Jose Miguel Garcia Gurtubay moreno
Matricula: A01373750
Robot limpiador
11 Octubre del 2022
"""

class Robot(Agent):
    """
    Robo
    """

    def  __init__(self, unique_id, model):
        """
        Constructor de Agente Roomba
        """

        super(). __init__(unique_id, model)
    
    def step(self) -> None:
        """
        Funcion que dicta que hacer en cada tick o step
        Si Roomba se encuetra en una casilla sucia, llama a la funcion para limpiar
        En caso de que no se encuentre en una casilla sucia, llama a la funcion para moverse
        """
        
        contents = self.model.grid.get_cell_list_contents([self.pos])
        
        for i in contents:
            if type(i) == Floor:
                floor = i
                break
       

        if floor.state == "Dirty":
            
            self.clean(floor)
        else:
            
            
            self.move(floor)
        
        

    def move(self,floor) -> None:
        """
        Roomba elije 1 de sus 8 posibles casillas para moverse
        Si la celda que elijió ya se encuentra otra Roomba, permanece en su lugar
        """
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos, moore=True,include_center=False
        )
        newPosition = self.random.choice(possibleSteps)
        
        contents = self.model.grid.get_cell_list_contents(newPosition)
        
        c = 0
        """Todo lo que"""
        print("----------------------")
        for i in contents:
            print(type(i) == type(self))
            if type(i) == type(self):
                c = 1
                break
        
        print("-----------------------")
        if c == 1:
            pass
        else:
            self.model.grid.move_agent(self,newPosition)
        
        

    def clean(self,floorAgent):
        """
        Roomba permanece en su lugar y limpia el suelo
        """
        floorAgent.state = "Clean"

class Floor(Agent):
    """
    Suelo que tiene 2 estados
    Clean: El suelo esta limpio
    Dirty: El suelo esta sucio
    """

    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.state = "CLEAN"
        self.pos = pos
    def step(self):
        pass