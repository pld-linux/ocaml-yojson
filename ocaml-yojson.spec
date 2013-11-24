#
# Conditional build:
%bcond_with	opt		# build opt

%define		pkgname	yojson
%define		debug_package	%{nil}
Summary:	JSON library for OCaml
Name:		ocaml-%{pkgname}
Version:	1.1.7
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://mjambon.com/releases/yojson/yojson-%{version}.tar.gz
# Source0-md5:	7017f2009a33d08c25ab0478598c9023
URL:		http://mjambon.com/yojson.html
BuildRequires:	cppo >= 0.9.3
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-biniou-devel >= 1.0.6
BuildRequires:	ocaml-easy-format-devel >= 1.0.1
BuildRequires:	ocaml-findlib >= 1.4
%requires_eq	ocaml-runtime
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

%description devel
This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów używających
tej biblioteki.

%prep
%setup -q -n %{pkgname}-%{version}

%build
%{__make} -j1 all %{?with_opt:opt} \
	CC="%{__cc} %{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{%{module},stublibs}
cp -p *.cm[ixa]* $RPM_BUILD_ROOT%{_libdir}/ocaml/%{module}

install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
cat > $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}/META <<EOF
requires = ""
version = "%{version}"
directory = "+%{module}"
archive(byte) = "%{module}.cma"
archive(native) = "%{module}.cmxa"
linkopts = ""
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc LICENSE *.mli
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/%{module}/*.cm[ixa]*
%{_libdir}/ocaml/site-lib/%{module}
