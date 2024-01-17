%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2ef3fe0ec2b075ab7458b5f8b702b20b13df2318

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global client python-observabilityclient
%global sclient observabilityclient
%global with_doc 0

%global common_desc \
This is an OpenStackClient (OSC) plugin that implements commands for \
management of Prometheus.

Name:       %{client}
Version:    0.1.1
Release:    1%{?dist}
Summary:    OpenStack observability client OSC plugin
License:    Apache-2.0
URL:        http://launchpad.net/%{client}/

Source0:    https://tarballs.openstack.org/%{client}/%{client}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:  https://tarballs.openstack.org/%{client}/%{client}-%{upstream_version}.tar.gz.asc
Source102:  https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
BuildRequires:  openstack-macros
%endif

%description
%{common_desc}

%package -n python3-%{sclient}
Summary:    OpenStack observability client OSC plugin
%{?python_provide:%python_provide python3-%{sclient}}

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  git-core

%description -n python3-%{sclient}
%{common_desc}


%package -n python3-%{sclient}-tests
Summary:    OpenStack observability client OSC plugin tests
Requires:   python3-%{sclient} = %{version}-%{release}

# Requirements to run unit tests included in the -tests subpackage
Requires:       python3-pytest
Requires:       python3-testtools

BuildRequires:  python3-testtools

%description -n python3-%{sclient}-tests
%{common_desc}

This package contains the observability client test files.

%if 0%{?with_doc}
%package -n python-%{sclient}-doc
Summary:    OpenStack observability client OSC plugin docs

%description -n python-%{sclient}-doc
%{common_desc}

This package contains the documentation.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{client}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i 's/.\[test\]//g' tox.ini
sed -i 's/^requires.*/'requires\ =\ [\'setuptools\']'/' pyproject.toml

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%pyproject_install

%check
%tox -e %{default_toxenv}

%files -n python3-%{sclient}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{sclient}
%{python3_sitelib}/*.dist-info
%exclude %{python3_sitelib}/%{sclient}/tests

%files -n python3-%{sclient}-tests
%{python3_sitelib}/%{sclient}/tests

%if 0%{?with_doc}
%files -n python-%{sclient}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Wed Jan 17 2024 RDO <dev@lists.rdoproject.org> 0.1.1-1
- Update to 0.1.1

