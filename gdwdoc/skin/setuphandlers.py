# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.app.portlets.portlets import navigation
from Products.CMFCore.utils import getToolByName
from Products.Five.component import enableSite
from zope.app.component.interfaces import ISite


import logging
logger = logging.getLogger('gdwdoc.skin')

LANGUAGES = ['fr', 'nl']


def setupgdwdoc(context):
    logger.debug('Setup gdwdoc skin')
    portal = context.getSite()
    if not ISite.providedBy(portal):
        enableSite(portal)
    # setupLanguages(portal)
    # setupSimpleNavigationPortlet(portal, 'left')


def setupLanguages(portal):
    lang = getToolByName(portal, 'portal_languages')
    lang.supported_langs = LANGUAGES
    lang.setDefaultLanguage('fr')
    lang.display_flags = 0


def getManager(folder, column):
    if column == 'left':
        manager = getUtility(IPortletManager, name=u'plone.leftcolumn', context=folder)
    else:
        manager = getUtility(IPortletManager, name=u'plone.rightcolumn', context=folder)
    return manager


def setupSimpleNavigationPortlet(folder, column):
    #Add simple navigation portlet to folder
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager,), IPortletAssignmentMapping)
    assignment = navigation.Assignment()
    assignments['gdwdoc_navigation'] = assignment
