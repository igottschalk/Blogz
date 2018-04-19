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

    title_error = ""
    entry_error = ""
    title = ""
    entry = ""

    if request.method == 'POST':
        blog_add = request.form['blog_title']
        new_entry = request.form['blog_entry'] 

        if len(title) == 0:
            title_error = "Please fill in title"

        if len(entry) == 0:
            entry_error = "Please fill in body"

        if len(title_error) == 0 and len(entry_error) == 0:
            new_blog = Blog(blog_add, new_entry)
            db.session.add(new_blog, new_entry)
            db.session.commit()
            return render_template('newpost.html', title_error=title_error, entry_error=entry_error)

    blogs = Blog.query.all()
    entrys = Blog.query.all() 

    return render_template('newpost.html', blogs=blogs, entrys=entrys)


@app.route("/blog", methods=['GET'])
def index():

    request_id = request.args.get('id')
    
    if request_id:
       
       blog_post = Blog.query.get(int(request_id))
       
       return  render_template('blog_post.html', blog=blog_post)

    return render_template('blog.html', blogs=Blog.query.all())

@app.route('/blog', methods=['POST'])
def display_blog():

    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)

    return render_template('blog_post.html', blog=blog)

if __name__ == '__main__':
    app.run()