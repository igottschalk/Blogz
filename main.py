from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:teddy@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_entry = db.Column(db.String(120))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, blog_title, blog_entry, owner):
        self.blog_title = blog_title, owner
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


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()   
        if user and user.password == password:
            session['username'] = username
            return redirect('/')
        else:
            return '<h1>Error!</h1>'      

    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        #TODO -check if valid input

        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            #TODO - message that user exists
            return '<h1>Duplicate user</h1>'

    return render_template('signup.html')

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_add = request.form['blog_title']
        new_entry = request.form['blog_entry'] 

        title_error = ""
        entry_error = ""

        if len(blog_add) == 0:
            title_error = "Please fill in the title"

        if len(new_entry) == 0:
            entry_error = "Please fill in the body"

        if len(title_error) > 0 or len(entry_error) > 0:
            return render_template('newpost.html', 
                title_error=title_error, 
                entry_error=entry_error, 
                blog_add=blog_add, 
                new_entry=new_entry)

        new_blog = Blog(blog_add, new_entry, owner)

        db.session.add(new_blog, new_entry)
        db.session.commit()
      

        blogs = Blog.query.all()
        blog =  blogs[len(blogs)-1]

        return render_template('blog_post.html', blog=blog) 

    return render_template('newpost.html') 

@app.route("/blog", methods=['GET'])
def index():

    request_id = request.args.get('id')
    
    if request_id:
       
       blog_post = Blog.query.get(int(request_id))
       
       return  render_template('blog_post.html', blog=blog_post)

    return render_template('blog.html', blogs=Blog.query.all())



if __name__ == '__main__':
    app.run()