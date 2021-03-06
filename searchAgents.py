# searchAgents.py
# ---------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
This file contains all of the agents that can be selected to control Pacman.  To
select an agent, use the '-p' option when running pacman.py.  Arguments can be
passed to your agent using '-a'.  For example, to load a SearchAgent that uses
depth first search (dfs), run the following command:

> python pacman.py -p SearchAgent -a fn=depthFirstSearch

Commands to invoke other search strategies can be found in the project
description.

Please only change the parts of the file you are asked to.  Look for the lines
that say

"*** YOUR CODE HERE ***"

The parts you fill in start about 3/4 of the way down.  Follow the project
description for details.

Good luck and happy searching!
"""
import math

from game import Directions
from game import Agent
from game import Actions
import util
import time
import search

class GoWestAgent(Agent):
    "An agent that goes West until it can't."

    def getAction(self, state):
        "The agent receives a GameState (defined in pacman.py)."
        if Directions.WEST in state.getLegalPacmanActions():
            return Directions.WEST
        else:
            return Directions.STOP

#######################################################
# This portion is written for you, but will only work #
#       after you fill in parts of search.py          #
#######################################################

class SearchAgent(Agent):
    """
    This very general search agent finds a path using a supplied search
    algorithm for a supplied search problem, then returns actions to follow that
    path.

    As a default, this agent runs DFS on a PositionSearchProblem to find
    location (1,1)

    Options for fn include:
      depthFirstSearch or dfs
      breadthFirstSearch or bfs


    Note: You should NOT change any code in SearchAgent
    """

    def __init__(self, fn='depthFirstSearch', prob='PositionSearchProblem', heuristic='nullHeuristic'):
        # Warning: some advanced Python magic is employed below to find the right functions and problems

        # Get the search function from the name and heuristic
        if fn not in dir(search):
            raise AttributeError(fn + ' is not a search function in search.py.')
        func = getattr(search, fn)
        if 'heuristic' not in func.__code__.co_varnames:
            #print('[SearchAgent] using function ' + fn)
            self.searchFunction = func
        else:
            if heuristic in globals().keys():
                heur = globals()[heuristic]
            elif heuristic in dir(search):
                heur = getattr(search, heuristic)
            else:
                raise AttributeError(heuristic + ' is not a function in searchAgents.py or search.py.')
            print('[SearchAgent] using function %s and heuristic %s' % (fn, heuristic))
            # Note: this bit of Python trickery combines the search algorithm and the heuristic
            self.searchFunction = lambda x: func(x, heuristic=heur)

        # Get the search problem type from the name
        if prob not in globals().keys() or not prob.endswith('Problem'):
            raise AttributeError(prob + ' is not a search problem type in SearchAgents.py.')
        self.searchType = globals()[prob]
        #print('[SearchAgent] using problem type ' + prob)

    def registerInitialState(self, state):
        """
        This is the first time that the agent sees the layout of the game
        board. Here, we choose a path to the goal. In this phase, the agent
        should compute the path to the goal and store it in a local variable.
        All of the work is done in this method!

        state: a GameState object (pacman.py)
        """
        if self.searchFunction == None: raise Exception("No search function provided for SearchAgent")
        starttime = time.time()
        problem = self.searchType(state) # Makes a new search problem
        self.actions  = self.searchFunction(problem) # Find a path
        totalCost = problem.getCostOfActions(self.actions)
        print('Path found with total cost of %d in %.1f seconds' % (totalCost, time.time() - starttime))
        if '_expanded' in dir(problem): print('Search nodes expanded: %d' % problem._expanded)

    def getAction(self, state):
        """
        Returns the next action in the path chosen earlier (in
        registerInitialState).  Return Directions.STOP if there is no further
        action to take.

        state: a GameState object (pacman.py)
        """
        if 'actionIndex' not in dir(self): self.actionIndex = 0
        i = self.actionIndex
        self.actionIndex += 1
        if i < len(self.actions):
            return self.actions[i]
        else:
            return Directions.STOP

class PositionSearchProblem(search.SearchProblem):
    """
    A search problem defines the state space, start state, goal test, successor
    function and cost function.  This search problem can be used to find paths
    to a particular point on the pacman board.

    The state space consists of (x,y) positions in a pacman game.

    Note: this search problem is fully specified; you should NOT change it.
    """

    def __init__(self, gameState, costFn = lambda x: 1, goal=(1,1), start=None, warn=True, visualize=True):
        """
        Stores the start and goal.

        gameState: A GameState object (pacman.py)
        costFn: A function from a search state (tuple) to a non-negative number
        goal: A position in the gameState
        """
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        if start != None: self.startState = start
        self.goal = goal
        self.costFn = costFn
        self.visualize = visualize
        if warn and (gameState.getNumFood() != 1 or not gameState.hasFood(*goal)):
            print('Warning: this does not look like a regular search maze')

        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE



        # For display purposes
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE
    def getStartState(self):
        return self.startState

    def isGoalState(self, state):
        isGoal = state == self.goal

        # For display purposes only
        if isGoal and self.visualize:
            self._visitedlist.append(state)
            import __main__
            if '_display' in dir(__main__):
                if 'drawExpandedCells' in dir(__main__._display): #@UndefinedVariable
                    __main__._display.drawExpandedCells(self._visitedlist) #@UndefinedVariable

        return isGoal

    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
             For a given state, this should return a list of triples,
         (successor, action, stepCost), where 'successor' is a
         successor to the current state, 'action' is the action
         required to get there, and 'stepCost' is the incremental
         cost of expanding to that successor
        """

        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextState = (nextx, nexty)
                cost = self.costFn(nextState)
                successors.append( ( nextState, action, cost) )

        # Bookkeeping for display purposes
        self._expanded += 1 # DO NOT CHANGE
        if state not in self._visited:
            self._visited[state] = True
            self._visitedlist.append(state)

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions. If those actions
        include an illegal move, return 999999.
        """
        if actions == None: return 999999
        x,y= self.getStartState()
        cost = 0
        for action in actions:
            # Check figure out the next state and see whether its' legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
            cost += self.costFn((x,y))
        return cost

class StayEastSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the West side of the board.

    The cost function for stepping into a position (x,y) is 1/2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: .5 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn, (1, 1), None, False)

class StayWestSearchAgent(SearchAgent):
    """
    An agent for position search with a cost function that penalizes being in
    positions on the East side of the board.

    The cost function for stepping into a position (x,y) is 2^x.
    """
    def __init__(self):
        self.searchFunction = search.uniformCostSearch
        costFn = lambda pos: 2 ** pos[0]
        self.searchType = lambda state: PositionSearchProblem(state, costFn)

def manhattanHeuristic(position, problem, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristic(position, problem, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position
    xy2 = problem.goal
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################

class CornersProblem(search.SearchProblem):
    """
    This search problem finds paths through all four corners of a layout.

    You must select a suitable state space and successor function
    """

    """
    @author Gerard
    Concretament he afegit 4 lines de codi en la inicialització del problema, ja que dades les condicions d'aquest
    es necessari guardar el nombre de corners visitats en tot moment. Genero aquesta variable com a cornerVisits, la qual 
    es una tupla de 4 booleans ordenats segons l'ordre en que estan ordenats els corners a la variable corner, d'aquesta manera
    mai perdrem el registre de quin es cada un. Aquesta variable es guardada al primer estat juntament amb la posició, ja que es 
    una informació necessaria per acabar el problema
    """
    def __init__(self, startingGameState):
        """
        Stores the walls, pacman's starting position and corners.
        """
        self.walls = startingGameState.getWalls()
        self.startingPosition = startingGameState.getPacmanPosition()
        top, right = self.walls.height-2, self.walls.width-2
        self.corners = ((1,1), (1,top), (right, 1), (right, top))
        for corner in self.corners:
            if not startingGameState.hasFood(*corner):
                print('Warning: no food in corner ' + str(corner))
        self._expanded = 0 # DO NOT CHANGE; Number of search nodes expanded
        # Please add any code here which you would like to use
        # in initializing the problem
        "*** YOUR CODE HERE ***"
        cornerVists = tuple((self.startingPosition == corner for corner in self.corners))
        self.startState = (self.startingPosition, cornerVists)
        self.costFn = lambda x: 1

    """
    @author Gerard
    L'unic que hem de retornar es l'estat inicial del problema, que es una variable d'aquest.
    """
    def getStartState(self):
        """
        Returns the start state (in your state space, not the full Pacman state
        space)
        """
        "*** YOUR CODE HERE ***"
        return self.startState

    """
    @author Gerard
    Condició de victoria del problema. En cas que hi hagi algun dels elements de la tupla que guarda si hem visitat 
    totes les cantonades en False (es a dir, que hi ha alguna cantonada sense visitar, no guanyarem. En cas que no hi hagi cap False,
    guanyarem.
    """
    def isGoalState(self, state):
        """
        Returns whether this search state is a goal state of the problem.
        """
        "*** YOUR CODE HERE ***"
        cont = 0
        for i in state[1]:
            if i==False:
                cont += 1
        return cont == 0

    """
    @author Gerard
    La funció getSuccessors ha de generar els estats fills d'un estat actual. Segons la dinamica d'aquest problema
    els estats han de tenir la posició on es troben i la tupla de booleans on es guarda si s'han visitat totes les cantonades
    Aquesta funció doncs genera les dues coses. Per a fer-ho, realitzem un for del zip entre les posicions de les cantonades
    i els estats booleans del problema respecte aquestes i guardem el boolea tal y com esta en la llista o en cas que la següent 
    posició sigui una de les cantonades que no ha estat vista, li canviem el False per un True. A continuació es converteix aquesta
    llista en una tupla i per acabar es crear l'estat, que correspon de la posició del estat en primer lloc, i en segon la tupla de
    booleans que hem creat.
    """
    def getSuccessors(self, state):
        """
        Returns successor states, the actions they require, and a cost of 1.

         As noted in search.py:
            For a given state, this should return a list of triples, (successor,
            action, stepCost), where 'successor' is a successor to the current
            state, 'action' is the action required to get there, and 'stepCost'
            is the incremental cost of expanding to that successor
        """
        successors = []
        for action in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x, y = state[0]
            dx, dy = Actions.directionToVector(action)
            nextx, nexty = int(x + dx), int(y + dy)
            hitsWall = self.walls[nextx][nexty]
            if not hitsWall:

                nextCorners = []
                for corner,estadoCorner in zip(self.corners,state[1]):
                    nextCorners.append(estadoCorner or ((nextx,nexty)==corner))
                tuplaCorners = tuple(nextCorners)

                nextState = ((nextx, nexty),tuplaCorners)
                cost = self.costFn(nextState)
                successors.append((nextState, action, cost))

        # Bookkeeping for display purposes
        self._expanded += 1  # DO NOT CHANGE

        return successors

    def getCostOfActions(self, actions):
        """
        Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999.  This is implemented for you.
        """
        if actions == None: return 999999
        x,y= self.startingPosition
        for action in actions:
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]: return 999999
        return len(actions)

"""
@author Gerard
Funció que ens permet realitzar la distancia de Manhattan entre dos posicions cualsevols, ens serveix d'ajuda en la funció
de CornersHeuristic.
"""
def manhattanHeuristic2pos(position, position2, info={}):

    xy1 = position
    xy2 = position2
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

"""
@author Gerard
En la següent funció es crea la Heuristica del problema dels Corners. Com que els mapes son rectangulars i les seves cantonades son els objectius,
la heuristica del problema es pot intuir que tindra bastant a veure amb la distancia Manhattan. El que es fa es agafar les mesures minimes entre cantonades, ja siguin el shortSide,
el largeSide i el diagonalSide, que basicament son les distancies Manhattan entre cantonades, depenen entre quines sigui.
    longside    
-----------------
|               |
|               | shortside     I el diagonalSide es la hipotenusa del triangle rectangle entre longside i shortside.
|               |
|               |
-----------------
Al començament de la funció, es guarden en una variable quines son exactament les cantonades que falten per visitar.

Posteriorment, es crea una lista mitjançant una list comprehesion de les distancies Manhattan entre la posicio actual i les cantonades que falten per visitar.

Es guarda la cantonada que esta mes aprop a cornerMin i la distancia fins a aquesta a distanciaMinima.

A continuació s'entra en una serie de casos, donat que segons si queden mes o menys cantonades a visitar, la heuristica ha de ser diferent, ja que ja no cal un cami minim a recorrer tant gran quan
queda per visitar 1 cantonada que quan en queden 4.

En cas que quedin 4 cantonades, la heuristica serà de la distancia minima a la cantonada minima mes 2 cops el shortside i 1 cop el longside.
En cas que quedin 3 cantonades, la heuristica serà la distancia minima a la cantonada minima mes:
    Com que queden 3 cantonades, excepte rotacions del rectangle sempre podem veure les cantonades així: A----------B
                                                                                                                    |
                                                                                                                    |
                                                                                                                    |
                                                                                                                    C
    I el la cantonada D seria la que ja esta visitada. Aleshores en cas que la cantonada minima sigui A o C, sumarem a la distancia minima un longside i un shortside.
    En cas que la cantonada minima sigui B sumarem un shortside i un diagonalSide, això es per les propietats fisiques del cami minim que poden recorre segons cada posició.
En cas que quedin 2 cantonades, la heuristica serà la distancia minima a la cantonada minima mes la distancia manhattan entre les dos cantonades que falten.
En cas que quedi 1 cantonada, la heuristica sera simplement la distancia minima a la cantonada minima.

D'aquesta manera es soporten tots els casos y la heuristica es admissible i consistent.


############
        #Heuristica alternativa, mirem el cami mes llarg.
    if len(cantonadesNoVisitades) != 0:

        manhattanDistanciesCorners = [manhattanHeuristic2pos(statePosition,i) for i in cantonadesNoVisitades]
        heuristica += max(manhattanDistanciesCorners)
############
"""
def cornersHeuristic(state, problem):
    """
    A heuristic for the CornersProblem that you defined.

      state:   The current search state
               (a data structure you chose in your search problem)

      problem: The CornersProblem instance for this layout.

    This function should always return a number that is a lower bound on the
    shortest path from the state to a goal of the problem; i.e.  it should be
    admissible (as well as consistent).
    """
    corners = problem.corners # These are the corner coordinates
    walls = problem.walls # These are the walls of the maze, as a Grid (game.py)

    statePosition = state[0]
    stateCornersTuple = state[1]
    heuristica = 0
    shortSide = min(corners[3][0],corners[3][1])-1
    largeSide = max(corners[3][0],corners[3][1])-1
    diagonalSide = math.sqrt(shortSide^2+largeSide^2)

    cantonadesNoVisitades = [corners[i] for i in range(4) if not stateCornersTuple[i]]


    if len(cantonadesNoVisitades) != 0:
        manhattanDistanciesCorners = [(manhattanHeuristic2pos(statePosition, i),i) for i in cantonadesNoVisitades]
        distanciaMinima, cornerMin = min(manhattanDistanciesCorners)


    if len(cantonadesNoVisitades) == 4:
        heuristica += (distanciaMinima + shortSide*2 + largeSide)
    elif len(cantonadesNoVisitades) == 3:

        if(cornerMin[0] != i[0] and cornerMin[1] != i[1] for i in cantonadesNoVisitades):
            heuristica += (distanciaMinima + shortSide + largeSide)
        else:
            heuristica += (distanciaMinima + shortSide + diagonalSide)
    elif len(cantonadesNoVisitades) == 2:
        heuristica += (distanciaMinima + manhattanHeuristic2pos(cantonadesNoVisitades[0],cantonadesNoVisitades[1]))
    elif len(cantonadesNoVisitades) == 1:
        heuristica += (distanciaMinima)


    return heuristica


class AStarCornersAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, cornersHeuristic)
        self.searchType = CornersProblem

class FoodSearchProblem:
    """
    A search problem associated with finding the a path that collects all of the
    food (dots) in a Pacman game.

    A search state in this problem is a tuple ( pacmanPosition, foodGrid ) where
      pacmanPosition: a tuple (x,y) of integers specifying Pacman's position
      foodGrid:       a Grid (see game.py) of either True or False, specifying remaining food
    """
    def __init__(self, startingGameState):
        self.start = (startingGameState.getPacmanPosition(), startingGameState.getFood())
        self.walls = startingGameState.getWalls()
        self.startingGameState = startingGameState
        self._expanded = 0 # DO NOT CHANGE
        self.heuristicInfo = {} # A dictionary for the heuristic to store information

    def getStartState(self):
        return self.start

    def isGoalState(self, state):
        return state[1].count() == 0

    def getSuccessors(self, state):
        "Returns successor states, the actions they require, and a cost of 1."
        successors = []
        self._expanded += 1 # DO NOT CHANGE
        for direction in [Directions.NORTH, Directions.SOUTH, Directions.EAST, Directions.WEST]:
            x,y = state[0]
            dx, dy = Actions.directionToVector(direction)
            nextx, nexty = int(x + dx), int(y + dy)
            if not self.walls[nextx][nexty]:
                nextFood = state[1].copy()
                nextFood[nextx][nexty] = False
                successors.append( ( ((nextx, nexty), nextFood), direction, 1) )
        return successors

    def getCostOfActions(self, actions):
        """Returns the cost of a particular sequence of actions.  If those actions
        include an illegal move, return 999999"""
        x,y= self.getStartState()[0]
        cost = 0
        for action in actions:
            # figure out the next state and see whether it's legal
            dx, dy = Actions.directionToVector(action)
            x, y = int(x + dx), int(y + dy)
            if self.walls[x][y]:
                return 999999
            cost += 1
        return cost

class AStarFoodSearchAgent(SearchAgent):
    "A SearchAgent for FoodSearchProblem using A* and your foodHeuristic"
    def __init__(self):
        self.searchFunction = lambda prob: search.aStarSearch(prob, foodHeuristic)
        self.searchType = FoodSearchProblem

"""
@author Gerard
La heuristica del problema del menjar, a diferencia de la heuristica dels Corners, no pot utilitzar distanciaManhattan perque hi ha masses objectius simultanis i no seria una distancia acurada, per 
això en aquest cas farem servir la mazeDistance.

El primer que es fa en aquesta funció es guardar o crear les variables que es necessiten per a començar com poden ser: statePosition que guarda la posició actual del pacman, stateFoodGrid que es el Grid d'on es troba
tot el menjar que falta per a consumir, la stateFoodLlista que s'extreu de la stateFoodGrid i es una llista on estan les coordenades de tot el menjar que falta per a ser consumit, la heuristica del problema que de moment es 
0, i les dues llistes que ens ajudaran a donarli un valor a aquesta heuristica: la minFood, llista que guarda les distanciesMaze entre la posicio actual i els diferents menjars que falten per a ser consumits i la llista
distanciesEntreFood que com be diu el seu nom, guarda les distancies entre els diferents menjars del mapa. 

Aleshores, per a començar a guardar valors es realitza un doble for. Per a cada menjar que hi ha a la llista de menjars a ser consumits, es mira si es te guardada la informació de la distancia entre aquests al diccionari
del problema, en cas que no ho estigui es calcula amb la funcio mazeDistance i es guarda al diccionari. Posteriorment aquesta informació es guarda a la llista de minFood. A continuació,
per aquest menjar es calcula la distancia entre ell i tots els demes menjars del mapa, cada una d'aquestes informacions es guarda en el diccionari del problema i posteriorment a la llista distanciesEntreFood.

Un cop es tot això es retorna la distancia minima entre la posicio actual i la fruita mes propera, cosa que es fa fent un min en la llista minfood,
mes la distancia maxima entre dos menjars del mapa, cosa que es fa fent un max en la llista distanciesEntreFood

Podem veure que la distancia a la fruita mes propera mes la distancia entre les dos fruites mes llunyanes es una heuristica consistent.

#################
        #9551 expanded
        if len(statefoodLlista) != 0:
            manhattanDistanciesFood = [manhattanHeuristic2pos(statePosition, i) for i in statefoodLlista]
            heuristica += max(manhattanDistanciesFood)
#################

"""
def foodHeuristic(state, problem):
    """
    Your heuristic for the FoodSearchProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come
    up with an admissible heuristic; almost all admissible heuristics will be
    consistent as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the
    other hand, inadmissible or inconsistent heuristics may find optimal
    solutions, so be careful.

    The state is a tuple ( pacmanPosition, foodGrid ) where foodGrid is a Grid
    (see game.py) of either True or False. You can call foodGrid.asList() to get
    a list of food coordinates instead.

    If you want access to info like walls, capsules, etc., you can query the
    problem.  For example, problem.walls gives you a Grid of where the walls
    are.

    If you want to *store* information to be reused in other calls to the
    heuristic, there is a dictionary called problem.heuristicInfo that you can
    use. For example, if you only want to count the walls once and store that
    value, try: problem.heuristicInfo['wallCount'] = problem.walls.count()
    Subsequent calls to this heuristic can access
    problem.heuristicInfo['wallCount']
    """

    statePosition, statefoodGrid = state
    statefoodLlista = statefoodGrid.asList()
    heuristica = 0
    minFood = []
    distanciesEntreFood = [0]


    for food in statefoodLlista:
        if (statePosition,food) not in problem.heuristicInfo:
            problem.heuristicInfo[(statePosition, food)] = mazeDistance(statePosition, food, problem.walls, state)
            problem.heuristicInfo[(food,statePosition)] = problem.heuristicInfo[(statePosition,food)]
        minFood.append(problem.heuristicInfo[(statePosition,food)])
        for mesFood in statefoodLlista:
            if(food != mesFood):
                if (food, mesFood) not in problem.heuristicInfo:
                    problem.heuristicInfo[(food, mesFood)] = mazeDistance(food,mesFood,problem.walls,state)
                    problem.heuristicInfo[(mesFood, food)] = problem.heuristicInfo[(food, mesFood)]
                distanciesEntreFood.append(problem.heuristicInfo[(food, mesFood)])

    if len(minFood) != 0:
        heuristica += (min(minFood)+max(distanciesEntreFood))
    else:
        heuristica += max(distanciesEntreFood)
    return heuristica

"""
@author Gerard
Funció que recolza la foodHeuristic, estaba ja creada, pero l'he hagut de modificar per a poder treballar amb ella donat que no sabia com passarli el gameState des de la funcio foodHeuristic,
ara rep les walls i l'state en que es troba l'agent. Aleshores crida a un problema de busqueda per a que trobi la distancia entre dues posicions amb la longitud del bfs que retorna aquest problema..
"""
def mazeDistance(point1, point2, wallsS, state):
    """
    Returns the maze distance between any two points, using the search functions
    you have already built. The gameState can be any game state -- Pacman's
    position in that state is ignored.

    Example usage: mazeDistance( (2,4), (5,6), gameState)

    This might be a useful helper function for your ApproximateSearchAgent.
    """
    x1, y1 = point1
    x2, y2 = point2
    walls = wallsS
    assert not walls[x1][y1], 'point1 is a wall: ' + str(point1)
    assert not walls[x2][y2], 'point2 is a wall: ' + str(point2)
    prob = especialPositionSearchProblem(walls,state[0],state[1],len(state[1].asList())!=0, start=point1, goal=point2, warn=False, visualize=False)
    return len(search.bfs(prob))

"""
@author Gerard
Classe que hereda de PositionSearchProblem pero que disposa d'un altre init per a poder inicialitzar-lo amb les dades que es tenen a foodHeuristic. Totes les demes funcions que te son les de 
PositionSearchProblem, per tant pot fer les mateixes coses que ell. 
"""
class especialPositionSearchProblem(PositionSearchProblem):

    def __init__(self,walls,pacmanPosition,food,hasFood,start,goal,warn=True,visualize=True):
        self.food = food
        self.hasFood = hasFood
        self.goal = goal
        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = walls
        self.startState = start
        self.visualize = visualize
        self.warn = warn
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0  # DO NOT CHANGE

class ClosestDotSearchAgent(SearchAgent):
    "Search for all food using a sequence of searches"
    def registerInitialState(self, state):
        self.actions = []
        currentState = state
        while(currentState.getFood().count() > 0):
            nextPathSegment = self.findPathToClosestDot(currentState) # The missing piece
            self.actions += nextPathSegment
            for action in nextPathSegment:
                legal = currentState.getLegalActions()
                if action not in legal:
                    t = (str(action), str(currentState))
                    raise Exception('findPathToClosestDot returned an illegal move: %s!\n%s' % t)
                currentState = currentState.generateSuccessor(0, action)
        self.actionIndex = 0
        print('Path found with cost %d.' % len(self.actions))

    def findPathToClosestDot(self, gameState):
        """
        Returns a path (a list of actions) to the closest dot, starting from
        gameState.
        """
        # Here are some useful elements of the startState
        startPosition = gameState.getPacmanPosition()
        food = gameState.getFood()
        walls = gameState.getWalls()
        problem = AnyFoodSearchProblem(gameState)

        "*** YOUR CODE HERE ***"
        afsp = AnyFoodSearchProblem(gameState)
        return search.bfs(afsp)

class AnyFoodSearchProblem(PositionSearchProblem):
    """
    A search problem for finding a path to any food.

    This search problem is just like the PositionSearchProblem, but has a
    different goal test, which you need to fill in below.  The state space and
    successor function do not need to be changed.

    The class definition above, AnyFoodSearchProblem(PositionSearchProblem),
    inherits the methods of the PositionSearchProblem.

    You can use this search problem to help you fill in the findPathToClosestDot
    method.
    """

    def __init__(self, gameState):
        "Stores information from the gameState.  You don't need to change this."
        # Store the food for later reference
        self.food = gameState.getFood()

        # Store info for the PositionSearchProblem (no need to change this)
        self.walls = gameState.getWalls()
        self.startState = gameState.getPacmanPosition()
        self.costFn = lambda x: 1
        self._visited, self._visitedlist, self._expanded = {}, [], 0 # DO NOT CHANGE

    def isGoalState(self, state):
        """
        The state is Pacman's position. Fill this in with a goal test that will
        complete the problem definition.
        """
        x,y = state

        return self.food[x][y]


