import pickle
import json
import os

def read_file(file_name):
    """
    Read a file and returns the data based on its extension. Supported file
    types: .pkl, .json.

    Returns
    -------
    The data loaded from the file.
    """
    try:
        # Extract file extension.
        _, extn = os.path.splitext(file_name)
        extn = extn.lower()

        # Open and read the file.
        file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', file_name)
        
        if extn == '.pkl':
            with open(file_path, 'rb') as f:
                data = pickle.load(f)
        elif extn == '.json':
            with open(file_path, 'r') as f:
                data = json.load(f)
        else:
            print(f"Unsupported file type: {extn}")
            return None
        
        return data
    
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An exception occured: {e}")
        return None

def write_file(data, file_name):
    """
    Writes data to a file based on its extension. Supported file types:
    .pkl, .json.
    """

    try:
        # Extract file extension.
        _, extn = os.path.splitext(file_name)
        extn = extn.lower()

        # Write the data to the file path.
        file_path = os.path.join('../data', file_name)
        
        if extn == '.pkl':
            try:
                with open(file_path, 'wb') as f:
                    pickle.dump(data, f)
            except RecursionError as e:
                str_data = [str(element) for element in data]

                with open(file_path, 'wb') as f:
                    pickle.dump(str_data, f)
        elif extn == '.json':
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            print(f"Unsupported file type: {extn}")
    except IOError as e:
        print(f"An error occurred while writing to the file path {file_path}: {e}")