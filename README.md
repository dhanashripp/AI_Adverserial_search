# AI_Adverserial_search
Implementation for Reflex agent, MiniMax agent, Alpha-Beta pruning, Expetimax agent

Solution Details:
Question 1. Reflex Agent
This type of rational agent takes action on the basis of current state only. Here the pacman takes action by examining the values of an evaluation function, higher the value more the chance of taking that action.
The evaluation function implementation is based on the status of ghost (Active or Scared) and Manhattan distance of food pellets. Since the new food grid, successorGameState.getFood() keeps on changing based on the remaining food pellets, we have chosen old food grid, currentGameState.getFood(). Thus the closest food pellet to be eaten is selected by calculating the Manhattan distance of new position of Pacman from the food in old food grid.
The action that leads Pacman to an active ghost is given Max negative score. Similarly the action that leads Pacman towards wall is given MAx negative score. The negation of minimum Manhattan distance is returned. Thus the bestScore chooses Max out of all above scores giving higher priority to eating food pellets.


Question 2. Minimax Agent

This agent returns the minimax action from the current gameState using self.depth and self.evaluationFunction. It uses a simple recursive computation of the minimax values of each successor state. The recursion proceeds all the way down to the leaves of the tree (gridDepth==0 or gameState.isWin() or gameState.isLose()), and then the values are backed up through the tree as the recursion unwinds.
During implementation, the Pacman(Max) chooses the maximum among the values returned by evaluation function and hands over the turn to ghost (Min). In case of multiple ghosts, the ghost function is called recursively and for every ghost, minimum among all values returned by evaluation function is chosen. When the ghost is called from the pacmanTurn() for the first time, we send the number of ghosts remained(numGhosts) as NumAgents-2 (Since the turn of Pacman as well as the current ghost being called is over). Further inside ghostTurn() we check for the number of ghosts remained continue the execution as per following pseudocode:
if(numGhosts == 0):
   pacmanTurn()
else:
   ghostTurn(numGhosts-1)


Question 3. Alpha-Beta Pruning
Alpha-Beta pruning helps to reduce the expansion of unnecessary nodes. Here we introduce two variables Alpha (initialized to lowest possible value -∞) and Beta ( initialized to highest possible value +∞). Alpha value is updated in PacmanTurn(), where it is replaced by max value among the values returned by evaluation function. Beta value is updated in GhostTurn(), where it is replaced by min value among the values returned by evaluation function.The search space is cut down when the value of Alpha surpasses that of Beta.

Question 4. Expectimax
The unpredictability of external factors is mirrored by introducing randomness in Expectimax agent. Here instead of always choosing minimum value in GhostTurn (Min), we write write another function expectiGhost, which takes into consideration randomness of the ghost. It calculates the the average of all the values returned by evaluation function. We achieve this by using below constant:

probability = 1.0/len(gameState.getLegalActions(agentIndex))

Further, multiplying this probability with each leaf value and summing up all these values for the Min ply.

The advantage that Pacman gains because of randomness included in Expectimax is proved by the increased win rate than that that of Alpha Beta Algorithm:

$ python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Average Score: -501.0
Scores:        -501.0, -501.0, -501.0, -501.0, -501.0, -501.0, -501.0, -501.0, -501.0, -501.0
Win Rate:      0/10 (0.00)
Record:        Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss



$ python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10
Pacman emerges victorious! Score: 532
Pacman emerges victorious! Score: 532
Pacman emerges victorious! Score: 532
Pacman emerges victorious! Score: 532
Pacman died! Score: -502
Pacman emerges victorious! Score: 532
Pacman died! Score: -502
Pacman emerges victorious! Score: 532
Pacman emerges victorious! Score: 532
Pacman died! Score: -502
Average Score: 221.8
Scores:        532.0, 532.0, 532.0, 532.0, -502.0, 532.0, -502.0, 532.0, 532.0, -502.0
Win Rate:      7/10 (0.70)
Record:        Win, Win, Win, Win, Loss, Win, Loss, Win, Win, Loss
