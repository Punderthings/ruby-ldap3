# $Id: ruby-ldap.spec,v 1.13 2006/08/09 11:24:42 ianmacd Exp $

%define openldap %( rpm -q --qf '%%{version}' openldap | ruby -e 'puts gets.sub(/\\d+$/,"0")' )
# Build documentation if we have rdoc on the build system.
%define rdoc %( type rdoc > /dev/null && echo 1 || echo 0 )
Summary: LDAP API (RFC1823) library module for Ruby.
Name: ruby-ldap
Version: 0.9.20
Release: 1
License: Redistributable
Group: Applications/Ruby
Source: http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
URL: http://%{name}.sourceforge.net/
Packager: Ian Macdonald <ian@caliban.org>
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
* Wed Jul 11 21:58:38 UTC 2018 Alexey Chebotar <alexey.chebotar@gmail.com> 0.9.20-1
- 0.9.20
- Added support of LDAP_OPT_X_TLS_NEWCTX.
  Thanks to Kouhei Sutou.

* Mon Jun 20 14:30:52 UTC 2016 Alexey Chebotar <alexey.chebotar@gmail.com> 0.9.19-1
- 0.9.19
- Fixed parsing of LDIF with CR LF line separators (GH-38).
  Thanks to doppelreim.

* Fri Mar  4 11:17:21 UTC 2016 Alexey Chebotar <alexey.chebotar@gmail.com> 0.9.18-1
- 0.9.18
- backout issue32 to compile for ruby-1.8.x.
  Thanks to SUENAGA Hiroki.

* Fri Feb  6 08:51:09 UTC 2015 Alexey Chebotar <alexey.chebotar@gmail.com> 0.9.17-1
- 0.9.17
- Use ruby object to keep LDAP search result instead of libldap's data structure.
- Use macro Check_LDAPENTRY for assertion inside native extension codes.
- Remove assertion code from macro GET_LDAPENTRY_DATA.
  Thanks to SUENAGA Hiroki.

* Fri Sep  6 07:04:07 UTC 2013 Alexey Chebotar <alexey.chebotar@gmail.com> 0.9.16-1
- 0.9.16
- Fixed undefined method 'each' in LDAP::LDIF.mods_to_ldif (GH-26). Thanks to Francesco Malvezzi.

* Thu Aug 29 10:18:48 UTC 2013 Alexey Chebotar <alexey.chebotar@gmail.com> 0.9.15-1
- 0.9.15
- Accept nil for new_parent_dn for rename. Thanks to Kouhei Sutou.

* Wed Aug 28 13:21:53 UTC 2013 Alexey Chebotar <alexey.chebotar@gmail.com> 0.9.14-1
- 0.9.14
- Fixed option parsing bug for LDAP::Conn.sasl_bind. Thanks to Brian Leake.
- Added possibility to use :nocanon option in rb_ldap_conn_sasl_bind.
  See ldap_set_option(3) for more information. Thanks to Brian Leake.
- Added function conn.rename(dn, new_rdn, new_parent_dn, delete_old_rdn, sctrls, cctrls)  => self
  Modify the RDN of the entry with DN, dn, giving it the new RDN in parent new_parent_dn,
  new_rdn. If delete_old_rdn is true, the old RDN value will be deleted from the entry.
  Thanks to Marek Veber.
- Added option LDAP_OPT_NETWORK_TIMEOUT for openLDAP. Thanks to David Campbell.
- Fixed build error with GCC 4.8.1. Thanks to Kouhei Sutou.
- Add missing ldap_raname_s() function availability check. Thanks to Kouhei Sutou.

* Wed Jun  5 17:44:47 UTC 2013 Alexey Chebotar <alexey.chebotar@gmail.com> 0.9.13-1
- 0.9.13
- Prevent SyntaxError raised under Ruby 2.0.0 by line 107 regex
  (invalid multibyte escape). Thanks to Andrew Broman.

* Tue Dec 27 15:17:03 UTC 2011 Alexey Chebotar <alexey.chebotar@gmail.com> 0.9.12-1
- 0.9.12
- Enable client certificate authentication for mozilla ldap 6.0 only. Thank to Yuri Arabadji.
- New patch for LDAP::Mod data corruption. Thanks to Aprotim Sanyal.
- Modify mod_type dangling pointer corruption. Thank you, anon!
- Fixed bug in ldap/ldif.rb (GH-6). Thanks to bbense.
- Added functions: LDAP::Conn.open_uri(uri), LDAP::explode_dn(dn, notypes), LDAP::explode_rdn(rdn, notypes)
  Thanks to Marek Veber and Antonio Terceiro.
- Fixed many memory leaks. Thanks to Marek Veber and Antonio Terceiro.
- Fixed compile with ruby 1.9.2. Thanks to Hiroki Najima.
- On windows, the default ldap library became wldap32. Thanks to Hiroki Najima.

