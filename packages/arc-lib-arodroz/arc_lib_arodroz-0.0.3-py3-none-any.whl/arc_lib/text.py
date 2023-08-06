def strcpy(destination: str, source: str, index: int) -> str:
    """
    Copies the source string to the destination string starting at the index.
    The destination string is automatically expanded to fit the source string.

            Parameters:
                    destination (str): Destination string which will contain the source string
                    source (str): Source string to copy
                    index (int): Position to copy the source string to the destination string
            Returns:
                    result (str): New string
    """
    destination = destination.ljust(index)
    destination = list(destination)
    destination[index : index + len(source)] = source
    result = "".join(destination)
    return result
