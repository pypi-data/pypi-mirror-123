================
FAB CoreUI Theme
================


.. image:: https://img.shields.io/pypi/v/fab_coreui_theme.svg
        :target: https://pypi.python.org/pypi/fab_coreui_theme

CoreUI theme for FlaskAppbuilder

This theme is still *very much* a WIP. If you'd like to use it take a look at the `fab_coreui_theme/templates/coreui/init.html` and start overriding the blocks to make it your own.


Usage
------

This theme is meant to be with used with FlaskAppbuilder_. Just grab the coreui_bp from fab_coreui_theme and you're ready to use the views. Here is an example app.

QuickStart
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

	from flask_appbuilder.models.sqla.interface import SQLAInterface
	from fab_coreui_theme.fab_coreui_theme import CoreUIBaseView, CoreUIModelView, CoreUISimpleFormView, coreui_bp
	# Make sure you import your app and register the blueprint!
	from .www import app
	app.register_blueprint(coreui_bp)

	# Create a base view that inherits from CoreUIBaseView
	class MyView(CoreUIBaseView):

		default_view = 'blank'
		@expose('/blank')

		@has_access
		def blank(self):
			return self.render_template(
				'coreui/init.html'
			)

	# Register the view with AppBuilder
	appbuilder.add_view(MyView, "My View", category='My View')


Bootstrap the Flask App
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Make sure the FlaskAppbuilder is used. If you used the fab cli to initialize the project it should be in there somewhere.

.. code-block:: python

	import logging

	from flask import Flask
	from flask_appbuilder import AppBuilder, SQLA
	from flask_appbuilder.menu import Menu


	logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
	logging.getLogger().setLevel(logging.DEBUG)

	app = Flask(__name__)
	app.config.from_object("config")
	db = SQLA(app)

	appbuilder = AppBuilder(
		app,
		db.session,
		menu=Menu(reverse=False),
	)

	from . import views  # noqa


This registers the CoreUI Flask_ Blueprint. (This is only shown here for reference.)

.. code-block:: python

	# This is only shown for reference.
	TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), 'templates')
	STATIC_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
	STATIC_URL_PATH = '/static/coreui'

	# Use the Flask Blueprint to create an appized app and setup our routing
	# https://flask.palletsprojects.com/en/2.0.x/blueprints/#templates

	coreui_bp = Blueprint(
		'coreui_theme', __name__,
		template_folder=TEMPLATE_FOLDER,
		static_folder=STATIC_FOLDER,
		static_url_path=STATIC_URL_PATH
	)


Then in  your HTML templates you can bring in the static files relative to `static`  -

.. code-block:: python

	{{url_for('coreui_theme.static',filename='coreui/node_modules/@coreui/coreui/dist/js/coreui.bundle.min.js')}}


Example Base View
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

	from flask_appbuilder.models.sqla.interface import SQLAInterface
	from fab_coreui_theme.fab_coreui_theme import CoreUIBaseView, CoreUIModelView, CoreUISimpleFormView, coreui_bp
	# Make sure you import your app and register the blueprint!
	from .www import app
	app.register_blueprint(coreui_bp)

	# Create a base view that inherits from CoreUIBaseView
	class MyView(CoreUIBaseView):

		default_view = 'blank'
		@expose('/blank')

		@has_access
		def blank(self):
			return self.render_template(
				'coreui/init.html'
			)

	# Register the view with AppBuilder
	appbuilder.add_view(MyView, "My View", category='My View')

