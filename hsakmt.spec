%global rocm_release 5.7
%global rocm_patch 1
%global rocm_version %{rocm_release}.%{rocm_patch}

#squidf: from LIB_VERSION_ in CMakeLists.txt
%define lib_major   1
%define lib_minor   0
%define lib_patch   6

%define libname    %mklibname %{name} %{lib_major}
%define devel_name %mklibname %{name} -d

%define rel     1
Name:           hsakmt
Version:        %{lib_major}.%{lib_minor}.%{lib_patch}
Release:        %mkrel -c %{rocm_version} %{rel}
Summary:        AMD HSA thunk library
Group:          System/Libraries
License:        MIT
URL:            https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface
Source0:        https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface/archive/rocm-%{rocm_version}.tar.gz#/ROCT-Thunk-Interface-rocm-%{rocm_version}.tar.gz
Patch1:         hsakmt-pkg-conf.patch
Patch2:         hsakmt-global-visibility.patch

# Mageia builds AMD HSA kernel support for these 64bit targets:
ExclusiveArch:  x86_64 aarch64
BuildRequires:  cmake
BuildRequires:  pkgconfig(libpci)
BuildRequires:  pkgconfig(libdrm_amdgpu)
BuildRequires:  pkgconfig(numa)

%description
This package includes the libhsakmt (HSA thunk) libraries for AMD KFD

%package -n %{libname}
Summary:    AMD HSA thunk library
Group:      System/Libraries
Provides:   hsakmt(rocm) = %{rocm_version}

%description -n %{libname}
Libraries for %{name}.

%package -n %{devel_name}
Summary:    AMD HSA thunk library development package
Group:      Development/Other
Requires:   %{libname} = %{version}-%{release}
Provides:   hsakmt-devel(rocm) = %{rocm_version}

%description -n %{devel_name}
Development library for the libhsakmt (HSA thunk) libraries for AMD KFD

%prep
%autosetup -n  ROCT-Thunk-Interface-rocm-%{rocm_version} -p1

%build
%cmake -B build \
    -Wno-dev \
    -S "." \
    -DBUILD_SHARED_LIBS=ON
%cmake_build

%install
%cmake_install

echo '%{_libdir}' > %{name}.conf
install -Dm644 %{name}.conf %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf

# Installation this via license macro instead:
rm -r %{buildroot}/%{_datadir}/doc/hsakmt

%files -n %{libname}
%doc README.md
%license LICENSE.md
%{_libdir}/libhsakmt.so.%{version}
%{_libdir}/libhsakmt.so.%{lib_major}
%{_sysconfdir}/ld.so.conf.d/%{name}.conf

%files -n %{devel_name}
%{_libdir}/libhsakmt.so
%dir %{_libdir}/cmake/hsakmt
%{_libdir}/cmake/hsakmt/hsakmtTargets*cmake
%{_libdir}/cmake/hsakmt/hsakmt-config*cmake
%{_libdir}/pkgconfig/libhsakmt.pc
#These headers are deprecated and will be removed soon:
%dir %{_includedir}/hsakmt
%{_includedir}/hsakmt/hsakmt.h
%{_includedir}/hsakmt/hsakmttypes.h
%exclude %{_includedir}/hsakmt.h
%exclude %{_includedir}/hsakmttypes.h

