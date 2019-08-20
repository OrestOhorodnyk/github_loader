from flask import render_template, url_for, flash, redirect, Blueprint, session
from flask_login import login_required, current_user
from github_loader.repositories.forms import NewRepoForm
from github_loader.utils.github_helper import create_repo, load_project_to_repo
from github_loader.models import Load
from github_loader import db, LOGGER
from github.GithubException import GithubException
import pickle
from sqlalchemy.exc import SQLAlchemyError, DatabaseError


repositories = Blueprint('repositories', __name__)


@repositories.route("/repositories/new", methods=['GET', 'POST'])
@login_required
def new_repo():
    form = NewRepoForm()
    if form.validate_on_submit():
        github_user = pickle.loads(session['github_user'])
        try:
            repo = create_repo(user=github_user, name=form.repository_name.data, description=form.description.data)
            load_project_to_repo(repo)
        except GithubException as e:
            if e.status == 422:
                flash('Name already exists on this account, please use different name', 'danger')
                LOGGER.error(f"Failed to create repo, user: {current_user.username}, error {e}")
                return render_template(
                    template_name_or_list='create_repo.html',
                    title='Create Repository',
                    form=form,
                    legend='Create Repository'
                )
            else:
                raise e
        load = Load(user_login_id= current_user.id)
        db.session.add(load)
        try:
            db.session.commit()
        except (SQLAlchemyError, DatabaseError) as e:
            LOGGER.error(f"DB error: {e} ")
        flash('The source code of this app has been uploaded to your GutHub!', 'success')
        LOGGER.info(f'New load by user {current_user.username}, login id {current_user.id}')
        return redirect(url_for('main.home'))
    return render_template(
        template_name_or_list='create_repo.html',
        title='Create Repository',
        form=form,
        legend='Create Repository'
    )
