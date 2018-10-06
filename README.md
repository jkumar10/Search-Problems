# Search-Problems

Part 1: The 16-puzzle (20 pts)
Here's a variant of the 15-puzzle that we studied in class. The game board consists of a 4x4 grid, but with
no empty space, so there are 16 tiles instead of 15. In each turn, the player can either (1) choose a row of
the puzzle and slide the entire row of tiles left or right, with the left- or right-most tile \wrapping around"
to the other side of the board, or (3) choose a column of the puzzle and slide the entire the column up or
down, with the top- or bottom-most tile \wrapping around." For example, here are two moves on such a
puzzle:
1 2 3 4 1 2 3 4 1 14 3 4
5 6 7 8 ! 8 5 6 7 ! 8 2 6 7
9 10 11 12 9 10 11 12 9 5 11 12
13 14 15 16 13 14 15 16 13 10 15 16
The goal of the puzzle is to nd the shortest sequence of moves that restores the canonical conguration (on
the left above) given an initial board conguration. We've written an initial implementation of a program
to solve these puzzles | nd it in your github repository. You can run the program like this:
./solver16.py [input-board-filename]
where input-board-filename is a text le containing a board conguration in a format like:
5 7 8 1
10 2 4 3
6 9 11 12
15 13 14 16
We've included a few sample test boards in your repository. While the program works, the problem is that
it is quite slow for complicated boards. Using this code as a starting point, implement a faster version, using
A* search with a suitable heuristic function that guarantees nding a solution in is few moves as possible.
2
The program can output whatever you'd like, except that the last line of output should be a machine-readable
representation of the solution path you found, in this format:
[move-1] [move-2] ... [move-n]
where each move is encoded as a letter L, R, U, or D for left, right, up, or down, respectively, and a row
or column number (indexed beginning at 1). For instance, the two moves in the picture above would be
represented as:
R2 D4

Part 2: Road trip! (50 pts)

