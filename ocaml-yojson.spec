#
# Conditional build:
%bcond_without	ocaml_opt	# native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	yojson
%define		debug_package	%{nil}
Summary:	JSON library for OCaml
Summary(pl.UTF-8):	Biblioteka JSON dla OCamla
Name:		ocaml-%{module}
Version:	1.7.0
Release:	4
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/ocaml-community/yojson/releases
Source0:	https://github.com/ocaml-community/yojson/releases/download/%{version}/%{module}-%{version}.tbz
# Source0-md5:	b89d39ca3f8c532abe5f547ad3b8f84d
URL:		https://github.com/ocaml-community/yojson
BuildRequires:	cppo >= 1.5.0
BuildRequires:	ocaml >= 1:4.02.3
BuildRequires:	ocaml-biniou-devel >= 1.2.0
BuildRequires:	ocaml-dune
BuildRequires:	ocaml-easy-format-devel >= 1.0.1
BuildRequires:	ocaml-findlib >= 1.4
%requires_eq	ocaml-runtime
Requires:	ocaml-biniou >= 1.2.0
Requires:	ocaml-easy-format >= 1.0.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Yojson is an optimized parsing and printing library for the JSON
format. It addresses a few shortcomings of json-wheel including 3x
speed improvement, polymorphic variants and optional syntax for tuples
and variants.

%description -l pl.UTF-8
Yojson to zoptymalizowana biblioteka do analizy i wypisywania formatu
JSON. Wychodzi naprzeciw kilku ograniczeniom biblioteki json-wheel,
m.in. daje trzykrotne przyspieszenie, warianty polimorficzne i
składnię opcjonalną dla krotek i wariantów.

%package devel
Summary:	JSON library for OCaml - development part
Summary(pl.UTF-8):	Biblioteka JSON dla OCamla - cześć programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml
Requires:	ocaml-biniou-devel >= 1.2.0
Requires:	ocaml-easy-format-devel >= 1.0.1

%description devel
This package contains files needed to develop OCaml programs using
this library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki yojson.

%prep
%setup -q -n %{module}-%{version}

%build
dune build --verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/%{module}/*.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/%{module}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE.md README.md
%dir %{_libdir}/ocaml/yojson
%{_libdir}/ocaml/yojson/META
%{_libdir}/ocaml/yojson/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_bindir}/ydump
%attr(755,root,root) %{_libdir}/ocaml/yojson/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/ocaml/yojson/*.cmi
%{_libdir}/ocaml/yojson/*.cmt
%{_libdir}/ocaml/yojson/*.cmti
%{_libdir}/ocaml/yojson/*.mli
%if %{with ocaml_opt}
%{_libdir}/ocaml/yojson/*.a
%{_libdir}/ocaml/yojson/*.cmx
%{_libdir}/ocaml/yojson/*.cmxa
%endif
%{_libdir}/ocaml/yojson/dune-package
%{_libdir}/ocaml/yojson/opam
