from datetime import datetime

from fabric.api import cd, run, env, local, hide, settings
from fabric.operations import get
from fabric.contrib import django
from fabvenv import virtualenv


def staging():
    env.hosts = ['']
    env.path = '/srv/wechange.sinnwerkstatt.com/wechange'
    env.virtualenv_path = '/srv/wechange.sinnwerkstatt.com/wechangeenv/'
    env.backup_path = '/srv/wechange.sinnwerkstatt.com/backups'
    env.maintenance_mode_path = '/srv/wechange.sinnwerkstatt.com/maintenance_mode'
    env.push_branch = 'staging'
    env.push_remote = 'origin'
    env.reload_cmd = 'sudo supervisorctl restart %s'
    env.stop_cmd = 'sudo supervisorctl stop %s'
    env.start_cmd = 'sudo supervisorctl start %s'
    env.restart_db_cmd = 'service postgresql restart'
    env.supervisor_instances = ['wechange', 'kiel',]
    env.portal_instances = env.supervisor_instances
    env.special_requirements = 'requirements_staging.txt'
    env.db_name = 'wechange'
    env.db_username = 'wechange'
    env.after_deploy_url = 'http://wechange.sinnwerkstatt.com'
    
def production():
    env.hosts = ['']
    env.path = '/srv/wechange/neww'
    env.virtualenv_path = '/srv/wechange/wechangeenv/'
    env.backup_path = '/srv/wechange/backups'
    env.maintenance_mode_path = '/srv/maintenance_mode'
    env.push_branch = 'master'
    env.push_remote = 'origin'
    env.reload_cmd = 'supervisorctl restart %s'
    env.stop_cmd = 'supervisorctl stop %s'
    env.start_cmd = 'supervisorctl start %s'
    env.restart_db_cmd = 'service postgresql restart'
    env.supervisor_instances = ['wachstumswende', 'netzwerkn', 'wechange', 'klarzurwende', 'energiebuerger', 'zukunftsmacher', 'unternehmensgruen']
    env.portal_instances = env.supervisor_instances
    env.special_requirements = 'requirements_production.txt'
    env.db_name = 'wechange'
    env.db_username = 'wechange'
    env.after_deploy_url = 'https://wachstumswende.de'

def root():
    production()
    env.hosts = ['root@wachstumswende.de']


def restart():
    for portal in env.supervisor_instances:
        run(env.reload_cmd % portal)

def stop():
    for portal in env.supervisor_instances:
        run(env.stop_cmd % portal)

def start():
    for portal in env.supervisor_instances:
        run(env.start_cmd % portal)
        
def restart_db():
    run(env.restart_db_cmd)
    
def maintenance_on():
    with cd(env.maintenance_mode_path):
        run("mv maintenance_mode_off maintenance_mode_on")

def maintenance_off():
    with cd(env.maintenance_mode_path):
        run("mv maintenance_mode_on maintenance_mode_off")

def migrate():
    with virtualenv(env.virtualenv_path):
        #run("%(path)s/manage.py syncdb" % env)
        run("%(path)s/manage.py migrate --fake-initial" % env)

def ping():
    run("echo %(after_deploy_url)s returned:  \>\>\>  $(curl --write-out %%{http_code} --silent --output /dev/null %(after_deploy_url)s)" % env)


def _run_deploy(do_update_requirements=True):
    with cd(env.path):
        run("git pull %(push_remote)s %(push_branch)s" % env)
        with virtualenv(env.virtualenv_path):
            if do_update_requirements:
                run("pip install -Ur %(special_requirements)s" % env)
                
                
def collectstatic():        
    with cd(env.path):
        with virtualenv(env.virtualenv_path):    
            if env.portal_instances:
                for portal in env.portal_instances:
                    # this will collect the staticfiles for each portal into a seperate folder
                    # nginx or whichever server will need to point each subdomain to their
                    # respective folder to serve static files
                    run("./manage.py collectstatic --noinput --cosinnus-portal %s" % portal)
            else:
                run("./manage.py collectstatic --noinput")

def compile_less():
    with virtualenv(env.virtualenv_path):
        run("lessc --clean-css %(virtualenv_path)ssrc/cosinnus/cosinnus/static/less/cosinnus.less %(virtualenv_path)ssrc/cosinnus/cosinnus/static/css/cosinnus.css" % env)

def compile_webpack():
    with virtualenv(env.virtualenv_path):
        with cd("%(virtualenv_path)ssrc/cosinnus/" % env):
            run("npm install")
            run("npm run production") # -->can also run "npm run dev", but it stays in watch mode
            
def backup():
    with cd(env.backup_path):
        run("pg_dump -Fc -U %(db_username)s %(db_name)s > %(db_name)s_backup_$(date +%%F-%%T).sql" % env)
        run("ls -lt")

def rebuild_index():
    with virtualenv(env.virtualenv_path):
        run("%(path)s/manage.py rebuild_index -v 2" % env)

def update_index():
    with virtualenv(env.virtualenv_path):
        run("%(path)s/manage.py update_index -v 2" % env)

def clear_cache():
    """ Restarts the memcache instances. Needs to be run with ```fab root clear_cache``` """
    run("/etc/init.d/memcached restart")

def pipfreeze():
    with cd(env.path):
        with virtualenv(env.virtualenv_path):
            run("pip freeze")

def deploy(do_maintenance=True):
    """ Main deploy command, will do the following in order: 
          * pull up a maintenance notice page
          * stop the servers
          * do a DB backup
          * pull from git
          * pip update
          * migrate
          * start the servers
          * remove the maintenance notice page """
    if do_maintenance:
        maintenance_on()
    stop()
    backup()
    _run_deploy(do_update_requirements=True)
    compile_less()
    compile_webpack()
    collectstatic()
    # restart_db()
    migrate()
    start()
    if do_maintenance:
        maintenance_off()

def deploy_nomaint():
    deploy(do_maintenance=False)
    
def hotdeploy():
    """ Fast deploy with pip update and soft server restarts. No migrating done. """
    _run_deploy(do_update_requirements=True)
    compile_less()
    compile_webpack()
    collectstatic()
    migrate()
    restart()
    
def hotdeploy_noreq():
    """ Fast deploy with soft server restarts. No migrating or pip update done. """
    _run_deploy(do_update_requirements=False)
    collectstatic()
    restart()
    
