import os


# Central directory for storing exports and reading imports.
# Useful when you want to export content from one Plone Site
# to another on the same server.
# Or prepare content on your development machine,
# and copy it to this central directory on the server.
# When set, this is used instead of for example
# var/instance/ or var/instance/import/
CENTRAL_DIRECTORY = os.path.expanduser(
    os.path.expandvars(os.getenv("COLLECTIVE_EXPORTIMPORT_CENTRAL_DIRECTORY", ""))
)
