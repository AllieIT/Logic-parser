# Logic Parser

This project was created to parse logical expressions to evaluate their value and analyze their properties, such as satisfiability, etc. It can also check if the expression is a tautology, non-satisfiable, or if an expression is a logical consequence of another expression. 

# Installation

This program doesn't use any external packages. Only requirement is Python installed on your device.

# Usage and working principle

LogicEvaluator performs basic operation on logical expressions. To use it, create an object, which will automatically initialize needed data. There are several methods, which can be of use while dealing with logical expressions:

- `are_equal` method takes any number of string expressions as parameters and checks if they are equivalent
- `is_tautology` method checks if an expression is True for all possible interpretations
- `is_satisfiable` method checks if expression is satified for at least one interpretation
- `is_logical_consequence` method checks if second given parameter is a logical consequence of the first parameter

Evaluator works using the RPN (Reverse Polish Notation) algorithm, which preserves order of operations. It also uses automatic variable detection (which can only be one-letter symbols).
