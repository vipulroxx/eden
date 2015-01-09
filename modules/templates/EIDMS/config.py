# -*- coding: utf-8 -*-

try:
    # Python 2.7
    from collections import OrderedDict
except:
    # Python 2.6
    from gluon.contrib.simplejson.ordered_dict import OrderedDict

from gluon import current
from gluon.storage import Storage
from gluon.validators import IS_NOT_EMPTY, IS_EMPTY_OR, IS_IN_SET

from s3 import s3_date, S3Represent

"""
    Welcome to Eastern India Disaster Management System
"""
# -----------------------------------------------------------------------------

def config(settings):

    T = current.T
    settings = current.deployment_settings
    # -------------------------------------------------------------------------
    # Pre-Populate
    settings.base.prepopulate = ("EIDMS", "default/users")
    settings.base.system_name = T("Welcome to Eastern India Disaster Management System")
    settings.base.system_name_short = T("Sahana Eden - Eastern India")
    settings.base.theme = "EIDMS"

    # -------------------------------------------------------------------------
    # Email settings
    settings.mail.default_email_subject = True
    settings.mail.auth_user_in_email_subject = True

    # -------------------------------------------------------------------------
    # Authentication settings
    settings.auth.registration_requests_mobile_phone = True
    settings.auth.registration_mobile_phone_mandatory = True
    settings.auth.registration_requests_organisation = True
    # Uncomment this to have the Organisation selection during registration be mandatory
    #settings.auth.registration_organisation_required = True
    settings.auth.always_notify_approver = False
    settings.security.self_registration = False

    # Security Policy
    # http://eden.sahanafoundation.org/wiki/S3AAA#System-widePolicy
    settings.security.policy = 7


    # -------------------------------------------------------------------------
    # L10n settings
    settings.L10n.languages = OrderedDict([
        ("en", "English"),

    ])
    settings.L10n.default_language = "en"
    settings.L10n.utc_offset = "UTC +0530"
    settings.L10n.date_format = T("%d/%m/%Y")
    settings.L10n.mandatory_lastname = True
    settings.L10n.translate_gis_location = True

    # Finance settings
    settings.fin.currency_default = "INR"
    settings.fin.currencies = {
        "INR": T("Indian Rupees"),
        "USD": T("United States Dollars"),
    }

    # -------------------------------------------------------------------------
    # GIS (Map) settings
    # GeoNames username
    settings.gis.geonames_username = "geoname_username"
    settings.gis.countries = ["IT"]
    settings.gis.legend = "float"
    settings.gis.nav_controls = False

    # -------------------------------------------------------------------------
    # Shelters
    settings.cr.shelter_population_dynamic = True
    settings.cr.shelter_housing_unit_management = True

    # -------------------------------------------------------------------------
    # Events
    settings.event.types_hierarchical = True

    # -------------------------------------------------------------------------
    # Organisations
    settings.org.branches = True
    settings.org.branches_tree_view = True
    settings.org.facility_types_hierarchical = True

    # -------------------------------------------------------------------------
    # Human Resource Management
    settings.hrm.email_required = False
    settings.hrm.org_required = False
    settings.hrm.deletable = True
    settings.hrm.multiple_job_titles = True
    settings.hrm.staff_experience = False
    settings.hrm.vol_active = True
    settings.hrm.vol_experience = False
    settings.hrm.show_organisation = True
    settings.hrm.use_awards = False
    settings.hrm.use_certificates = False
    settings.hrm.use_skills = True
    settings.hrm.use_trainings = False

    # -------------------------------------------------------------------------
    # RSS feeds
    settings.frontpage.rss = [
       # @ Todo : rss newsfeeds on homepage
    ]

    # -------------------------------------------------------------------------
    # Resource customization
    #
    settings.customise_cr_shelter_resource = customise_cr_shelter_resource
    settings.customise_pr_group_resource = customise_pr_group_resource
    settings.customise_event_event_resource = customise_event_event_resource
    settings.customise_event_incident_resource = customise_event_incident_resource
    settings.customise_project_location_resource = customise_project_location_resource

    # -------------------------------------------------------------------------
    # Comment/uncomment modules here to disable/enable them
    # @ToDo: Have the system automatically enable migrate if a module is enabled
    # Modules menu is defined in modules/eden/menu.py
    settings.modules = OrderedDict([
        # Core modules which shouldn't be disabled
        ("default", Storage(
            name_nice = T("Home"),
            restricted = False, # Use ACLs to control access to this module
            access = None,      # All Users (inc Anonymous) can see this module in the default menu & access the controller
            module_type = None  # This item is not shown in the menu
        )),
        ("admin", Storage(
            name_nice = T("Administration"),
            #description = "Site Administration",
            restricted = True,
            access = "|1|",     # Only Administrators can see this module in the default menu & access the controller
            module_type = None  # This item is handled separately for the menu
        )),
        ("appadmin", Storage(
            name_nice = T("Administration"),
            #description = "Site Administration",
            restricted = True,
            module_type = None  # No Menu
        )),
        #("errors", Storage(
        #   name_nice = T("Ticket Viewer"),
        #    #description = "Needed for Breadcrumbs",
        #    restricted = False,
        #    module_type = None  # No Menu
        #)),
        ("sync", Storage(
            name_nice = T("Synchronization"),
            #description = "Synchronization",
            restricted = True,
            access = "|1|",     # Only Administrators can see this module in the default menu & access the controller
            module_type = None  # This item is handled separately for the menu
        )),
        ("translate", Storage(
            name_nice = T("Translation Functionality"),
            #description = "Selective translation of strings based on module.",
            module_type = None,
        )),
        ("gis", Storage(
            name_nice = T("Map"),
            #description = "Situation Awareness & Geospatial Analysis",
            restricted = True,
            module_type = 1,     # 6th item in the menu
        )),
        ("pr", Storage(
            name_nice = T("Person Registry"),
            #description = "Central point to record details on People",
            restricted = True,
            access = "|1|",     # Only Administrators can see this module in the default menu (access to controller is possible to all still)
            module_type = 10
        )),
        ("org", Storage(
            name_nice = T("Organizations"),
            #description = 'Lists "who is doing what & where". Allows relief agencies to coordinate their activities',
            restricted = True,
            module_type = 10
        )),
        # All modules below here should be possible to disable safely
        ("hrm", Storage(
            name_nice = T("Staff"),
            #description = "Human Resources Management",
            restricted = True,
            module_type = 10,
        )),
        ("vol", Storage(
            name_nice = T("Volunteers"),
            #description = "Human Resources Management",
            restricted = True,
            module_type = 10,
        )),
        ("doc", Storage(
            name_nice = T("Documents"),
            #description = "A library of digital resources, such as photos, documents and reports",
            restricted = True,
            module_type = 10,
        )),
        ("msg", Storage(
            name_nice = T("Messaging"),
            #description = "Sends & Receives Alerts via Email & SMS",
            restricted = True,
            # The user-visible functionality of this module isn't normally required. Rather it's main purpose is to be accessed from other modules.
            module_type = 2,
        )),
        ("inv", Storage(
            name_nice = T("Resouce Inventories"),
            #description = "Sends & Receives Alerts via Email & SMS",
            restricted = True,
            # The user-visible functionality of this module isn't normally required. Rather it's main purpose is to be accessed from other modules.
            module_type = 2,
        )),        
        ("cr", Storage(
            name_nice = T("Shelters"),
            #description = "Tracks the location, capacity and breakdown of victims in Shelters",
            restricted = True,
            module_type = 10
        )),
        ("project", Storage(
            name_nice = T("Projects"),
            #description = "Tracks the location, capacity and breakdown of victims in Shelters",
            restricted = True,
            module_type = 10
        )),
        ("event", Storage(
            name_nice = T("Events"),
            #description = "Activate Events (e.g. from Scenario templates) for allocation of appropriate Resources (Human, Assets & Facilities).",
            restricted = True,
            module_type = 10,
        )),
    ])


