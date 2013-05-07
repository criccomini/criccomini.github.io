from fabric.api import *

env.hosts = ['riccomini.name']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa-pstam-keypair'

html_path = '/var/www/html/riccomini.name'

def setup():
  """ One-time setup for an Ubuntu EC2 instance. """
  sudo('apt-get install nginx')
  put('config/nginx-riccomini.conf', '/etc/nginx/conf.d', use_sudo=True)
  sudo('service nginx restart')

def release():
  """ Build and push the current build. """
  local('jekyll --no-auto')
  sudo('rm -rf %s' % html_path)
  sudo('mkdir -p %s' % html_path)
  put('./_site/*', html_path, use_sudo=True)