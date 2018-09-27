%define url_ver %(echo %{version}|cut -d. -f1,2)
%define _disable_rebuild_configure 1

%define	gstapi	1.0
%define	gtk_maj	25
%define	major	8
%define	gir_maj	3.0
%define	libname	%mklibname %{name} %{major}
%define	gtkname	%mklibname %{name}-gtk %{gtk_maj}
%define	girname	%mklibname %{name}-gtk-gir %{gir_maj}
%define	devname	%mklibname -d %{name}
%define	devgtk	%mklibname -d %{name}-gtk

Summary:	A GNOME application for taking pictures and videos from a webcam
Name:		cheese
Version:	3.30.0
Release:	1
License:	GPLv2+
Group:		Video
Url:		http://www.gnome.org/projects/cheese/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/cheese/%{url_ver}/%{name}-%{version}.tar.xz

BuildRequires:	desktop-file-utils
BuildRequires:	glib2.0-common
BuildRequires:	gnome-doc-utils >= 0.20
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	vala vala-devel
BuildRequires:	pkgconfig(appstream-glib)
BuildRequires:	pkgconfig(cairo) >= 1.10.0
BuildRequires:	pkgconfig(clutter-1.0) >= 1.6.1
BuildRequires:	pkgconfig(clutter-gst-3.0)
BuildRequires:	pkgconfig(clutter-gtk-1.0) >= 0.91.8
BuildRequires:	pkgconfig(gdk-3.0) >= 2.99.4
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glib-2.0) >= 2.28.0
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 2.91.6
BuildRequires:	pkgconfig(gnome-video-effects)
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.6.7
BuildRequires:	pkgconfig(gstreamer-%{gstapi}) >= 1.0
BuildRequires:	pkgconfig(gstreamer-pbutils-%{gstapi}) >= 1.0
BuildRequires:	pkgconfig(gstreamer-plugins-bad-%{gstapi}) >= 1.0
BuildRequires:	pkgconfig(gstreamer-plugins-base-%{gstapi}) >= 1.0
BuildRequires:	pkgconfig(gtk+-3.0) >= 2.99.4
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libcanberra-gtk3) >= 0.26
BuildRequires:	pkgconfig(librsvg-2.0) >= 2.32.0
BuildRequires:	pkgconfig(pangocairo) >= 1.28.0
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xtst)

Requires:	gsettings-desktop-schemas
Requires:	gstreamer%{gstapi}-plugins-base
Requires:	gstreamer%{gstapi}-plugins-good
Requires:	gstreamer%{gstapi}-plugins-bad
Suggests:	gstreamer%{gstapi}-rtpvp8
Suggests:	gstreamer%{gstapi}-vp8
Requires:	gnome-video-effects
Requires:	gstreamer%{gstapi}-gstclutter

# TODO update features once added upstream
%description
Cheese is a Photobooth-inspired GNOME application for taking pictures and
videos from a webcam. It also includes fancy graphical effects based on
the gstreamer-backend.

%package -n	%{libname}
Group:		System/Libraries
Summary:	Shared library part of %{name}
Obsoletes:	%{gtkname} < 3.5.1-1
Provides:	%{gtkname} = 3.5.1-1

%description -n	%{libname}
This package contains the shared library for %{name}.

%package -n	%{gtkname}
Group:		System/Libraries
Summary:	Shared library part of %{name} - gtk
Obsoletes:	%{libname} < 3.5.1-1
Provides:	%{libname} = 3.5.1-1

%description -n	%{gtkname}
This package contains the shared library for %{name}-gtk.

%package -n	%{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n	%{girname}
GObject Introspection interface description for %{name}.

%package -n	%{devname}
Group:		Development/C
Summary:	Developent files for %{name}
Requires:	%{libname} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}

%description -n	%{devname}
This packages contains the development library and header files for %{name}.

%package -n	%{devgtk}
Group:		Development/C
Summary:	Developent files for %{name}-gtk
Requires:	%{gtkname} = %{version}-%{release}

%description -n	%{devgtk}
This packages contains the development library and header files for %{name}-gtk.

%prep
%setup -q

%build
%configure \
	--disable-static \
	--enable-compile-warnings=no

%make

%install
%makeinstall_std
%find_lang %{name} --with-gnome --all-name

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%define launchers %{_sysconfdir}/dynamic/launchers/webcam
# dynamic support
mkdir -p %{buildroot}%launchers
cat > %{buildroot}%launchers/%{name}.desktop << EOF
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

%post
update-alternatives --install %{launchers}/kde.desktop webcam.kde.dynamic %launchers/%{name}.desktop 60
update-alternatives --install %{launchers}/gnome.desktop webcam.gnome.dynamic %launchers/%{name}.desktop 60

%postun
if [ "$1" = "0" ]; then
   update-alternatives --remove webcam.kde.dynamic %launchers/%{name}.desktop
   update-alternatives --remove webcam.gnome.dynamic %launchers/%{name}.desktop
fi

%files -f %{name}.lang
%config(noreplace) %launchers/*.desktop
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/glib-2.0/schemas/org.gnome.Cheese.gschema.xml
%{_iconsdir}/hicolor/*/*/*
%{_mandir}/man1/cheese.1.xz
%{_datadir}/appdata/org.gnome.Cheese.appdata.xml
#{_datadir}/dbus-1/services/org.gnome.Cheese.service
#{_datadir}/dbus-1/services/org.gnome.Camera.service
#{_libexecdir}/gnome-camera-service
%{_datadir}/dbus-1/services/org.gnome.Cheese.service

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{gtkname}
%{_libdir}/lib%{name}-gtk.so.%{gtk_maj}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Cheese-%{gir_maj}.typelib

%files -n %{devname}
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/gir-1.0/Cheese-%{gir_maj}.gir
%{_datadir}/gtk-doc/html/%{name}/

%files -n %{devgtk}
%{_libdir}/lib%{name}-gtk.so
%{_libdir}/pkgconfig/%{name}-gtk.pc
