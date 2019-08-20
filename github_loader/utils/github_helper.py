import os
from github.AuthenticatedUser import AuthenticatedUser
from github.Repository import Repository
from github.GithubException import GithubException
from github_loader import LOGGER

project_file_extensions = ['py', 'css', 'html', 'Dockerfile', 'md', 'odt']


def project_files(root: str) -> list:
    """
    :param root: path to the project folder
    :return: list of path's to each file in the project directory
    """
    file_paths = []
    for root, dirs, files in os.walk(root):
        for f in files:
            file__extension = f.split('.')[-1]
            if file__extension in project_file_extensions:
                file_paths.append(os.path.join(root, f))
    return file_paths


def create_repo(
        user: AuthenticatedUser,
        name: str,
        description: str = None,
        is_private: bool = False,
        auto_init: bool = True
) -> Repository:
    """
    This function creates new repository for the user
    :param description:
    :param user: repo will be created for the user account
    :param name: repos name
    :param is_private: True if private and False if public
    :param auto_init: if True repo will be initiated and README.md file will be added to the master branch
     :return: new Repository obj
    """
    try:
        repo = user.create_repo(name=name, description=description, private=is_private, auto_init=auto_init) # create the repository
        contents = repo.get_contents("README.md", ref="master") # get automatically generated README.md file
        repo.delete_file(contents.path, "remove invalid README.md", contents.sha, branch="master") # delete the invalid README.md
    except GithubException as e:
        LOGGER.error(f"Failed to create repository due to error {e}")
        raise e
    LOGGER.info(f"Repository {name} created")
    return repo


def load_project_to_repo(repo: Repository, branch: str = 'master') -> None:
    LOGGER.info(f"Start loading files to the repository {repo.full_name}")
    """
    This method will load project to the repository
    :param repo: user's repo
    :param branch: branch to commit
    """
    try:
        for file_path in project_files(os.getcwd()):
            with open(file_path) as f:
                content = f.read()
            repo_path = file_path.split('app')[-1] # get path to project files
            repo.create_file(path=repo_path[1:], message="initial_commit", content=content, branch=branch)
    except GithubException as e:
        LOGGER.error(f"Failed to load files repository due to error {e}")
    LOGGER.info(f"Files loaded to the repository {repo.full_name}")
