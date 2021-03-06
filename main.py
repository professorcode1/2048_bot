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
    def __init__(self, board, next_turn_player, parent):
        self.board = board
        self.children = []
        self.next_turn_player = next_turn_player # will be true is this board state is created by a game move. So this will be set true for all leaf's and root
        self.parent = parent

    def create_children_from_player_moves(self):
        assert (not len(self.children)), "create children method called on a node which already has children"
        up_board = create_up_board(self.board)
        if up_board == self.board:
            self.children.append(None)
        else:
            self.children.append(Node(up_board, False, self))

        right_board = create_right_board(self.board)
        if right_board == self.board:
            self.children.append(None)
        else:
            self.children.append(Node(right_board, False, self))

        down_board = create_down_board(self.board)
        if down_board == self.board:
            self.children.append(None)
        else:
            self.children.append(Node(down_board, False, self))

        left_board = create_left_board(self.board)
        if left_board == self.board:
            self.children.append(None)
        else:
            self.children.append(Node(left_board, False, self))

    def create_children_from_game_moves(self):
        assert (not len(self.children)), "create children method called on a node which already has children"
        for i in range(4):
            for j in range(4):
                if not self.board[i][j]:
                    create_2_board = deepcopy(self.board)
                    create_2_board[i][j] = 1
                    self.children.append(Node(create_2_board, True, self))

                    create_4_board = deepcopy(self.board)
                    create_4_board[i][j] = 2
                    self.children.append(Node(create_4_board, True, self))

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
            total_fitness = 0
            #worst_move_fitness = self.children[0].evaluate_fitness()
            for i in range(len(self.children)):
                # if self.children[i].evaluate_fitness() < worst_move_fitness:
                #     worst_move_fitness = self.children[i].evaluate_fitness()
                if i%2:
                   total_fitness += self.children[i].evaluate_fitness() / 10
                else:
                  total_fitness += (9 * self.children[i].evaluate_fitness()) / 10
            return total_fitness / len(self.children)
            #return worst_move_fitness

    def monotonicity_measure(self):
        best = -1
        for i in range(4):
            current = 0
            for row in range(4):
                for column in range(3):
                    if self.board[row][column] >= self.board[row][column + 1]:
                        current += 1
            for column in range(4):
                for row in range(3):
                    if self.board[row][column] >= self.board[row + 1][column]:
                        current += 1
            if current > best:
                best = current
            old_board = deepcopy(self.board)
            self.board[0][0] = old_board[3][0]
            self.board[0][1] = old_board[2][0]
            self.board[0][2] = old_board[1][0]
            self.board[0][3] = old_board[0][0]

            self.board[1][0] = old_board[3][1]
            self.board[1][1] = old_board[2][1]
            self.board[1][2] = old_board[1][1]
            self.board[1][3] = old_board[0][1]

            self.board[2][0] = old_board[3][2]
            self.board[2][1] = old_board[2][2]
            self.board[2][2] = old_board[1][2]
            self.board[2][3] = old_board[0][2]

            self.board[3][0] = old_board[3][3]
            self.board[3][1] = old_board[2][3]
            self.board[3][2] = old_board[1][3]
            self.board[3][3] = old_board[0][3]
        return best

    def empty_measure(self):
        zero_count = 0
        for row in range(4):
            for col in range(4):
                if not self.board[row][col]:
                    zero_count += 1
        return zero_count

    def fitness_heuristic(self):
        return self.monotonicity_measure() + 1.2 * self.empty_measure() - self.cluter_heurisitc()
        return self.patter_heuristic() * (2.7 + self.empty_measure())
        return self.patter_heuristic() - self.cluter_heurisitc() + \
               (self.monotonicity_measure() * (2.75 + self.empty_measure()))

    def cluter_heurisitc(self):
        penalty = 0
        for i in range(4):
            for j in range(4):
                if i < 3:
                    penalty += abs(self.board[i][j] - self.board[i+1][j])
                if j < 3:
                    penalty += abs(self.board[i][j] - self.board[i][j+1])
        return penalty - 544

    def patter_heuristic(self):
        weight_mat = [[0, 0, 0, 3], [0, 0, 3, 5], [0, 3, 5, 15], [3, 5, 15, 30]]
        weight_mat = [[17, 16, 15, 14], [13, 12, 11, 10], [9, 8, 7, 6], [5, 4, 3, 2]]
        val = 0
        for i in range(4):
            for j in range(4):
                val += weight_mat[i][j] * weight_mat[i][j] * self.board[i][j]
        return val

    def big_number_not_on_corners(self):
        penalty = 1
        # count_penalty_after = 4
        # if self.board[1][1] <= count_penalty_after:
        #     penalty += self.board[1][1]
        # if self.board[2][1] <= count_penalty_after:
        #     penalty += self.board[2][1]
        # if self.board[1][2] <= count_penalty_after:
        #     penalty += self.board[1][2]
        # if self.board[2][2] <= count_penalty_after:
        #     penalty += self.board[2][2]
        #
        # if self.board[0][1] <= count_penalty_after:
        #     penalty += self.board[0][1]/2
        # if self.board[0][2] <= count_penalty_after:
        #     penalty += self.board[0][2]/2
        # if self.board[1][0] <= count_penalty_after:
        #     penalty += self.board[1][0]/2
        # if self.board[2][0] <= count_penalty_after:
        #     penalty += self.board[2][0]/2
        # if self.board[3][1] <= count_penalty_after:
        #     penalty += self.board[3][1]/2
        # if self.board[3][2] <= count_penalty_after:
        #     penalty += self.board[3][2]/2
        # if self.board[1][3] <= count_penalty_after:
        #     penalty += self.board[1][3]/2
        # if self.board[2][3] <= count_penalty_after:
        #     penalty += self.board[2][3]/2
        penalty_matrix = [[0, 0, 1, 3], [0, 1, 3, 5], [1, 3, 5, 15], [3, 5, 15, 30]]
        for i in range(4):
            for j in range(4):
                if self.board[i][j] <4:
                    penalty += (4 - self.board[i][j]) * penalty_matrix[i][j]
        return penalty - 360
