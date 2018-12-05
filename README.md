# CS 107 Project 8 -- AI Adventure

**Due: Fri, Dec 14, 5PM**

You specifically **may not** use lag days on this project, as per the
college-level requirements about work into finals week.

In this project you'll be implementing an AI for HaverQuest. The goal
of this project is for you to have fun experimenting on your own while
designing something cool to end the term. If you find yourself writing
over 2-300 lines of code, you're probably working too hard.

The basic goal of your project is to make an AI that can automatically
navigate to the exit tile under a certain set of constraints:

- You are playing the squirrel

- You start with 30 fuel

- Each half-second, you receive 3 more fuel

- To move, you pay 1 fuel

- You can figure out where each of the ferrets on the board if you
  "pay" 5 fuel (of course, they might move)

- You can figure out where the exit tile is if you pay 30 fuel

- You can figure out where each of the health packs are by paying 20
  fuel

- You cannot set the speed (speed is always 0)

- You can only move one tile at a time (but you can move diagonally)

- You can look up the positions of all of the current stones on the
  board for free (without using any fuel)

- You may not manually set the position of any tile or move in a
  discontinuous way

To implement your AI, you will extend the `clockTick` method in
`MyAISquirrel` within the `ai.py` file. If you read what I have
written there right now, you can see an extremely naive AI that does a
random walk: every four times it is called, it picks a random
direction to travel in and walks that way. Every 40 times it is
called, it gets the position of all the ferrets. Every 80 times it is
called, it gets the position of all health packs. Every 160 times it
is called, it gets the location of the exit tile.

This project is meant for you to have fun with and play around with a
bunch of different potential solutions. I recommend the following
solution:

- Wait until you have enough fuel to find the exit, plus some left
  over

- Use your pathfinder solution (if you didn't do this right there's a
  solution in `pathfinder.py`) to figure out how to get to the exit

- Avoid getting hit by a stone

- Try to make sure you don't hit a ferret!

### Use different levels

The game is currently set up to use the single level you see before
you. But I will ask you to demonstrate your AI with different
levels. All of them will be solvable (I will never trick you). But
some may have ferrets placed in different places and use different
maps. To test this, I encourage you to experiment with the
configuration file `config.json`, which specifies the position of the
ferrets and the map to use. Try out some other maps and move the
ferret around. I won't award points to solutions that just hard code
the answers for *some particular* level.

## Functions to Use

- `canMove`, which accepts `x` and `y` in the range `[-1,1]` and tells
  you whether or not you can move to that tile.

- `move`, which accepts `x` and `y` in the range `[-1,1]` and moves to
  that tile using |x| + |y| fuel

- `fireStone(x,y)`, which fires a stone with a set speed along the
  vector `(x * speed, y * speed)`. You don't have any control over
  speed, but x and y must be in the range `[-1,1]`

- `getStones()` will get all the stones on the board fired by the
  ferrets. No fuel used. (Useful for avoiding them!)

- `getFerrets()` will get all the ferrets on the board. Uses 5 fuel

- `getHealthPacks()` will get all the ferrets on the board. Uses 30
  fuel. However, tells you health packs that may have already been
  "used up" (so you need to remember if you want to use them).

- `getFuel()` will return how much fuel you have left.

## Part 1 [30%]: Design Document

For the first part of the assignment, I want you to think about how
you want to solve the project. After doing so, write between 400 and
1500 words in the document (DESIGN) describing your approach at the
solution, using good prose to describe your solution at a high
level. Next, indicate which functions you will use to achieve your
goals and in what orders. To some extent, we will check that this
actually matches what you implement.

## Part 2 [70%]: AI Implementation

This will all occur in the file `ai.py`, and specifically the
`clockTick` method. I invite you to add more methods. Do not break the
rules. If you're doing something that feels like cheating by making
the game easier, please ask first. Don't just hack the game to make it
give you points, that's not taking the assignment seriously and I will
be unhappy if you circumvent the point of thinking about this by doing
something hacky like modifying other files to increase fuel.

I will assign four categories of points (out of 70%):

- Did you even attempt the exercise at all (30%). You at least wrote
  some of your own code, but what you did didn't seem like a good
  faith attempt at building an AI.

- Does your AI do *anything* remotely sensible (55%). This doesn't
  even have to be solving the maze, it just has to be something you
  thought up and can explain.

- Can your AI actually make it to the end of the maze at least some of
  the time (63%). You used the path finder, integrated it into your
  solution, and did something sensible.

- Can your AI make it to the end of the maze basically all the time,
  along with using some intelligence to fire at the ferrets (67%).

- Can your AI make it to the end, get health packs, avoid the stones,
  and fire at the ferrets (70%).

I think *everyone* should be able to get to 63% on this part without
too much work. Just use some logic to wait until you have enough fuel
(say 60) to solve the maze, and then solve it and quickly move there!

### Extra Credit

If you volunteer to demonostrate your solution in class, you will
receive 20% extra credit to use on some previous lab (or the current
one). You tell me which one you want to use it on. You can't "split"
it across labs or anything like that, so please avoid getting to gamey
about it. My only constraint here is that if you want to demo during
class, you have to email me 48 hours ahead of next Thursday's class
time with a video demonstrating your current AI: again, this can be as
rudimentary as you want, it doesn't have to be getting a 70%. But you
can't just decide day of that you want the 20%: it needs to be a
thought out thing. (And yes, this is to encourage you to start early!)

### Grading

I really do want this project to be easyish. I expect everyone to be
able to get a 93%, many student to be able to get 97%, and a few to be
able to get 100%.

Your design document will essentially be completion-based.  To get
your grade for the second part, you will either (a) find me and
demonstrate your solution or (b) make a video and show me.

### Strategic Advice

Do the simple thing first. I think you can figure a path through the
level without too much work, that part should be easy, which will get
you a 63% on that part off the bat.
