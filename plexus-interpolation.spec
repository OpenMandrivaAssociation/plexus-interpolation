Name:		plexus-interpolation
Version:	1.30.0
Release:	2
Summary:	Resolves expression placeholders in strings
Group:		Development/Java
License:	ASL 2.0
URL:		https://github.com/codehaus-plexus/plexus-interpolation
Source0:	https://github.com/codehaus-plexus/plexus-interpolation/archive/refs/tags/plexus-interpolation-%{version}.tar.gz#/plexus-interpolation-%{version}.tar.gz
# Gradle 9.9.1 strictly pins 1.26. No prebuilt jars.
Source1:	https://github.com/codehaus-plexus/plexus-interpolation/archive/refs/tags/plexus-interpolation-1.26.tar.gz#/plexus-interpolation-1.26.tar.gz

BuildArch:	noarch
BuildRequires:	mvn(org.codehaus.plexus:plexus:pom::)
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven

%description
Plexus Interpolation resolves expression placeholders in strings.
1.30.0 caches interpolator answers and adds a feedback value source.
1.30.0 stays the default jar. Gradle 9.9.1 strictly pins 1.26, so
that jar is installed beside it. Tests are skipped.

%prep
%setup -q -n plexus-interpolation-plexus-interpolation-%{version}
%setup -q -T -D -a 1 -n plexus-interpolation-plexus-interpolation-%{version}
find . \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -delete
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

%build -a
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java}"
mkdir -p pi126/classes
find plexus-interpolation-plexus-interpolation-1.26/src/main/java -name '*.java' ! -name 'module-info.java' > pi126/sources.list
test -s pi126/sources.list
"$JAVA_HOME/bin/javac" --release 8 -encoding UTF-8 -Xlint:-options \
	-d pi126/classes @pi126/sources.list
"$JAVA_HOME/bin/jar" cf pi126/plexus-interpolation.jar -C pi126/classes .
cat > pi126/plexus-interpolation.pom << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.codehaus.plexus</groupId>
  <artifactId>plexus-interpolation</artifactId>
  <version>1.26</version>
  <name>Plexus Interpolation</name>
  <description>Resolves expression placeholders in strings.</description>
  <url>https://github.com/codehaus-plexus/plexus-interpolation</url>
  <licenses>
    <license>
      <name>Apache License, Version 2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
</project>
EOF

%install -p
sysjar install --buildroot %{buildroot} \
	--artifact pi126/plexus-interpolation.pom:pi126/plexus-interpolation.jar \
	--file-name plexus-interpolation-1.26 \
	--filelist .mfiles126
# 1.30.0 owns plexus-interpolation.sysjar. 1.26 keeps a second index.
/bin/mv %{buildroot}/usr/share/sysjar/index/org.codehaus.plexus/plexus-interpolation.sysjar \
	%{buildroot}/usr/share/sysjar/index/org.codehaus.plexus/plexus-interpolation-1.26.sysjar
sed -i 's|/usr/share/sysjar/index/org.codehaus.plexus/plexus-interpolation\.sysjar|/usr/share/sysjar/index/org.codehaus.plexus/plexus-interpolation-1.26.sysjar|' .mfiles126

%install -a
while IFS= read -r line; do
	grep -qxF -- "$line" .mfiles || printf '%s\n' "$line" >> .mfiles
done < .mfiles126

%check -a
export JAVA_HOME="${JAVA_HOME:-/usr/lib/jvm/java}"
cat > PiSmoke.java << 'EOF'
import org.codehaus.plexus.interpolation.StringSearchInterpolator;
import org.codehaus.plexus.interpolation.MapBasedValueSource;
import java.util.Collections;
public class PiSmoke {
	public static void main(String[] args) throws Exception {
		StringSearchInterpolator interpolator = new StringSearchInterpolator();
		interpolator.addValueSource(new MapBasedValueSource(Collections.singletonMap("k", "42")));
		String out = interpolator.interpolate("${k}");
		if (!"42".equals(out)) {
			throw new AssertionError(out);
		}
		System.out.println(args[0] + " " + out);
	}
}
EOF
"$JAVA_HOME/bin/javac" --release 8 -encoding UTF-8 -Xlint:-options \
	-cp %{buildroot}%{_javadir}/plexus-interpolation.jar PiSmoke.java
"$JAVA_HOME/bin/java" -cp "%{buildroot}%{_javadir}/plexus-interpolation.jar:." PiSmoke pi130_ok > check130.log
cat check130.log
grep -F -q 'pi130_ok 42' check130.log
"$JAVA_HOME/bin/javac" --release 8 -encoding UTF-8 -Xlint:-options \
	-cp %{buildroot}%{_javadir}/plexus-interpolation-1.26.jar PiSmoke.java
"$JAVA_HOME/bin/java" -cp "%{buildroot}%{_javadir}/plexus-interpolation-1.26.jar:." PiSmoke pi126_ok > check126.log
cat check126.log
grep -F -q 'pi126_ok 42' check126.log

%files -f .mfiles
%doc README.md
