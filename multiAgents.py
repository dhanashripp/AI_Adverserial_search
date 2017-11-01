# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]

        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newGhostStates = successorGameState.getGhostStates()
        oldFood = currentGameState.getFood()
        foodList = oldFood.asList()
        minDistance = 100000000-1
        distance = 0
        newPos = successorGameState.getPacmanPosition()
        if action == 'Stop':
            return -10000000

        for ghost in newGhostStates:
            if (manhattanDistance(ghost.getPosition(),newPos)==0):
                if(ghost.scaredTimer==0):
                    return -10000000

        for i in range(len(foodList)):
            distance = (manhattanDistance(foodList[i], newPos))
            if (distance < minDistance):
                minDistance = distance

        return -1*minDistance

def scoreEvaluationFunction(currentGameState):
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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    This agent returns the minimax action from the current gameState using self.depth and self.evaluationFunction.
    It uses a simple recursive computation of the minimax values of each successor state. The recursion proceeds
    all the way down to the leaves of the tree , and then the values are backed up through the tree
    as the recursion unwinds.
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        agentIndex=0
        gridDepth=self.depth
        NumAgents = gameState.getNumAgents();
        decision=["", float('0')]
        if(gridDepth==0 or gameState.isWin() or gameState.isLose()):
            decision = self.evaluationFunction(gameState)
        decision = self.pacmanTurn(gameState, gridDepth, NumAgents, agentIndex)
        return decision[0]

    def noOfGhosts(self,NumAgents,turn):

        return NumAgents-turn

    def pacmanTurn(self, gameState, gridDepth, NumAgents, agentIndex):
        """
        The Max agent function which internally calls Min agent
        """
        v = ["", -float('inf')]
        val = float('0')
        decision1=[]

        if(gridDepth==0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)


        for legal_action in gameState.getLegalActions(agentIndex):
            if legal_action == "Stop":
                continue
            successorState = gameState.generateSuccessor(agentIndex, legal_action)

            decision1.append(self.ghostTurn(successorState, gridDepth, self.noOfGhosts(NumAgents,2), NumAgents, (agentIndex+1)%NumAgents))
            for x in decision1:
                if isinstance(x,float):
                    val=x
                else:
                    for x1 in x:
                        if isinstance(x1,float):
                            val=x1

            if val >  v[1]:
                #Update the value so as to choose the Maximum among the values returned by evaluationFunction
                v = [legal_action, val] #Return the legal action with Max value

        return v

    def ghostTurn(self, gameState, gridDepth, numGhosts, NumAgents, agentIndex):
        v = ["", float('inf')]
        val = float('0')
        decision1=[]
        if(gridDepth==0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)

        for legal_action in gameState.getLegalActions(agentIndex):
            if legal_action == "Stop":
                continue

            successorState = gameState.generateSuccessor(agentIndex, legal_action)

            if(numGhosts == 0):
                decision1.append(self.pacmanTurn(successorState, gridDepth-1, NumAgents, (agentIndex+1)%NumAgents))
            else:
                decision1.append(self.ghostTurn(successorState, gridDepth, self.noOfGhosts(numGhosts,1), NumAgents, (agentIndex+1)%NumAgents))

            for x in decision1:
                if isinstance(x,float):
                    val=x
                else:
                    for x1 in x:
                        if isinstance(x1,float):
                            val=x1
            if val < v[1]:
                #Update the value so as to choose the Minmum among the values returned by evaluationFunction
                v = [legal_action, val] #Return the legal action with minimum value
        return v



