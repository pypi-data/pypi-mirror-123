from tcgame.envs.path_finding import PathFinding
from tcgame.envs.path_finding_2d import Maze
from tcgame.envs.flappy import FlappyBird


def getGameEnv(gameName):
    if gameName == 'path_finding':
    	return PathFinding()
    if gameName == 'path_finding_2d':
        return Maze()
    if gameName == 'flappybird':
        return FlappyBird()

