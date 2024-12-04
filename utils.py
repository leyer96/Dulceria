import os

class Paths:
    base = os.path.dirname(__file__)
    data = os.path.join(base, "data")
    icons = os.path.join(base, "resources/icons")  
    models = os.path.join(base, "models")
    settings = os.path.join(base, "config")
    style = os.path.join(base, "resources/styles.qss")
    threads = os.path.join(base, "models/threads")
    views = os.path.join(base, "views")
    
    # File loaders
    @classmethod
    def db(cls):
        return os.path.join(cls.data, "db.db")
    @classmethod
    def icon(cls, filename):
        return os.path.join(cls.icons, filename)
    @classmethod
    def image(cls, filename):
        return os.path.join(cls.images, filename)
    @classmethod
    def model(cls, filename):
        return os.path.join(cls.models, filename)
    @classmethod
    def setting(cls, filename):
        return os.path.join(cls.settings, filename)
    @classmethod
    def thread(cls, filename):
        return os.path.join(cls.settings, filename)
    @classmethod
    def view(cls, filename):
        return os.path.join(cls.views, filename)
    