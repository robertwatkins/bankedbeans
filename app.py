# pip3 install CherryPy
import os
import cherrypy
import process

PATH = os.path.abspath(os.path.dirname(__file__)) + "/html"


class Root(object):
    pass


class CategoryTotals(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        return process.show_annual_category_totals()


class MemoById(object):
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def index(self):
        data = cherrypy.request.json
        return process.update_memo_by_id(str(data))


class Source(object):
    def __init__(self):
        self.transactions = Transactions()

    def _cp_dispatch(self, vpath):
        cherrypy.request.params['source'] = "All"
        cherrypy.request.params['year'] = "Any"
        cherrypy.request.params['category'] = None
        cherrypy.request.params['subcategory'] = None
        if len(vpath) == 1:
            cherrypy.request.params['source'] = vpath.pop()
            return self.transactions

        if len(vpath) == 2:
            cherrypy.request.params['source'] = vpath.pop(0)
            cherrypy.request.params['year'] = vpath.pop(0)
            return self.transactions

        if len(vpath) == 3:
            cherrypy.request.params['source'] = vpath.pop(0)
            cherrypy.request.params['year'] = vpath.pop(0)
            cherrypy.request.params['category'] = vpath.pop(0)
            return self.transactions

        if len(vpath) == 4:
            cherrypy.request.params['source'] = vpath.pop(0)
            cherrypy.request.params['year'] = vpath.pop(0)
            cherrypy.request.params['category'] = vpath.pop(0)
            cherrypy.request.params['subcategory'] = vpath.pop(0)
            return self.transactions

        return vpath

    @cherrypy.expose
    def index(self, source):
        return 'About %s ...' % source


class Transactions(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self, source, year, category, subcategory):

        print( 'About %s, %s, %s, %s...' % (source, year, category, subcategory))
        return process.show_transactions(source, year, category, subcategory)


if __name__ == '__main__':
   cherrypy.tree.mount(Root(), '/', "static.conf")
   cherrypy.tree.mount(MemoById(), '/memobyid', "app.conf")
   cherrypy.tree.mount(CategoryTotals(), '/categorytotals', "app.conf")
   cherrypy.tree.mount(Source(), '/transactions', "app.conf")
   cherrypy.config.update({'tools.staticdir.dir': PATH})
   cherrypy.engine.start()
   cherrypy.engine.block()

