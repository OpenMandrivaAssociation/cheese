Name:		cheese
Version:	0.1.4
Release:	%mkrel 1
Summary:	A GNOME application for taking pictures and videos from a webcam.
License:	GPL
Group:      TODO		
URL:		http://live.gnome.org/Cheese
Source:		%{name}-%{version}.tar.bz2
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root
Buildrequires: libglade2.0-devel libdbus-devel libgstreamer0.10-devel
Buildrequires: libgstreamer0.10-plugins-base-devel libgnome-vfs2-devel
	
%description
TODO

%prep
%setup -q

%build
%configure
%make 

%install
rm -rf %{buildroot}
%makeinstall
rm -f %{buildroot}/%{_datadir}/icons/hicolor/icon-theme.cache
%find_lang %{name} --with-gnome --all-name

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/applications/*

