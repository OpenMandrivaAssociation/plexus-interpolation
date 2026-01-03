Name:           plexus-interpolation
Version:        1.27
Release:        1
Summary:        Plexus Interpolation API
# Most of the code is ASL 2.0, a few source files are ASL 1.1 and some tests are MIT
License:        Apache-2.0 AND Apache-1.1 AND MIT
URL:            https://github.com/codehaus-plexus/plexus-interpolation
BuildArch:      noarch

Source0:        https://github.com/codehaus-plexus/plexus-interpolation/archive/plexus-interpolation-%{version}.tar.gz

Patch1:         0001-Use-PATH-env-variable-instead-of-JAVA_HOME.patch

BuildRequires:  javapackages-bootstrap

%description
Plexus interpolator is the outgrowth of multiple iterations of development
focused on providing a more modular, flexible interpolation framework for
the expression language style commonly seen in Maven, Plexus, and other
related projects.

%prep
%autosetup -p1 -C
%pom_add_dep junit:junit:4.13.1:test
%pom_remove_plugin :maven-release-plugin
%pom_remove_plugin :maven-scm-publish-plugin

%build
%mvn_file : plexus/interpolation
%mvn_build -j

%install
%mvn_install

%files -f .mfiles
