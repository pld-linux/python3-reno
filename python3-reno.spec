# TODO: fix tests and doc
#
# Conditional build:
%bcond_with	doc	# Sphinx documentation (requires git repo?)
%bcond_with	tests	# subunit tests (requires git repo?)

Summary:	reno: a New Way to manage Release Notes
Summary(pl.UTF-8):	reno: nowy sposób zarządzania informacjami o wydaniu (Release Notes)
Name:		python3-reno
Version:	4.1.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/reno
Source0:	https://files.pythonhosted.org/packages/source/r/reno/reno-%{version}.tar.gz
# Source0-md5:	765a468a3ba485747504d7a3a6e78604
URL:		https://docs.openstack.org/reno/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-pbr >= 1.4
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-PyYAML >= 5.3.1
BuildRequires:	python3-Sphinx >= 1.6.1
BuildRequires:	python3-coverage >= 4.0
BuildRequires:	python3-dulwich >= 0.15.0
BuildRequires:	python3-packaging >= 20.4
BuildRequires:	python3-stestr >= 2.0.0
BuildRequires:	python3-subunit >= 0.0.18
BuildRequires:	python3-testscenarios >= 0.4
BuildRequires:	python3-testtools >= 1.4.0
%endif
%if %{with doc}
BuildRequires:	python3-docutils >= 0.11
BuildRequires:	python3-openstackdocstheme >= 2.2.1
BuildRequires:	sphinx-pdg >= 2.0.0
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

%build
%py3_build

%if %{with tests}
%{__python3} -m unittest discover -s reno/tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html doc/source doc/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%{__mv} $RPM_BUILD_ROOT%{_bindir}/reno{,-3}
ln -s reno-3 $RPM_BUILD_ROOT%{_bindir}/reno

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.rst
%attr(755,root,root) %{_bindir}/reno-3
%{_bindir}/reno
%{py3_sitescriptdir}/reno
%{py3_sitescriptdir}/reno-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc doc/_build/html/*
%endif
