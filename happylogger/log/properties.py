"""Contains properties for the logger, such as file path and line number."""
funcs = []

print_time = True
print_file_path = False
print_file_name = True
print_line_num = True


def add_func(func):
    """
    Add a function to add something in brackets before the contents of the log
    
    :param func: A function that returns a string or something with the  __str__ method
    :type func: function 
    :return: None
    """
    funcs.append(func)


def remove_func(func):
    """
    Remove a function to add something in brackets before the contents of the log
    
    :param func: A function in :var:`log.properties.funcs`
    :return: None
    """
    funcs.remove(func)
