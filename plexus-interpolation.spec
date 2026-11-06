Name:		plexus-interpolation
Version:	1.30.0
Release:	1
Summary:	Resolves expression placeholders in strings
Group:		Development/Java
License:	ASL 2.0
URL:		https://github.com/codehaus-plexus/plexus-interpolation
Source0:	https://github.com/codehaus-plexus/plexus-interpolation/archive/refs/tags/plexus-interpolation-%{version}.tar.gz#/plexus-interpolation-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	mvn(org.codehaus.plexus:plexus:pom::)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven

%description
Plexus Interpolation resolves expression placeholders in strings.
1.30.0 caches interpolator answers and adds a feedback value source.
Tests are skipped.

%prep
%setup -q -n plexus-interpolation-plexus-interpolation-%{version}
# The bundle plugin is not packaged, and it is what defines bundle packaging.
python - <<'PY'
from pathlib import Path
path = Path("pom.xml")
text = path.read_text()
old = "<packaging>bundle</packaging>"
if old not in text:
    raise SystemExit("bundle packaging not found")
path.write_text(text.replace(old, "<packaging>jar</packaging>", 1))
PY

%files -f .mfiles
%doc README.md
