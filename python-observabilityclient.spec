%global srcname observabilityclient
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global upstream_version %{version}

%global client python-observabilityclient
%global sclient observabilityclient
%global with_doc 0
%global with_tests 0

# If a executable is provided by the package uncomment following line
# % global executable example
%global common_desc \
OpenStackClient plugin for management of observability components.

Name:           %{client}
Version:        0.0.1
Release:        1
Summary:        OpenStackClient plugin for management of observability components
License:        ASL 2.0
URL:            https://www.github.com/infrawatch/python-observabilityclient

Source0:        https://github.com/infrawatch/python-observabilityclient/archive/%{upstream_version}/python-observabilityclient-%{upstream_version}.tar.gz

BuildArch:      noarch

%description
%{common_desc}

%package -n python3-%{sclient}
Summary:    OpenStackClient plugin for management of observability components
%{?python_provide:%python_provide python3-%{sclient}}

BuildRequires:  python3-devel
BuildRequires:  python3-pbr
BuildRequires:  git-core
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel

# Q: Is there a lower bound on the version of osc that can be used?
Requires: python3-openstackclient

%description -n python3-%{sclient}
%{common_desc}

%if %{?with_tests}
%package -n python3-%{sclient}-tests
Summary:    OpenStack %{sclient} tests
Requires:   python3-%{sclient} = %{version}-%{release}

# testing framework packages required to run unit tests or any additional package
# which is not required for python3-%{ service} but it is for unit tests.
Requires:       python3-stestr

%description -n python3-%{sclient}-tests
%{common_desc}

This package contains the %{sclient} test files.
%endif

%if 0%{?with_doc}
%package -n python-%{sclient}-doc
Summary:    OpenStack %{sclient} documentation

#BuildRequires: python3-sphinx
#BuildRequires: python3-openstackdocstheme

%description -n python-%{sclient}-doc
%{common_desc}

This package contains the documentation.
%endif

%prep
%autosetup -n %{client}-%{upstream_version} -S git
%{python3} -c 'import pbr'

%build
%py3_build

%install
%py3_install
# If an executable is provided by the package uncomment following lines
#ln -s %{ executable} %{ buildroot}%{ _bindir}/%{ executable}-3
# If the client has man page uncomment following line
# install -p -D -m 644 man/%{ executable}.1 %{ buildroot}%{ _mandir}/man1/%{ executable}.1

%check
#stestr run

%files -n python3-%{sclient}
%doc README*
%license LICENSE
# /usr/lib/python3.x/site-packages
%{python3_sitelib}/%{sclient}
%{python3_sitelib}/*.egg-info
%exclude %{python3_sitelib}/%{sclient}/tests
# If the client has man page uncomment
#%{ _mandir}/man1/%{ executable}.1
# If an executable is provided by the package uncomment following lines
#%{ _bindir}/%{ executable}
#%{ _bindir}/%{ executable}-3

%if 0%{?with_tests}
%files -n python3-%{sclient}-tests
%{python3_sitelib}/%{sclient}/tests
%endif

%if 0%{?with_doc}
%files -n python-%{sclient}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog

