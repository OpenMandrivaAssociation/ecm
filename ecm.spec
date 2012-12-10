%define libmajor	0
%define libname		%mklibname %{name} %{libmajor}
%define devname		%mklibname %{name} -d

Summary:	GMP ECM - Elliptic Curve Method for Integer Factorization
Name:		ecm
Version:	6.3
Release:	0.1434.4
Group:		Sciences/Mathematics
License:	GPL
URL:		http://gforge.inria.fr/projects/ecm/
Source:		http://gforge.inria.fr/frs/download.php/4837/ecm-6.3-r1434.tar.xz
Patch0:		ecm-6.3-fix-build.patch
Patch1:		ecm-6.3-install.patch
BuildRequires:	gmp-devel
BuildRequires:	xsltproc
BuildRequires:	docbook-style-xsl

%description
GMP ECM - Elliptic Curve Method for Integer Factorization.

%package	-n %{libname}
Group:		System/Libraries
License:	LGPL
Summary:	Shared GMP ECM library
Provides:	lib%{name} = %{version}-%{release}

%description	-n %{libname}
This package contains the libraries needed to run ecm.

%package	-n %{devname}
Group:		Development/C
License:	LGPL
Summary:	Development files for GMP ECM
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	lib%{name}-devel < %{version}-%{release}

%description	-n %{devname}
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
%makeinstall_std

%files
%doc NEWS README
%{_bindir}/%{name}
%{_mandir}/man1/ecm.1*

%files -n %{libname}
%{_libdir}/libecm.so.%{libmajor}*

%files -n %{devname}
%doc AUTHORS README.lib TODO
%{_includedir}/ecm.h
%{_libdir}/libecm.so

