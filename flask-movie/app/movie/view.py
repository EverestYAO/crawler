from flask import request,render_template, redirect,url_for
from . import movie
from ..models import Movie,Magnet
from .form import SearchForm
from .searchcrawl import crawl
import time

@movie.route('/movie/cartoon', methods=['GET', 'POST'])
def cartoon():
	if request.method =='POST':
		searchkey=request.form.get('searchkey')#提交按钮时输入的关键词
		movies=Movie.query.filter(Movie.title.like('%{searchkey}%'.format(searchkey=searchkey))).all()#模糊查询数据库中包含关键词的数据
		return render_template('movie.html',movies=movies)#渲染模板

	endpoint = 'movie.cartoon'#路由，传入翻页宏
	page = request.args.get('page',1, type=int)#页码，默认为1
	pagination = Movie.query.filter_by(movietype='动漫').paginate(
        page,per_page=10,
        error_out=False)#从数据库查询数据
	movies = pagination.items#获取数据
	return render_template('movie.html',movies=movies,pagination=pagination,e=endpoint)#渲染模板

@movie.route('/movie/action', methods=['GET', 'POST'])
def action():
	endpoint = 'movie.action'#路由，传入翻页宏
	page = request.args.get('page',1, type=int)#页码，默认为1
	pagination = Movie.query.filter_by(movietype='动作片').paginate(
        page,per_page=10,
        error_out=False)
	movies = pagination.items
	return render_template('movie.html',movies=movies,pagination=pagination,e=endpoint)

@movie.route('/movie/horrible', methods=['GET', 'POST'])
def horrible():
	endpoint = 'movie.horrible'
	page = request.args.get('page',1, type=int)
	pagination = Movie.query.filter_by(movietype='恐怖片').paginate(
        page,per_page=10,
        error_out=False)
	movies = pagination.items
	return render_template('movie.html',movies=movies,pagination=pagination,e=endpoint)

@movie.route('/movie/science', methods=['GET', 'POST'])
def science():
	endpoint='.science'
	page = request.args.get('page',1, type=int)
	pagination = Movie.query.filter_by(movietype='科幻片').paginate(
        page,per_page=10,
        error_out=False)
	movies = pagination.items
	return render_template('movie.html',movies=movies,pagination=pagination,e=endpoint)

@movie.route('/movie/story', methods=['GET', 'POST'])
def story():
	endpoint='movie.story'
	page = request.args.get('page',1, type=int)
	pagination = Movie.query.filter_by(movietype='剧情片').paginate(
        page,per_page=10,
        error_out=False)
	movies = pagination.items
	return render_template('movie.html',movies=movies,pagination=pagination,e=endpoint)

@movie.route('/movie/love', methods=['GET', 'POST'])
def love():
	endpoint='movie.love'
	page = request.args.get('page',1, type=int)
	pagination = Movie.query.filter_by(movietype='爱情片').paginate(
        page,per_page=10,
        error_out=False)
	movies = pagination.items
	return render_template('movie.html',movies=movies,pagination=pagination,e=endpoint)
@movie.route('/movie/war', methods=['GET', 'POST'])
def war():
	endpoint='movie.war'
	page = request.args.get('page',1, type=int)
	pagination = Movie.query.filter_by(movietype='战争片').paginate(
        page,per_page=10,
        error_out=False)
	movies = pagination.items
	return render_template('movie.html',movies=movies,pagination=pagination,e=endpoint)
@movie.route('/movie/record', methods=['GET', 'POST'])
def record():
	endpoint='movie.record'
	page = request.args.get('page',1, type=int)
	pagination = Movie.query.filter_by(movietype='记录片').paginate(
        page,per_page=10,
        error_out=False)
	movies = pagination.items
	return render_template('movie.html',movies=movies,pagination=pagination,e=endpoint)
@movie.route('/movie/comedy', methods=['GET', 'POST'])
def comedy():
	endpoint='movie.comedy'
	page = request.args.get('page',1, type=int)
	pagination = Movie.query.filter_by(movietype='喜剧片').paginate(
        page,per_page=10,
        error_out=False)
	movies = pagination.items
	return render_template('movie.html',movies=movies,pagination=pagination,e=endpoint)
@movie.route('/movie/jpkorTV', methods=['GET', 'POST'])
def jpkorTV():
	endpoint='movie.jpkorTV'
	page = request.args.get('page',1, type=int)
	pagination = Movie.query.filter_by(movietype='日韩剧').paginate(
        page,per_page=10,
        error_out=False)
	movies = pagination.items
	return render_template('movie.html',movies=movies,pagination=pagination,e=endpoint)

@movie.route('/movie/<int:id>', methods=['GET', 'POST'])#传入id
def content(id):
	film = Movie.query.get_or_404(id)#通过传入的id获取电影数据
	return render_template('moviedetail.html', film=film,url=list(eval(film.url)))#渲染模板

@movie.route('/movie/search', methods=['GET', 'POST'])
def search():
	if request.method =='POST':#用户点击提交后将参数post
		searchkey=request.form.get('searchkey')
		print(searchkey)
		crawl(searchkey)
		time.sleep(5)
		page = request.args.get('page', 1, type=int)
		pagination=Magnet.query.filter_by(key=searchkey).paginate(
        page,per_page=10,
        error_out=False)
		searchresults = pagination.items
		return render_template('magnetsearch.html', searchresults=searchresults)

	return  render_template('magnetsearch.html')



