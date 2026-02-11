# CS480 – Module 3 Assignment
Informed Search (24-Puzzle)  
Author: Donnel Garner  
Date: 02/12/2026  

This program solves the 24-Puzzle (5x5 sliding tile puzzle) using A* informed search, which combines Uniform Cost Search and Greedy Best-First Search to maximize the advantages and minimize disadvantages.  

To run with output in the terminal:  
- Run python3 HW1_InformedSearch.py  
- The program will direct you from there.  
	
INITIAL SET: 2,11,0,4,5,6,1,3,9,12,8,19,13,7,10,18,17,14,15,20,16,21,22,23,24  
SOLUTION SET: 1,2,3,4,5,6,7,8,9,10,11,12,14,18,15,16,17,13,19,20,21,22,23,0,24  
BEST SET FOR COMPARISON: 2,3,4,5,10,1,7,8,9,15,6,12,13,14,20,11,17,18,19,24,16,21,22,23,0  

WEBSITE: N/A  
GOOGLE COLAB: N/A  
GITHUB: https://github.com/skyelogic/cs480-informedsearch  

## INTRODUCTION

The user can select between two admissible heuristics:  
1. h1(x): Number of misplaced tiles  
2. h2(x): Sum of Manhattan distances of each tile to its goal position  

The program:  
- Accepts user input as a comma-separated list  
- Verifies solvability  
- Uses A* search  
- Avoids revisiting states  
- Outputs performance statistics  
- Optionally prints intermediate states  

## h1 – Misplaced Tiles

Counts the number of tiles not in their goal position (excluding the blank).

Properties:  
- Admissible  
- Consistent  
- Simpler but less informed  

## h2 – Manhattan Distance 

Computes the sum of horizontal and vertical distances of each tile from its goal position.

Properties:  
- Admissible  
- Consistent  
- More informed than h1  
- Expands fewer nodes in most cases  

## ALGORITHM USED 
The program uses A* search.  

Evaluation function:  
		f(n)=g(n)+h(n)

Where:  
g(n) = cost from start to node  
h(n) = heuristic estimate to goal

The implementation includes:  
- Priority queue (min-heap)  
- Best-cost dictionary (closed set)  
- Avoids immediate backtracking  
- Solvability check using inversion count  


## Heuristic Comparison

| Metric   | h1 (Misplaced) | h2 (Manhattan) |
|--------|-----|---------|
| Accuracy | Low  | Higher     |
| Nodes Expanded   | More  | Fewer     |
| Time | Slower  | Faster     |
| Informedness   | Weak  | Strong     |

Conclusion:  
Manhattan distance (h2) generally performs better because it provides a more accurate estimate.  


## REFERENCES 
Russell & Norvig, Artificial Intelligence: A Modern Approach  
https://code.claude.com/docs/en/overview
https://code.visualstudio.com/
