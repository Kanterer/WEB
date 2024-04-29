from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

@app.route('/recipes/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    if request.method == 'POST':
        recipe.title = request.form['title']
        recipe.ingredients = request.form['ingredients']
        db.session.commit()
        return redirect(url_for('favorites'))
    return render_template('edit_recipe.html', recipe=recipe)

@app.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return redirect(url_for('favorites'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    db.create_all()
    app.run()
