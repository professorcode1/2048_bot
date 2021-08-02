import math
import random
import time
from copy import deepcopy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.action_chains import ActionChains
minimum_fitness = 0

def print_board(board):
    for i in range(4):
        print(board[i])
    print("\n\n")


def create_up_board(board):
    up_board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for j in range(4):
        hlpr_arr = []
        for i in range(4):
            if board[i][j]:
                hlpr_arr.append(board[i][j])
        # print(hlpr_arr)
        for i in range(0, len(hlpr_arr) - 1):
            # print(hlpr_arr[i], hlpr_arr[i+1], hlpr_arr[i] == hlpr_arr[i+1])
            if hlpr_arr[i] == hlpr_arr[i + 1] and hlpr_arr[i]:
                hlpr_arr[i] += 1
                for x in range(i + 1, len(hlpr_arr) - 1):
                    hlpr_arr[x] = hlpr_arr[x + 1]
                hlpr_arr[len(hlpr_arr) - 1] = 0
        for i in range(len(hlpr_arr)):
            up_board[i][j] = hlpr_arr[i]
    return up_board


def create_left_board(board):
    left_board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(4):
        hlpr_arr = []
        for j in range(4):
            if board[i][j]:
                hlpr_arr.append(board[i][j])
        # print(hlpr_arr)
        for j in range(0, len(hlpr_arr) - 1):
            # print(hlpr_arr[i], hlpr_arr[i+1], hlpr_arr[i] == hlpr_arr[i+1])
            if hlpr_arr[j] == hlpr_arr[j + 1] and hlpr_arr[j]:
                hlpr_arr[j] += 1
                for x in range(j + 1, len(hlpr_arr) - 1):
                    hlpr_arr[x] = hlpr_arr[x + 1]
                hlpr_arr[len(hlpr_arr) - 1] = 0
        for j in range(len(hlpr_arr)):
            left_board[i][j] = hlpr_arr[j]
    return left_board


def create_right_board(board):
    right_board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(4):
        hlpr_arr = []
        for j in range(4):
            if board[i][j]:
                hlpr_arr.append(board[i][j])
        # print(hlpr_arr)
        for j in range(len(hlpr_arr) - 1, 0, -1):
            # print(hlpr_arr[i], hlpr_arr[i+1], hlpr_arr[i] == hlpr_arr[i+1])
            if hlpr_arr[j] == hlpr_arr[j - 1] and hlpr_arr[j]:
                hlpr_arr[j] += 1
                for x in range(j - 1, 0, -1):
                    hlpr_arr[x] = hlpr_arr[x - 1]
                hlpr_arr[0] = 0
        for j in range(len(hlpr_arr)):
            right_board[i][4 - len(hlpr_arr) + j] = hlpr_arr[j]
    return right_board


def create_down_board(board):
    down_board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for j in range(4):
        hlpr_arr = []
        for i in range(4):
            if board[i][j]:
                hlpr_arr.append(board[i][j])
        # print(hlpr_arr)
        for i in range(len(hlpr_arr) - 1, 0, -1):
            # print(hlpr_arr[i], hlpr_arr[i+1], hlpr_arr[i] == hlpr_arr[i+1])
            if hlpr_arr[i] == hlpr_arr[i - 1] and hlpr_arr[i]:
                hlpr_arr[i] += 1
                for x in range(i - 1, 0, -1):
                    hlpr_arr[x] = hlpr_arr[x - 1]
                hlpr_arr[0] = 0
        for i in range(len(hlpr_arr)):
            down_board[4 - len(hlpr_arr) + i][j] = hlpr_arr[i]
    return down_board


