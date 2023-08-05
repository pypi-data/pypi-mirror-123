import os
import sys
import glob
import warnings
from copy import deepcopy
import itertools


def _create_text_file(dir_name, path):
    """Creates a text file inside the directory of the same name.

    :param dir_name: Name of the subdirectory.
    :param path: Path where the text file must be created.
    """
    file_name = path + "/" + dir_name + ".txt"
    with open(file_name, "w") as file:
        file.write(dir_name)


def _create_path_from_param(dir_name, path):
    """Returns the path based upon the parameters passed.

    :param dir_list: Name of the subdirectory.
    :param path: Path where the root directory needs to be created.

    :returns final_path: The final path to the subdirectory.
    """

    if not path:
        warnings.warn("Path not provided. This will create multiple folders in unexpected location!")
        response = input("Do you wish to continue?[y/n]: ")

        if response == 'y':
            final_path =  dir_name
            return final_path
        else:
            sys.exit(1)
    else:
        final_path = path + "/" + dir_name
        return final_path


def _sub_dir_files(dir_name):
    """Returns a list of the files in the given directory

    :param dir_name: Name of the directory where the text files are stored.

    :returns file_path: List of all the files present in `dir_name`
    :returns file_list: List of all the file titles present in `dir_name`

    :raises ValueError: Invalid input.
    """
    try:
        file_path = [f for f in glob.glob(dir_name + "**/*txt", recursive=True)]

        file_list = [f.rsplit('.',3)[0] for f in os.listdir(dir_name) if f.endswith('.txt')]
    except ValueError as e:
        print(e)
        raise

    return file_path, file_list

def _create_directories(sub_dir_list, path="", with_text=False):
    """Creates set of directory from the list.
    :param sub_dir_list: List of the subdirectory.
    :param path: Path to store the subdirectories.
    :param with_text: Boolean that makes a text file with the subdirectory name. (Default=False)
    """
    for sub_dir in sub_dir_list:
        dir = _create_path_from_param(sub_dir, path)
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
                if with_text:
                    _create_text_file(sub_dir, dir)
            else:
                print(f"Directory: {dir} already exists!")
        except TypeError as e:
            print(e)
            raise

def create_directories_from_text(sub_dir_names, path="", with_text=False):
    """Creates the sub directories inside a directory.

    :param sub_dir_names: A text file with the list of the sub directories.
    :param path: The file path to create the subdirectories from ``sub_dir_list``  (Default="").
    :param with_text: Boolean that makes a text file with the subdirectory name. (Default=False)

    :raises TypeError: Missing positional arguments.

    :Example:

    >>> import autodirs
    >>> autodirs.create_directories_from_text(sub_dir_names="sample", path="sample_directories")
    """

    with open(sub_dir_names) as f:
        sub_dir_list = f.read().splitlines()

    _create_directories(sub_dir_list, path, with_text)


def group_by_text_files(text_path, path="", with_text=False):
    """Creates directory structure to the set path from a group of text files.
    The `text_path` file name forms the directory in the root of the `path`.
    The list inside the text files form the sub directories.

    :param text_path: path where the text files are located.
    :param path: path where the directories must be created.
    :param with_text: Boolean that makes a text file with the subdirectory name. (Default=False)

    :Example:

    >>> import autodirs
    >>> autodirs.group_by_text_files(text_path="text_path", path="sample_directories")
    """

    file_path, file_heading = _sub_dir_files(text_path)

    for (file, heading) in zip(file_path, file_heading):
        with open(file) as f:
            sub_dir_list = f.read().splitlines()

        final_path = path + "/" + heading
        _create_directories(sub_dir_list, final_path, with_text)


def create_directories_from_list(dir_list, path="", with_text=False):
    """Creates directory structure from the list provided.

    :param dir_list: List of the subdirectories.
    :param path: Path where the file structure must be created.
    :param with_text: Boolean that makes a text file with the subdirectory name. (Default=False)

    :Example:

    >>> import autodirs
    >>> foo = ["bar", "baz"]
    >>> autodirs.create_directories_from_list(dir_list=foo, path="sample_directories")
    """
    _create_directories(dir_list, path, with_text)


