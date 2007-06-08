#
Summary:	Brother scanner driver
Name:		brscan
Version:	0.2.3
Release:	1
License:	GPL v2
Group:		Applications
Source0:	http://solutions.brother.com/Library/sol/printer/linux/rpmfiles/sane_source/%{name}-src-%{version}.tar.gz
# Source0-md5:	99a7f21fc15661690b296023253bcca6
URL:		http://solutions.brother.com/linux/sol/printer/linux/sane_drivers.html
Patch0:		%{name}-fixes.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	ncurses-devel
Requires:	sane-backends
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Scanner driver for Brother MFC printers, both USB and network.

%prep
%setup -q -n %{name}-src-%{version}
%patch0 -p1

%build
cd brscan
rm configure acinclude.m4
%{__libtoolize}
%{__aclocal}
%{__autoconf}
#%%{__autoheader}
#%%{__automake}
%configure
cd lib
%{__make}
cd ..
cd netconfig
%{__make}
cd ..
cd sanei
%{__make}
cd ..
cd backend_brscan
%{__make}
cd ..
cd backend_brscan2
%{__make}
cd ..

#%{__make} \
#	CFLAGS="%{rpmcflags}" \
#	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
# create directories if necessary
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_libdir}/sane}
#install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

cd brscan
cd backend_brscan
libtool --mode=install install libsane-brother.la $RPM_BUILD_ROOT%{_libdir}/sane/
cd ..
cd backend_brscan2
libtool --mode=install install libsane-brother2.la $RPM_BUILD_ROOT%{_libdir}/sane/
cd ..
cd netconfig
libtool --mode=install install brsaneconfig $RPM_BUILD_ROOT%{_sbindir}/
libtool --mode=install install brsaneconfig2 $RPM_BUILD_ROOT%{_sbindir}/
cd ..



%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/sane/lib*.so
%attr(755,root,root) %{_libdir}/sane/lib*.so.*.*.*
%attr(755,root,root) %{_sbindir}/brsaneconfig
%attr(755,root,root) %{_sbindir}/brsaneconfig2
