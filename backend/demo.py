"""
Command-line demo of sudoku solver
"""
from sudoku_algorithm import *

def small_demo():
    sudoku_string = "000008900603049010000500600004000009230000001050002060007000000302051000508960203"
    solution = sudoku_solver(sudoku_string)
    print(solution)

def big_demo():
    """
    Solving all 400 test sudokus. It takes about 20 seconds on my laptop. 
    """
    # get solutions
    with open("sudokus_finish.txt") as file:
        all_solutions = [line.strip() for line in file]

    #solve sudokus and compare with solutions:
    with open("sudokus_start.txt") as all_sudokus:
        for i, sudoku in enumerate(all_sudokus):
            calculated = sudoku_solver(sudoku)
            expected = all_solutions[i]
            assert(calculated == expected)
            assert(is_solved(gen_board(calculated.split()[0])))
            print("#{}: {}".format(i+1, calculated))
    
    print("Solved all 400 sudokus correctly")

small_demo()