%define		snap	20090303
Summary:	POHMELFS userspace server
Summary(pl.UTF-8):	-
Name:		pohmelfs-server
Version:	0.%{snap}
Release:	0.1
License:	GPL
Group:		Applications
# http://www.ioremap.net/cgi-bin/gitweb.cgi?p=pohmelfs-server.git;a=snapshot;h=d7d71622d11d83a7561c364e0456e211882da8ac
Source0:	%{name}-%{snap}.tar.gz
# Source0-md5:	8de864c0d08c72c5f42a512a409e70dd
# http://www.ioremap.net/cgi-bin/gitweb.cgi?p=pohmelfs.git;a=tree;f=fs/pohmelfs;h=e9d065bc52109e58aac854dc8694aa266b5f8b02;hb=1050c802c95b592d853616f72b78db5bb8e96e81
Source1:	%{name}-netfs.h
URL:		http://www.ioremap.net/projects/pohmelfs
%if %{with initscript}
BuildRequires:	rpmbuild(macros) >= 1.228
Requires(post,preun):	/sbin/chkconfig
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
POHMELFS userspace server.

%description -l pl.UTF-8

%prep
%setup -q -n %{name}.git
install -D %{SOURCE1} fs/pohmelfs/netfs.h

%build
%{__make} \
	CC=%{__cc} \
	KDIR=.

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sbindir}
install cfg flush fserver $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with initscript}
%post init
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun init
if [ "$1" = "0" ]; then
	%service -q %{name} stop
	/sbin/chkconfig --del %{name}
fi
%endif

%files
%defattr(644,root,root,755)
%doc README

%attr(755,root,root) %{_sbindir}/*

%if %{with initscript}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%endif
