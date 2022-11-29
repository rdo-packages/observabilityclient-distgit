%global srcname observabilityclient
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global upstream_version %{version}
%global tarsources python-observabilityclient

Name:           python-observabilityclient
Version:        0.0.1
Release:        1
Summary:        OpenStackClient plugin for management of observability components
License:        ASL 2.0
URL:            https://www.github.com/infrawatch/python-observabilityclient
Source0:        https://github.com/infrawatch/python-observabilityclient/archive/%{upstream_version}/python-observabilityclient-%{upstream_version}.tar.gz
BuildArch:      noarch
BuildRequires:  git-core
BuildRequires:  python3-devel
#BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
# Needed to install pbr from pip for now, because the package isn't being found
BuildRequires: python3-pip

# Q: Is there a lower bound on the version of osc that can be used?
Requires: python3-openstackclient

%description
OpenStackClient plugin for management of observability components

%prep
%autosetup -n %{tarsources}-%{upstream_version} -S git

%build
%{py3_build}

%install
%{py3_install}

# I probably need a provides section if there's an executable installed.

%files
%doc README*
%license LICENSE
%{_datadir}/%{name}
%{python3_sitelib}/observabilityclient*

%changelog

