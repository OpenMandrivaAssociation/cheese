%define gtk_major 21
%define major 3
%define girmajor 3.0
%define libname %mklibname %{name} %{major}
%define gtkname %mklibname %{name}-gtk %{gtk_major}
%define girname	%mklibname %{name}-gtk-gir %{girmajor}
%define develname %mklibname -d %{name}
%define develgtk %mklibname -d %{name}-gtk

Summary:	A GNOME application for taking pictures and videos from a webcam
Name:		cheese
Version:	3.4.1
Release:	1
License:	GPLv2+
Group:		Video
URL:		http://www.gnome.org/projects/cheese/
Source:		ftp://ftp.gnome.org/pub/GNOME/sources/cheese/%{name}-%{version}.tar.xz

BuildRequires:	desktop-file-utils
BuildRequires:	glib2.0-common
BuildRequires:	gnome-doc-utils >= 0.20
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	vala vala-devel
BuildRequires:	pkgconfig(cairo) >= 1.10.0
BuildRequires:	pkgconfig(clutter-1.0) >= 1.6.1
BuildRequires:	pkgconfig(clutter-gst-1.0) >= 1.0.0
BuildRequires:	pkgconfig(clutter-gtk-1.0) >= 0.91.8
BuildRequires:	pkgconfig(gdk-3.0) >= 2.99.4
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
BuildRequires:	pkgconfig(gee-1.0) >= 0.6.0
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(glib-2.0) >= 2.28.0
BuildRequires:	pkgconfig(gnome-desktop-3.0) >= 2.91.6
BuildRequires:	pkgconfig(gnome-video-effects)
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.6.7
BuildRequires:	pkgconfig(gstreamer-0.10) >= 0.10.32
BuildRequires:	pkgconfig(gstreamer-plugins-base-0.10) >= 0.10.32
BuildRequires:	pkgconfig(gtk+-3.0) >= 2.99.4
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libcanberra-gtk3) >= 0.26
BuildRequires:	pkgconfig(librsvg-2.0) >= 2.32.0
BuildRequires:	pkgconfig(mx-1.0)
BuildRequires:	pkgconfig(nautilus-sendto)
BuildRequires:	pkgconfig(pangocairo) >= 1.28.0
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xtst)

Requires: gsettings-desktop-schemas
Requires: gstreamer0.10-plugins-base
Requires: gstreamer0.10-plugins-good

# TODO update features once added upstream
%description
Cheese is a Photobooth-inspired GNOME application for taking pictures and
videos from a webcam. It also includes fancy graphical effects based on
the gstreamer-backend.

%package -n %{libname}
Group: System/Libraries
Summary: Shared library part of %{name}

%description -n %{libname}
This package contains the shared library for %{name}.

%package -n %{gtkname}
Group: System/Libraries
Summary: Shared library part of %{name} - gtk

%description -n %{gtkname}
This package contains the shared library for %{name}-gtk.

%package -n %{girname}
Summary: GObject Introspection interface description for %{name}
Group: System/Libraries

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n %{develname}
Group: Development/C
Summary: Developent files for %{name}
Requires: %{libname} = %{version}-%{release}
Requires: %{girname} = %{version}-%{release}

%description -n %{develname}
This packages contains the development library and header files for %{name}.

%package -n %{develgtk}
Group: Development/C
Summary: Developent files for %{name}-gtk
Requires: %{gtkname} = %{version}-%{release}

%description -n %{develgtk}
This packages contains the development library and header files for %{name}-gtk.

%prep
%setup -q

%build
%configure2_5x \
	--disable-static

%make

%install
%makeinstall_std
%find_lang %{name} --with-gnome --all-name
# copied from aisleriot
echo "%%dir %%{_datadir}/help/C" >> aisleriot.lang
echo "%%{_datadir}/help/C/%%{name}" >> aisleriot.lang
for l in ca cs de el en_GB es fi fr gl hu it ko lv nl oc pa pt_BR ru sl sv te th zh_CN; do
	echo "%%dir %%{_datadir}/help/$l"
	echo "%%lang($l) %%{_datadir}/help/$l/%%{name}"
done >> %{name}.lang

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
%{_datadir}/%{name}
%{_datadir}/glib-2.0/schemas/org.gnome.Cheese.gschema.xml
%{_iconsdir}/hicolor/*/*/*
%{_mandir}/man1/cheese.1*

%files -n %{libname}
%{_libdir}/lib%{name}-gtk.so.%{gtk_major}*

%files -n %{gtkname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Cheese-%{girmajor}.typelib

%files -n %{develname}
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_datadir}/gir-1.0/Cheese-%{girmajor}.gir
%{_datadir}/gtk-doc/html/%{name}/

%files -n %{develgtk}
%{_libdir}/lib%{name}-gtk.so
%{_libdir}/pkgconfig/%{name}-gtk.pc

