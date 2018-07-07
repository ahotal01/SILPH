import webapp2, cgi, jinja2, os, re
from google.appengine.ext import db
from datetime import datetime
import hashutils

# set up jinja
template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

# a list of pages that anyone is allowed to visit
# (any others require logging in)
allowed_routes = [
    "/login",
    "/logout",
    "/register"
    "/rules_faq"
    "/guide"
]

class Team(db.Model):
    """ Represents a user on our site """
    teamname = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    members = db.StringProperty(required = True)
    discords = db.StringProperty(required = True)

class Movie(db.Model):
    """ Represents a movie that a user wants to watch or has watched """
    title = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    watched = db.BooleanProperty(required = True, default = False)
    datetime_watched = db.DateTimeProperty()
    rating = db.StringProperty()
    owner = db.ReferenceProperty(User, required = True)


class Handler(webapp2.RequestHandler):
    """ A base RequestHandler class for our app.
        The other handlers inherit form this one.
    """

    def renderError(self, error_code):
        """ Sends an HTTP error code and a generic "oops!" message to the client. """
        self.error(error_code)
        self.response.write("Oops! Something went wrong.")

    def login_user(self, team):
        """ Logs in a user specified by a Team object """
        team_id = team.key().id()
        self.set_secure_cookie('team_id', str(team_id))

    def logout_user(self):
        """ Logs out the current user """
        self.set_secure_cookie('team_id', '')

    def read_secure_cookie(self, name):
        """ Returns the value associated with a name in the user's cookie,
            or returns None, if no value was found or the value is not valid
        """
        cookie_val = self.request.cookies.get(name)
        if cookie_val:
            return hashutils.check_secure_val(cookie_val)

    def set_secure_cookie(self, name, val):
        """ Adds a secure name-value pair cookie to the response """
        cookie_val = hashutils.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))

    def initialize(self, *a, **kw):
        """ Any subclass of webapp2.RequestHandler can implement a method called 'initialize'
            to specify what should happen before handling a request.

            Here, we use it to ensure that the user is logged in.
            If not, and they try to visit a page that requires an logging in (like /ratings),
            then we redirect them to the /login page
        """
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('team_id')
        self.team = uid and Team.get_by_id(int(uid))

        if not self.team and self.request.path not in allowed_routes:
            self.redirect('/login')
            return

    def get_team_by_name(self, teamname):
        """ Given a teamname, try to fetch the user from the database """
        team = db.GqlQuery("SELECT * from teams WHERE teamname = '%s'" % teamname)
        if team:
            return team.get()


