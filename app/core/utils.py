import os


def content_file_name(instance, filename):
    """Creates a string for portrait image"""
    ext = filename.split('.')[-1]
    filename = "%s-%s.%s" % (instance.owner.id, "portrait", ext)
    return os.path.join('portraits', filename)