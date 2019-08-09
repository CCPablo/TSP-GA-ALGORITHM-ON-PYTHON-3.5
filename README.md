# TSP GA ALGORITHM ON PYTHON 3.5

Implementation of the problem defined by The Workshop project: (https://github.com/The-Workshop-Inventors-of-play/pepi-challenge)
Citing:
## Game rules:
- Earn points for each city you visit.
- Every city has a reward score, representing the points earned for travelling there.
- Travelling between two connected cities takes up 1 day, and consumes a certain amount of petrol (this amount can be seen as a number along the connecting lines).
- You may travel to the same city several times but the reward can be collected only once.
- Your trip is a week long; the route length can’t exceed the maximum number of days (7).
- Your journey must start and end in Madrid.
- The optimal route is the one that has the highest score, which is calculated by: Total rewards – Total gas. For example, if you only have 5 days, on this super-simple roadmap of Europe the optimal route would be: 
Madrid – London – Paris – Berlin – Rome – Madrid : 152 – 55 = 97
- If two or more routes produce the same score, the optimal route will be the shortest route.

## Challenge rules:
- We challenge you to write an application to find the optimal route given the inputs:
  - A file describing the route map (cities, rewards and connections). Find an example [here](src/test/resources/input/exercise1.json)
  - A maximum duration in days.
- Use whichever coding language you like, and share your solution with us via GitHub.
  - If you’d like to use it, we’ve included an optional scaffold for a Java application (JDK 10 or higher).
- Include a README file explaining how to run the code.
- Present the results in any format (e.g. console output, a formatted file, etc.)
- Your results must include:
  - The cities that make up the optimal route in order of visiting.
  - Total score calculated.
- Solutions will be judged by these criteria:
  - Have you resolved the challenge, and how?
  - Have you applied basic coding & design principles?
  - Is the solution innovative?
  - Have you followed best practices? (extra point)

## NAME

Pablo Caravaca Calvo

## SOLUTION (V0)

![Alt text](evolution.png?raw=true "Title")

Best route path found: Madrid -> Roma -> Berlin -> Paris -> Londres -> Paris -> Madrid

Score: 91

My implementation is based on Python. I have used external libraries: DEAP, NUMPY, MATHPLOTLIB.

## V2

- Added command line arguments. Arguments:
  - JSON file.
  - Trip size
- Changed population first generation (function routeInit()). Now the first individual is partially routed.
- Defined new function for mutation. It generates random links in the route.

With this solution, the algorithm requires much less number of generations and size of population, and is more flexible to find new routes when the algorithm has already found some valid ones.


