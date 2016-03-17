# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.app.portlets.portlets import navigation
from Products.CMFCore.utils import getToolByName
from Products.Five.component import enableSite
from Products.PloneLDAP.factory import genericPluginCreation
from Products.PloneLDAP.plugins.ldap import PloneLDAPMultiPlugin
from zope.app.component.interfaces import ISite


import logging
logger = logging.getLogger('gdwdoc.skin')

LANGUAGES = ['fr', 'nl']


def setupgdwdoc(context):
    logger.debug('Setup gdwdoc skin')
    portal = context.getSite()
    if not ISite.providedBy(portal):
        enableSite(portal)
    activatePloneLDAPPlugin(portal)
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


def activatePloneLDAPPlugin(portal):
    """
    Go in the acl and active our plugin
    """
    acl = portal.acl_users
    if 'ldap' not in acl.objectIds():
        luf = genericPluginCreation(acl, PloneLDAPMultiPlugin, id='ldap',
                title='LDAP Connexion', login_attr='cn', uid_attr='cn',
                users_base="dc=gitesdewallonie,dc=net",
                users_scope=2, roles="Member",
                groups_base="ou=groups,dc=gitesdewallonie,dc=net",
                groups_scope=2, binduid="cn=admin,dc=gitesdewallonie,dc=net",
                bindpwd='*****',
                binduid_usage=1, rdn_attr='cn',
                obj_classes='person,organizationalPerson',
                local_groups=0, use_ssl=0, encryption='SHA',
                read_only=0, LDAP_server="kepler.interne.affinitic.be", REQUEST=None)

        luf.manage_addLDAPSchemaItem("registeredAddress", "email",
                                     public_name="email")
        luf.manage_addLDAPSchemaItem("title", "fullname",
                                     public_name="fullname")

    interfaces = ['IAuthenticationPlugin',
                  'ICredentialsResetPlugin',
                  'IGroupEnumerationPlugin',
                  'IGroupIntrospection',
                  'IGroupManagement',
                  'IGroupsPlugin',
                  'IPropertiesPlugin',
                  'IRoleEnumerationPlugin',
                  'IRolesPlugin',
                  'IUserAdderPlugin',
                  'IUserEnumerationPlugin',
                  'IUserManagement']
    ldap = getattr(acl, 'ldap')
    ldap.manage_activateInterfaces(interfaces)
    for interface in interfaces:
        interface_object = acl.plugins._getInterfaceFromName(interface)
        acl.plugins.movePluginsUp(interface_object, ['ldap'])