class Node:
    def __init__(self, board, next_turn_player):
        self.board = board
        self.children = []
        self.next_turn_player = next_turn_player # will be true is this board state is created by a game move. So this will be set true for all leaf's and root

    def create_children_from_player_moves(self):
        assert (not len(self.children)), "create children method called on a node which already has children"
        up_board = create_up_board(self.board)
        if up_board == self.board:
            self.children.append(None)
        else:
            self.children.append(Node(up_board, False))

        right_board = create_right_board(self.board)
        if right_board == self.board:
            self.children.append(None)
        else:
            self.children.append(Node(right_board, False))

        down_board = create_down_board(self.board)
        if down_board == self.board:
            self.children.append(None)
        else:
            self.children.append(Node(down_board, False))

        left_board = create_left_board(self.board)
        if left_board == self.board:
            self.children.append(None)
        else:
            self.children.append(Node(left_board, False))

    def create_children_from_game_moves(self):
        assert (not len(self.children)), "create children method called on a node which already has children"
        for i in range(4):
            for j in range(4):
                if not self.board[i][j]:
                    create_2_board = deepcopy(self.board)
                    create_2_board[i][j] = 1
                    self.children.append(Node(create_2_board, True))

                    create_4_board = deepcopy(self.board)
                    create_4_board[i][j] = 2
                    self.children.append(Node(create_4_board, True))

    def increment_depth(self, depth):
        if depth <= 0:
            return
        self.create_children_from_player_moves()
        for player_move_child in self.children:
            if player_move_child:
                player_move_child.create_children_from_game_moves()
                for game_move_child in player_move_child.children:
                    game_move_child.increment_depth(depth-2)

    def evaluate_fitness(self):
        if not len(self.children):
            return self.fitness_heuristic()
        if self.next_turn_player:
            fitness_left = minimum_fitness
            fitness_up = minimum_fitness
            fitness_right = minimum_fitness
            fitness_down = minimum_fitness
            if self.children[0]:
                fitness_up = self.children[0].evaluate_fitness()
            if self.children[1]:
                fitness_right = self.children[1].evaluate_fitness()
            if self.children[2]:
                fitness_down = self.children[2].evaluate_fitness()
            if self.children[3]:
                fitness_left = self.children[3].evaluate_fitness()
            return max(fitness_up, fitness_left, fitness_down, fitness_right)
        else:
            probability_ = 20 / (11 * len(self.children))
            total_fitness = 0
            for i in range(len(self.children)):
                if i%2:
                    total_fitness += self.children[i].evaluate_fitness() / 10
                else:
                    total_fitness += self.children[i].evaluate_fitness()
            return probability_ * total_fitness

    def fitness_heuristic(self):
        if lost(self.board):
            return 0
        return random.random() # The fitness value has to be in [0,1] for expectimax to work
# The nodes which have the players turn next will have 4 children in the Order of UP,Right,Down,left
# The nodes which have the games turn will have anywhere b/w 2-30 children. The children will be created by
# transversing the board in a row major order and appending two children for each empty spot, one child for if that
# spot is filled by a 2 and another node for if that spot is filled by a 4


class Tree:  # The tree will have the property that leaf nodes are always board states that have the players turn
    depth_of_expectimax = 6

    def __init__(self, board):
        self.root = Node(board, True)
        assert(not lost(board)), "Cannot initialise a state-space tree with a board that has already lost"
        self.root.increment_depth(Tree.depth_of_expectimax)

    def move_to_make(self):
        fitness_up = minimum_fitness
        fitness_right = minimum_fitness
        fitness_down = minimum_fitness
        fitness_left = minimum_fitness
        if self.root.children[0]:
            fitness_up = self.root.children[0].evaluate_fitness()
        if self.root.children[1]:
            fitness_right = self.root.children[1].evaluate_fitness()
        if self.root.children[2]:
            fitness_down = self.root.children[2].evaluate_fitness()
        if self.root.children[3]:
            fitness_left = self.root.children[3].evaluate_fitness()
        max_fitness = max(fitness_up, fitness_left, fitness_down, fitness_right)
        print(fitness_up,  fitness_right, fitness_down, fitness_left)
        if max_fitness == fitness_up:
            return "UP"
        if max_fitness == fitness_right:
            return "RIGHT"
        if max_fitness == fitness_down:
            return "DOWN"
        if max_fitness == fitness_left:
            return "LEFT"


def get_board(drive_window_):
    board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(1, 5):
        for j in range(1, 5):
            board_index_str = "tile-position-" + str(i) + "-" + str(j)
            element_list = drive_window_.find_elements_by_class_name(board_index_str)
            if element_list:
                board_element = element_list[len(element_list)-1]
                board[j - 1][i - 1] = math.floor(math.log2(int(board_element.text)))
    print_board(board)
    return board


def up_action(action):
    action.key_down(Keys.ARROW_UP)
    action.key_up(Keys.ARROW_UP)
    action.perform()
    return time.time()


def left_action(action):
    action.key_down(Keys.ARROW_LEFT)
    action.key_up(Keys.ARROW_LEFT)
    action.perform()
    return time.time()


def right_action(action):
    action.key_down(Keys.ARROW_RIGHT)
    action.key_up(Keys.ARROW_RIGHT)
    action.perform()
    return time.time()


def down_action(action):
    action.key_down(Keys.ARROW_DOWN)
    action.key_up(Keys.ARROW_DOWN)
    action.perform()
    return time.time()


def lost(board):
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j+1]:
                return False
    for i in range(3):
        for j in range(4):
            if board[i][j] == board[i+1][j]:
                return False
    return True


def play():
    with webdriver.Firefox() as driver:
        driver.get("https://2048game.com/")
        action = ActionChains(driver)
        time.sleep(10)  # wait for the js to take effect and make the game appear
        board = get_board(driver)
        state_space_tree = Tree(board)
        print(state_space_tree.move_to_make())

        # keep-playing-button , this is gonna be the class of the anchor tag , clicking on which will continue the game


if __name__ != "__main__":
    pass
else:
    play()

