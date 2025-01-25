# $Id: ruby-ldap.spec,v 1.13 2006/08/09 11:24:42 ianmacd Exp $

%define openldap %( rpm -q --qf '%%{version}' openldap | ruby -e 'puts gets.sub(/\\d+$/,"0")' )
# Build documentation if we have rdoc on the build system.
%define rdoc %( type rdoc > /dev/null && echo 1 || echo 0 )
Summary: LDAP API (RFC1823) library module for Ruby.
Name: ruby-ldap3
Version: 0.10.1
Release: 1
License: BSD-3-Clause
Group: Applications/Ruby
Source: https://github.com/Punderthings/ruby-ldap3/
URL: https://github.com/Punderthings/ruby-ldap3/
Packager: Shane Curcuru <shane@punderthings.com>
BuildRoot: /var/tmp/%{name}-%{version}
BuildRequires: ruby, ruby-devel, openssl-devel, openldap-devel >= %{openldap}
Requires: ruby, openssl, openldap >= %{openldap}

%description
Ruby/LDAP is an extension module for Ruby. It provides the interface to some
LDAP libraries (for example, OpenLDAP, UMich LDAP, Netscape SDK and
ActiveDirectory). The common API for application development is described in
RFC1823 and most libraries comply with it. Ruby/LDAP supports those libraries.

%prep
%setup

%build
ruby extconf.rb
make
strip ldap.so

%clean 
rm -rf $RPM_BUILD_ROOT

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
%if %{rdoc}
  rdocpath=`ruby -rrdoc/ri/ri_paths -e 'puts RI::Paths::PATH[1] ||
					     RI::Paths::PATH[0]'`
  rdoc -r -o $RPM_BUILD_ROOT$rdocpath -x CVS *.c lib
  rm $RPM_BUILD_ROOT$rdocpath/created.rid
%endif
find $RPM_BUILD_ROOT -type f -print | \
  ruby -pe 'sub(%r(^'$RPM_BUILD_ROOT'), "")' > %{name}-%{version}-filelist
%if %{rdoc}
  echo '%%docdir' $rdocpath >> %{name}-%{version}-filelist
%endif

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc ChangeLog FAQ README* TODO
%doc example/ test/

%changelog
Sun Jan 25 08:00:00 UTC 2024 Shane Curcuru <shane@punderthings.com>
	 * Forked from bearded/ruby-ldap at 3cfab0fd05c9fdf4c92c60d52457a6dadad4c8c0
	 * Renaming to ruby-ldap3 to avoid conflicts
	 * Applying existing PRs on bearded to run on Ruby 3.x
   * For earlier ChangeLog see https://github.com/bearded/ruby-ldap/blob/master/ChangeLog
