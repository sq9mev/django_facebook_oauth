from celery.task import task

@task(name='fb_post_pages')
def post_pages(message, attachment=None):
    from fbbackends import FBGraphBackend
    backend=FBGraphBackend()
    backend.post_pages(message, attachment)

@task(name='fb_post_as_app')
def post_as_app(profile_id, message, attachment=None):
    from fbbackends import FBGraphBackend
    backend=FBGraphBackend()
    backend.post_as_app(profile_id, message, attachment)
