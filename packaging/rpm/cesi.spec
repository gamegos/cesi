%define name cesi
%define setup_path /opt/%{name}

Name:           %{name}
Version:        1.0
Release:        1%{?dist}
Summary:        CeSI is a web interface for managing multiple supervisors from the same place.

Group:          Utilities
License:        GPLv3+
URL:            https://github.com/gamegos/%{name}
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

%if "%{?fedora}" >= "28" 
Requires:       sqlite, python2-flask
%else
%if "%{?rhel}" >= "7"
Requires:       python-flask
%endif
%endif

%description
CeSI is a web interface for managing multiple supervisors from the same place.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{setup_path}
cp -r ./* $RPM_BUILD_ROOT%{setup_path}
install -p -D -m 644 defaults/cesi.service $RPM_BUILD_ROOT%{_unitdir}/cesi.service
install -p -D -m 644 defaults/cesi.conf $RPM_BUILD_ROOT%{_sysconfdir}/cesi.conf
sqlite3 $RPM_BUILD_ROOT%{setup_path}/userinfo.db < $RPM_BUILD_ROOT%{setup_path}/userinfo.sql

%post
systemctl start cesi

%postun
systemctl stop cesi
rm -rf $RPM_BUILD_ROOT%{setup_path}

%files
%defattr(-,root,root,-)
%{setup_path}
%config(noreplace) %{_unitdir}/cesi.service
%config(noreplace) %{_sysconfdir}/cesi.conf

%changelog
* Fri Aug 17 2018 pleycpl <h4rvey@protonmail.com> 1.0-1
- Initial RPM release

