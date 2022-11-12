from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.UserParam import UserSettableParameter

from Agent import *
from Model import CleaningModel

"""
Autor: Josué Bernardo Villegas Nuño 
Matricula: A01751694
Autor: Jose Miguel Garcia Gurtubay moreno
Matricula: A01373750
Robot limpiador
11 Octubre del 2022
"""

SIZE_OF_CANVAS_IN_PIXELS_X = 500
SIZE_OF_CANVAS_IN_PIXELS_Y = 500

NUMBER_OF_CELLS = 20

COLORS = {
    "Limpio":"blue",
    "Sucio":"red"
}

simulationParams = {
    "numberOfAgents": UserSettableParameter(
        "slider",
        "Number of agents",
        10,     # Default
        2,      #Min
        100,    #Max
        1,       #Step
        description="Choose how many agents you want to include",
    ),
    "width": NUMBER_OF_CELLS,
    "height": NUMBER_OF_CELLS,
    "dirtPercentaje": UserSettableParameter(
        "slider",
        "Floor Covered in dirt",
        0.5,        # Default
        0.1,        #Min
        1,          #Max
        0.1,        #Step
        description="Choose the persentaje of the floor to be covered by dirt",
    ),
    "maxSteps": UserSettableParameter(
        "number",
        "Max steps",
        value=100,
        description="Choose how many steps you want"
        
    )
}


def roomba_Floor_Portrayal(agent):
    if agent is None:
        return
    
    portrayal = {}
    if type(agent) is Superficie:
        if agent.state == "Limpio":
            portrayal["Shape"] = "circle"
            portrayal["Layer"] = 0
            portrayal["r"] = 0.2
            portrayal["Color"] = "white"
        else:
            portrayal["Shape"] = "./images/Suciedad.png"
            portrayal["Layer"] = 0
            portrayal["Scale"] = 1
    else:
        portrayal["Shape"] = "./images/roomba.png"
        portrayal["Scale"] = 20
        portrayal["Layer"] = 1
        

        
    return portrayal

#Data Collector
floorChart = ChartModule(
    [{
        "Label":label,
        "Color":color
    }
    for (label, color) in COLORS.items()]
)


grid = CanvasGrid(roomba_Floor_Portrayal,NUMBER_OF_CELLS, NUMBER_OF_CELLS,SIZE_OF_CANVAS_IN_PIXELS_X,SIZE_OF_CANVAS_IN_PIXELS_Y)
server = ModularServer(CleaningModel,
                        [grid,floorChart],
                        "Robot limpiadores",
                        simulationParams)
server.port = 15200
server.launch()