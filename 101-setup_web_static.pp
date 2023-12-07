# Manifest for setting up web servers for the deployment of web_static

# Update package repositories
package { 'nginx':
  ensure => 'installed',
}

# Create directories
file { '/data/web_static/releases/test/':
  ensure => 'directory',
}

file { '/data/web_static/shared/':
  ensure => 'directory',
}

# Create index.html
file { '/data/web_static/releases/test/index.html':
  content => 'Holberton School',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/',
  require => File['/data/web_static/releases/test/'],
}

# Set ownership
file { '/data/':
  recurse => true,
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Configure Nginx
file { '/etc/nginx/sites-available/default':
  content => "server {
  location /hbnb_static {
      alias /data/web_static/current/;
      index index.htm index.html;
  }
}",
  notify  => Service['nginx'],
}

# Restart Nginx
service { 'nginx':
  ensure    => 'running',
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
