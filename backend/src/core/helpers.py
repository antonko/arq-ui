def join_paths_safely(base_path: str, relative_path: str) -> str:
    """
    Joins a base path and a relative path safely, ensuring only one slash between them.
    
    This function ensures that there's exactly one slash between the base and relative paths,
    regardless of whether the base path ends with a slash or the relative path starts with one.
    
    Parameters:
    base_path (str): The base path to be joined.
    relative_path (str): The relative path to append to the base path.
    
    Returns:
    str: The resulting path after safely joining the base and relative paths.
    
    Examples:
    >>> join_paths_safely('/base/path/', '/relative/path')
    '/base/path/relative/path'
    
    >>> join_paths_safely('/base/path', 'relative/path')
    '/base/path/relative/path'
    """
    # Remove the trailing slash from the base path if it exists, and add a leading slash to the relative path if it's missing
    # Then concatenate the paths
    return base_path.rstrip('/') + '/' + relative_path.lstrip('/')