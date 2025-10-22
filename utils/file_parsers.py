def read_lines(filename):
    """Read a file and return a list of lines."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f]