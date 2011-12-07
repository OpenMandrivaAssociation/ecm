%define name		ecm
%define libmajor	0
%define libname		%mklibname %{name} %{libmajor}

Name:		%{name}
Group:		Sciences/Mathematics
License:	GPL
Summary:	GMP ECM - Elliptic Curve Method for Integer Factorization
Version:	6.3
Release:	%mkrel -c 1434 3
Source:		http://gforge.inria.fr/frs/download.php/4837/ecm-6.3-r1434.tar.xz
Patch0:		ecm-6.3-fix-build.patch
Patch1:		ecm-6.3-install.patch
URL:		http://gforge.inria.fr/projects/ecm/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	libgmp-devel
BuildRequires:	xsltproc docbook-style-xsl

%description
GMP ECM - Elliptic Curve Method for Integer Factorization.

%package	-n %{libname}
Group:		System/Libraries
License:	LGPL
Summary:	Shared GMP ECM library
Provides:	lib%{name} = %{version}-%{release}

%description	-n %{libname}
This package contains the libraries needed to run ecm.

%package	-n lib%{name}-devel
Group:		Development/C
License:	LGPL
Summary:	Development files for GMP ECM
Requires:	lib%{name} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description	-n lib%{name}-devel
This package contains the GMP ECM development header files and
libraries.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build
autoreconf -fi
%configure2_5x			\
	--enable-shared		\
	--disable-static	\
%ifarch %{ix86}
	--enable-sse2
%else
  %ifarch x86_64
	--enable-asm-redc
  %endif
%endif

%make

%install
rm -rf %{buildroot}
%makeinstall_std
rm %{buildroot}%{_libdir}/libecm.la

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%{_mandir}/man1/ecm.1*
%doc NEWS README

%files		-n %{libname}
%defattr(-,root,root)
%{_libdir}/libecm.so.*

%files		-n lib%{name}-devel
%defattr(-,root,root)
%{_includedir}/ecm.h
%{_libdir}/libecm.so
%doc AUTHORS README.lib TODO
