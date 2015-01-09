# -*- coding: utf-8 -*-

from os import path

try:
    import json # try stdlib (Python 2.6)
except ImportError:
    try:
        import simplejson as json # try external module
    except:
        import gluon.contrib.simplejson as json # fallback to pure-Python module

from gluon import current
from gluon.html import *
from gluon.storage import Storage

from s3 import FS, S3CustomController
from s3theme import formstyle_foundation_inline

THEME = "EIDMS"

# =============================================================================
class index(S3CustomController):
    """ Custom Home Page """

    def __call__(self):

        output = {}

        # Allow editing of page content from browser using CMS module
        if current.deployment_settings.has_module("cms"):
            system_roles = current.auth.get_system_roles()
            ADMIN = system_roles.ADMIN in current.session.s3.roles
            s3db = current.s3db
            table = s3db.cms_post
            ltable = s3db.cms_post_module
            module = "default"
            resource = "index"
            query = (ltable.module == module) & \
                    ((ltable.resource == None) | \
                     (ltable.resource == resource)) & \
                    (ltable.post_id == table.id) & \
                    (table.deleted != True)
            item = current.db(query).select(table.body,
                                            table.id,
                                            limitby=(0, 1)).first()
            if item:
                if ADMIN:
                    item = DIV(XML(item.body),
                               BR(),
                               A(current.T("Edit"),
                                 _href=URL(c="cms", f="post",
                                           args=[item.id, "update"]),
                                 _class="action-btn"))
                else:
                    item = DIV(XML(item.body))
            elif ADMIN:
                if current.response.s3.crud.formstyle == "bootstrap":
                    _class = "btn"
                else:
                    _class = "action-btn"
                item = A(current.T("Edit"),
                         _href=URL(c="cms", f="post", args="create",
                                   vars={"module": module,
                                         "resource": resource
                                         }),
                         _class="%s cms-edit" % _class)
            else:
                item = ""
        else:
            item = ""
        output["item"] = item

        self._view(THEME, "index.html")
        return output

    # -------------------------------------------------------------------------
    def shelter_list(self):
        """ Provide a dropdown of links to shelters """

        T = current.T
        s3db = current.s3db

        resource = s3db.resource("cr_shelter",
                                    filter = FS("status")
                                                            .belongs([2, None]))
        data = resource.select(["id", "name"])
        shelter_list = UL(_id = "shelter_list",
                          _class = "f-dropdown",
                          data = {"dropdown-content": ""})
        rows = data["rows"]
        if rows:
            for row in rows:
                shelter_list.append(LI(A(row["cr_shelter.name"],
                                            _href=URL(c="cr",
                                                    f="shelter",
                                                    args=[row["cr_shelter.id"]])
                                            )
                                        )
                                    )
            return LI(A(T("Shelters"),
                        _class="button dropdown",
                        data = {"dropdown": "shelter_list"}),
                      shelter_list
                      )
        else:
            if current.auth.s3_has_permission("create", current.db.cr_shelter):
                return LI(A(T("Create Shelter"),
                            _href=URL(c="cr",
                                      f="shelter",
                                      args=["create"]),
                            _class="button button-home"
                            )
                          )
            return ""

# END =========================================================================