# The nodes which have the players turn next will have 4 children in the Order of UP,Right,Down,left
# The nodes which have the games turn will have anywhere b/w 2-30 children. The children will be created by
# transversing the board in a row major order and appending two children for each empty spot, one child for if that
# spot is filled by a 2 and another node for if that spot is filled by a 4


class Tree:  # The tree will have the property that leaf nodes are always board states that have the players turn
    depth_of_expectimax = 2
    _2048_achieved = False
    _512_achieved = False
    _128_achieved = False # will keep increasing depth by 2 as bigger and bigger numbers are achieved

    def __init__(self, board):
        self.root = Node(board, True, None)
        assert(not lost(board)), "Cannot initialise a state-space tree with a board that has already lost"
        self.root.increment_depth(Tree.depth_of_expectimax)
        all_zeros = True
        for i in range(4):
            for j in range(4):
                all_zeros = all_zeros or board[i][j] == 0
        assert all_zeros, "This board has all zeros"

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
        if max_fitness == fitness_up and self.root.children[0]:
            return "UP"
        if max_fitness == fitness_right and self.root.children[1]:
            return "RIGHT"
        if max_fitness == fitness_down  and self.root.children[2]:
            return "DOWN"
        if max_fitness == fitness_left  and self.root.children[3]:
            return "LEFT"

    def game_move_update(self, new_board, move):
        if move == "UP":
            player_board = self.root.children[0]
        elif move == "RIGHT":
            player_board = self.root.children[1]
        elif move == "DOWN":
            player_board = self.root.children[2]
        elif move == "LEFT":
            player_board = self.root.children[3]
        else:
            raise Exception("The move is not any of the four directions")
        new_root = None
        for player_board_children_itrt in player_board.children:
            if player_board_children_itrt:
                if player_board_children_itrt.board == new_board:
                    new_root = player_board_children_itrt
                    break
        if not new_root:
            print_board(player_board.board)
            for player_board_children_itrt in player_board.children:
                print_board(player_board_children_itrt.board)
            input("The assert error is gonna trigger")
        assert new_root, "The board that the game is in, is absent from the state space tree"
        self.root = new_root
        self.root.parent = None
        _2048 = False
        _512 = False
        _128 = False
        for row in range(4):
            for col in range(4):
                if self.root.board[row][col] == 7:
                    _128 = True
                elif self.root.board[row][col] == 9:
                    _512 = True
                elif self.root.board[row][col] == 11:
                    _2048 = True

        if _128 and not self._128_achieved :
            self._128_achieved = True
            self.bfs_and_increment(self.root, 4)
            Tree.depth_of_expectimax = 4
        elif _512 and not self._512_achieved:
            self._512_achieved = True
            self.bfs_and_increment(self.root, 4)
            Tree.depth_of_expectimax = 6
        elif _2048 and not self._2048_achieved:
            self._2048_achieved = True
            self.bfs_and_increment(self.root, 4)
            Tree.depth_of_expectimax = 8
        else:
            self.bfs_and_increment(self.root, 2)

    def bfs_and_increment(self, node, depth):
        if node is None:
            return
        if len(node.children):
            for child_node in node.children:
                self.bfs_and_increment(child_node, depth)
        else:

            # 1 Gear version
            node.increment_depth(depth)

            # 2 GEAR VERSION
            # if Tree.depth_of_expectimax == 4:
            #     if self.root.empty_measure() <=4 :
            #         node.increment_depth(4)
            #         Tree.depth_of_expectimax = 6
            #     else:
            #         node.increment_depth(2)
            # elif Tree.depth_of_expectimax == 6:
            #     if self.root.empty_measure() <= 4:
            #         node.increment_depth(2)
            #     else:
            #         Tree.depth_of_expectimax = 4
            # else:
            #     raise Exception("State Space Tree does not have a depth of 4,6 or 8")

            # 4 GEAR VERSION
            # if Tree.depth_of_expectimax == 4:
            #     if self.root.empty_measure() <=4 :
            #         node.increment_depth(6)
            #         Tree.depth_of_expectimax = 8
            #     elif self.root.empty_measure() <=8:
            #         node.increment_depth(4)
            #         Tree.depth_of_expectimax = 6
            #     else:
            #         node.increment_depth(2)
            # elif Tree.depth_of_expectimax == 6:
            #     if self.root.empty_measure() <=4:
            #         node.increment_depth(4)
            #         Tree.depth_of_expectimax = 8
            #     elif self.root.empty_measure() <= 8:
            #         node.increment_depth(2)
            #     else:
            #         Tree.depth_of_expectimax = 4
            # elif Tree.depth_of_expectimax == 8:
            #     if self.root.empty_measure() <= 4:
            #         node.increment_depth(2)
            #     else:
            #         Tree.depth_of_expectimax = 6
            # else:
            #     raise Exception("State Space Tree does not have a depth of 4,6 or 8")
        # find all the leaf nodes, expand state space tree by one more(player and game)


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
    print("Up action called")
    action.key_down(Keys.ARROW_UP)
    action.key_up(Keys.ARROW_UP)
    action.perform()


