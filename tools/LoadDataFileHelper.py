from pathlib import Path

def get_data_file(filename):
    """
    Returns the absolute path of a file inside the 'data' folder.
    This function resolves the path relative to the project root directory.
    """
    # Get the project root directory
    project_root = Path(__file__).resolve().parents[1]
    
    # Build the full path to the 'data' folder and the requested file
    data_path = project_root / "data" / filename
    
    # Return the path (you can use it to open or process the file)
    return data_path