Example Form View
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

	from flask_appbuilder.fieldwidgets import BS3TextFieldWidget
	from flask_appbuilder.forms import DynamicForm
	from flask_babel import lazy_gettext
	from wtforms import StringField
	from wtforms.validators import DataRequired
	from fab_coreui_theme.fab_coreui_theme import CoreUIBaseView, CoreUIModelView, CoreUISimpleFormView, coreui_bp
	# Make sure you import your app and register the blueprint!
	from .www import app
	app.register_blueprint(coreui_bp)


	# Declare the Form
	class TestForm(DynamicForm):
	    TestFieldOne = StringField(
			lazy_gettext("Test Field One"),
			validators=[DataRequired()],
			widget=BS3TextFieldWidget(),
	    )
	    TestFieldTwo = StringField(
			lazy_gettext("Test Field One"),
			validators=[DataRequired()],
			widget=BS3TextFieldWidget(),
	    )


	# Create the Form View and inherit from the CoreUISimpleFormView
	class TestFormView(CoreUISimpleFormView):
	    form = TestForm
	    form_title = "This is my Test Form"
	    default_view = "this_form_get"
	    message = "My form submitted"

	    def form_post(self, form):
			# process form
			flash(as_unicode(self.message), "info")

	# Register the view
	appbuilder.add_view(TestFormView, "My form View",
						icon="fa-group", label="My Test form")


Example Model View
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

	from flask_appbuilder.models.sqla.interface import SQLAInterface
	from fab_coreui_theme.fab_coreui_theme import CoreUIBaseView, CoreUIModelView, CoreUISimpleFormView, coreui_bp
	# Make sure you import your app and register the blueprint!
	from .www import app
	app.register_blueprint(coreui_bp)


	class ProductModelView(CoreUIModelView):
	    datamodel = SQLAInterface(ProductModel)

	appbuilder.add_view(ProductModelView, "Products",
						icon="fa-group", label="Products")



Extending
-----------------

If you see something you don't like you can customize it by overriding the blocks in the templates.

Customization - Flask AppBuilder - Server Side
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See the `Flask AppBuilder docs on Customization <https://flask-appbuilder.readthedocs.io/en/latest/templates.html#>`_ to customize the theme. You can fork this project, or create a new project that overrides blocks and templates.

In your app create a `templates/mytheme/index.html` file.

Override a block entirely -

.. code-block:: html

	{% extends "coreui/init.html" %}

	{% block content %}
		<h1>My content!</h1>
	{% endblock %}

Extend a block -

.. code-block:: html

	{% extends "coreui/init.html" %}

	{% block content %}
		{{ super() }}
		<h1>My content!</h1>
	{% endblock %}

See the `fab_coreui_theme/templates/coreui/init.html` for the menus, breadcrumbs, and sidebars.

Please note that menus are not implemented the way they are in FlaskAppbuilder and registering a view does not populate the menus.

Further Customization - CoreUI - Front End
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some relevant docs:

- `CoreUI Docs <https://coreui.io/docs/getting-started/introduction/>`_
- `Theming <https://coreui.io/docs/getting-started/theming/>`_
- `Build Tools <https://coreui.io/docs/getting-started/build-tools/>`_
- `Web Pack <https://coreui.io/docs/getting-started/webpack/>`_
- `CoreUI Layout <https://coreui.io/docs/layout/overview/>`_
- `CoreUI Icons <https://icons.coreui.io/icons/>`_


Install the javascript node_modules.

.. code-block:: bash

	# Clone or fork the repo and clone it locally
	cd fab_coreui_theme/coreui_theme/static
	npm install

	# or use the MakeFile - make npm-install

If this command gives you trouble try removing the package-lock.json and deleting the node_modules folder.

Then you can reference the js and css files as:

.. code-block:: html

	<script src="{{url_for('coreui_theme.static',filename='coreui/node_modules/thing.js')}}"></script>
	<link
        href="{{url_for('coreui_theme.static',filename='coreui/node_modules/thing.css')}}"
        rel="stylesheet"
      />


Licenses
----------

* Free software: MIT license
* Documentation: https://fab-coreui-theme.readthedocs.io.

Features
--------

* CoreUI Theme - Flask Blueprint
* CoreUI Theme - Flask AppBuilder BaseView
* CoreUI Theme - Flask AppBuilder ModelView
* CoreUI Theme - Flask AppBuilder SimpleFormView

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template. It makes use of Flask AppBuilder and CoreUI.

.. _Flask: https://flask.palletsprojects.com/en/2.0.x/blueprints/#templates
.. _FlaskAppbuilder: https://flask-appbuilder.readthedocs.io/en/latest/templates.html
.. _CoreUI: https://coreui.io/
.. _CoreUIIcons: https://icons.coreui.io/icons/
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage