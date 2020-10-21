# Shufflez
Poker range construction tool

Shufflez is intended to be an intermediate level tool for developing poker strategy.
It has greater functionality than basic Equilab or Flopzilla but is much more accessible
than current solvers such as PioSolver.

Shufflez follows a single poker hand as it was played and the user can select an action
(value, bluff, call) for each hole card combination in their range based on the made hand
or drawing hand it makes.  This will then give the user the frequency at which each
action is taking place, allowing them to find vulnerabilities in their strategy or exploits
in their opponents'.

ShufflezUI.py is the main file to run the program.  It builds the windows of the program

ShufflezWidgets are the widgets that make up the program.  RangeMatrix, RangeStats,
ActionButtons are all here.

test_ShufflezWidgets is unit testing.
