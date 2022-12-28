import sys
from io import StringIO

# Define the code to execute
code = """
print("Hello, world!")
a = 5
b = 10
c = a + b
print(c)
"""

# Redirect the standard output to a string buffer
old_stdout = sys.stdout
sys.stdout = StringIO()

# Execute the code
exec(code)

# Retrieve the output from the string buffer
output = sys.stdout.getvalue()

# Reset the standard output
sys.stdout = old_stdout

# Print the output
print(output) 