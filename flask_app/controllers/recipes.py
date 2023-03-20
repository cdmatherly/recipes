from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
import datetime

@app.route('/recipes/new')
def add_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('new_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if not Recipe.validate(request.form):
        return redirect('/recipes/new')
    Recipe.create_recipe(request.form)
    return redirect('/dashboard')

@app.route('/recipes/<int:recipe_id>')
def show_one(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    logged_user = User.get_user_by_id(session['user_id'])
    recipe = Recipe.get_one(recipe_id)
    print(f"RECIPE >>> {recipe.date}")
    recipe.date = recipe.date.strftime("%B") + " " + recipe.date.strftime("%d") + ", " + recipe.date.strftime("%Y")
    print(f"RECIPE >>> {recipe.date}")
    return render_template('one_recipe.html', user = logged_user, recipe = recipe)

@app.route('/recipes/edit/<int:recipe_id>')
def edit(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    recipe = Recipe.get_one(recipe_id)
    if not session['user_id'] == recipe.user_id:
        return redirect('/dashboard')
    return render_template('edit_recipe.html', recipe = recipe)

@app.route('/recipes/update/<int:recipe_id>', methods=['POST'])
def update(recipe_id):
    if not Recipe.validate(request.form):
        return redirect(f'/recipes/edit/{recipe_id}')
    data = {
        **request.form,
        'id': recipe_id
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/recipes/delete/<int:recipe_id>')
def delete(recipe_id):
    Recipe.delete(recipe_id)
    return redirect('/dashboard')