Besides baseball, McDonald's, and reality TV, few things are as canonically American as hopping in the car
for an old-fashioned road trip. We've prepared a dataset of major highway segments of the United States
(and parts of southern Canada and northern Mexico), including highway names, distances, and speed limits;
you can visualize this as a graph with nodes as towns and highway segments as edges. We've also prepared
a dataset of cities and towns with corresponding latitude-longitude positions. These les should be in the
GitHub repo you cloned in step 0. Your job is to implement algorithms that nd good driving directions
between pairs of cities given by the user. Your program should be run on the command line like this:
./route.py [start-city] [end-city] [routing-algorithm] [cost-function]
where:
 start-city and end-city are the cities we need a route between.
 routing-algorithm is one of:
{ bfs uses breadth-rst search (which ignores edge weights in the state graph)
{ uniform is uniform cost search (the variant of bfs that takes edge weights into consideration)
{ dfs uses depth-rst search
{ ids uses iterative deepening search
{ astar uses A* search, with a suitable heuristic function
 cost-function is one of:
{ segments tries to nd a route with the fewest number of \turns" (i.e. edges of the graph)
{ distance tries to nd a route with the shortest total distance
{ time tries to nd the fastest route, for a car that always travels at the speed limit
The output of your program should be a nicely-formatted, human-readable list of directions, including travel
times, distances, intermediate cities, and highway names, similar to what Google Maps or another site might
produce. In addition, the last line of output should have the following machine-readable output about the
route your code found:
[optimal?] [total-distance-in-miles] [total-time-in-hours] [start-city] [city-1] [city-2] ... [end-city]
The rst item on the line, [optimal?], should be either yes or no to indicate whether the program can guar-
antee that the solution found is one with the lowest cost. The reason for this 
ag is that some combinations
of algorithms and cost functions may not guarantee optimality; for example BFS with the segments cost
function will give an optimal answer, but BFS with distance cost function does not. Make sure that A*'s
3
optimality can always be guaranteed (by designing admissible (and potentially also consistent) heuristics for
each cost-function).
Please be careful to follow these interface requirements so that we can test your code properly. For instance,
the last line of output might be:
no 51 1.0795 Bloomington,_Indiana Martinsville,_Indiana Jct_I-465_&_IN_37_S,_Indiana Indianapolis,_Indiana
Like any real-world dataset, our road network has mistakes and inconsistencies; in the example above, for
example, the third city visited is a highway intersection instead of the name of a town. Some of these \towns"
will not have latitude-longitude coordinates in the cities dataset; you should design your code to still work
well in the face of these problems.
In the comment section at the top of your code le, remember to explain your search abstraction (as described
above under What to Do). Be sure to explain the heuristic functions you chose, and why you chose them.
Hints: This problem involves implementing three cost functions and 5 algorithms, so you could solve it by
writing 3  5 = 15 dierent functions. But this is a bad idea! You'll do a lot more work, and it will be hard
to debug and test all of that code. Instead, think about writing your algorithm functions so that they can
handle any of the cost functions; that means you'll need to write just 3+5 = 8 functions instead of 15. Also,
many of the algorithms are very similar; BFS, DFS, uniform and A* are almost the same, but with slightly
dierent uses of data structures. Use this to your advantage to save yourself work!

Part 3: Group assignments (30 pts)

In a hypothetical mid-western university, the sta of a CS course randomly assigns students to project
teams, but does so based on some input from the students. In particular, each student answers the following
questions:
1. What is your user ID?
2. Would you prefer to work alone, in a team of two, in a team of three, or do you not have a preference?
Please enter 1, 2, 3, or 0, respectively.
3. Which student(s) would you prefer to work with? Please list their user IDs separated by commas, or
leave this box empty if you have no preference.
4. Which students would you prefer not to work with? Please list their IDs, separated by commas.
Unfortunately, student preferences often con
ict with one another, so that it is not possible to nd an
assignment that makes everyone happy. Instead, the course sta tries to nd an assignment that will
minimize the amount of work they have to do after assigning the groups. They estimate that:
 They need k minutes to grade each assignment, so total grading time is k times number of teams.
 Each student who requested a specic group size and was assigned to a dierent group size will complain
to the instructor after class, taking 1 minute of the instructor's time.
 Each student who is not assigned to someone they requested will send a complaint email, which will
take n minutes for the instructor to read and respond. If a student requested to work with multiple
people, then they will send a separate email for each person they were not assigned to.
 Each student who is assigned to someone they requested not to work with (in question 4 above) will
request a meeting with the instructor to complain, and each meeting will last m minutes. If a student
4
requested not to work with two specic students and is assigned to a group with both of them, then
they will request 2 meetings.
The total time spent by the course sta is equal to the sum of these components. Your goal is to write a
program to nd an assignment of students to teams that minimizes the total amount of work the course sta
needs to do, subject to the constraint that no team may have more than 3 students. Your program should
take as input a text le that contains each student's response to these questions on a single line, separated
by spaces. For example, a sample le might look like:
djcran 3 zehzhang,chen464 kapadia
chen464 1 _ _
fan6 0 chen464 djcran
zehzhang 1 _ kapadia
kapadia 3 zehzhang,fan6 djcran
steflee 0 _ _
where the underscore character ( ) indicates an empty value. Your program should be run like this:
./assign.py [input-file] [k] [m] [n]
where k, m, and n are values for the parameters mentioned above, and the output of your program should
be a list of group assignments, one group per line, with user names separated by spaces followed by the total
time requirement for the instructors, e.g.:
djcran chen464
kapadia zehzhang fan6
steflee
534
which proposes three groups, with two people, three people, and one person, respectively.
What to turn in
Turn in the three programs on GitHub (remember to add, commit, push) | we'll grade whatever version
you've put there as of 11:59PM on the due date. To make sure that the latest version of your work has
been accepted by GitHub, you can log into the github.iu.edu website and browse the code online. Your
programs must obey the input and output formats we specify above so that we can run them,
and your code must work on the SICE Linux computers. We will provide test programs soon to
help you check this.
Tip: These three problems are very dierent, but they can all be posed as search problems. This means that
if you design your code well, you can reuse or share a lot of it across the three problems, instead of having
to write each one from scratch.
5
