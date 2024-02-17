import click
import json


@click.command(
    help="""
    Sort a JSON file by key.
    Example usage: python3 reorder_json.py reorder_json_example.json
    """
)
@click.argument("filename", type=click.Path(exists=True))
def reorder_json(filename):
    # Load the JSON file into a Python object
    with open(filename, "r") as f:
        data = json.load(f)

    # Sort the object by key
    sorted_data = dict(sorted(data.items()))

    # Write the sorted object to a new file
    new_filename = filename.replace(".json", "_sorted.json")
    with open(new_filename, "w") as f:
        json.dump(sorted_data, f, indent=4)  # indent=4 for pretty printing

    click.echo(f"Successfully sorted {filename} and saved as {new_filename}.")


if __name__ == "__main__":
    reorder_json()
