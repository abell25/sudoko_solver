import math
import os

BOARD = "4     8 5 3          7      2     6     8 4      1       6 3 7 5  2     1 4      "
SOLUTION = list(len(BOARD)*[' '])
CELLS = len(BOARD)
ROWS = int(math.sqrt(CELLS))
COLUMNS = ROWS
NUMBER_OF_SQUARES = ROWS
SQUARE_SIDE = int(math.sqrt((CELLS/NUMBER_OF_SQUARES)))
VALUES = range(1, ROWS+1)
INFILE = "sudoku.cnf"
OUTFILE = 'sudoku.out'
LINES = []
CONSTRAINTS = []
KNOWNS = []
VERBOSE = False
NUM_VARIABLES = len(VALUES)*CELLS
print "sudoku.py starting!"

def init_board(board):
  global LINES, KNOWNS, BOARD, SOLUTION, CELLS, ROWS, COLUMNS
  global NUMBER_OF_SQUARES, SQUARE_SIDE, VALUES, NUM_VARIABLES

  BOARD = board
  SOLUTION = list(len(BOARD)*[' '])
  CELLS = len(BOARD)
  ROWS = int(math.sqrt(CELLS))
  COLUMNS = ROWS
  NUMBER_OF_SQUARES = ROWS
  SQUARE_SIDE = int(math.sqrt((CELLS/NUMBER_OF_SQUARES)))
  VALUES = range(1, ROWS+1)
  print "len(lines) = %d" % len(LINES)
  LINES = []
  KNOWNS = []
  NUM_VARIABLES = len(VALUES)*CELLS
  
def getBool(variable, value):
  return variable + ((value-1)*CELLS)

def allDiff(variables, values):
  remaining = list(variables)
  for v1 in variables:
    remaining.remove(v1)
    for v2 in remaining:
      for val in values:
        CONSTRAINTS.append("-%d -%d 0" % (getBool(v1, val), getBool(v2, val)))
  for val in values:
    CONSTRAINTS.append("%s 0" % ' '.join([str(getBool(x, val)) for x in values]))

def getKnown():
  for i in range(1,CELLS+1):
    if BOARD[i-1] != ' ':
      KNOWNS.append("%d 0" % getBool(i, int(BOARD[i-1])))
      if VERBOSE: print "%d 0" % getBool(i, int(BOARD[i-1]))

def constraints():
  if len(CONSTRAINTS) > 0: return
  # Contraint %1: Every row value is different
  for r in range(1,ROWS+1):
      allDiff([c + (r-1)*COLUMNS for c in range(1,COLUMNS+1)], VALUES)
  # Constraint %2: Every column value is different
  for c in range(1,COLUMNS+1):
      allDiff([c + (r-1)*ROWS for r in range(1,ROWS+1)], VALUES)
      #allDiff([r + (c-1)*ROWS for r in range(1,ROWS+1)], VALUES)
  #Constraint %3: Every square value is different
  for sq in range(1, NUMBER_OF_SQUARES+1):
      allDiff(getSquare(sq), VALUES)
  #Constraint %4: Every cell has 1 value 
  # (exactly 1 to be precise but the previous constraints ensure this)
  for c in range(1,CELLS+1):
      CONSTRAINTS.append('%s 0' % ' '.join([str(getBool(c, val)) for val in VALUES]))
      if VERBOSE: print '%s 0' % ' '.join([str(getBool(c, val)) for val in VALUES])

def run():
  total_variables = CELLS*len(VALUES)
  getKnown()
  constraints()
  total_expressions = len(CONSTRAINTS) + len(KNOWNS)
  f = open(INFILE, 'w')
  f.write("c **** sudoku solver tony bell 2013 ****\n")
  f.write("p cnf %d %d\n" % (total_variables, total_expressions))
  f.write('\n'.join(CONSTRAINTS + KNOWNS))
  f.close()

def getSquare(square_no):
  sq_col = ((square_no-1) % SQUARE_SIDE)
  sq_row = ((square_no-1) / SQUARE_SIDE)
  square = []
  for r in range(1,SQUARE_SIDE+1):
    row = SQUARE_SIDE*sq_row + r
    column = SQUARE_SIDE*sq_col
    square.extend([x+column + (row-1)*COLUMNS for x in range(1,SQUARE_SIDE+1)])
  return square

def solve():
  run()
  os.system('MiniSat_v1.14_cygwin %s %s' % (INFILE, OUTFILE))
  if VERBOSE: os.system('cat %s' % INFILE)
  result = open(OUTFILE, 'r').readlines()
  if result[0].find('UNSAT') == 0 :
    SOLUTION = "UNSAT"
    return False
  else:  
    printResults(result[1][0:-3])
    return True

def printResults(results):
  for r in [int(x) for x in results.split(' ') if int(x) > 0]:
    cell  = ((r-1) % CELLS) + 1
    value = ((r-1) / CELLS) + 1
    SOLUTION[cell-1] = str(value)

  soln = ''.join(SOLUTION)
  T = ""
  for r in range(1,ROWS+1):
    if r!=1 and (r-1) % SQUARE_SIDE == 0:
      T += '-'*(COLUMNS + (SQUARE_SIDE-1)) + '\n'
    for c in range(1, COLUMNS+1):
      if c!=1 and (c-1) % SQUARE_SIDE == 0:
        T += '|'
      T += soln[(r-1)*COLUMNS + (c-1)]
    T += '\n'
  print T


def solve_hard_problems():
  f = open('hard.data', 'r')
  problems = [x[0:-1] for x in f.readlines() if len(x) > 4]
  successful = 0

  for prob in problems:
    init_board(prob)
    if solve() is True: successful += 1

  print "%d/%d successfully solved!" % (successful, len(problems))

if __name__ == "__main__":
  solve_hard_problems()

