%define old_libname	%mklibname %{name} 0
%define old_devname	%mklibname %{name} -d

Name:           ecm
Version:        6.4.4
Release:        1%{?dist}
Summary:        Elliptic Curve Method for Integer Factorization
License:        GPLv3+
URL:            https://gforge.inria.fr/projects/ecm/
Source0:        https://gforge.inria.fr/frs/download.php/32159/ecm-%{version}.tar.gz
Source1:	%{name}.rpmlintrc
BuildRequires:	docbook-style-xsl
BuildRequires:	gmp-devel
BuildRequires:	gomp-devel
BuildRequires:  gsl-devel
BuildRequires:	xsltproc
BuildRequires:  m4
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
Programs and libraries employing elliptic curve method for factoring
integers (with GMP for arbitrary precision integers).

%package	devel
License:	LGPL
Summary:	Shared GMP ECM library
%rename %{old_devname}

%description    devel
The libraries and header files for using %{name} for development.

%package        libs
Summary:        Elliptic Curve Method library
License:        LGPLv3+
%rename %{old_libname}

%description    libs
The %{name} library.

%prep
%setup -q

# Fix non-UTF-8 encodings
for badfile in ChangeLog README AUTHORS ; do
  iconv -f iso-8859-1 -t utf-8 -o $badfile.UTF-8 $badfile 
  touch -r $badfile $badfile.UTF-8
  mv $badfile.UTF-8 $badfile
done

# Fix the FSF's address
for badfile in `grep -FRl 'Fifth Floor' .`; do
  sed -e 's/Fifth Floor/Suite 500/' -e 's/02111-1307/02110-1335/' \
      -i.orig $badfile
  touch -r $badfile.orig $badfile
  rm -f $badfile.orig
done

%build
FLGS="--enable-shared --enable-openmp --disable-gmp-cflags"

# Build an SSE2-enabled version for 32-bit x86
%ifarch %{ix86}
%configure ${FLGS} --build=pentium4-pc-linux-gnu --host=pentium4-pc-linux-gnu \
  --disable-static --enable-sse2 \
  CFLAGS="$RPM_OPT_FLAGS -std=gnu99 -march=pentium4 -Wa,--noexecstack" \
  LDFLAGS="$RPM_LD_FLAGS -Wl,-z,noexecstack -lgmp -lgomp"

# Eliminate hardcoded rpaths
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -i libtool

rm -f ecm-params.h
ln -s ecm-params.h.pentium4 ecm-params.h
make %{?_smp_mflags}
cp -a .libs .sse2
make clean
# Make clean doesn't clean everything....
rm -f config.h config.log config.status ecm-params.h stamp-h1
ln -s ecm-params.h.default ecm-params.h
%endif

# Build a non-SSE2 version (x86_64 loses out; the assembly code containing
# SSE2 instructions is 32-bit only).
%configure ${FLGS} --disable-static --disable-sse2 \
  CFLAGS="$RPM_OPT_FLAGS -std=gnu99 -Wa,--noexecstack" \
  LDFLAGS="$RPM_LD_FLAGS -Wl,-z,noexecstack -lgmp -lgomp"

# Eliminate hardcoded rpaths
sed -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    -i libtool

make --eval='.SECONDARY:' %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%ifarch %ix86
mkdir -p $RPM_BUILD_ROOT%{_libdir}/sse2
cp -p .sse2/libecm.so.0.0.0 $RPM_BUILD_ROOT%{_libdir}/sse2
%endif

%check
export LD_LIBRARY_PATH=`pwd`/.libs
make check

%files
%doc COPYING README
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%files devel
%doc README.lib
%{_includedir}/ecm.h
%{_libdir}/libecm.so

%files libs
%doc COPYING.LIB AUTHORS ChangeLog NEWS TODO
%{_libdir}/libecm.so.*
%ifarch %ix86
%{_libdir}/sse2/libecm.so.*
%endif
