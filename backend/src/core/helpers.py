def join_paths_safely(base_path: str, relative_path: str) -> str:
    """Joins a base path and a relative path safely, ensuring only one slash between them.

    This function ensures that there's exactly one slash between the base and relative paths,
    regardless of whether the base path ends with a slash or the relative path starts with one.
    """
    return base_path.rstrip("/") + "/" + relative_path.lstrip("/")