class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning. Returns the alpha-beta action using self.depth and self.evaluationFunction
      Here we prune the search tree when Alpha value surpasses Beta value.
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        agentIndex=0
        gridDepth=self.depth
        NumAgents = gameState.getNumAgents();
        alpha = -float('inf')
        beta = float('inf')
        decision=["", float('0')]
        if(gridDepth == 0 or gameState.isWin() or gameState.isLose()):
            decision = self.evaluationFunction(gameState)
        decision = self.pacmanTurn(gameState, gridDepth*NumAgents, NumAgents, agentIndex, alpha, beta)
        return decision[0]

    def pacmanTurn(self, gameState, gridDepth, NumAgents, agentIndex, alpha, beta):
        """
        The Max agent function which internally calls Min agent
        """

        v = ["", -float('inf')]
        val = float('0')
        decision1=[]

        if(gridDepth==0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)

        for legal_action in gameState.getLegalActions(agentIndex):
            if legal_action == "Stop":
                continue
            successorState = gameState.generateSuccessor(agentIndex, legal_action)

            decision1.append( self.ghostTurn(successorState, gridDepth-1, NumAgents-2, NumAgents, (agentIndex+1)%NumAgents, alpha, beta))
            for x in decision1:
                if isinstance(x,float):
                    val=x
                else:
                    for x1 in x:
                        if isinstance(x1,float):
                            val=x1

            if val >  v[1]:
                #Update the value so as to choose the Maximum among the values returned by evaluationFunction
                v = [legal_action, val] #Return the legal action with Max value
            #Update alpha value in pacman turn
            alpha = max(alpha, v[1])
            #Check whether Alpha value surpasses Beta in order to prune the search space
            if alpha > beta:
                return v

        return v

    def ghostTurn(self, gameState, gridDepth, NumMins, NumAgents, agentIndex, alpha, beta):
        """
        The Min agent function which internally calls either Max or Min based on number of agents remained
        """
        v = ["", float('inf')]
        val = float('0')
        decision1=[]
        if(gridDepth==0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)


        for legal_action in gameState.getLegalActions(agentIndex):
            if legal_action == "Stop":
                continue

            successorState = gameState.generateSuccessor(agentIndex, legal_action)

            if(NumMins == 0):
                decision1.append( self.pacmanTurn(successorState, gridDepth-1, NumAgents, (agentIndex+1)%NumAgents, alpha, beta))
            else:
                decision1.append(self.ghostTurn(successorState, gridDepth-1, NumMins-1, NumAgents, (agentIndex+1)%NumAgents, alpha, beta))

            for x in decision1:
                if isinstance(x,float):
                    val=x
                else:
                    for x1 in x:
                        if isinstance(x1,float):
                            val=x1
            if val < v[1]:
                #Update the value so as to choose the Minmum among the values returned by evaluationFunction
                v = [legal_action, val] #Return the legal action with minimum value
            #update beta value in ghost turn
            beta = min(beta, v[1])
            #Check whether Alpha value surpasses Beta in order to prune the search space
            if beta < alpha:
                return v
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Advanced case of MinimaxAgent which takes into consideration randomness of the ghost. Here the Max function(pacmanTurn)
    is kept the same as that of MinimaxAgent. The expectiGhost() function in place of ghostTurn(), takes care of randomness
    of the ghosts
    """
    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts are modeled as choosing uniformly at random from their
          legal moves.
        """

        agentIndex=0
        gridDepth=self.depth
        NumAgents = gameState.getNumAgents();
        decision=["", float('0')]
        if(gridDepth==0 or gameState.isWin() or gameState.isLose()):
            decision = self.evaluationFunction(gameState)
        decision = self.pacmanTurn(gameState,gridDepth, NumAgents, agentIndex)
        return decision[0]

    def noOfGhosts(self, NumAgents, turn):
        """
        returns the number of remaining ghosts
        """
        return NumAgents-turn

    def pacmanTurn(self, gameState, gridDepth, NumAgents, agentIndex):
        """
        The Max agent function which internally calls Min agent
        """

        v = ["", -float('inf')]
        val = float('0')
        decision1=[]


        if(gridDepth==0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)


        for legal_action in gameState.getLegalActions(agentIndex):
            if legal_action == "Stop":
                continue
            successorState = gameState.generateSuccessor(agentIndex, legal_action)

            decision1.append(self.expectiGhost(successorState, gridDepth, self.noOfGhosts(NumAgents,2), NumAgents, (agentIndex+1)%NumAgents))

            for x in decision1:
                if isinstance(x,float):
                    val = x
                else:
                    for x1 in x:
                        if isinstance(x1, float):
                            val = x1
            if val >  v[1]:
                #Update the value so as to choose the Maximum among the values returned by evaluationFunction
                v = [legal_action, val] #Return the legal action with Max value
        return v

    def expectiGhost(self, gameState, gridDepth, numGhosts, NumAgents, agentIndex):
        """
        The Min agent function which internally calls either Max or Min based on number of agents remained.
        Here instead of always choosing minimum value in GhostTurn (Min), we write write another function expectiGhost,
        which takes into consideration randomness of the ghost. It calculates the the average of all the values returned
        by evaluation function.
        """
        v = ["", 0]
        val = float('0')
        decision1 = []

        if(gridDepth==0 or gameState.isWin() or gameState.isLose()):
            return self.evaluationFunction(gameState)
        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)
        #The multiplication factor for finding average of the values returned by evaluationFunction
        probability = 1.0/len(gameState.getLegalActions(agentIndex))
        for legal_action in gameState.getLegalActions(agentIndex):
            if legal_action == "Stop":
                continue

            successorState = gameState.generateSuccessor(agentIndex, legal_action)

            if(numGhosts == 0):
                decision1.append(self.pacmanTurn(successorState, gridDepth-1, NumAgents, (agentIndex+1)%NumAgents))
            else:
                decision1.append(self.expectiGhost(successorState, gridDepth, self.noOfGhosts(numGhosts,1), NumAgents, (agentIndex+1)%NumAgents))

            for x in decision1:
                if isinstance(x,float):
                    val=x
                else:
                    for x1 in x:
                        if isinstance(x1,float):
                            val=x1
            #the multiplication factor is multiplied to each value and the average is calculated
            v[1] += val*probability

            v[0] = legal_action

        return v

    def betterEvaluationFunction(currentGameState):
        """
          Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
          evaluation function (question 5).

          DESCRIPTION: <write something here so we know what you did>
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

    # Abbreviation
    better = betterEvaluationFunction
