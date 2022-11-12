from mesa import Agent

"""
Autor: Josué Bernardo Villegas Nuño 
Matricula: A01751694
Autor: Jose Miguel Garcia Gurtubay moreno
Matricula: A01373750
Robot limpiador
11 Octubre del 2022

El agente superficie que puede estar limpio o sucio en cada casilla del ambiente
"""
class Superficie(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.state = "Limpio"
        self.pos = pos
    def step(self):
        pass
"""
Clase Agente Robot
"""
class Robot(Agent):
    """Contructor de la clase Robot"""
    def  __init__(self, unique_id, model):
        super(). __init__(unique_id, model)

    """
    Esta funcion determina el comportamineto del agente robot,
    condicionada por la interaccion con el agente que determina si el piso esta sucio o limpio.
    """
    def step(self) -> None:
        valoresGrilla = self.model.grid.get_cell_list_contents([self.pos])       
        for i in valoresGrilla:
            if type(i) == Superficie:
                superficie = i
                break      
            ##Aqui invertir 
        if superficie.state == "Limpio":            
            self.move(superficie)
        else:                        
            self.clean(superficie)
        
        
    """
    El Robot se mueve a una de las casillas adyacentes, a menos que encuentre otro robot.
    """
    def move(self,superficie) -> None:

        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True,include_center=False
        )
        new_position = self.random.choice(possible_steps)
        
        valoresGrilla = self.model.grid.get_cell_list_contents(new_position)
        
        op = 0
        
        
        for i in valoresGrilla:
            if type(i) == Robot:
                op = 1
                break
        if op == 1:
            pass
        else:
            self.model.grid.move_agent(self,new_position)
        
        
    """
    El robot limpia y se cambia el estado de la superficie
    """
    def clean(self,superficieAgent):
        superficieAgent.state = "Limpio"
