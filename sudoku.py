import math
import os

BOARD1 = "1  4 3 23   2 43"
BOARD2 =  "195  6   " + \
         "8 7  163 " + \
         "  47 21  " + \
         " 7  2391 " + \
         "         " + \
         " 5314  6 " + \
         "  92 78  " + \
         " 865  3 7" + \
         "   3  526"

BOARD =  "6    41  " + \
         "7    8   " + \
         "9 4 17   " + \
         " 6738    " + \
         "82 7 1 36" + \
         " 13  57 9" + \
         " 981 3 7 " + \
         " 4   6 1 " + \
         "   49  5 "

SOLUTION = list(len(BOARD)*[' '])#list(BOARD)
CELLS = len(BOARD)
ROWS = int(math.sqrt(CELLS))
COLUMNS = ROWS
NUMBER_OF_SQUARES = ROWS
SQUARE_SIDE = int(math.sqrt((CELLS/NUMBER_OF_SQUARES)))
VALUES = range(1, ROWS+1)
INFILE = "sudoku.cnf"
OUTFILE = 'sudoku.out'
lines = []
VERBOSE = False
f = open(INFILE, 'w')
NUM_VARIABLES = len(VALUES)*CELLS
print "sudoku.py running!"

def getBool(variable, value):
  return variable + ((value-1)*CELLS)

def allDiff(variables, values):
  remaining = list(variables)
  for v1 in variables:
    remaining.remove(v1)
    for v2 in remaining:
      for val in values:
        lines.append("-%d -%d 0" % (getBool(v1, val), getBool(v2, val)))
        if VERBOSE: print "-%d -%d 0" % (getBool(v1, val), getBool(v2, val))
  for val in values:
    lines.append("%s 0" % ' '.join([str(getBool(x, val)) for x in values]))
    if VERBOSE: print "%s 0" % ' '.join([str(getBool(x, val)) for x in values])

def getKnown():
  for i in range(1,CELLS+1):
    if BOARD[i-1] != ' ':
      lines.append("%d 0" % getBool(i, int(BOARD[i-1])))
      if VERBOSE: print "%d 0" % getBool(i, int(BOARD[i-1]))

def constraints():
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
  for c in range(1,CELLS+1):
      lines.append('%s 0' % ' '.join([str(getBool(c, val)) for val in VALUES]))
      if VERBOSE: print '%s 0' % ' '.join([str(getBool(c, val)) for val in VALUES])

def run():
  total_variables = CELLS*len(VALUES)
  getKnown()
  constraints()
  total_expressions = len(lines)
  f.write("c **** sudoku solver tony bell 2013 ****\n")
  f.write("p cnf %d %d\n" % (total_variables, total_expressions))
  f.write('\n'.join(lines))
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
  printResults(result[1][0:-3])

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

  nums = [x for x in results.split(' ') if int(x) > 0 ]
  print "%d nums found: %s" % (len(nums), str(nums))
    #print soln[(r-1)*COLUMNS:r*COLUMNS]

def testForSecondSolution():
  f = open(OUTFILE, 'r')
  g = open(INFILE, 'a')
  g.write(negate(f.readlines()[1]))
  f.close()
  g.close()
  os.system('MiniSat_v1.14_cygwin %s %s' % (INFILE, OUTFILE))
  result = open(OUTFILE, 'r').readlines()
  printResults(result[1][0:-3])

  
def negate(s):
  return ' '.join(map(lambda x: str(-int(x)) if int(x)!=0 else '0',s.split(' ')))

if __name__ == "__main__":
  solve()
  testForSecondSolution()
