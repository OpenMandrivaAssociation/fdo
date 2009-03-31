%define fdodir %_prefix/lib/fdo

%define _disable_ld_as_needed 1

%define libfdo	 %mklibname fdo 3.4
%define libshp   %mklibname shpprovider 3.4
%define librdbms %mklibname rdbmsprovider 3.4
%define libsdf	 %mklibname sdfprovider 3.4
%define libwfs	 %mklibname wfsprovider 3.4
%define libwms	 %mklibname wmsprovider 3.4
%define libpostgis %mklibname postgisprovider 3.4
%define libgdal	%mklibname gdalprovider 3.4

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
BuildRequires: libcurl-devel
BuildRequires: boost-devel
BuildRequires: mkcatdefs
BuildRequires: python-devel
BuildRequires: openssl-devel
BuildRequires: sed
BuildConflicts: cppunit-devel
Requires: %{libfdo} = %version
Requires: %{libshp} = %version
Requires: %{librdbms} = %version
Requires: %{libsdf} = %version
Requires: %{libwfs} = %version
Requires: %{libpostgis} = %version
Requires: %{libgdal} = %version

%description
Feature Data Objects (FDO) is an API for manipulating, defining, and analyzing
geospatial information regardless of where it is stored. FDO uses a
provider-based model for supporting a variety of geospatial data sources, where
each provider typically supports a particular data format or data store.

%files

#-------------------------------------------------------------------------------

%package common
Group: System/Libraries
Summary: FDO common data

%description common
FDO common data.

%files common
%defattr(-,root,root,-)
%_libdir/com
%_libdir/providers.xml
%dir %_prefix/nls
%_prefix/nls/FDOMessage.cat
%_prefix/nls/SmMessage.cat

%package -n %libfdo
Group: System/Libraries
Summary: Fdo core library
Requires: fdo-common = %version

%description -n %libfdo
Fdo core library.

%files -n %libfdo
%defattr(-,root,root,-)
%_libdir/libExpressionEngine-%version.so
%_libdir/libFDO-%version.so
%_libdir/libFdoOws-%version.so
%_libdir/libSchemaMgr*-%version.so
%_libdir/libsqlitefdo.so.*

#-------------------------------------------------------------------------------

%package shp-common
Group: System/Libraries
Summary: Fdo shp library provider common data

%description shp-common
FDO shp library provider common data.

%files shp-common
%defattr(-,root,root,-)
%_prefix/nls/ShpMessage.cat

%package -n %libshp
Group: System/Libraries
Summary: Fdo shp library provider
Provides: fdo-shp = %version
Requires: fdo-shp-common = %version
Requires: %libfdo = %version

%description -n %libshp
Fdo shp library provider.

%files -n %libshp
%defattr(-,root,root,-)
%_libdir/libSHP*-%version.so

#-------------------------------------------------------------------------------

%package rdbms-common
Group: System/Libraries
Summary: Fdo rdbms library provider common data

%description rdbms-common
FDO rdbms library provider common data.

%files rdbms-common
%defattr(-,root,root,-)
%_prefix/nls/fdordbmsmsg.cat

%package -n %librdbms
Group: System/Libraries
Summary: Fdo rdbms library provider
Provides: fdo-rdbms = %version
Provides: fdo-odbc = %version
Provides: fdo-mysql = %version
BuildRequires: mysql-devel
BuildRequires: unixODBC-devel
Requires: fdo-rdbms-common = %version
Requires: %libfdo = %version

%description -n %librdbms
Fdo rdbms library provider.

%files -n %librdbms
%defattr(-,root,root,-)
%_libdir/libFdoMySQL-%version.so
%_libdir/libFdoODBC-%version.so

#-------------------------------------------------------------------------------

%package sdf-common
Group: System/Libraries
Summary: Fdo sdf library provider common data

%description sdf-common
Fdo sdf library provider common data.

%files sdf-common
%defattr(-,root,root,-)
%_prefix/nls/SDFMessage.cat

