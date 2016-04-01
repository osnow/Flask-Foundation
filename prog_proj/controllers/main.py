from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required

from prog_proj.extensions import cache
from prog_proj.forms import LoginForm
from prog_proj.models import User
import numpy as np
import pandas as pd
import math
import subprocess

main = Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=1000)
def home():
    return render_template('index.html')


@main.route("/submit", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        flash("submitted successfully.", "success")
        psiblast(form)
        subprocess.call(['~/Programming_project_20-02-2016/svm_light/svm_classify','~/Flask-Foundation/prog_proj/svm.txt','~/Programming_project_20-02-2016/Output/Models/modelall_rad',
'~/Programming_project_20-02-2016/Output/Predictions/predictions_web'], shell=True, executable='/bin/bash')

        top = []
        with open('snow@elof05/Programming_project_20-02-2016/Output/Predictions/predictions_web') as f:
            pred = f.readlines()
            for i in pred:
                if i > 0:
                    top.append('M')
                else:
                    top.append('o')

        return form
        return ''.join(top)

    return render_template("login.html", form=form)

def psiblast(matrix):
    subprocess.call(['blastpgp','-j','3','-a','3','-d','~/blast/legacy/db/uniref90.fasta','-i',
    '<input>','-o','~/Programming_project_20-02-2016/output.blastpgp','-Q',
    '~/Flask-Foundation/prog_proj/matrix.psi'], shell=True, executable="/bin/bash")
    makematrix('snow@elof05/Flask-Foundation/prog_proj/matrix.psi')

# function to read matrix file and make svm input file 
def sigmoid(t):
    """converts scores to log odds"""
    return 1/(1+math.exp(-t))

def makematrix(input):
    """converts psiblast PSSM into dataframe"""
    array = np.genfromtxt(input, usecols=range(2,22), skip_header=3, skip_footer=5)
    matrix = pd.DataFrame(array, columns=range(1,21))
    matrix.applymap(sigmoid)
    cols = matrix.columns.values.tolist()
    f = open('snow@elof05/Flask-Foundation/prog_proj/svm.txt', 'w')
    for index, row in matrix.iterrows():
        values = [str(cols[i])+':'+str(row[i+1]) for i in range(0, 20)]
        f.write(' '.join(values)+'\n')
    f.close()



"""@main.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "success")

    return redirect(url_for(".home"))"""


"""@main.route("/restricted")
@login_required
def restricted():
    return "You can only see this if you are logged in!", 200"""
