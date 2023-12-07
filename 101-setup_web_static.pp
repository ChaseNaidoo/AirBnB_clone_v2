# Manifest for setting up web servers for the deployment of web_static

# Update configuration
$nginx_conf = "server {
    location /hbnb_static {
            alias /data/web_static/current/;
            index index.htm index.html;
    }
}"

package { 'nginx':
    ensure => 'latest',
    provider => 'apt'
} ->

file { '/data/web_static/shared/':
    ensure => 'directory',
} ->

file { '/data/web_static/releases/test/index.html':
    ensure  => 'file',
    content => 'Holberton School',
} ->

file { '/data/web_static/current':
    ensure => 'link',
    target => '/data/web_static/releases/test/',
    force  => true,
    owner  => 'ubuntu',
    group  => 'ubuntu',
} ->

file { '/etc/nginx/sites-available/default':
    ensure  => 'file',
    content => $nginx_conf,
    require => File['/data/web_static/current'],
    notify  => Service['nginx'],
} ->

service { 'nginx':
    ensure    => 'running',
    enable    => true,
    require   => File['/etc/nginx/sites-available/default'],
    subscribe => File['/etc/nginx/sites-available/default'],
}
