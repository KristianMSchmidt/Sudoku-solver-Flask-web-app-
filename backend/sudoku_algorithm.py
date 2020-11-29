"""
Automatic soduko solver using two different algorithms:
 1) AC-3 algorithm (short for Arc Consistency Algorithm #3)
 2) BTS (Back Tracking Search) - a depth first search using search heuristics 
In both cases, a soduko puzzle is viewed as a 'constraint satisfaction problem'.

This version solves all 400 test cases in about 18 seconds on my laptop.

From Wiki: 
"Backtracking is a general algorithm for finding all (or some) solutions to some 
computational problems, notably constraint satisfaction problems, that
incrementally builds candidates to the solutions, and abandons a candidate 
("backtracks") as soon as it determines that the candidate cannot possibly
be completed to a valid solution."
"""
import copy

def BTS(sudoku):
    """
    Recursive Sudoku solver using depth first search with "pruning").
    When a variable is assigned, I apply forward checking to reduce variables domains.
    
    NB: This function alters it's argument.
    NB: The soduku must have been through AC_3 before applying this function.
    """
    if is_solved(sudoku):  #If sudoko is solvable, the recursion stops here 
        return(sudoku)

    # Select unassigned tile as start point of solution proces. 
    # It's a clever move to choose tile with as few remaining values left 
    # as possible (2 is minimum for an unassigned tile). This is my 'search heuristic'
    tile = min([(len(val), key) for key, val in sudoku.items() if len(val) > 1])[1]
    
    # Loop through the possible values for chosen tile
    for value in sudoku[tile]: 
        sudoku[tile] = set([value]) # Let's try to assign value to tile
        result_from_AC3 = AC_3_single_tile(sudoku, tile) # Check for inconsistencies with this choice
        if result_from_AC3 != False: # in this case AC_3 did not find any problems with the assignment
            result = BTS(result_from_AC3) # Proceed recursively 
            # The result from BTS is either False (if no solution exists with the current assignment) or
            # else the result = a solved sudoku
            if result != False:    
                return result 

    # if we finish the loop without finding a solution, it means that the soduko is unsolvable
    return False

def AC_3_single_tile(sudoku, tile):
    """
    Arc consistency algorithm for single tile of soduko. This will be called from BTS-algorithm.
    
    Returns false if an inconsistency is found. In this case the sudoku is unsolvable.
    Returns simplified sudoku otherwise. NB: This does not mean that sudoku is solved or solvable.
    NB: This version assumes, that the sudoku was arc-reduced before adding a value to the argument tile...
    """
    current_sudoku = copy.deepcopy(sudoku)

    worklist = set([constraint for constraint in CONSTRAINT_DICT[tile]])

    while worklist:
        X_i, X_j = worklist.pop()
        if current_sudoku[X_j].issubset(current_sudoku[X_i]):
            if len(current_sudoku[X_i]) == 1:
                return False
            current_sudoku[X_i].difference_update(current_sudoku[X_j])
            if len(current_sudoku[X_i]) == 1:
                worklist.update(CONSTRAINT_DICT[X_i].difference((X_j, X_i)))

    return current_sudoku

def AC_3_all_constraints(sudoku):
    """
    Arc consistency 3 algorithm for sodukos. 
    In my speed-uptimized implementation, this version is to be used before applying BTS. 

    Note that in most cases, this algorithm will not be enough to solve the sudoku. It will only
    reduce the number of options left for each unassighed tile before applying BTS. 
    
    Returns false if an inconsistency is found (in this case the input sudoku is unsolvable).
    Returns simplified sudoku otherwise. NB: This does not mean that sudoku is solved or solvable.
    """
    current_sudoku = sudoku
    worklist = ALL_CONSTRAINTS.copy()

    # We examine one constraint in the work list at a time, and keep doing this
    # untill the there are no constraints left
    while worklist: 
        X_i, X_j = worklist.pop()
        # If we know the value of at tile X_j and this value is in the set of possible values for tile X_i, we can update the set of possible values for til X_i
        if len(current_sudoku[X_j]) == 1 and current_sudoku[X_j].issubset(current_sudoku[X_i]):
            if len(current_sudoku[X_i]) == 1:  #In this case the two tiles have the same value, which is not allowed. A constraint it not met, and the puzzle is unsolvable!
                return False
            current_sudoku[X_i].difference_update(current_sudoku[X_j])  # We remove the value of tile X_i from the possible values of tile X_j
            worklist.update(CONSTRAINT_DICT[X_i].difference((X_j, X_i))) # We add constraints that now have to be re-examined to the worklist
    return current_sudoku

