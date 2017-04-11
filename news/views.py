from django.http import HttpResponse
from django.conf import settings
from django.template import Template, Context
from django.shortcuts import render
import sqlite3
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage


#create database tables
def db(request):
	#with connection.cursor() as cursor:
	#	cursor.execute("CREATE TABLE admin ( admin_id INTEGER PRIMARY KEY, admin_name VARCHAR(255) , admin_password VARCHAR(255) )")
	#	cursor.execute("CREATE TABLE category ( cat_id INTEGER PRIMARY  KEY, cat_name VARCHAR(255) )")
	#	cursor.execute("CREATE TABLE news ( n_id INTEGER PRIMARY  KEY, n_name VARCHAR(255), n_desc TEXT, n_image VARCHAR(255), n_catid INTEGER )")
	#	cursor.execute("CREATE TABLE comment ( c_id INTEGER PRIMARY  KEY, c_name VARCHAR(255), c_desc TEXT, c_email VARCHAR(100), c_pid INTEGER, c_status INTEGER )")
	#	cursor.execute("CREATE TABLE user ( u_id INTEGER PRIMARY  KEY, u_name VARCHAR(255), u_pass VARCHAR(255), u_email VARCHAR(100) )")
	#	cursor.execute("INSERT INTO admin (admin_name, admin_password) VALUES ('admin@gmail.com', '123456')")
	#	cursor.execute("CREATE TABLE bookmark ( b_id INTEGER PRIMARY  KEY, b_newsid INTEGER, b_userid INTEGER )")
	#	cursor.execute("DROP TABLE user")
 	return HttpResponse('post comment has been created')

#******	login ********
@csrf_exempt
def login(request):
	if request.method == 'POST':
		admin_name 	=	request.POST['admin_name']
		password 	=	request.POST['password']
		with connection.cursor() as cursor:
			sql 	=  	cursor.execute("SELECT * FROM admin WHERE admin_name = '"+admin_name+"' AND admin_password = '"+password+"'")
			sql 	=	sql.fetchone()

			# if user authenticated
			if(sql):
				request.session['name'] 		= admin_name
   				return HttpResponseRedirect("/add_category/")

   			#if user does not authenticated
			else:
				return HttpResponseRedirect("/dashboard/")

	fp 		= 	open("news/templates/login.html")
	t 		= 	Template(fp.read())
	fp.close()
	html	= 	t.render(Context())
	return HttpResponse(html)

#****** logout *******
def logout(request):
	del request.session['name']
	return HttpResponseRedirect('/dashboard/')

#****** user logout *******
def userlogout(request):
	del request.session['u_email']
	del request.session['u_name']
	del request.session['u_id']
	return HttpResponseRedirect('/')	

