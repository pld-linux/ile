#
# TODO:
# - more clean init script ? (especially ile.sh),

%include        /usr/lib/rpm/macros.perl
Summary:	Email notify for Jabberd2 (ILoveEmail)
Summary(pl):	Modu³ powiadamiania o poczcie dla Jabberd2
Name:		ile
Version:	0.4
Release:	1.1
License:	GPL
Group:		Applications/Communications
Source0:	http://jabberstudio.org/projects/ile/releases/%{name}-%{version}.tar.gz
# Source0-md5:	120bff223043e0af1da48aa321206836
Source1:	jabber-ile-transport.init
Source2:	%{name}.sh
Patch0:		%{name}-jabberd2.patch
Patch1:		%{name}-config.patch
URL:		http://jabberstudio.org/projects/ile
BuildRequires:	rpm-perlprov
Requires(pre):	jabber-common
Requires(post,preun):	/sbin/chkconfig
Requires(post):	/usr/bin/perl
Requires:	jabberd >= 2.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
I Love Email - email notify for Jabberd2.

%description -l pl
I Love Email - powiadamianie o poczcie dla Jabberd2.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/jabber,%{_sbindir},/etc/rc.d/init.d,/var/lib/jabber/ile,/var/log/ile}

install ile.xml $RPM_BUILD_ROOT%{_sysconfdir}/jabber/ile.xml
install ile.pl $RPM_BUILD_ROOT%{_sbindir}
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/jabber-ile-transport
install %{SOURCE2} $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /etc/jabber/secret ] ; then
	SECRET=`cat /etc/jabber/secret`
	if [ -n "$SECRET" ] ; then
		echo "Updating component authentication secret in ile.xml..."
		perl -pi -e "s/>secret</>$SECRET</" /etc/jabber/ile.xml
	fi
fi
/sbin/chkconfig --add jabber-ile-transport
if [ -r /var/lock/subsys/jabber-ile-transport ]; then
	/etc/rc.d/init.d/jabber-ile-transport restart >&2
else
	echo "Run \"/etc/rc.d/init.d/jabber-ile-transport start\" to start Jabber ILE transport."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -r /var/lock/subsys/jabber-ile-transport ]; then
		/etc/rc.d/init.d/jabber-ile-transport stop >&2
	fi
	/sbin/chkconfig --del jabber-ile-transport
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog
%attr(755,root,root) %{_sbindir}/*
%attr(640,root,jabber) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/jabber/ile.xml
%attr(754,root,root) /etc/rc.d/init.d/jabber-ile-transport
%attr(770,root,jabber) /var/lib/jabber/ile
%attr(770,root,jabber) /var/log/ile
