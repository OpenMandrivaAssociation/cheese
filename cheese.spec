%define major 18
%define libname %mklibname cheese-gtk %major
%define develname %mklibname -d cheese-gtk

Name:		cheese
Version:	2.32.0
Release:	%mkrel 1
Summary:	A GNOME application for taking pictures and videos from a webcam
License:	GPLv2+
Group:		Video
URL:		http://www.gnome.org/projects/cheese/
Source:		ftp://ftp.gnome.org/pub/GNOME/sources/cheese/%{name}-%{version}.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: libglade2.0-devel
BuildRequires: libgstreamer0.10-plugins-base-devel libgnome-vfs2-devel
BuildRequires: dbus-glib-devel
BuildRequires: gnome-desktop-devel >= 2.25.1
BuildRequires: libcanberra-gtk-devel
BuildRequires: libxxf86vm-devel
BuildRequires: libgudev-devel
BuildRequires: gnome-doc-utils desktop-file-utils
BuildRequires: librsvg2-devel
BuildRequires: intltool
Requires: %libname = %version-%release
# TODO update features once added upstream
%description
Cheese is a Photobooth-inspired GNOME application for taking pictures and
videos from a webcam. It also includes fancy graphical effects based on
the gstreamer-backend.

%package -n %libname
Group: System/Libraries
Summary: Shared library part of %name

%description -n %libname
Cheese is a Photobooth-inspired GNOME application for taking pictures and
videos from a webcam. It also includes fancy graphical effects based on
the gstreamer-backend.

%package -n %develname
Group: Development/C
Summary: Developent files for %name
Requires: %libname = %version-%release
Provides: libcheese-gtk-devel = %version-%release

%description -n %develname
Cheese is a Photobooth-inspired GNOME application for taking pictures and
videos from a webcam. It also includes fancy graphical effects based on
the gstreamer-backend.

%prep
%setup -q

%build
%configure2_5x --disable-schemas-install
%make

%install
rm -rf %{buildroot} %name.lang
%makeinstall_std

%find_lang %{name} --with-gnome --all-name

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%define launchers %{_sysconfdir}/dynamic/launchers/webcam
# dynamic support
mkdir -p $RPM_BUILD_ROOT%launchers
cat > $RPM_BUILD_ROOT%launchers/%name.desktop << EOF
[Desktop Entry]
Name=Webcam Photobooth
Comment=Cheese Webcam Photobooth using \$devicename
TryExec=%{_bindir}/cheese
Exec=%{_bindir}/cheese
Terminal=false
Icon=cheese
Type=Application
StartupNotify=true
EOF

%clean
rm -rf %{buildroot}

%define schemas %name

%post
update-alternatives --install %{launchers}/kde.desktop webcam.kde.dynamic %launchers/%name.desktop 60
update-alternatives --install %{launchers}/gnome.desktop webcam.gnome.dynamic %launchers/%name.desktop 60
%if %mdkversion < 200900
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

%postun
if [ "$1" = "0" ]; then
   update-alternatives --remove webcam.kde.dynamic %launchers/%name.desktop
   update-alternatives --remove webcam.gnome.dynamic %launchers/%name.desktop
fi
%if %mdkversion < 200900
%clean_menus
%clean_desktop_database
%clean_mime_database
%clean_icon_cache hicolor
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%config(noreplace) %launchers/*.desktop
%{_sysconfdir}/gconf/schemas/%name.schemas
%{_bindir}/*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/applications/*
%{_datadir}/omf/%{name}/*
%_datadir/dbus-1/services/org.gnome.Cheese.service

%files -n %libname
%defattr(-,root,root)
%_libdir/libcheese-gtk.so.%{major}*

%files -n %develname
%defattr(-,root,root)
%_libdir/libcheese-gtk.so
%_libdir/libcheese-gtk.la
%_libdir/libcheese-gtk.a
%_includedir/%name
%_libdir/pkgconfig/cheese-gtk.pc
%_datadir/gtk-doc/html/%name/
