### Guided tour of debugger actions using simple function calls.

# Continue / Pause (F5)
# Continue → Resume normal execution until next breakpoint.
# Pause → Inspect current line and debug line‑by‑line.

# Step Over (F10)
# Execute the current line without entering called functions.

# Step Into (F11)
# Enter the called function and debug it line‑by‑line.
# If there are no function calls on the current line, behaves like Step Over.

# Step Out (Shift+F11)
# Finish the current function and return to the caller.

# Restart (Ctrl+Shift+F5)
# Stop execution and start debugging again with the same configuration.

# Stop (Debugging)
# Terminate the current program execution.


def a(x):
    y = x + 1  # 3: Step Over
    z = b(y)  # 4: Step Into.10: Step Over
    return z * 2  # 11: Step Over


def b(v):
    w = v * 3  # 5: Step Over
    q = c(w)  # 6: Step Into. 8: in debug console check q, then Step Over
    return q - 4  # 9: Step Out


def c(k):
    return k + 10  # 7: inspect call stack, then Step Out


result = a(5)  # 1: Breakpoint, 2: Step Into, 12: Step over
print(result)  # 13: Continue