def dir_path_list(dirs, root_path='', list_dir=None):
    """Generates a list of all the directory paths from the dirs dictionary

    :param dirs: A dictionary of complex directory structure where the last directory's key has a value of an empty list.
    :param root_path: A root path where the directory structure must be created. (Default='')
    :param list_dir: A list that is None and not yet assigned.

    :returns list_dir: A list of all the directory paths.

    :Example:

    >>> import autodirs
    >>> foo_dict = {'sub1': {'sub1_sub1': [], 'sub1_sub2': []}, 'sub2': {'sub2_sub1': []}, 'sub3': []}
    >>> foo_list = autodirs.dir_path_list(foo_dict, root_path='main')
    >>> print(foo_list)
    ['main/sub1/sub1_sub1', 'main/sub1/sub1_sub2', 'main/sub2/sub2_sub1', 'main/sub3']
    """

    # Makes a deepcopy of root_path into path variable to use in further operations.
    path = deepcopy(root_path)

    # Creating an empty list only if there is nothing inside yet.
    # Make sure it executes once in the beginning and remembers all the appended strings.
    if list_dir is None:
        list_dir = []

    for k, v in dirs.items():
        dir_path = os.path.join(path, k)

        # Checks if the value is a of the type dictionary
        if isinstance(v, dict):
            path = deepcopy(dir_path)

            # Recursive function call
            dir_path_list(v, path, list_dir)
        else:
            list_dir.append(dir_path)

        # Again copying the root path before the next iteration
        path = deepcopy(root_path)

    return list_dir

def create_dirs_from_dict(dir_dict, root_path=''):
    """Creates a directory structure followed by the directory structure.

    :param dir_dict: Dictionary of dictionaries that suggest the directory structure.
    :param root_path: Path where the directories must be created.

    :Example:

    >>> import autodirs
    >>> dir_dict = {'sub1': {'sub1_sub1': [], 'sub1_sub2': []}, 'sub2': {'sub2_sub1': []}, 'sub3': []}
    >>> autodirs.create_dirs_from_dict(dir_dict)
    """
    dir_list = dir_path_list(dir_dict, root_path)

    for dir in dir_list:
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
                print(f"Directory: {dir} created!")
            else:
                print(f"Directory: {dir} already exists!")
        except TypeError as e:
            print(e)
            raise

class Node:
    """A class to create a tree node of the directories.

    :param dir: Name of the directory.
    """
    def __init__(self, dir):
        """Constructs all the necessary attributes for the Node object.

        :param dir: Name of the directory.
        """
        # Removing white spaces
        self.dir = dir.strip()

        # Finding the levels by calculating the empty spaces in indentation
        self.level = len(dir) - len(dir.lstrip())

        self.children = []

    def add_children(self, children):
        """Takes a list of child node which are instance of Node class.
        :param children: A list of child nodes of class Node.
        """
        child_level = children[0].level
        # loop over while list is not empty
        while children:
            child = children.pop(0)

            # Add node as a child
            if child.level == child_level:
                self.children.append(child)

            # Add nodes as grandchildren of the last
            elif child.level > child_level:
                children.insert(0, child)
                self.children[-1].add_children(children)

            # Sibling node and no more children
            elif child.level <= self.level:
                children.insert(0, child)
                return

    def as_path(self):
        """Creates a path of all the parent and child in the tree data structure.

        :return: A list of directory paths.
        """

        if len(self.children) >= 1:
            return [self.join_paths(dir=self.dir, sub=child.as_path()) for child in self.children]
        else:
            return [[self.dir]]

    def join_paths(self, dir, sub):
        """Takes a string and a list and makes a list.
        :param dir: The parent Node with the dir attribute.
        :param sub: A list of list containing all the child subdirectory.

        :return paths: A list of all the paths in the directory structure.
        """
        paths = []

        # Combining all the sub-lists to one list
        sub = list(itertools.chain.from_iterable(sub))

        # creating path for every child with parent node.
        for s in sub:
            paths.append(os.path.join(dir, s))

        return paths

    def get_path(self):
        """Organises all the paths into one list"""
        path = self.as_path()
        all_path = list(itertools.chain.from_iterable(path))
        return all_path

def create_nested_dirs_from_text(text, root_path='root'):
    """Creates a complex directory structure from a text file.

    :param text: Path to the text file. (Example: ``example_text_file.txt``)
    :root_path: Path where the directories must be created.

    :Example:

    >>> import autodirs
    >>> autodirs.create_nested_dirs_from_text(text='textfile.txt', root_path='root')
    """

    try:
        with open(text) as f:
            dirs = f.read().splitlines()
    except Exception as e:
        print(e)
        raise

    # Creates a root node
    root = Node(root_path)

    # Adds all the children to the root node
    root.add_children([Node(dir) for dir in dirs if dir.strip()])

    paths = root.get_path()

    for dir in paths:
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
                print(f"Directory: {dir} created!")
            else:
                print(f"Directory: {dir} already exists!")
        except TypeError as e:
            print(e)
            raise
