from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:teddy@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_entry = db.Column(db.String(120))

    def __init__(self, blog_title, blog_entry):
        self.blog_title = blog_title
        self.blog_entry = blog_entry


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():

    if request.method == 'POST':
        blog_add = request.form['blog_title']
        new_entry = request.form['blog_entry'] 

        new_blog = Blog(blog_add, new_entry)

        db.session.add(new_blog, new_entry)
        db.session.commit()

    blogs = Blog.query.all()
    entrys = Blog.query.all() 

    return render_template('newpost.html')


@app.route('/blog', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        blog_add = request.form['blog_title']
        new_entry = request.form['blog_entry'] 

        new_blog = Blog(blog_add, new_entry)

        db.session.add(new_blog, new_entry)
        db.session.commit()

    blogs = Blog.query.all()
    entrys = Blog.query.all() 

    return render_template('blog.html', blogs=blogs, entrys=entrys)

@app.route('/blog', methods=['POST'])
def display_blog():

    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)

    return render_template('blog.html', blog=blog)

if __name__ == '__main__':
    app.run()