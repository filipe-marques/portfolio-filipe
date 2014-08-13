#!/usr/bin/env python

# Python 2.7.5

#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	any later version.
#	
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#	
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/agpl-3.0.html>.

import webapp2
import jinja2
import os
import cgi

from google.appengine.api import mail

jinjaenvironment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), extensions=['jinja2.ext.autoescape'], autoescape=True)

class MainPage(webapp2.RequestHandler):
	def get(self):
		templatevalues = {}
		template = jinjaenvironment.get_template('index.html')
		self.response.write(template.render(templatevalues))
		#self.response.out.write('Hello World!')

class ProcessForm(webapp2.RequestHandler, object):
	def post(self):
		name = cgi.escape(self.request.get('name'))
		email = cgi.escape(self.request.get('email'))
		message = cgi.escape(self.request.get('message'))
		
		fields = [name,email,message]
		
		if not mail.is_email_valid(fields[1]):
			self.response.write('<h1>Por favor corrija os erros!</h1><br><h2><a href="/#contact">Voltar</a></h2>')
		elif not fields:
			self.response.write('<h1>Por favor insira algo!</h1><br><h2><a href="/#contact">Voltar</a></h2>')
		else:
			mensagem = mail.EmailMessage(sender="eagle.software3@gmail.com", subject="Mensagem do Portfolio - Nome: "+fields[0]+" Email:"+fields[1])
			mensagem.to = "youxuse.com@gmail.com"
			mensagem.body = fields[2]
			mensagem.send()
			
			# as 'keys' do dictionario sao as variaveis da template
			template_values = {'nome': fields[0], 'email': fields[1], 'mensagem': fields[2],}
			template = jinjaenvironment.get_template('info.html')
			self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', MainPage),
								('/messagesuccess', ProcessForm),
								], debug=True)
