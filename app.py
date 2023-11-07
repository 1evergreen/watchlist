from flask import Flask, request, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import click
import os 
import sys

app = Flask(__name__)
# 操作系统
WIN = sys.platform.startswith('win')
prefix = 'sqlite:///' if WIN else 'sqlite:////' 
# Note: 在扩展类实例化之前加载配置
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/user/<name>')
def user_page(name):
    return f'hello, {name}'

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# 模板上下文处理函数
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))
    
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database')

#生成虚拟数据
@app.cli.command()
def forge():
    '''Generate fake data'''
    db.create_all()
    
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    db.session.add_all([Movie(title=m['title'], year=m['year']) for m in movies])
    
    db.session.commit()
    click.echo('Done.')
    