* Mon Mar 15 19:15:49 UTC 2010 Alexey Chebotar <alexey.chebotar@gmail.com> 0.9.11-1
- 0.9.11
- Allow passing SASL interaction options. Thanks to Anthony M. Martinez.

* Fri Jan 29 07:50:30 UTC 2010 Alexey Chebotar <alexey.chebotar@gmail.com> 0.9.10-1
- 0.9.10
- Added controls and referral extraction to #search_ext and 
  #search_ext2. Thanks to Michael Granger.

* Thu Jun 11 06:51:30 UTC 2009 Alexey Chebotar <alexey.chebotar@gmail.com> 0.9.9-1
_ 0.9.9
- Fixed LDAP::VERSION. Thanks to Kouhei Sutou
- Gem Packaging Support. Thanks to S. Potter [mbbx6spp]
- LDAP_OPT_X_TLS_PROTOCOL changed to LDAP_OPT_X_TLS_PROTOCOL_MIN
  (more information in ITS#5655). Thanks to Milos Jakubicek.
- Fixed regular expression in LDAP::Schema.attr()
	
* Thu Mar 25 08:45:02 UTC 2009 Alexey Chebotar <alexey.chebotar@gmail.com> 0.9.8-1
- 0.9.8
- Supported Ruby 1.9.x.

* Wed Aug  9 2006 Ian Macdonald <ian@caliban.org> 0.9.7-1
- 0.9.7
- Replacement and deletion operations did not work on Win32 systems.

* Tue Aug  1 2006 Ian Macdonald <ian@caliban.org> 0.9.6-1
- 0.9.6
- Fix segfault on AMD64 on FreeBSD.
- Minor documentation clarifications.

* Thu Apr 20 2006 Ian Macdonald <ian@caliban.org> 0.9.5-1
- 0.9.5
- The software now builds and works out of the box on Windows.

* Wed Mar  8 2006 Ian Macdonald <ian@caliban.org> 0.9.4-1
- 0.9.4
- Modify LDAP::Conn#search, LDAP::Conn#search2, LDAP::Conn#search_ext and
  LDAP::Conn#search_ext2 to treat LDAP_SIZELIMIT_EXCEEDED as success. After
  using any of these four methods, the user should check whether
  LDAP::Conn#err == LDAP::LDAP_SIZELIMIT_EXCEEDED. If true, the results set
  has been truncated by the server. Previously, LDAP_SIZELIMIT_EXCEEDED would
  raise an exception and no results would be returned, which is not the
  correct behaviour if the user has deliberately put a limit on the number of
  results to be returned, in order to spare the server.
- Duplicate code refactored.
- Missing RDoc documentation added for LDAP::Conn#err.

* Sat Feb 18 2006 Ian Macdonald <ian@caliban.org> 0.9.3-1
- 0.9.3
- LDAP::Schema#names and LDAP::Schema#attr will now allow names with hyphens
  and/or underscores.
- Silence a warning about @sasl_quiet when run in debug mode.
- Fix uninitialised data structures in LDAP::SSLConn#bind and
  LDAP::SSLConn#simple_bind.
- Build properly with OpenLDAP 2.3.
- Build-time options --with-ldap-incdir and --with-ldap-libdir have been
  replaced by --with-ldap-include and --with-ldap-lib. This is a consequence of
  making extconf.rb more standard.
- Windows build has been improved, so that it should now at least build without
  error. Whether it will work is another matter.

* Wed Jul  6 2005 Ian Macdonald <ian@caliban.org> 0.9.2-1
- 0.9.2
- Minor build problem fixed for certain architectures.
- For Conn#search, Conn#search2, Conn#search_ext and Conn#search_ext2,
  allow attrs to be a string, in which case it is treated as a single-element
  array.

* Tue Mar 15 2005 Ian Macdonald <ian@caliban.org> 0.9.1-1
- 0.9.1
- Conn#search, Conn#search2, Conn#search_ext2 and Conn#search_ext2 now accept
  only nil or an array for the attrs parameter.
- LDAP::Entry#[] is now an alias for LDAP::Entry#get_values.
- Conn#compare and Conn#compare_ext now return either true or false, rather
  than raising an LDAP::ResultError exception and indicating success or
  failure in the message.
- If an LDAP::Conn or LDAP::SSLConn connection becomes unbound, calling #bind,
  #simple_bind or #sasl_bind now reconnects to the server using the original
  parameters and then performs the bind. This allows one to rebind using new
  credentials.
- LDAP::Conn#bound? was throwing an exception when invoked on a Conn object on
  which an explicit #unbind had been performed. This has been fixed.
- Invoking LDAP::Conn#sasl_bind now sets the LDAP protocol to v3 if it is not
  already so. This is required for a SASL bind.
- LDAP::Conn#sasl_bind did not detect attempts to bind more than once. This is
  now done.
- SSLConn#open now throws a NotImplementedError exception. Previously, it
  would call the same method in the superclass, which would not work.
- Unused variables removed to silence gcc warnings.
- More unit tests and documentation fixes.
- ldap.so is now stripped.

* Wed Mar  2 2005 Ian Macdonald <ian@caliban.org> 0.9.0-1
- 0.9.0
- There is a new, fully functional LDIF module, complete with unit tests.
- In LDAP::Conn#add, LDAP::Conn#add_ext, LDAP::Conn#modify and
  LDAP::Conn#modify_ext, LDAP_MOD_BVALUES should be set when passing in a
  hash, in case there are mods containing binary values.
- LDAP::Conn#sasl_bind now returns nil when a block is passed to it, not self.
- The LDAP module, as well as the LDAP::Conn, LDAP::SSLConn, LDAP::Entry,
  LDAP::Mod, LDAP::Control and LDAP::Schema classes, now have extensive
  RDoc documentation.

* Mon Feb  7 2005 Ian Macdonald <ian@caliban.org> 0.8.4-1
- 0.8.4
- All patches from 0.8.3-[3-9] merged upstream into 0.8.4.

* Mon Dec  6 2004 Ian Macdonald <ian@caliban.org> 0.8.3-9
- New accessor LDAP::Conn#sasl_quiet silences OpenLDAP SASL messages when
  set to true. It is false by default.

* Thu Nov 18 2004 Ian Macdonald <ian@caliban.org> 0.8.3-8
- Issue a warning if an attempt is made to set the LDAP protocol version
  after a bind has taken place.
- Implement LDAP::Conn#bound?

* Sat Nov 13 2004 Ian Macdonald <ian@caliban.org> 0.8.3-7
- Controls patch now returns controls from both LDAP::Conn#search and
  LDAP::Conn#search2.

* Fri Nov 12 2004 Ian Macdonald <ian@caliban.org> 0.8.3-6
- Further refinement of controls patch, so that controls are now returned
  as the @controls attribute of the connection object.
- New patch to provide more grammatical error message.

* Thu Nov 11 2004 Ian Macdonald <ian@caliban.org> 0.8.3-5
- Improve patch to allow controls to be duped or cloned.
- Add ldap/control.rb to extend the usefulness of controls.

* Tue Nov  9 2004 Ian Macdonald <ian@caliban.org> 0.8.3-4
- Patch to allow setting and retrieving of LDAP controls.

* Mon Nov  8 2004 Ian Macdonald <ian@caliban.org> 0.8.3-3
- Patch to fix setting of OID when LDAP controls are created.

* Sat Nov  6 2004 Ian Macdonald <ian@caliban.org> 0.8.3-2
- Build with specific OpenLDAP dependencies, as .so version changed in
  OpenLDAP 2.2.x.

* Wed Oct 20 2004 Ian Macdonald <ian@caliban.org> 0.8.3-1
- SASL GSSAPI patch removed, since it's been merged upstream.
- Patch incorrect library version.

* Sun Dec 14 2003 Ian Macdonald <ian@caliban.org> 0.8.2-4
- Further refine saslconn.c patch

* Thu Dec 11 2003 Ian Macdonald <ian@caliban.org> 0.8.2-3
- Further refine saslconn.c patch

* Thu Dec 11 2003 Ian Macdonald <ian@caliban.org> 0.8.2-2
- Patch saslconn.c to allow GSSAPI via SASL

* Sun Dec  7 2003 Ian Macdonald <ian@caliban.org> 0.8.2-1
- 0.8.2

* Sun Oct 19 2003 Ian Macdonald <ian@caliban.org> 0.8.1-1
- 0.8.1

* Mon Mar 17 2003 Ian Macdonald <ian@caliban.org>
- 0.8.0

* Tue Jul 30 2002 Ian Macdonald <ian@caliban.org>
- 0.7.2

* Fri Jul 19 2002 Ian Macdonald <ian@caliban.org>
- 0.7.1

* Tue Jul  2 2002 Ian Macdonald <ian@caliban.org>
- Add BuildRequires for openssl-devel and openldap-devel

* Sun Jun  2 2002 Ian Macdonald <ian@caliban.org>
- 0.7.0

* Mon Apr 29 2002 Ian Macdonald <ian@caliban.org>
- Simplified install section

* Fri Apr  5 2002 Ian Macdonald <ian@caliban.org>
- Added test directory to docs

* Tue Apr  2 2002 Ian Macdonald <ian@caliban.org>
- 0.6.1

* Wed Mar 13 2002 Ian Macdonald <ian@caliban.org>
- 0.6.0

* Mon Jan  7 2002 Ian Macdonald <ian@caliban.org>
- 0.5.0
