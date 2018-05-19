![ecobasa logo](http://cloud.ecobasa.org/public.php?service=files&t=976069b03a5d7f4153c5cfc16e7ab309&download)

Repository of the future http://ecobasa.org

# Requisites
* Django (Python)
* PostgreSQL
* LESS (use node.js Grunt or Compass to compile CSS)

wechange
=========================

This is the base project for wechange. It is mainly a configurable shell for the actual wechange apps, which are pluggable components. Most of the actual code resides in "cosinnus-core". See `requirements_staging.txt` for a full list of internal apps.

Note: The wechange project is often refered to as "neww" in code and imports and the internal apps and python Objects are named "cosinnus" for historical reasons. 

# How to set up local development for wechange

This will set up a local development envirenment, getting you ready to work on wechange and all its internal apps.

Note: Wechange still runs on Python 2.7.15 using Django 1.8, but we are in the process of upgrading to Python 3 and Django >= 2.0!


### Install PostgresSql 

* Install PostgreSql for your system 
* Create new psql database. Name it "wechange" or similar and note its password and user
  * you can use the root psql user, but we advise you to use a different one
  
### Install Python, Pip and Virtualenv
 
* Install python 2.7.15. Please refer to external guides if you are unsure how to do this for your system!
  * It is important that the python version is 2.7.15 exactly!
* `pip install --upgrade pip` - Upgrade pip. Don't skip this step!
* `pip install virtualenv` - Install virtualenv

### Install Git

* Install a git client. Please refer to external guides if you are unsure how to do this for your system!

### Create a virtualenv and project folders
 
* `virtualenv <your-path>/wechangeenv` - create your virtualenv once
* `source <your-path>/wechangeenv/bin/activate` - activate your wechange virtualenv (do this in every new console when working on wechange)
* `mkdir <your-project-folder>/wechange-source` - create the new wechange project location
* `cd <your-project-folder>/wechange-source`

### Get the wechange and cosinnus source code

* `git clone git@git.sinnwerkstatt.com:wechange/wechange.git wechange`
* `./ecobasa/local_install.sh | tee install.log`

### Set up the local wechange source and install all dependencies

* `./ecobasa/local_setup.sh | tee setup.log`
  * This sets up all of the cosinnus-projects into individual folders and runs "python setup.py develop". This means that the source of the cosinnus dependency is localized in the same directory, and you can edit the files in there as if it were a source directory.
* `pip install -r wechange/requirements_local.txt | tee reqs.log`
  
**Notes:** 

* For wechange, we install the full set of dependencies via requirements.txt files. These are also used during our deployment and there are different files for local, staging and production environments.
* We tee the stdout so you can see errors more clearly.
* Deal with any errors you encounter here! Only move to the next step if you do not get any errors. Warnings are usually ok.
  * Especially Pillow and some other dependencies are known to cause trouble on some systems! 
  * if you see any compile errors, often time the solution is to install the offending dependency using a pip Wheel for your system.

### Configure up your local wechange projects

* `cd wechange`
* `cp neww/settings_local.py neww/settings.py`
* Edit `neww/settings.py`:
  * replace the database settings in ``DATABASES['default']``: 
    * NAME, USER, PASSWORD: based on how you created your psql database
  * (this settings.py file is in .gitignore)

### One-Time Django Setup 
  
* `./manage.py migrate` - creates all the empty database tables
* `./manage.py createsuperuser` - create your own user account
  * enter the credentials for your local user
  * the username doesn't matter, you will log in using the email as credential

### First-Time Wechange Setup

* navigate to `http://localhost:8000/admin` and log in with the email address and password you just created
  * navigate to `http://localhost:8000/admin/sites/site/1/` and change the default Site to 
    * domain: localhost:8000
    * name: Local Site (or anything you wish)
* restart the server using "ctrl+c" and `./manage.py runserver`

### First-Time Wagtail Setup

We use Wagtail as CMS, and it will show up automatically as a root URL dashboard. You can skip this step configuring it, but all you will see on your root URL will be a blank page. Navigate to a page like `http://localhost:8000/projects/` to see the wechange-page.

* navigate to `http://localhost:8000/cms-admin/pages/`
  * Delete the page "Welcome to your new Wagtail Site"
  * create new Subpage on the root level
    * Tab Inhalt (de): Title: enter "Root"
    * Tab Förderung: Kurtitel (slug): enter "root"
    * Tab Einstellungen: Portal: choose "Default Portal"
    * below in the drop-up: Click "Publish"
  * Hover over the new "Root" page and click "Add new Subpage"
    * Choose "Start-Page: Modular"
    * Tab Inhalt (de): Title: enter "Dashboard"
    * Tab Förderung: Kurtitel (slug): enter "dashboard"
    * below in the drop-up: Click "Publish"
  * In the left side menu, go to Settings > Sites
    * click "Add Site"
    * Hostname: localhost:8000
    * Port: 8000
    * click Choose Origin Site:
      * Navigate below Root using ">", choose page "Dashboard"
    * Check "Default Site" on
    * click "Save"
* navigate to `http://localhost:8000/`, you should see the blank CMS dashboard. 
  * Its content can be edited in the "Dashboard" Page you just created in http://localhost:8000/cms-admin/pages/. 

### Check if you're up-and-running and create the Forum Group

* navigate to `http://localhost:8000/groups/`
* click "Create Group" in the left sidebar
  * enter Group Name: "Forum" (must be exact!)
  * click "Save" below
* If you get redirected to the Forum's Group Dashboard and "Forum" appears in the top navigation bar, you're all set!


# Git Structure

NEWW pulls Cosinnus-core and all cosinnus apps in directly from their Git repositories. See `requirements_staging.txt` for the repo locations and used branches.

# Deployment

Deployment is automated with a comprehensive fab-file. Check wechange/fabfile.py!

When deploying using `fab staging`, the wechange and **all** the cosinnus projects will be deployed using their staging-branches! Same goes for production.

* To deploy to staging use:
  * `fab staging deploy` for a full deploy, shutting down the server, creating a database snapshot, and pulling up an "Under Maintenance" blanket on all URLs.
  * `fab staging hotdeploy` for a non-interruptive deploy. This is faster, creates no backups, and lets the site run as usual.
    * Note: **hotdeploy** should never be used when new database migrations are being pushed!


Set up the special group
------------------------

Edit your local settings.py for ECOBASA_SPECIAL_COSINNUS_GROUP to point to the
primary key of the special group every pioneer will become a member of and
whose blog posts are exposed. You will have to do that after setting up the
group in the admin interface.


We use LESS - CSS has to be compiled
------------------------------------
You can use grunt with node.js. Package.json will install all necessary dependencies, just type
	$ npm install