def gen_constraints():
    """
    Function that generates two crucial datastructures needed in the algorithm
    
     1) the set 'constraints' of all constraint. A constraint is a pair of tiles 
        (tile_1, tile_2) that constraint each other in the game of sudoku by belonging
        to the same row, the same colums, or the same 3x3-square. Note that if
        (tile_1, tile_2) is in the set, (tile_2, tile_1) will also be in the set
        
    2) A dictionary the form {tile: set of all constraints containing tile as the second element in tuple}    
    """
    # First we add all row and column constraints
    # These are all tuples of tiles belonging to either same row or same column
    # Eg.  (A1, A5), (A5, A1), (D3, D6), (A1, C1), (B3, D3).... ect, etc 
    constraints = set([(tile_1, tile_2)
                  for tile_1 in TILES
                  for tile_2 in TILES
                  if (tile_1[0] == tile_2[0] or tile_1[1] == tile_2[1])  #If same row or if same column
                  and tile_1 != tile_2])   # no tuple of identical tiles, i.g. (C4, C4) will be in the set

    # square constraints:
    for ver in ["ABC", "DEF", "GHI"]:
        for hor in ["123","456", "789"]:
            square = [v+h for v in ver for h in hor] #all tiles belonging to one of the nine 3x3 square regions
                                                    # of the sudoko board
            square_constraints = [(tile_1, tile_2)    #Add add square constraint to the set off all constraints
                  for tile_1 in square                #I.g. (A1, C3) will be in the set.
                  for tile_2 in square
                  if tile_1 != tile_2]
            constraints.update(square_constraints)

    constraint_dict = {}  #constraint dict will be of the form {tile: set of all constraints containing tile}

    for tile in TILES:
        constraint_dict[tile] = set()

    for constraint in constraints:
        tile_1, tile_2 = constraint    
        constraint_dict[tile_2].add(constraint)    
    return constraints, constraint_dict

def gen_board(sudoku_string):
    """
    Generates an internal representation of the input sudoku string
    Input sudoku is a string of the kind "3170....."
    Output sudoku is a dictionary {'A1': set([3]), 'A2': set([4]), 'A3':set([7]), 'A4':set[(1,2,3,4,5,6,7,8,9)], 'A5': ....}
    """
    sudoku = {}
    for indx, tile in enumerate(TILES):
        number = int(sudoku_string[indx]) 
        if number != 0:
            sudoku[tile] = set([number])
        else:
            sudoku[tile] = set(range(1,10))  
    return sudoku

def is_solved(sudoku):
    """
    Checks if sudoku is solved (== only one option left at each position, and no inconsistencies)
    NB: Only works when sudoku has been through AC3 already.
    """
    for val in sudoku.values():
        if len(val) != 1:
            return False

    return True

def gen_solve_string(sudoku):
    """
    Generates a string representation of a solved sudoku.
    """
    #assert(is_solved(sudoku))
    return "".join([str(next(iter(val))) for _, val in sorted(sudoku.items())])

def sudoku_solver(sudoku_string):
    """
    Solves a sudoku given as a string. 
    Returns the solved sudoku as a string + some information about the solution proces. 
    """
    sudoku = gen_board(sudoku_string)

    AC_3_attempt = AC_3_all_constraints(sudoku)
    
    assert(AC_3_attempt), "Input sudoku is unsolvable " + sudoku_string

    if is_solved(AC_3_attempt):        
        return gen_solve_string(AC_3_attempt) + " AC3"   # only AC3 algoritm has been used

    BTS_solution = BTS(AC_3_attempt)

    return gen_solve_string(BTS_solution) + " BTS"  # both AC3 and BTS algorithms have been used

# A few useful global constants:
TILES = [row + col for row in "ABCDEFGHI" for col in "123456789"]
ALL_CONSTRAINTS, CONSTRAINT_DICT = gen_constraints()