from sqlalchemy import select, func
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required

from . import bp_views as bp
from app.app import db
from app.models import Entry
from .forms import EntryForm, EntriesForm


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/create-entry', methods=('GET', 'POST'))
@login_required
def create_entry():
    form = EntryForm()
    if request.method == 'POST' and form.validate_on_submit():
        content = form.content.data
        user_id = current_user.id

        new_entry = Entry(content, user_id)
        db.session.add(new_entry)
        db.session.commit()
        flash('Entry has been added.', 'success')
        return redirect(url_for('bp_views.index'))
    
    return render_template('create-entry.html', form=form)


@bp.route('/entries', methods=('GET', 'POST'))
@login_required
def entries():
    form = EntriesForm()
    
    e_years = func.extract('year', Entry.timestamp).label(None)
    q_years = select(e_years).distinct()
    years = db.session.scalars(q_years).all()

    months_dict = {
        1:'January',2:'February',3:'March',4:'April',5:'May',6:'June',
        7:'July',8:'August',9:'September',10:'October',11:'November',12:'December'
    }

    form.year.choices = [year for year in years]
    form.month.choices = [(k,v) for k,v in months_dict.items()]

    q = (select(
            Entry
        )
        .where(Entry.user_id == current_user.id)
        .order_by(Entry.timestamp))

    if request.method == 'POST' and form.validate_on_submit():
        year = form.year.data
        month = form.month.data

        year_extract = func.extract('year', Entry.timestamp).label(None)
        month_extract = func.extract('month', Entry.timestamp).label(None)

        q = (select(
            Entry
        )
        .where(Entry.user_id == current_user.id)
        .group_by(Entry)
        .having(year_extract == year, month_extract == month)
        .order_by(Entry.timestamp))

        print(month, year)

        entries = db.session.scalars(q).all()

        return render_template('entries.html', form=form, entries=entries)

    all_entries = db.session.scalars(q).all()
    return render_template('entries.html', form=form, entries=all_entries)