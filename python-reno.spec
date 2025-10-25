# TODO: fix tests and doc
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation [broken, requires git repo?]
%bcond_with	tests	# subunit tests (requires git repo?)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	reno: a New Way to manage Release Notes
Summary(pl.UTF-8):	reno: nowy sposób zarządzania informacjami o wydaniu (Release Notes)
Name:		python-reno
# keep 2.x here for python2 support
Version:	2.11.3
Release:	8
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/reno/
Source0:	https://files.pythonhosted.org/packages/source/r/reno/reno-%{version}.tar.gz
# Source0-md5:	c582cf344169a91f8d9a86b22ae3660a
Patch0:		%{name}-mock.patch
URL:		https://docs.openstack.org/reno/
%if %{with python2}
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python-pbr >= 1.4
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PyYAML >= 3.10.0
BuildRequires:	python-Sphinx >= 1.6.1
BuildRequires:	python-coverage >= 4.0
BuildRequires:	python-dulwich >= 0.15.0
BuildRequires:	python-mock >= 1.2
BuildRequires:	python-six >= 1.9.0
BuildRequires:	python-testtools >= 1.4.0
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.4
BuildRequires:	python3-pbr >= 1.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PyYAML >= 3.10.0
BuildRequires:	python3-Sphinx >= 1.6.1
BuildRequires:	python3-coverage >= 4.0
BuildRequires:	python3-dulwich >= 0.15.0
BuildRequires:	python3-six >= 1.9.0
BuildRequires:	python3-testtools >= 1.4.0
%endif
%endif
%if %{with doc}
BuildRequires:	python3-docutils >= 0.11
BuildRequires:	python3-openstackdocstheme >= 1.11.0
BuildRequires:	sphinx-pdg >= 1.6.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Reno is a release notes manager designed with high throughput in mind,
supporting fast distributed development teams without introducing
additional development processes. The goal is to encourage detailed
and accurate release notes for every release.

%description -l pl.UTF-8
Reno to zarządca informacji o wydaniu, zaprojektowany z myślą o dużym
przepływie, obsługujący szybkie, rozproszone zespoły programistów bez
wprowadzania dodatkowych procesów. Celem jest wspieranie szczegółowych
i dokładnych informacji dla każdego wydania.

%package -n python3-reno
Summary:	reno: a New Way to manage Release Notes
Summary(pl.UTF-8):	reno: nowy sposób zarządzania informacjami o wydaniu (Release Notes)
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.4

%description -n python3-reno
Reno is a release notes manager designed with high throughput in mind,
supporting fast distributed development teams without introducing
additional development processes. The goal is to encourage detailed
and accurate release notes for every release.

%description -n python3-reno -l pl.UTF-8
Reno to zarządca informacji o wydaniu, zaprojektowany z myślą o dużym
przepływie, obsługujący szybkie, rozproszone zespoły programistów bez
wprowadzania dodatkowych procesów. Celem jest wspieranie szczegółowych
i dokładnych informacji dla każdego wydania.

%package apidocs
Summary:	API documentation for reno
Summary(pl.UTF-8):	Dokumentacja API modułu reno
Group:		Documentation

%description apidocs
API documentation for reno.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu reno.

%prep
%setup -q -n reno-%{version}
%patch -P 0 -p1

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m unittest discover -s reno/tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m unittest discover -s reno/tests
%endif
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html doc/source doc/source/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/reno{,-2}

%py_postclean
%endif

%if %{with python3}
%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/reno{,-3}
ln -s reno-3 $RPM_BUILD_ROOT%{_bindir}/reno
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%attr(755,root,root) %{_bindir}/reno-2
%{py_sitescriptdir}/reno
%{py_sitescriptdir}/reno-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-reno
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%attr(755,root,root) %{_bindir}/reno
%attr(755,root,root) %{_bindir}/reno-3
%{py3_sitescriptdir}/reno
%{py3_sitescriptdir}/reno-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/*
%endif
