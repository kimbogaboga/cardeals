from cardealsapp import app

from cardealsapp.controllers import user_controllers, car_controllers

if __name__=="__main__":
    app.run(debug=True)