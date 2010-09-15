from plone.app.portlets.portlets.recent import Renderer
#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MyRecentRenderer(Renderer):
    @property
    def available(self):
        return len(self._data())