#******* add category *******
@csrf_exempt
def add_category(request):
	if 'name' not in request.session:
		return HttpResponseRedirect("/dashboard/")

	# when submit button clicked
	if request.method == 'POST':
		cat_name 	=	request.POST['cat_name']
		with connection.cursor() as cursor:
			sql 	=  	cursor.execute("INSERT INTO category (cat_name) VALUES ('"+cat_name+"')")

	#***** include header *****
	header	= 	open("news/templates/header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context())
	#***** include add_category page template *****
	tem 	= 	open("news/templates/add_category.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context())
	html 	=	html+tem_html
	return HttpResponse(html)

#******* view category *******
def view_category(request):
	if 'name' not in request.session:
		return HttpResponseRedirect("/dashboard/")

	#***** include header *****
	header	= 	open("news/templates/header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context())

	#***** include view_category page template *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	tem 	= 	open("news/templates/view_category.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'record': result,}))
	html 	=	html+tem_html
	return HttpResponse(html)

#******* delete category *******
def delete_category(request, id):
	with connection.cursor() as cursor:
		cursor.execute("DELETE FROM category WHERE cat_id = '"+id+"'")
		return HttpResponseRedirect('/view_category/')

#******* edit category *******
@csrf_exempt
def edit_category(request, id):

	# when submit button clicked
	if request.method == 'POST':
		cat_name 	=	request.POST['cat_name']
		with connection.cursor() as cursor:
			sql 	=  	cursor.execute("UPDATE category SET cat_name = '"+cat_name+"' WHERE cat_id = '"+id+"'")
			return HttpResponseRedirect('/view_category/')

	with connection.cursor() as cursor:
		rec =	cursor.execute("SELECT * FROM category WHERE cat_id = '"+id+"'")
		rec = 	rec.fetchone()
	
	#***** include header *****
	header	= 	open("news/templates/header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context())

	#***** include edit_category page template *****
	tem 	= 	open("news/templates/edit_category.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'record': rec,}))
	html 	=	html+tem_html
	return HttpResponse(html)

#******* add post *******
@csrf_exempt
def add_news(request):
	if 'name' not in request.session:
		return HttpResponseRedirect("/dashboard/")

	# when submit button clicked
	if request.method == 'POST':
		n_name 		=	request.POST['n_name']
		n_desc 		=	request.POST['n_desc']
		n_catid 	=	request.POST['n_catid']
		filename 	=	''
		if len(request.FILES):
			myfile 	= 	request.FILES['myfile']
			if len(request.FILES) :
				fs 		= 	FileSystemStorage()
				filename= 	fs.save(myfile.name, myfile)
				uploaded_file_url 	= 	fs.url(filename)
		with connection.cursor() as cursor:
			sql 	=  	cursor.execute("INSERT INTO news (n_name, n_desc, n_image, n_catid) VALUES ('"+n_name+"', '"+n_desc+"', '"+filename+"', '"+n_catid+"')")		

	#***** include header *****
	header	= 	open("news/templates/header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context())

	#***** include add_post page template *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	tem 	= 	open("news/templates/add_news.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'record': result,}))
	html 	=	html+tem_html
	return HttpResponse(html)

#******* view post *******
def view_news(request):
	if 'name' not in request.session:
		return HttpResponseRedirect("/dashboard/")

	#***** include header *****
	header	= 	open("news/templates/header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context())

	#***** include view_post page template *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT n.*, c.cat_name FROM news n, category c WHERE c.cat_id = n.n_catid"):
			result.append(x)
	tem 	= 	open("news/templates/view_news.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'record': result,}))
	html 	=	html+tem_html
	return HttpResponse(html)

#******* delete post *******
def delete_news(request, id):
	with connection.cursor() as cursor:
		cursor.execute("DELETE FROM news WHERE n_id = '"+id+"'")
		return HttpResponseRedirect('/view_news/')

#******* edit post *******
@csrf_exempt
def edit_news(request, id):

	with connection.cursor() as cursor:
		rec =	cursor.execute("SELECT * FROM news WHERE n_id = '"+id+"'")
		rec = 	rec.fetchone()
		result 	=	[]
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)	

	# when submit button clicked
	if request.method == 'POST':
		n_name 		=	request.POST['n_name']
		n_desc 		=	request.POST['n_desc']
		n_catid 	=	request.POST['n_catid']
		filename	=	rec[3]
		if len(request.FILES):
			myfile 	= 	request.FILES['myfile']
			if len(request.FILES) :
				fs 		= 	FileSystemStorage()
				filename= 	fs.save(myfile.name, myfile)
				uploaded_file_url 	= 	fs.url(filename)
		with connection.cursor() as cursor:
			sql 	=  	cursor.execute("UPDATE news SET n_name = '"+n_name+"' , n_desc = '"+n_desc+"', n_image = '"+filename+"', n_catid ='"+n_catid+"' WHERE n_id = '"+id+"'")		
			return HttpResponseRedirect('/view_news/')

	#***** include header *****
	header	= 	open("news/templates/header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context())

	#***** include edit_post page template *****
	tem 	= 	open("news/templates/edit_news.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'record': rec, 'category': result, }))
	html 	=	html+tem_html
	return HttpResponse(html)

#******* view comments *******
def view_users(request):
	if 'name' not in request.session:
		return HttpResponseRedirect("/dashboard/")

	#***** include header *****
	header	= 	open("news/templates/header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context())

	#***** include view_comment page template *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM user"):
			result.append(x)
	tem 	= 	open("news/templates/view_users.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'record': result,}))
	html 	=	html+tem_html
	return HttpResponse(html)

#**** index *****
def index(request):

	result	=	[]
	result	=	[]
	post 	=	[]

	#***** include header *****
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	header	= 	open("news/templates/front_header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context({'record': result, 'request': request, }))

	#***** include index page template *****
	with connection.cursor() as cursor:
		for p in cursor.execute("SELECT * FROM news ORDER BY n_id DESC  LIMIT 4"):
			post.append(p)
	tem 	= 	open("news/templates/index.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'news': post, }))
	html 	=	html+tem_html

	#****** include footer ******
	footer	= 	open("news/templates/front_footer.html")
	footer_t= 	Template(footer.read())
	footer.close()
	f_html	= 	footer_t.render(Context())
	html 	=	html+f_html
	return HttpResponse(html)

#**** news *****
def news(request):

	#***** include header *****
	result	=	[]
	post 	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	header	= 	open("news/templates/front_header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context({'record': result, 'request': request, }))

	#***** include news page template *****
	with connection.cursor() as cursor:
		for p in cursor.execute("SELECT * FROM news"):
			post.append(p)
	tem 	= 	open("news/templates/news.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'news': post, }))
	html 	=	html+tem_html

	#****** include footer ******
	footer	= 	open("news/templates/front_footer.html")
	footer_t= 	Template(footer.read())
	footer.close()
	f_html	= 	footer_t.render(Context())
	html 	=	html+f_html
	return HttpResponse(html)

#**** contact *****
def contact(request):

	#***** include header *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	header	= 	open("news/templates/front_header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context({'record': result, 'request': request, }))

	#***** include contact page template *****
	tem 	= 	open("news/templates/contact.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context())
	html 	=	html+tem_html

	#****** include footer ******
	footer	= 	open("news/templates/front_footer.html")
	footer_t= 	Template(footer.read())
	footer.close()
	f_html	= 	footer_t.render(Context())
	html 	=	html+f_html
	return HttpResponse(html)


#**** about *****
def about(request):

	#***** include header *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	header	= 	open("news/templates/front_header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context({'record': result, 'request': request, }))

	#***** include about page template *****
	tem 	= 	open("news/templates/about.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context())
	html 	=	html+tem_html

	#****** include footer ******
	footer	= 	open("news/templates/front_footer.html")
	footer_t= 	Template(footer.read())
	footer.close()
	f_html	= 	footer_t.render(Context())
	html 	=	html+f_html
	return HttpResponse(html)

#**** news detail *****
@csrf_exempt
def newsdetail(request, id):

	#***** include header *****
	result	=	[]
	post 	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	header	= 	open("news/templates/front_header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context({'record': result, 'request': request, }))

	#***** include blogdetail page template *****
	with connection.cursor() as cursor:
		rec =	cursor.execute("SELECT * FROM news WHERE n_id = '"+id+"'")
		rec = 	rec.fetchone()
		if 'u_id' in request.session:
			userid = str(request.session['u_id'])
			p = cursor.execute("SELECT b.*, n.* FROM news n, bookmark b WHERE b.b_newsid = '"+id+"' AND b.b_userid = '"+userid+"' GROUP BY b.b_newsid")
			post = p.fetchone()
	tem 	= 	open("news/templates/news_detail.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'detail': rec, 'post': post , 'request': request, }))
	html 	=	html+tem_html

	#****** include footer ******
	footer	= 	open("news/templates/front_footer.html")
	footer_t= 	Template(footer.read())
	footer.close()
	f_html	= 	footer_t.render(Context())
	html 	=	html+f_html
	return HttpResponse(html)

#**** news against category *****
def catnews(request, id):

	#***** include header *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	header	= 	open("news/templates/front_header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context({'record': result, 'request': request, }))

	#***** include blog with category filter page template *****
	post 	=	[]
	with connection.cursor() as cursor:
		for p in cursor.execute("SELECT * FROM news WHERE n_catid = '"+id+"'"):
			post.append(p)
	tem 	= 	open("news/templates/news.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'news': post, }))
	html 	=	html+tem_html

	#****** include footer ******
	footer	= 	open("news/templates/front_footer.html")
	footer_t= 	Template(footer.read())
	footer.close()
	f_html	= 	footer_t.render(Context())
	html 	=	html+f_html
	return HttpResponse(html)

#******* signup for user *******
@csrf_exempt
def signup(request):

	# when submit button clicked
	if request.method == 'POST':
		u_name 	=	request.POST['u_name']
		u_email =	request.POST['u_email']
		u_pass 	=	request.POST['u_pass']
		with connection.cursor() as cursor:
			sql =  	cursor.execute("INSERT INTO user (u_name, u_email, u_pass) VALUES ('"+u_name+"', '"+u_email+"', '"+u_pass+"')")
			sql =  	cursor.execute("SELECT * FROM user WHERE u_email = '"+u_email+"' AND u_pass = '"+u_pass+"'")
			sql	=	sql.fetchone()
			request.session['u_name']	= u_name
			request.session['u_email']	= u_email
			request.session['u_id']	= sql[0]
			return HttpResponseRedirect("/")

	#***** include header *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	header	= 	open("news/templates/front_header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context({'record': result, 'request': request, }))

	#***** include add_category page template *****
	tem 	= 	open("news/templates/signup.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context())
	html 	=	html+tem_html
	return HttpResponse(html)

#******	login ********
@csrf_exempt
def userlogin(request):
	if request.method == 'POST':
		u_email =	request.POST['u_email']
		u_pass 	=	request.POST['u_pass']
		with connection.cursor() as cursor:
			sql 	=  	cursor.execute("SELECT * FROM user WHERE u_email = '"+u_email+"' AND u_pass = '"+u_pass+"'")
			sql 	=	sql.fetchone()
			# if user authenticated
			if(sql):
				request.session['u_name'] 		= sql[1]
				request.session['u_email'] 		= u_email
				request.session['u_id'] 		= sql[0]
				return HttpResponseRedirect("/")

   			#if user does not authenticated
			else:
				return HttpResponseRedirect("/login/")

	#***** include header *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	header	= 	open("news/templates/front_header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context({'record': result, 'request' : request}))


	#***** include add_category page template *****
	tem 	= 	open("news/templates/userlogin.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context())
	html 	=	html+tem_html
	return HttpResponse(html)

#**** add bookmark *****
def add_bookmarknews(request, id):
	with connection.cursor() as cursor:
		userid 	=	str(request.session['u_id'])
		cursor.execute("INSERT INTO bookmark(b_newsid, b_userid) VALUES ( '"+id+"' , '"+userid+"' )")
		return HttpResponseRedirect('/newsdetail/'+id)

#**** bookmark category *****
def bookmarknews(request):

	if 'u_id' not in request.session:
		return HttpResponseRedirect('/login/')

	#***** include header *****
	result	=	[]
	with connection.cursor() as cursor:
		for x in cursor.execute("SELECT * FROM category"):
			result.append(x)
	header	= 	open("news/templates/front_header.html")
	header_t= 	Template(header.read())
	header.close()
	html	= 	header_t.render(Context({'record': result,  'request' : request}))

	#***** include blog with category filter page template *****
	post 	=	[]
	with connection.cursor() as cursor:
		userid 	=	str(request.session['u_id'])
		for p in cursor.execute("SELECT n.*, b.* FROM news n, bookmark b WHERE b.b_newsid = n.n_id AND b.b_userid = '"+userid+"' GROUP BY b.b_newsid"):
			post.append(p)
	tem 	= 	open("news/templates/news.html")
	temp 	= 	Template(tem.read())
	tem.close()
	tem_html= 	temp.render(Context({'news': post,}))
	html 	=	html+tem_html

	#****** include footer ******
	footer	= 	open("news/templates/front_footer.html")
	footer_t= 	Template(footer.read())
	footer.close()
	f_html	= 	footer_t.render(Context())
	html 	=	html+f_html
	return HttpResponse(html)
