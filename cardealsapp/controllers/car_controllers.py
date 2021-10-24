from flask import render_template,redirect,session,request, flash
from cardealsapp import app
from cardealsapp.models.car import Car
from cardealsapp.models.user import User

@app.route('/new/car')
def new_car():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_car.html',user=User.get_by_id(data))


@app.route('/create/car',methods=['POST'])
def create_car():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Car.validate_car(request.form):
        return redirect('/dashboard')
    data = {
        "price": int(request.form["price"]),
        "model": request.form["model"],
        "make": request.form["make"],
        "year": int(request.form["year"]),
        "description": request.form["description"],
        "seller_id": session["user_id"],
    }
    Car.save(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit.html",car=Car.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/car',methods=['POST'])
def update_car():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Car.validate_car(request.form):
        return redirect('/edit/<int:id>')
    data = {
        "price": int(request.form["price"]),
        "model": request.form["model"],
        "make": request.form["make"],
        "year": int(request.form["year"]),
        "description": request.form["description"],
        "seller_id": session["user_id"],
        "id": request.form['id']
    }
    Car.update(data)
    return redirect('/dashboard')


@app.route('/show/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }  
    return render_template('show.html', user=User.get_by_id(user_data), car = Car.get_one_complete(data))

@app.route('/user/<int:id>')
def mycars(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    return render_template('mypurchases.html', user=User.get_by_id(data), allcars = Car.get_buyer_cars_complete(data))

@app.route('/purchase',methods=['POST'])
def purchase():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "buyer_id":session['user_id'],
        "id": request.form['id']
    } 
    Car.purchase(data)
    return redirect('/dashboard')


@app.route('/destroy/car/<int:id>')
def destroy_car(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Car.destroy(data)
    return redirect('/dashboard')