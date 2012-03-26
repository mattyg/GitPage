import web
import os
import markdown2
import subprocess
import ayah
from settings import *




REPO_REMOTE_PATH = REPO_USERNAME+'@'+REPO_SERVER+REPO_NAME+'.git'
REPO_PATH = ROOT_PATH+REPO_NAME+'/'
flatfiles_path = REPO_PATH
templates = web.template.render(ROOT_PATH+'templates/')
#print 'cd '+REPO_PATH+' && git fetch '+REPO_REMOTE_PATH+' && git reset --soft master'
# check if git repo is up-to-date
res =subprocess.Popen('cd '+REPO_PATH+' && git fetch '+REPO_REMOTE_PATH+' && git reset --soft master',shell=True)

# configure ayah
ayah.configure(AYAH_PUB_KEY,AYAH_SCOR_KEY)


urls = (
	'^/contact', 'contact',
	'^/(.*)[/]*$', 'page'
)
app = web.application(urls, globals(),autoreload=False)


def load_pagefile(name):
	if os.path.isdir(flatfiles_path+name):
		flatfiles = os.listdir(flatfiles_path+name)
		if 'index' in flatfiles:
			return markdown2.markdown_path(flatfiles_path+name+'/index')
		else:
			return False
	else:
		if os.path.isfile(flatfiles_path+name):
			return markdown2.markdown_path(flatfiles_path+name)
		else:
			return False


class contact:
	def GET(self):
		sidebar = load_pagefile('/sidebar')
		footer = load_pagefile('/footer')
		contacttext = load_pagefile('/contact')
		if sidebar == False:
			sidebar = ''
		if footer == False:
			footer = ''
		if contacttext == False:
			contacttext = ''
		ayahhtml = ayah.get_publisher_html()
		return templates.contact(contacttext,ayahhtml,sidebar,footer)
	def POST(self):
		data = web.input()
		ishuman = False
		if data.__contains__('session-secret'):
			ishuman = ayah.score_result(data['session-secret'])
		if ishuman and data.__contains__('subject') and data.__contains__('message') and data.__contains__('senderemail'):
				# good
				web.sendmail('matt@webpy.org', 'matt@gabrenya.com', data['subject'], data['message'])
class page:
	def GET(self,name):
		pf = load_pagefile(name)
		sidebar = load_pagefile('/sidebar')
		footer = load_pagefile('/footer')
		if sidebar == False:
			sidebar = ''
		if footer == False:
			footer = ''
		if pf != False:
			return templates.page(pf,sidebar,footer)
		else:
			return web.notfound()
	



if __name__ == "__main__":
	app.run()
else:
	app.wsgifunc()
