import math
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.common.action_chains import ActionChains


depth_of_expectimax = 6


class Node:
    def __init__(self, board):
        self.board = board
        self.children = []

# The nodes which have the players turn next will have 4 children in the Order of UP,Right,Down,left
# The nodes which have the games turn will have anywhere b/w 2-30 children. The children will be created by
# transversing the board in a row major order and appending two children for each empty spot, one child for if that
# spot is filled by a 2 and another node for if that spot is filled by a 4


class Tree:  # The tree will have the property that leaf nodes are always board states that have the players turn
    def __init__(self, board):
        self.node = Node(board)
        assert(not lost(board)), "Cannot initialise a state-space tree with a board that has already lost"

    def increment_depth(self, node):
        pass;


def get_board(drive_window_):
    board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(1, 5):
        for j in range(1, 5):
            board_index_str = "tile-position-" + str(i) + "-" + str(j)
            element_list = drive_window_.find_elements_by_class_name(board_index_str)
            if element_list:
                board_element = element_list[len(element_list)-1]
                board[j - 1][i - 1] = math.floor(math.log2(int(board_element.text)))
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
        time.sleep(5)  # wait for the js to take effect and make the game appear
        board = get_board(driver)
        state_space_tree = Tree(board)
        while not lost(board):
            pass


if __name__ != "__main__":
    pass
else:
    play()

