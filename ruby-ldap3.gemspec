require 'rubygems'

Gem::Specification.new do |s|
  s.platform = Gem::Platform::RUBY
  s.name = 'ruby-ldap3'
  s.version = '0.10.0'
  s.summary = 'Ruby/LDAP is an extension module for Ruby'
  s.description = <<-EOF
It provides the interface to some LDAP libraries (e.g. OpenLDAP, Netscape SDK and Active Directory). The common API for application development is described in RFC1823 and is supported by Ruby/LDAP.
  EOF
  s.authors = ['Shane Curcuru', 'Alexey.Chebotar']
  s.email = 'shane@punderthings.com'
  s.homepage = 'https://github.com/Punderthings/ruby-ldap3'
  s.licenses = [ 'BSD-3-Clause', 'Nonstandard' ]

  s.require_path = 'lib'

  s.files = [ 'ChangeLog', 'COPYING', 'FAQ', 'NOTES', 'README', 'TODO', 'LICENSE' ]
  s.files += Dir.glob('**/*.rb')
  s.files += Dir.glob('**/*.h')
  s.files += Dir.glob('**/*.c')
  s.files += Dir.glob('**/*.def')

  s.extensions = ['extconf.rb']
end
