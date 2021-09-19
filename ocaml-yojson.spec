#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), remove when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	yojson
%define		debug_package	%{nil}
Summary:	JSON library for OCaml
Name:		ocaml-%{module}
Version:	1.7.0
Release:	4
License:	BSD
Group:		Libraries
Source0:	https://github.com/ocaml-community/yojson/releases/download/%{version}/%{module}-%{version}.tbz
# Source0-md5:	b89d39ca3f8c532abe5f547ad3b8f84d
URL:		https://github.com/ocaml-community/yojson
BuildRequires:	cppo >= 1.5.0
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-biniou-devel >= 1.0.6
BuildRequires:	ocaml-dune
BuildRequires:	ocaml-easy-format-devel >= 1.0.1
BuildRequires:	ocaml-findlib >= 1.4
BuildRequires:	ocamlbuild-cppo >= 1.6.1
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
%requires_eq ocaml
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
dune build

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/ocaml}
%{__make} install \
	OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%dir %{_libdir}/ocaml/%{module}
%{_libdir}/ocaml/yojson/META
%{_libdir}/ocaml/yojson/dune-package
%{_libdir}/ocaml/yojson/opam
%if %{with ocaml_opt}
%{_libdir}/ocaml/%{module}/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%doc LICENSE.md
%{_libdir}/ocaml/%{module}/*.cm[ix]
%{_libdir}/ocaml/%{module}/*.cm[ao]
%{_libdir}/ocaml/%{module}/*.mli
%if %{with ocaml_opt}
%attr(755,root,root) %{_bindir}/ydump
%{_libdir}/ocaml/%{module}/*.[ao]
%{_libdir}/ocaml/%{module}/*.cmxa
%endif
%{_libdir}/ocaml/yojson/yojson.cmt
%{_libdir}/ocaml/yojson/yojson.cmti
%{_libdir}/ocaml/yojson/yojson_biniou.cmt
%{_libdir}/ocaml/yojson/yojson_biniou.cmti
