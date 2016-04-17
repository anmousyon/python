#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cherrypy
import os, random, string



class HelloWorld(object):

  site_header = """<html>
                <head>
                  <link href="/static/css/style.css" rel="stylesheet">
                </head>
                <body>
           """
  site_end = """  </body>
           </html>"""
  
  @cherrypy.expose
  def index(self):
    site_body = """      <form method="get" action="generate">
                      <input type="text" value="8" name="name" />
                      <button type="submit">Give it now!</button>
                    </form>"""

    result = (self.site_header,site_body,self.site_end)

    return result

  @cherrypy.expose
  def generate(self, name='worldnews'):
    some_string = str(name)
    cherrypy.session['mystring'] = some_string
    return some_string

  @cherrypy.expose
  def display(self):
    return cherrypy.session['mystring']

if __name__ == '__main__':
  conf = {
    '/': {
       'tools.sessions.on': True,
       'tools.staticdir.root': os.path.abspath(os.getcwd())
    },
    '/static': {
       'tools.staticdir.on': True,
       'tools.staticdir.dir': './public'
    }
  }

  cherrypy.quickstart(HelloWorld(), '/', conf)
