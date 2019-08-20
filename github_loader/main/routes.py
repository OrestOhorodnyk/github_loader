from flask import render_template, request, Blueprint, session
from flask_paginate import Pagination, get_page_args
from github_loader.users.utils import get_user_public_repos, paginate_repos
import pickle

main = Blueprint('main', __name__)


@main.route("/home")
def home():
    github_user = pickle.loads(session['github_user'])
    repos = get_user_public_repos(user=github_user)
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    sorted_by_date = sorted(repos, key=lambda k: k['date'], reverse=True)
    pagination_repos = paginate_repos(repos=sorted_by_date, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, total=len(repos), per_page_parameter=per_page, css_framework='bootstrap4')

    return render_template(
        template_name_or_list='home.html',
        title='Home',
        repos=pagination_repos,
        page=page,
        per_page=per_page,
        pagination=pagination,
        repos_all=repos
    )


@main.route("/about")
def about():
    return render_template('about.html', title='About')
