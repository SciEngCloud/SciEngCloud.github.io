from bottle import get, post, request, route, run, template

s = '''<p> pick one of a, b, c or d </p>
	<form action = "/lookup"  method="post">
		Image Name: <input name="image" type="text" />
                	<input value="display" type="submit" />
        </form>
'''
path = "."

@route('/')
def rootpath():
	return lookup()

@route('/images/<im>')
def route(im):
  f = open("/images/"+im, "rb")
  return f.read()

@get('/lookup')
def lookup():
	return s

@post('/lookup')
def do_lookup():
	image = request.forms.get('image')
	t = "<p>the image is </p> \
		<img src = %s/images/%s.jpg height=200>"%(path,image)
	return t+s

run(host='0.0.0.0', port=8000)
