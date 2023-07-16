from util import manhattanDistance
from game import Directions
import random
import util
from typing import Any, DefaultDict, List, Set, Tuple

from game import Agent
from pacman import GameState



class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def __init__(self):
        self.lastPositions = []
        self.dc = None

    def getAction(self, gameState: GameState):
        """
        getAction chooses among the best options according to the evaluation function.

        getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East}
        ------------------------------------------------------------------------------
        Description of GameState and helper functions:

        A GameState specifies the full game state, including the food, capsules,
        agent configurations and score changes. In this function, the |gameState| argument
        is an object of GameState class. Following are a few of the helper methods that you
        can use to query a GameState object to gather information about the present state
        of Pac-Man, the ghosts and the maze.

        gameState.getLegalActions(agentIndex):
            Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

        gameState.generateSuccessor(agentIndex, action):
            Returns the successor state after the specified agent takes the action.
            Pac-Man is always agent 0.

        gameState.getPacmanState():
            Returns an AgentState object for pacman (in game.py)
            state.configuration.pos gives the current position
            state.direction gives the travel vector

        gameState.getGhostStates():
            Returns list of AgentState objects for the ghosts

        gameState.getNumAgents():
            Returns the total number of agents in the game

        gameState.getScore():
            Returns the score corresponding to the current state of the game


        The GameState class is defined in pacman.py and you might want to look into that for
        other helper methods, though you don't need to.
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)


        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action: str) -> float:
        """
        The evaluation function takes in the current GameState (defined in pacman.py)
        and a proposed action and returns a rough estimate of the resulting successor
        GameState's value.

        The code below extracts some useful information from the state, like the
        remaining food (oldFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        oldFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState: GameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

######################################################################################
# Problem 1b: implementing minimax


class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (problem 1)
    """

    def getAction(self, gameState: GameState) -> str:
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction. Terminal states can be found by one of the following:
          pacman won, pacman lost or there are no legal moves.

          Don't forget to limit the search depth using self.depth. Also, avoid modifying
          self.depth directly (e.g., when implementing depth-limited search) since it
          is a member variable that should stay fixed throughout runtime.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game

          gameState.getScore():
            Returns the score corresponding to the current state of the game

          gameState.isWin():
            Returns True if it's a winning state

          gameState.isLose():
            Returns True if it's a losing state

          self.depth:
            The depth to which search should continue

        """

        # BEGIN_YOUR_CODE (our solution is 22 lines of code, but don't worry if you deviate from this)
        def minimax(gameState, depth, player):
            if gameState.isWin() or gameState.isLose(): return (gameState.getScore(), Directions.STOP)
            if depth == 0: return (self.evaluationFunction(gameState), Directions.STOP)
            if player == 0: return max([(minimax(gameState.generateSuccessor(0, action), depth, 1)[0], action) for action in gameState.getLegalActions(0)])
            if player == (gameState.getNumAgents() - 1): depth -= 1
            return min([(minimax(gameState.generateSuccessor(player, action), depth, (player + 1) % gameState.getNumAgents())[0], action) for action in gameState.getLegalActions(player)])
        
        return minimax(gameState, self.depth, 0)[1]
        # END_YOUR_CODE

######################################################################################
# Problem 2a: implementing alpha-beta


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (problem 2)
      You may reference the pseudocode for Alpha-Beta pruning here:
      en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning#Pseudocode
    """

    def getAction(self, gameState: GameState) -> str:
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        # BEGIN_YOUR_CODE (our solution is 43 lines of code, but don't worry if you deviate from this)
        def minimax_AlphaBeta(gameState, depth, alpha, beta, player):
            if gameState.isWin() or gameState.isLose(): return (gameState.getScore(), Directions.STOP)
            if depth == 0: return (self.evaluationFunction(gameState), Directions.STOP)
            if player == 0:
                maxValue = float('-inf')
                maxAction = ''
                for action in gameState.getLegalActions(player):
                    childValue = minimax_AlphaBeta(gameState.generateSuccessor(player, action), depth, alpha, beta, player + 1)[0]
                    if childValue > maxValue:
                        maxValue = childValue
                        maxAction = action
                        if maxValue > beta: break
                        alpha = max(maxValue, alpha)
                return (maxValue, maxAction)
            nextPlayer = player + 1
            if nextPlayer == gameState.getNumAgents():
                depth -= 1
                nextPlayer = 0
            minValue = float('inf')
            minAction = ''
            for action in gameState.getLegalActions(player):
                childValue = minimax_AlphaBeta(gameState.generateSuccessor(player, action), depth, alpha, beta, nextPlayer)[0]
                if childValue < minValue:
                    minValue = childValue
                    minAction = action
                    if minValue < alpha: break
                    beta = min(minValue, beta)
            return (minValue, minAction)
        
        return minimax_AlphaBeta(gameState, self.depth, float('-inf'), float('inf'), 0)[1]
        # END_YOUR_CODE

######################################################################################
# Problem 3b: implementing expectimax


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (problem 3)
    """

    def getAction(self, gameState: GameState) -> str:
     """
       Returns the expectimax action using self.depth and self.evaluationFunction

       All ghosts should be modeled as choosing uniformly at random from their
       legal moves.
     """

     # BEGIN_YOUR_CODE (our solution is 20 lines of code, but don't worry if you deviate from this)
     def expectimax(gameState, depth, player):
         if gameState.isWin() or gameState.isLose(): return (gameState.getScore(), Directions.STOP)
         if depth == 0: return (self.evaluationFunction(gameState), Directions.STOP)
         if player == 0: return max([(expectimax(gameState.generateSuccessor(0, action), depth, 1)[0], action) for action in gameState.getLegalActions(0)])
         if player == (gameState.getNumAgents() - 1): depth -= 1
         legalActions = gameState.getLegalActions(player)
         possibleScores = [expectimax(gameState.generateSuccessor(player, action), depth, (player + 1) % gameState.getNumAgents())[0] for action in legalActions]
         return (sum(possibleScores)/len(possibleScores), random.choice(legalActions))
     
     return expectimax(gameState, self.depth, 0)[1]
     # END_YOUR_CODE

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function


def betterEvaluationFunction(currentGameState: GameState) -> float:
    """
      Your extreme, unstoppable evaluation function (problem 4). Note that you can't fix a seed in this function.
    """

    # BEGIN_YOUR_CODE (our solution is 16 lines of code, but don't worry if you deviate from this)
    currentDistance = 0
    currentScore = currentGameState.getScore()
    min_capsuleDistance = float('inf')
    min_ghostDistance = float('inf')
    
    queue = util.Queue()
    queue.push(currentGameState.getPacmanPosition())

    for capsule in currentGameState.getCapsules():
        currentDistance = manhattanDistance(capsule, currentGameState.getPacmanPosition())
        if currentDistance < min_capsuleDistance: min_capsuleDistance = currentDistance
    
    for ghost in currentGameState.getGhostPositions():
        currentDistance = manhattanDistance(ghost, currentGameState.getPacmanPosition())
        if currentDistance < min_ghostDistance: min_ghostDistance = currentDistance
    
    features = [currentScore, 1.0/min_capsuleDistance, 1.0/min_ghostDistance, len(currentGameState.getCapsules()), currentGameState.getNumFood()]
    weights = [1, 3, -100, -10, -5]
    return sum([features[i]*weights[i] for i in range(len(features))])
    # END_YOUR_CODE


# Abbreviation
better = betterEvaluationFunction