class Index(Handler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.flicklist.com/
    """
    def get(self):
        t = jinja_env.get_template("puzzles.html")
        response = t.render()
        self.response.write(response)

"""
class AddMovie(Handler):
    # Handles requests coming in to '/add'
        e.g. www.flicklist.com/add

    def post(self):
        # User wants to add a new movie to their list

        new_movie_title = self.request.get("new-movie")

        # if the user typed nothing at all, redirect and yell at them
        if (not new_movie_title) or (new_movie_title.strip() == ""):
            error = "Please specify the movie you want to add."
            self.redirect("/?error=" + cgi.escape(error))
            return

        # if the user wants to add a terrible movie, redirect and yell at them
        if new_movie_title in terrible_movies:
            error = "Trust me, you don't want to add '{0}' to your Watchlist.".format(new_movie_title)
            self.redirect("/?error=" + cgi.escape(error, quote=True))
            return

        # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
        new_movie_title_escaped = cgi.escape(new_movie_title, quote=True)

        # construct a movie object for the new movie
        movie = Movie(title = new_movie_title_escaped, owner = self.user)
        movie.put()

        # render the confirmation message
        t = jinja_env.get_template("add-confirmation.html")
        response = t.render(movie = movie)
        self.response.write(response)


class WatchedMovie(Handler):
    # Handles requests coming in to '/watched-it'
        e.g. www.flicklist.com/watched-it

    def post(self):
        # User has watched a movie.
        watched_movie_id = self.request.get("watched-movie")
        watched_movie = Movie.get_by_id( int(watched_movie_id) )

        # if we can't find the movie, reject.
        if not watched_movie:
            self.renderError(400)
            return

        # update the movie object to say the user watched it at this date in time
        watched_movie.watched = True
        watched_movie.datetime_watched = datetime.now()
        watched_movie.put()

        # render confirmation page
        t = jinja_env.get_template("watched-it-confirmation.html")
        response = t.render(movie = watched_movie)
        self.response.write(response)


class MovieRatings(Handler):
    # Handles requests coming in to '/ratings'

    def get(self):
        # Show a list of the movies the user has already watched

        # query for movies that the current user has already watched
        query = Movie.all().filter("owner", self.user).filter("watched", True)
        watched_movies = query.run()

        t = jinja_env.get_template("ratings.html")
        response = t.render(movies = watched_movies)
        self.response.write(response)

    def post(self):
        # User wants to rate a movie

        rating = self.request.get("rating")
        movie_id = self.request.get("movie")

        movie = Movie.get_by_id( int(movie_id) )

        if movie and rating:
            # update the rating of the movie object
            movie.rating = rating
            movie.put()

            # render confirmation
            t = jinja_env.get_template("rating-confirmation.html")
            response = t.render(movie = movie)
            self.response.write(response)
        else:
            self.renderError(400)


class RecentlyWatchedMovies(Handler):
    # Handles requests coming in to '/recently-watched'


    def get(self):
        # Display a list of movies that have recently been watched (by any user)

        # query for watched movies (by any user), sorted by how recently the movie was watched
        query = Movie.all().filter("watched", True).order("-datetime_watched")
        # get the first 20 results
        recently_watched_movies = query.fetch(limit = 20)

        # TODO 4
        # Replace the code below with code that renders the 'recently-watched.html' template
        # Don't forget to pass recently_watched_movies over to your template.

        t = jinja_env.get_template("recently-watched.html")
        response = t.render(movies = recently_watched_movies)
        self.response.write(response)
"""

class Login(Handler):

    def render_login_form(self, error=""):
        t = jinja_env.get_template("login.html")
        response = t.render(error=error)
        self.response.write(response)

    def get(self):
        """ Display the login page """
        self.render_login_form()

    def post(self):
        """ User is trying to log in """
        submitted_teamname = self.request.get("teamname")
        submitted_password = self.request.get("password")

        team = self.get_team_by_name(submitted_teamname)
        if not team:
            self.render_login_form(error = "Invalid teamname")
        elif not hashutils.valid_pw(submitted_teamname, submitted_password, team.pw_hash):
            self.render_login_form(error = "Invalid password")
        else:
            self.login_user(team)
            self.redirect("/teampage")


class Logout(Handler):

    def get(self):
        """ User is trying to log out """
        self.logout_user()
        self.redirect("/rules_faq")


class Register(Handler):

    def validate_teamname(self, teamname):
        """ Returns the teamname string untouched if it is valid,
            otherwise returns an empty string
        """
        TEAM_RE = re.compile(r"^[a-zA-Z0-9_-]{3,25}$")
        if TEAM_RE.match(teamname):
            return teamname
        else:
            return ""

    def validate_password(self, password):
        """ Returns the password string untouched if it is valid,
            otherwise returns an empty string
        """
        PWD_RE = re.compile(r"^.{3,20}$")
        if PWD_RE.match(password):
            return password
        else:
            return ""

    def validate_verify(self, password, verify):
        """ Returns the password verification string untouched if it matches
            the password, otherwise returns an empty string
        """
        if password == verify:
            return verify
        else:
            return ""

    def validate_members(self, members):
        """ Returns the members string untouched if it is valid,
            otherwise returns an empty string
        """
        MBS_RE = re.compile(r"^[-\w\s]+(?:,[-\w\s]+)+{3,150}$")
        if MBS_RE.match(members):
            return members
        else:
            return ""

    def validate_discords(self, discords):
        """ Returns the discords string untouched if it is valid,
            otherwise returns an empty string
        """
        DCS_RE = re.compile(r"^[-\w\s]+(?:,[-\w\s]+)+{11,200}$")
        if DCS_RE.match(discords):
            return discords
        else:
            return ""

    def validate_verify2(self, members, discords):
        """ Returns 'SPH' if they contain the same number of elements,
            otherwise returns an empty string
        """
        mems_list = members.split(",")
        disc_list = discords.split(",")
        if len(mems_list) == len(disc_list):
            return "SPH"
        else:
            return ""

    def get(self):
        """ Display the registration page """
        t = jinja_env.get_template("register.html")
        response = t.render(errors={})
        self.response.out.write(response)

    def post(self):
        """ User is trying to register """
        submitted_teamname = self.request.get("teamname")
        submitted_password = self.request.get("password")
        submitted_verify = self.request.get("verify")
        submitted_members = self.request.get("members")
        submitted_discords = self.request.get("discords")

        teamname = self.validate_teamname(submitted_teamname)
        password = self.validate_password(submitted_password)
        verify = self.validate_verify(submitted_password, submitted_verify)
        members = self.validate_members(submitted_members)
        discords = self.validate_discords(submitted_discords)
        verify2 = self.validate_verify2(submitted_members, submitted_discords)

        errors = {}
        existing_team = self.get_team_by_name(teamname)
        has_error = False

        if existing_team:
            errors['teamname_error'] = "A team with that name already exists"
            has_error = True
        elif (teamname and password and verify and members and discords and verify2):
            # create new user object
            pw_hash = hashutils.make_pw_hash(teamname, password)
            team = Team(teamname=teamname, pw_hash=pw_hash)
            team.put()

            self.login_user(team)
        else:
            has_error = True

            if not teamname:
                errors['teamname_error'] = "That's not a valid teamname"

            if not password:
                errors['password_error'] = "That's not a valid password"

            if not verify:
                errors['verify_error'] = "Passwords don't match"

            if not members:
                errors['members_error'] = "That's not a valid list of members"

            if not discords:
                errors['discords_error'] = "That's not a valid list of discord tags"

        if has_error:
            t = jinja_env.get_template("register.html")
            response = t.render(teamname=teamname, errors=errors)
            self.response.out.write(response)
        else:
            self.redirect('/teampage')


class Credits(Handler):

    def get(self):
        t = jinja_env.get_template("credits.html")
        response = t.render()
        self.response.write(response)


class Guide(Handler):

    def get(self):
        t = jinja_env.get_template("guide.html")
        response = t.render()
        self.response.write(response)


""" TODO: Do it this way when making leaderboard
class Teams(Handler):

    def get(self):
        if
        t = jinja_env.get_template("leaderboard.html")
        response = t.render()
        self.response.write(response)
"""
class Leaderboard(Handler):

    def get(self):
        t = jinja_env.get_template("leaderboard.html")
        response = t.render()
        self.response.write(response)


class RulesFAQ(Handler):

    def get(self):
        t = jinja_env.get_template("rules_faq.html")
        response = t.render()
        self.response.write(response)


class Teampage(Handler):
    def get(self):
        team = Team.filter()

        t = jinja_env.get_template("teampage.html")
        response = t.render(team = team)
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/credits', Credits),
    ('/guide', Guide),
    ('/leaderboard', Leaderboard),
    ('/rules_faq', RulesFAQ),
    ('/teampage', Teampage),
    ('/login', Login),
    ('/logout', Logout),
    ('/register', Register)
], debug=True)
