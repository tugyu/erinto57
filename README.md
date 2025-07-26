# erinto57
A Mathematical Puzzle Solved with AI Collaboration
This repository contains the solution to a fascinating mathematical puzzle, developed through a process of collaboration with AI. The project demonstrates how targeted human guidance can enable AI to solve complex problems that it might otherwise fail to address efficiently.
# The Problem
The task is to determine if it's possible to form a special 3x3 grid, a semi-magic square, where only the row and column sums are required to be equal using numbers generated from permutations of the digits 1, 2, 3, 4, and 5.
# Solution
I have not seen any AI solving this problem alone, without further help, neither being capable to generate a code finding all solutions using realistic time & resource
I had to instruct AI how to approach to the problem. A working approach is attached
# Solution Approach
The Python script in this repository implements an efficient, heuristic-based approach to find all fundamental solutions. The strategy is as follows:
Generate Numbers: Create the complete list of 120 unique 5-digit numbers from permutations of {1, 2, 3, 4, 5}.
Pre-calculate Triplets: Instead of checking grids, first calculate the sum of every possible combination of three distinct numbers from the list. Group these triplets by their sum.
Find Candidate Rows: A valid 3x3 grid must have three rows that are disjoint (contain no common numbers) but share the same sum. The algorithm searches for a "magic sum" that has at least three such disjoint triplets associated with it.
Construct and Verify: For each set of 9 candidate numbers (forming three potential rows), the algorithm attempts to arrange them in a grid. It permutes the second and third rows to find an arrangement where the column sums also match the magic sum.
Identify Fundamental Solutions: A single solution can be varied by swapping rows and columns or by transposing the grid. To count only unique solutions, the program generates a "canonical key" for each valid grid. Only grids with a new, unseen key are counted as a new fundamental solution.
# Results
The program successfully finds all solutions to the puzzle.
# A Note on the AI Collaboration Journey
This project also served as an interesting case study on the capabilities and limitations of modern AI models for complex problem-solving.
My experience showed that:
Without specific guidance, most AI models (including free and premium versions like Gemini Pro) struggled answer the question or to produce a working code giving all solutions that could finish in a realistic time.
The key to success was providing the AI with the crucial heuristic: the strategy of pre-calculating triplet sums. Once this human-devised strategy was provided, the AI was highly effective at translating the logic into efficient and correct Python code.
This highlights that while AI is a powerful tool for code generation, human insight, strategic thinking, and a deep understanding of the problem domain remain indispensable for tackling novel and complex challenges.
