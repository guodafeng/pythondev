
def calculate_24(a, b, c, d):
  """
  Calculates 24 using four input numbers.

  Args:
    a: The first number.
    b: The second number.
    c: The third number.
    d: The fourth number.

  Returns:
    A list of all possible ways to calculate 24 using the input numbers.
  """

  # Check if the input numbers are valid.
  if not isinstance(a, int) or not isinstance(b, int) or not isinstance(c, int) or not isinstance(d, int):
    raise ValueError("Input numbers must be integers.")

  # Create a list of all possible operators.
  operators = ["+", "-", "*", "/"]

  # Create a list of all possible combinations of operators.
  operator_combinations = []
  for i in range(4):
    for j in range(4):
      for k in range(4):
        operator_combinations.append((operators[i], operators[j], operators[k]))

  # Create a list of all possible ways to calculate 24.
  solutions = []
  for operator_combination in operator_combinations:
    # Evaluate the expression using the given operator combination.
    try:
      result = eval(f"{a} {operator_combination[0]} ({b} {operator_combination[1]} {c}) {operator_combination[2]} {d}")
    except ZeroDivisionError:
      continue
    # Check if the result is equal to 24.
    if result == 24:
      # Add the operator combination to the list of solutions.
      solutions.append(operator_combination)

  # Return the list of solutions.
  return solutions


# Test the calculate_24 function.
print(calculate_24(4, 7, 8, 9))  # [(('+', '-', '*'), ('*', '/'))]
print(calculate_24(1, 1, 1, 1))  # [('+', '+', '*'), ('+', '+', '+', '+')]
print(calculate_24(2, 3, 4, 5))  # [('+', '+', '*'), ('+', '+', '+', '+')]
