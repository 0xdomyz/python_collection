import subprocess
import pandas as pd

# Run the "query user" command and capture its output
output = subprocess.check_output("query user")

# Convert the output to a string and split it into lines
output_str = output.decode("utf-8")
lines = output_str.split("\n")

# Parse the lines into a list of dictionaries
data = []
for line in lines[1:]:
    fields = line.strip().split()
    if len(fields) == 4:
        username, sessionname, id, state = fields
        data.append(
            {"Username": username, "SessionName": sessionname, "ID": id, "State": state}
        )

# Convert the list of dictionaries to a Pandas DataFrame
df = pd.DataFrame(data)

# Print the DataFrame
print(df)
