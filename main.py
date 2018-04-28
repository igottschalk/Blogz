from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:teddy@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y336kGcys&zP3B'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_entry = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, blog_title, blog_entry, owner):
        self.blog_title = blog_title
        self.blog_entry = blog_entry
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'index', 'signup', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()   
        if user and user.password == password:
            session['username'] = username
            flash('Logged in', 'success')
            return redirect('/newpost')
        else:
            flash('User password incorrect, or user does not exist', 'error')      

    return render_template('login.html')

@app.route("/signup", methods=['POST', 'GET'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        username_error = ""
        password_error = ""
        verify_error = ""
        user_error = ""

        existing_user = User.query.filter_by(username=username).first()

        if username == "" or " " in username:
            username_error = "Invalid username"
            #flash('Invalid username', 'error')
            username = ""

        if len(username) < 3 or len(username) > 20:
            username_error = "Invalid username"
            #flash('Invalid username', 'error')
            username = ""

        if len(password) < 3 or len(password) > 20:
            password_error = "Invalid password"
            #flash('Invalid password', 'error')
            password = ""

        if verify != password:
            verify_error = "Passwords do not match"
            #flash('Passwords do not match', 'error')
            verify = ""

        if username == existing_user:
            user_error = "Duplicate user"
            flash('Duplicate user', 'error')
            username = ""

        if not existing_user and not username_error and not password_error and not verify_error and not user_error:   
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['newuser'] = username
            return redirect('/newpost')

        else:
            return render_template('signup.html', username_error=username_error,
                password_error=password_error,
                verify_error=verify_error,
                user_error=user_error,
                username=username,
                password=password,
                verify=verify)   

    return render_template('signup.html')  


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':

        owner = User.query.filter_by(username=session['username']).first()
        blog_title = request.form['blog_title']
        blog_entry = request.form['blog_entry']

        title_error = ""
        entry_error = ""

        if len(blog_title) == 0:
            title_error = "Please fill in the title"

        if len(blog_entry) == 0:
            entry_error = "Please fill in the body"

        if len(title_error) > 0 or len(entry_error) > 0:
            return render_template('newpost.html', title_error=title_error, entry_error=entry_error, blog_title=blog_title, blog_entry=blog_entry)

        new_blog = Blog(blog_title, blog_entry, owner)

        db.session.add(new_blog)
        db.session.commit()
      

        blogs = Blog.query.all()
        blog =  blogs[len(blogs)-1]

        return render_template('blog_post.html', blog=blog) 

    return render_template('newpost.html') 

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/blog')
    #return redirect('/')


# @app.route('/blog', methods=['GET'])
# def blog():
   
#     request_id = request.args.get('id')
#     user_id = request.args.get('user')

    
#     if request_id:
       
#        blog_post = Blog.query.filter_by(id=request_id).first()
#        blog_user = User.query.filter_by(id=user_id).first()
#        return render_template('blog.html', blog_post=blog_post, blog_user=blog_user)

#     elif user_id:

#        blog_user = User.query.filter_by(id=user_id).first()
#        blog_post = Blog.query.filter_by(id=request_id).first()
#        return render_template('blog.html', blog_post=blog_post, blog_user=blog_user)

#     #this is default page with list of blogs using blog template
#     return render_template('blog.html', blogs=Blog.query.all())

@app.route("/blog", methods=['GET','POST'])
def blog():
    if not request.args:
        blogs = Blog.query.all()
        return render_template("blog.html", blogs=blogs)
    elif request.args.get('id'):
        user_id = request.args.get('id')
        blog = Blog.query.get(user_id)
        #user = User.query.filter_by(id=user_id).first()
        return render_template('blog_post.html', blog=blog)
    elif request.args.get('user'):
        user_id = request.args.get('user')
        user = User.query.filter_by(id=user_id).first()
        blogs = Blog.query.filter_by(owner_id=user_id).all()
        return render_template('blog.html', blogs=blogs, user=user)


@app.route('/', methods=['POST', 'GET'])
def index():

    request_id = request.args.get('id')   
        
    if request_id:
        
        blog_post = Blog.query.get(request_id)       
        return  render_template('index_post.html', blog_post=blog_post)

    #this is default page with list of users using index template
    return render_template('index.html', users=User.query.all() )


if __name__ == '__main__':
    app.run()