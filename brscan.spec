# TODO: place SANE drivers in sane-backend-* package
Summary:	Brother scanner driver
Summary(pl.UTF-8):	Sterownik do skanerów Brother
Name:		brscan
Version:	0.2.3
Release:	1
License:	GPL v2+/proprietary binary modules
Group:		Applications
Source0:	http://solutions.brother.com/Library/sol/printer/linux/rpmfiles/sane_source/%{name}-src-%{version}.tar.gz
# Source0-md5:	99a7f21fc15661690b296023253bcca6
Patch0:		%{name}-fixes.patch
Patch1:		%{name}-paths.patch
URL:		http://solutions.brother.com/linux/sol/printer/linux/sane_drivers.html
BuildRequires:	autoconf >= 2.10
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	ncurses-devel
Requires:	sane-backends
ExclusiveArch:	%{ix86} %{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Scanner driver for Brother MFC printers, both USB and network.

%description -l pl.UTF-8
Sterownik skanera dla drukarek Brother MFC, zarówno USB jak i
sieciowych.

%prep
%setup -q -n %{name}-src-%{version}
%patch0 -p1
%patch1 -p1

rm -f brscan/{acinclude.m4,configure}

%{__make} -C brscan/lib clean
%{__make} -C brscan/sanei clean

%build
cd brscan
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
	--disable-static
%{__make} -C lib
%{__make} -C netconfig
%{__make} -C sanei
%{__make} -C backend_brscan
%{__make} -C backend_brscan2

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir}/sane,%{_datadir}/brscan,%{_sysconfdir}/brscan,/var/log/brscan}

libtool --mode=install install brscan/backend_brscan/libsane-brother.la $RPM_BUILD_ROOT%{_libdir}/sane
libtool --mode=install install brscan/backend_brscan2/libsane-brother2.la $RPM_BUILD_ROOT%{_libdir}/sane
libtool --mode=install install brscan/netconfig/brsaneconfig $RPM_BUILD_ROOT%{_sbindir}
libtool --mode=install install brscan/netconfig/brsaneconfig2 $RPM_BUILD_ROOT%{_sbindir}

rm -f $RPM_BUILD_ROOT%{_libdir}/sane/*.la

%ifarch %{ix86}
install brscan/libbrcolm/libbrcolm.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}
install brscan/libbrcolm2/libbrcolm2.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}
install brscan/libbrscandec/libbrscandec.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}
install brscan/libbrscandec2/libbrscandec2.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}
%endif
%ifarch %{x8664}
install brscan64/libbrcolm/libbrcolm.so.1.0.1 $RPM_BUILD_ROOT%{_libdir}
install brscan64/libbrcolm2/libbrcolm2.so.1.0.1 $RPM_BUILD_ROOT%{_libdir}
install brscan64/libbrscandec/libbrscandec.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}
install brscan64/libbrscandec2/libbrscandec2.so.1.0.0 $RPM_BUILD_ROOT%{_libdir}
%endif

cp -rf brscan/libbrcolm/GrayCmData $RPM_BUILD_ROOT%{_datadir}/brscan
cp -rf brscan/libbrcolm2/GrayCmData/* $RPM_BUILD_ROOT%{_datadir}/brscan/GrayCmData
install brscan/mk_package/Brsane*.ini $RPM_BUILD_ROOT%{_datadir}/brscan
install brscan/mk_package/brsanenetdevice*.cfg $RPM_BUILD_ROOT%{_sysconfdir}/brscan

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc brscan/copying.brother
%attr(755,root,root) %{_sbindir}/brsaneconfig
%attr(755,root,root) %{_sbindir}/brsaneconfig2
%attr(755,root,root) %{_libdir}/libbrcolm.so.*.*.*
%attr(755,root,root) %{_libdir}/libbrcolm2.so.*.*.*
%attr(755,root,root) %{_libdir}/libbrscandec.so.*.*.*
%attr(755,root,root) %{_libdir}/libbrscandec2.so.*.*.*
%attr(755,root,root) %{_libdir}/sane/libsane-brother.so.*
%attr(755,root,root) %{_libdir}/sane/libsane-brother2.so.*
%{_datadir}/brscan
%dir %{_sysconfdir}/brscan
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/brscan/brsanenetdevice.cfg
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/brscan/brsanenetdevice2.cfg
%dir /var/log/brscan