%package -n %libsdf
Group: System/Libraries
Summary: Fdo sdf library provider
Provides: fdo-sdf = %version
Requires: fdo-sdf-common = %version
Requires: %libfdo = %version

%description -n %libsdf
Fdo sdf library provider.

%files -n %libsdf
%defattr(-,root,root,-)
%_libdir/libSDF*-%version.so

#-------------------------------------------------------------------------------

%package wfs-common
Group: System/Libraries
Summary: Fdo wfs library provider common data

%description wfs-common
Fdo wfs library provider common data.

%files wfs-common
%defattr(-,root,root,-)
%_prefix/nls/WFSMessage.cat

%package -n %libwfs
Group: System/Libraries
Summary: Fdo wfs library provider
Provides: fdo-wfs = %version
Requires: fdo-wfs-common = %version
Requires: %libfdo = %version

%description -n %libwfs
Fdo wfs library provider.

%files -n %libwfs
%defattr(-,root,root,-)
%_libdir/libWFS*-%version.so

#-------------------------------------------------------------------------------

%package wms-common
Group: System/Libraries
Summary: Fdo wms library provider common data

%description wms-common
Fdo wms library provider common data.

%files wms-common
%defattr(-,root,root,-)
%_prefix/nls/FdoWmsMessage.cat

%package -n %libwms
Group: System/Libraries
Summary: Fdo wms library provider
Provides: fdo-wms = %version
Requires: fdo-wms-common = %version
Requires: %libfdo = %version

%description -n %libwms
Fdo wms library provider.

%files -n %libwms
%defattr(-,root,root,-)
%_libdir/libWMS*-%version.so

#-------------------------------------------------------------------------------

%package postgis-common
Group: System/Libraries
Summary: FDO postgis library provider common data

%description postgis-common
FDO SHP library provider common data.

%files postgis-common
%defattr(-,root,root,-)
%_prefix/nls/PostGisMessage.cat

%package -n %libpostgis
Group: System/Libraries
Summary: Fdo postgis library provider
Provides: fdo-postgis = %version
BuildRequires: postgresql-devel
BuildRequires: postgis-devel
Requires: fdo-postgis-common = %version
Requires: %libfdo = %version

%description -n %libpostgis
Fdo postgis library provider.

%files -n %libpostgis
%defattr(-,root,root,-)
%_libdir/libPostGIS*-%version.so

#-------------------------------------------------------------------------------

%package gdal-common
Group: System/Libraries
Summary: FDO gdal library provider common data

%description gdal-common
FDO SHP library provider common data.

%files gdal-common
%defattr(-,root,root,-)
%_prefix/nls/GRFPMessage.cat

%package -n %libgdal
Group: System/Libraries
Summary: Fdo gdal library provider
Provides: fdo-gdal = %version
BuildRequires: gdal-devel
BuildRequires: proj-devel
BuildRequires: ogdi-devel
Requires: fdo-gdal-common = %version
Requires: %libfdo = %version

%description -n %libgdal
Fdo gdal library provider.

%files -n %libgdal
%defattr(-,root,root,-)
%_libdir/libGRFP*-%version.so
%_libdir/libOGR*-%version.so

#-------------------------------------------------------------------------------

%package doc
Group: Books/Computer books
Summary: FDO Docs

%description doc
FDO Docs.

%files doc
%defattr(-,root,root,-)
%_docdir/fdo

#-------------------------------------------------------------------------------

%define libdev	%mklibname -d fdo

%package -n %libdev
Group: Development/C++
Summary: fdo library devel 
Provides: fdo-devel
Obsoletes: %{_lib}fdo3-devel
Requires: %{libfdo} = %version
Requires: %{libshp} = %version
Requires: %{librdbms} = %version
Requires: %{libsdf} = %version
Requires: %{libwfs} = %version
Requires: %{libpostgis} = %version
Requires: %{libgdal} = %version

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
