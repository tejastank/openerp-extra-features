# -*- coding: utf-8 -*-
##############################################################################
#
#    Tejas Tank, https://github.com/tejastank/openerp-extra-features
#    Email : tejas.tank.mca@gmail.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from lxml import etree
import time
from datetime import datetime, date

from tools.translate import _
from osv import fields, osv

class project(osv.osv):
    _name = "project.project"
    _description = "Project"
    _inherit = "project.project"

    def send_email(self, cr, uid, ids, subject, body, context=None):
        projects = self.browse(cr, uid, ids, context=context)
        ir_mail_server = self.pool.get('ir.mail_server')
        current_user = self.pool.get('res.users').browse(cr, uid, uid, context=context)        
        for prj in projects:            
            email_to = []
            if prj.user_id.user_email:
                email_to.append(prj.user_id.user_email)
            for users in prj.members:
                if users.user_email:
                    email_to.append(users.user_email)
            if current_user.user_email:
                #return tools.email_send(current_user.user_email,list(set(email_to)),subject,body) # for version 6.0
                msg = ir_mail_server.build_email(email_from=current_user.user_email, email_to=list(set(email_to)), subject=subject, body=body,  )
                return ir_mail_server.send_email(cr, uid, msg, context=context)        
            else:
                raise osv.except_osv(_('Unable to sent email !'), _('Require email address for TO/FROM.'))

    def write(self, cr, uid, ids, vals, context=None):
        res = super(project,self).write(cr, uid, ids, vals, context)        
        message = _("""Hello,\nProject is updated,\n\nHere below all detail regarding project updates\n""")
        
        if vals.has_key('date_start'):
            message += "\n" + _("Start date  : ") + vals['date_start']
        if vals.has_key('date'):
            message += "\n" + _("End date  : ") + vals['date']
        if vals.has_key('state'):
            message += "\n" + _("State  : ") + vals['state']
        if vals.has_key('description'):
            message += "\n" + _("Note  : ") + vals['description'] + "\n"
            
        message +="\n\n" + _("Thanks,") + "\n" + _('Yours Company')
        get_project = self.read(cr, uid, ids, ['name'])[0]
        project_name = get_project['name']
        self.send_email(cr, uid, ids, project_name + ": Project Updated", message, context)
        return res
        
    def create(self, cr, uid, vals, context=None):
        result = super(project, self).create(cr, uid, vals, context=context)
        self.send_email(cr, uid, [result], vals['name'] + ": Project Created", "Hell,\nNew Project created" + vals['name'] + "\n\nThanks,Yours Company.", context)
        return result
        
    def unlink(self, cr, uid, ids, context=None):
        get_project = self.read(cr, uid, ids, ['name'])[0]
        project_name = get_project['name']
        self.send_email(cr, uid, ids, project_name + ": Project Removed", "Hell,\n\n Project Removed " + project_name+"\n\nThanks,Yours Company.", context)
        res = super(project, self).unlink(cr, uid, ids, context)
        return res
        
project()
