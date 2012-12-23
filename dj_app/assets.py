from django_assets import Bundle, register

# js = Bundle('common/jquery.js', 'site/base.js', 'site/widgets.js',
#             filters='jsmin', output='gen/packed.js')

# register('js_all', js)

less = Bundle('/var/www/pman/data/www/django_test/templates/1.scss',
              filters='less', output='/var/www/pman/data/www/django_test/templates/less.css',
              debug=False)
register('all-css', less)

# scss_style = Bundle('/var/www/pman/data/www/django_test/templates/1.scss',
#               filters='scss', output='/var/www/pman/data/www/django_test/templates/scss.css',
#               debug=False)

# register('scss style', scss_style)