%define libname	%mklibname fdo 3
%define fdodir %_prefix/lib/fdo

%define _disable_ld_as_needed 1

Name: fdo
Version: 3.4.0
Release: %mkrel 0.rc3.1
Epoch: 1
License: LGPL
Summary: Feature Data Objects (FDO)
Group: Sciences/Geosciences
URL: https://fdo.osgeo.org
Source0: fdo-3.4.0.tar.gz
Source1: fdogdal-3.4.0.tar.gz
Source2: fdoogr-3.4.0.tar.gz
Source3: fdopostgis-3.4.0.tar.gz
Source4: fdordbms-3.4.0.tar.gz
Source5: fdosdf-3.4.0.tar.gz
Source6: fdoshp-3.4.0.tar.gz
Source7: fdowfs-3.4.0.tar.gz
Source8: fdowms-3.4.0.tar.gz
Source9: fdosqlite-3.4.0.tar.gz
Source10: CMakeLists.txt
Patch0: fdo-3.4.0-missing-cstd-includes.patch
Patch2: fdo-3.3.1-constify-chars.patch
Patch6: fdo-3.4.0-ows-shared-lib-link.patch
Patch10: fdo-3.4.0-ogr-thirdparty.patch
Patch12: fdo-3.4.0-postgis-thirdparty.patch
Patch13: fdo-3.4.0-sdf-thirdparty.patch
Patch14: fdo-3.4.0-sdf-precision.patch
Patch15: fdo-3.4.0-install.patch
Patch16: fdo-3.4.0-genericrdbms-install64.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Buildrequires: cmake
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: xalan-c-devel >= 1.10
BuildRequires: gdal-devel
BuildRequires: proj-devel
BuildRequires: ogdi-devel
BuildRequires: postgresql-devel
BuildRequires: postgis-devel
BuildRequires: openssl-devel
BuildRequires: libcurl-devel
BuildRequires: boost-devel
BuildRequires: unixODBC-devel
BuildRequires: mkcatdefs
BuildRequires: python-devel
BuildConflicts: cppunit-devel
BuildRequires: sed

%description
Feature Data Objects (FDO) is an API for manipulating, defining, and analyzing
geospatial information regardless of where it is stored. FDO uses a
provider-based model for supporting a variety of geospatial data sources, where
each provider typically supports a particular data format or data store.

#-------------------------------------------------------------------------------

%package -n %libname
Group: Library
Summary: fdo library
Provides: libfdo

%description -n %libname
fdo library

%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig

%files -n %libname
%defattr(-,root,root,-)
%_libdir/*-3.4.0.so
%_libdir/libsqlitefdo.so.*
%_libdir/com
%_libdir/providers.xml
#_datadir/locale/en/*
%_prefix/nls

#-------------------------------------------------------------------------------

%package doc
Group: Documentation
Summary: FDO Docs

%description doc
FDO Docs

%files doc
%defattr(-,root,root,-)
%_docdir/fdo

#-------------------------------------------------------------------------------

%define libdev	%mklibname -d fdo

%package -n %libdev
Group: Development
Summary: fdo library devel 
Provides: fdo-devel
Obsoletes: %{_lib}fdo3-devel

%description -n %libdev
fdo library devel

%files -n %libdev
%defattr(-,root,root,-)
%_libdir/*.so
%_libdir/*.la
%_includedir/*
%exclude %_libdir/*-3.4.0.so

#-------------------------------------------------------------------------------

%prep
%setup -q -T -c -n %name-%version -a 0 -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7 -a 8

# Remove undesired ThirdParty

for name in apache boost gdal gsar libcurl openssl pgsql util; do
    rm -rf OpenSource_FDO/Thirdparty/$name
done

cd OpenSource_FDO
%patch0 -p1 -b .cstd
%patch2 -p1 -b .const
%patch6 -p1 -b .ows
%patch10 -p1 -b .ogr_thirdparty
%patch12 -p1 -b .postgis_thirdparty
%patch13 -p1 -b .sdf_thirdparty
%patch14 -p1 -b .sdf_precision
%patch15 -p1 -b .install
%patch16 -p1 -b .install

%build
FDO=%_builddir/%name-%version/OpenSource_FDO/Fdo
FDOTHIRDPARTY=%_builddir/%name-%version/OpenSource_FDO/Thirdparty
FDOUTILITIES=%_builddir/%name-%version/OpenSource_FDO/Utilities
FDOGDAL=%_prefix
FDOODBC=%_prefix
PYTHON_LIB_PATH=%py_libdir
PYTHON_INCLUDE_PATH=%py_incdir

CPPFLAGS="$CPPFLAGS -I%_includedir/gdal -I%_includedir/pgsql"

export FDO FDOUTILITIES FDOGDAL FDOODBC PYTHON_LIB_PATH PYTHON_INCLUDE_PATH FDOTHIRDPARTY CPPFLAGS

# Required Thirdparty
pushd $FDOTHIRDPARTY/linux/cppunit
    ./build
popd

pushd $FDOTHIRDPARTY/Sqlite3.3.13/Src
    cp %SOURCE10 .
    %cmake
    %make
popd

cd OpenSource_FDO

# FDO Core
aclocal && libtoolize --force && automake --add-missing --copy && autoconf

%configure2_5x --enable-debug

%make

# Fdo and Utilities
for name in Fdo Utilities; do
    pushd $name
        %make
    popd
done

# Providers
for name in Providers/*; do
    pushd $name
        aclocal && libtoolize --force && automake --add-missing --copy && autoconf
        %configure2_5x --enable-debug
        %make
    popd
done


%install
rm -rf %buildroot

FDOTHIRDPARTY=%_builddir/%name-%version/OpenSource_FDO/Thirdparty
export FDOTHIRDPARTY

cd OpenSource_FDO

make DESTDIR=%buildroot install
make -C Fdo DESTDIR=%buildroot install
make -C Utilities DESTDIR=%buildroot install

pushd $FDOTHIRDPARTY/Sqlite3.3.13/Src/build
	%makeinstall_std
popd

for name in Providers/*; do
    pushd $name
        make DESTDIR=%buildroot install
    popd
done


# Fix providers file 
sed -i "s,/usr/local/fdo-3.4.0/lib,%_libdir,g" %buildroot/%_libdir/providers.xml
sed -i "s,.so</LibraryPath>,-3.4.0.so</LibraryPath>,g" %buildroot/%_libdir/providers.xml
