from github.AuthenticatedUser import AuthenticatedUser
from hurry.filesize import size, verbose


def paginate_repos(repos, offset=0, per_page=4):
    return repos[offset: offset + per_page]


def get_user_public_repos(user: AuthenticatedUser):
    result = []
    for item in user.get_repos():
        if not item.private:
            r = {
                "repo_name": item.name,
                "owner": item.owner.name,
                "size": size(item.size, system=verbose),
                "date": item.pushed_at.date()
            }
            result.append(r)
    result = sorted(result, key=lambda k: k['size'], reverse=True)
    return result
