
# find out if I should use the below
# from flask.ext.sqlalchemy import SQLAlchemy



# find out if I should use the below
# db = SQLAlchemy()

# def create_app(config_name):
#     app = Flask(__name__)
    
#     bootstrap.init_app(app)

#     # db.init_app(app)
    
#     from main import main as main_blueprint
#     app.register_blueprint(main_blueprint)
    
#     return app



from flask import Flask, render_template, redirect, request, flash
from flask import session as browser_session
from flask.ext.bootstrap import Bootstrap
import model
from sqlalchemy import desc

bootstrap = Bootstrap()

app = Flask(__name__)
app.secret_key = "ADFLKASDJF"
bootstrap.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")
    # # session = model.connect()
    # print "hello"
    # user_list = db_session.query(model.User).limit(25).all()
    # print user_list
    # return render_template("user_list.html", user_list=user_list)

@app.route("/signup")
def signup_view():
    pass
    # return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup_complete():
    pass
    # email = request.form.get("email")
    # password = request.form.get("password")
    # pass_validation = request.form.get("passwordvalidation")
    # age = request.form.get("age")
    # occupation = request.form.get("occupation")
    # zipcode = request.form.get("zip")

    # if password == pass_validation:
    #     new_user = model.User(email = email, password = password, age = age, occupation = occupation, zipcode = zipcode)
    #     db_session.add(new_user)
    #     db_session.commit()

    # return render_template("welcome.html", occupation=new_user.occupation)

@app.route("/login")
def login_view():
    pass
    # return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_validation():
    pass
    # email = request.form.get("email")
    # password = request.form.get("password")

    # # TODO: Consider what happens if there is more than one user with that email address
    # user = db_session.query(model.User).filter_by(email=email).first()
    # if user.password == password:
    #     browser_session["user"] = user.id
    #     print browser_session
    #     return render_template("welcome.html", occupation=user.occupation)
    # else:
    #     flash("Invalid password.")
    #     return redirect("/login")

@app.route("/user/<int:id>")
def view_user(id):
    pass
    # ratings_list = db_session.query(model.Rating).filter_by(user_id = id).all()
    # print len(ratings_list)
    # return render_template("user.html", ratings_list = ratings_list)


@app.route("/movie/<int:movie_id>")
def view_movie(movie_id): 
    pass
   #  movie = db_session.query(model.Movie).filter_by(id = movie_id).one()
   #  print "MOVIE ID ", movie.id
   #  # browser_session["movies"] = browser_session.setdefault("movies", [])
   #  # # print type(browser_session["movies"])
   #  # browser_session["movies"].append(movie.id)
   #  # print browser_session 
   #  user_has_rated = db_session.query(model.Rating).filter(model.Rating.movie_id == movie_id).filter(model.Rating.user_id == browser_session["user"]).order_by(desc(model.Rating.id)).all()

   # #print user_has_rated.rating
   #  return render_template("movie.html", movie_id = movie_id, user_has_rated = user_has_rated, title=movie.title , release_date=movie.release_date, url=movie.url, browser_session = browser_session)


@app.route("/new/rating", methods=["POST"])
def add_or_update_rating():
    pass
    # movie_id = request.form.get("movie_id")
    # rating_num = request.form.get("rating")
    # user_id = browser_session["user"]

    # if type(rating_num) != int or rating_num < 1 or rating_num > 5:
    #     flash("Rating must be a whole number from 1 to 5.")
    #     return redirect("/movie/%d" % int(movie_id))

    # rating_in_db = db_session.query(model.Rating).filter(model.Rating.movie_id==movie_id).filter(model.Rating.user_id==user_id).all()

    # if rating_in_db == []:
    #     rating = model.Rating(user_id=user_id, movie_id=movie_id, rating=rating_num)
    #     print rating.rating
    #     db_session.add(rating)
    # else:
    #     rating = rating_in_db[0]
    #     rating.rating = rating_num
    #     print rating.rating
    #     db_session.add(rating)

    # db_session.commit()

    # flash("Your rating has been saved!")
    # return redirect("/movie/%d" % rating.movie_id)

if __name__ == "__main__":
    app.run(debug=True)