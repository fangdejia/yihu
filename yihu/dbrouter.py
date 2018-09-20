class WordPressRouter(object):
	def db_for_read(self, model, **hints):
		return 'wordpress' if model._meta.app_label == 'wordpress' else None;

	def db_for_write(self, model, **hints):
		return 'wordpress' if model._meta.app_label == 'wordpress' else None;

	def allow_relation(self, obj1, obj2, **hints):
		return True if obj1._meta.app_label == 'wordpress' or obj2._meta.app_label == 'wordpress' else  None

	def db_for_migrate(self, db, app_label, model_name=None, **hints):
		return False if app_label == 'wordpress' else None