# -----------------------------------------------------------------------------
def customise_cr_shelter_resource(r, tablename):

    s3db = current.s3db
    from s3 import S3HierarchyWidget
    s3db.cr_shelter.capacity_day.writable = s3db.cr_shelter.capacity_night.writable = False
    s3db.cr_shelter.cr_shelter_environment_id.readable = s3db.cr_shelter.cr_shelter_environment_id.writable = True
    organisation_represent = current.s3db.org_OrganisationRepresent
    node_represent = organisation_represent(parent=False)
    org_widget = S3HierarchyWidget(lookup="org_organisation",
                                   represent=node_represent,
                                   multiple=False,
                                   leafonly=False,
                                   )
    s3db.cr_shelter.organisation_id.widget = org_widget

# -----------------------------------------------------------------------------
def customise_pr_group_resource(r, tablename):

    messages = current.messages
    field = r.table.group_type

    T = current.T
    pr_group_types = {1 : T("Family"),
                      2 : T("Tourist Group"),
                      3 : T("Relief Team"),
                      4 : T("other"),
                      5 : T("Mailing Lists"),
                      6 : T("Society"),
                      }
    field.represent = lambda opt: pr_group_types.get(opt, messages.UNKNOWN_OPT)
    field.requires = IS_IN_SET(pr_group_types, zero=None)

# -----------------------------------------------------------------------------
def customise_event_event_resource(r, tablename):

    table = r.table
    table.exercise.default = True
    table.organisation_id.readable = table.organisation_id.writable = True

# -----------------------------------------------------------------------------
def customise_event_incident_resource(r, tablename):

    from s3 import IS_ONE_OF
    db = current.db
    table = r.table
    table.exercise.default = True
    table.event_id.readable = table.event_id.writable = True
    represent = S3Represent(lookup=tablename)
    table.event_id.requires = IS_ONE_OF(db, "event_event.id",
                                        represent,
                                        filterby="closed",
                                        filter_opts=(False,),
                                        orderby="event_event.name",
                                        sort=True)

# -----------------------------------------------------------------------------
def customise_project_location_resource(r, tablename):

    field = current.s3db.project_location.status_id
    field.readable = field.writable = True

# END =========================================================================
