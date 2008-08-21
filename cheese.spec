Name:		cheese
Version:	2.23.90
Release:	%mkrel 1
Summary:	A GNOME application for taking pictures and videos from a webcam
License:	GPLv2+
Group:      Video
URL:		http://www.gnome.org/projects/cheese/
Source:	    ftp://ftp.gnome.org/mirror/gnome.org/sources/cheese/2.23/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libglade2.0-devel
BuildRequires: libgstreamer0.10-plugins-base-devel libgnome-vfs2-devel
BuildRequires: dbus-glib-devel
BuildRequires: evolution-data-server-devel
BuildRequires: pkgconfig(libgnomeui-2.0)
BuildRequires: libxxf86vm-devel
BuildRequires: gnome-doc-utils desktop-file-utils
BuildRequires: librsvg2-devel hal-devel
BuildRequires: intltool
# TODO update features once added upstream
%description
Cheese is a Photobooth-inspired GNOME application for taking pictures and
videos from a webcam. It also includes fancy graphical effects based on
the gstreamer-backend.

%prep
%setup -q

%build
%configure2_5x --disable-schemas-install
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %{name} --with-gnome --all-name

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%clean
rm -rf %{buildroot}

%define schemas %name

%if %mdkversion < 200900
%post
%post_install_gconf_schemas %{schemas}
%update_menus
%update_desktop_database
%update_mime_database
%update_icon_cache hicolor
%endif

%if %mdkversion < 200900
%preun
%preun_uninstall_gconf_schemas %{schemas}
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_desktop_database
%clean_mime_database
%clean_icon_cache hicolor
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%{_sysconfdir}/gconf/schemas/%name.schemas
%{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/applications/*
%{_datadir}/omf/%{name}/*
%_datadir/dbus-1/services/org.gnome.Cheese.service
