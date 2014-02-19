#
# Conditional build:
%bcond_without	opt		# build opt

%define		module	yojson
%define		debug_package	%{nil}
Summary:	JSON library for OCaml
Name:		ocaml-%{module}
Version:	1.1.8
Release:	2
License:	BSD
Group:		Libraries
Source0:	http://mjambon.com/releases/yojson/yojson-%{version}.tar.gz
# Source0-md5:	e3c53004f74410c3835d851b02c1bf21
URL:		http://mjambon.com/yojson.html
BuildRequires:	cppo >= 0.9.3
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-biniou-devel >= 1.0.6
BuildRequires:	ocaml-easy-format-devel >= 1.0.1
BuildRequires:	ocaml-findlib >= 1.4
%requires_eq	ocaml-runtime
Requires:	ocaml-biniou >= 1.0.6
Requires:	ocaml-easy-format >= 1.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Yojson is an optimized parsing and printing library for the JSON
format. It addresses a few shortcomings of json-wheel including 3x
speed improvement, polymorphic variants and optional syntax for tuples
and variants. . It is a replacement for json-wheel
(libjson-wheel-ocaml-dev). . This package contain the development
files needed for programming with the library.

%description -l pl.UTF-8
Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających tej biblioteki.

%package devel
Summary:	yojson binding for OCaml - development part
Summary(pl.UTF-8):	Wiązania yojson dla OCamla - cześć programistyczna
Group:		Development/Libraries
%requires_eq	ocaml
Requires:	%{name} = %{version}-%{release}
Requires:	ocaml-biniou-devel >= 1.0.6
Requires:	ocaml-easy-format-devel >= 1.0.1

%description devel
This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%prep
%setup -q -n %{module}-%{version}

%build
%{__make} -j1 all %{?with_opt:opt} \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/ocaml}
%{__make} install \
	OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

# move to dir pld ocamlfind looks
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
mv $RPM_BUILD_ROOT%{_libdir}/ocaml/{,site-lib/}%{module}/META
cat <<EOF >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}/META
directory="+%{module}"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/*.cmxs
%{_libdir}/ocaml/site-lib/%{module}

%files devel
%defattr(644,root,root,755)
%doc LICENSE
%{_libdir}/ocaml/%{module}/*.cm[ix]
%{_libdir}/ocaml/%{module}/*.cm[ao]
%{_libdir}/ocaml/%{module}/*.mli
%if %{with opt}
%attr(755,root,root) %{_bindir}/ydump
%{_libdir}/ocaml/%{module}/*.[ao]
#%{_libdir}/ocaml/%{module}/*.cmxa
%endif
