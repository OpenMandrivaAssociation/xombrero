%if %{mdvver} >= 201200
%define gtkver 3
%else
%define gtkver 2
%endif

Summary:	A minimalists web browser
Name:		xombrero
Version:	1.2.2
Release:	2
License:	MIT
Group:		Networking/WWW
URL:		https://opensource.conformal.com/wiki/xombrero
Obsoletes:	xxxterm < 2.0

Source0:	https://opensource.conformal.com/snapshots/%{name}/%{name}-%{version}.tgz
Patch0:		xombrero-1.2.2-mdv-usr-prefix.patch
%if %{gtkver} == 3
BuildRequires:	webkitgtk3-devel >= 1.3.1
%else
BuildRequires:	webkitgtk-devel >= 1.3.1
%endif
BuildRequires:	gtk+%{gtkver}-devel libsoup-devel gnutls-devel libbsd-devel
BuildRequires:	glib-networking

%description
%{name} is a minimalist web browser with sophisticated security features
designed-in (rather than through an add-on). In particular, it provides both
persistent and per-session controls for scripts and cookies, making it easy
to thwart tracking and scripting attacks.

In additional to providing a familiar mouse-based interface like other web
browsers, it offers a set of vi-like keyboard commands for users who prefer
to keep their hands on their keyboard.

The default settings provide a secure environment. With simple keyboard
commands, the user can "whitelist" specific sites, allowing cookies and scripts
from those sites. 

%prep
%setup -q
%patch0 -p1
sed 's,/usr/local,/usr,' -i %{name}.conf

%build
cd linux
export CFLAGS="%{optflags}"
%{__make} %{?_smp_mflags} OPTIMIZE="%{optflags}" GTK_VERSION=gtk%{gtkver} PREFIX=%{_prefix}

%install
export PREFIX=%{buildroot}/usr
pushd linux
%{__make} install
popd
for s in 16 32 48 64 128; do
	install -d -m 0755 %{buildroot}%{_iconsdir}/hicolor/${s}x${s}/apps/
	ln -s ../../../../%{name}/%{name}icon${s}.png %{buildroot}%{_iconsdir}/hicolor/${s}x${s}/apps/%{name}.png
done
install -D -m 0644 %{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
install -D -m 0644 style.css %{buildroot}%{_datadir}/%{name}/style.css
install -d -m 0755 %{buildroot}/%{_docdir}/%{name}
cat > %{buildroot}/%{_docdir}/%{name}/LICENSE << EOF
-= License =-

/*
 * Copyright (c) 2010, 2011 Marco Peereboom <marco@peereboom.us>
 * Copyright (c) 2011 Stevan Andjelkovic <stevan@student.chalmers.se>
 * Copyright (c) 2010, 2011 Edd Barrett <vext01@gmail.com>
 * Copyright (c) 2011 Todd T. Fries <todd@fries.net>
 * Copyright (c) 2011 Raphael Graf <r@undefined.ch>
 * Copyright (c) 2011 Michal Mazurek <akfaew@jasminek.net>
 *
 * Permission to use, copy, modify, and distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 */

-= javascript.h license =-

Javascript code was borrowed from the friendly folks at vimprobable2 under the following license:

/*
Copyright (c) 2009 Leon Winter
Copyright (c) 2009-2011 Hannes Schueller
Copyright (c) 2009-2010 Matto Fransen
Copyright (c) 2010-2011 Hans-Peter Deifel
Copyright (c) 2010-2011 Thomas Adam
Copyright (c) 2011 Albert Kim
Copyright (c) 2011 Daniel Carl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/
EOF

%files
%doc %dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/LICENSE
%{_mandir}/man1/%{name}.*
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/%{name}.css
%{_datadir}/%{name}/style.css
%{_datadir}/%{name}/%{name}*.png
%{_datadir}/%{name}/tld-rules
%{_iconsdir}/hicolor/*/apps/%{name}.png
