from flask import render_template, request, redirect, url_for, session

from . import symptom_checker


@symptom_checker.route('/symptoms', methods=['GET', 'POST'])
def symptoms():
    if request.method == 'POST':
        session['symptoms'] = request.form.getlist('symptoms')
        return redirect(url_for('symptom_checker.duration'))

    return render_template('symptom_checker/symptoms.html')


@symptom_checker.route('/duration', methods=['GET', 'POST'])
def duration():
    if request.method == 'POST':
        session['duration'] = request.form.get('duration')
        session['progress'] = request.form.get('progress')
        session['onset'] = request.form.get('onset')

        return redirect(url_for('symptom_checker.information'))

    return render_template('symptom_checker/duration.html')


@symptom_checker.route('/information', methods=['GET', 'POST'])
def information():
    if request.method == 'POST':
        session['previous_experience'] = (
            request.form.get('previous_experience')
        )
        session['medications'] = request.form.get('medications')
        session['medical_conditions'] = (
            request.form.get('medical_conditions')
        )
        session['family_history'] = request.form.get('family_history')
        session['additional_information'] = (
            request.form.get('additional_information')
        )

        return redirect(url_for('symptom_checker.assessment'))

    return render_template('symptom_checker/information.html')


@symptom_checker.route('/assessment')
def assessment():
    return render_template('symptom_checker/assessment.html')