def left_action(action):
    print("Left action called")
    action.key_down(Keys.ARROW_LEFT)
    action.key_up(Keys.ARROW_LEFT)
    action.perform()


def right_action(action):
    print("Right action called")
    action.key_down(Keys.ARROW_RIGHT)
    action.key_up(Keys.ARROW_RIGHT)
    action.perform()


def down_action(action):
    print("Down action called")
    action.key_down(Keys.ARROW_DOWN)
    action.key_up(Keys.ARROW_DOWN)
    action.perform()


def lost(board):
    for i in range(4):
        for j in range(3):
            if board[i][j] == board[i][j+1]:
                return False
    for i in range(3):
        for j in range(4):
            if board[i][j] == board[i+1][j]:
                return False
    for i in range(4):
        for j in range(4):
            if not board[i][j]:
                return False;
    return True


def play():
    with webdriver.Firefox() as driver:
        driver.get("https://2048game.com/")
        time.sleep(2)  # wait for the js to take effect and make the game appear
        board = get_board(driver)
        state_space_tree = Tree(board)
        got_2048 = False
        while True:
            action = ActionChains(driver)
            move = state_space_tree.move_to_make()
            if move == "UP":
                up_action(action)
            elif move == "RIGHT":
                right_action(action)
            elif move == "DOWN":
                down_action(action)
            elif move == "LEFT":
                left_action(action)
            else:
                raise Exception("The move is not any of the four directions")
            time.sleep(0.15) # wait for the move animation to play out and the webpage to get updated
            new_board = get_board(driver)
            if lost(new_board):
                break
            if not got_2048:
                for i in range(4):
                    for j in range(4):
                        if new_board[i][j] == 11:
                            time.sleep(3)
                            anchor_to_continue = driver.find_elements_by_class_name("keep-playing-button")
                            anchor_to_continue[0].click()
                            got_2048 = True
            state_space_tree.game_move_update(new_board, move)
        print("Game Over")
        time.sleep(20)
        #  , this is gonna be the class of the anchor tag , clicking on which will continue the game


if __name__ != "__main__":
    pass
else:
    play()

