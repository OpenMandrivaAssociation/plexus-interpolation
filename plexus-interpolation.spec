%{?_javapackages_macros:%_javapackages_macros}
Name:           plexus-interpolation
Version:        1.15
Release:        7.1%{?dist}
Summary:        Plexus Interpolation API


License:        ASL 2.0 and ASL 1.1 and MIT
URL:            http://plexus.codehaus.org/plexus-components/plexus-interpolation
Source0:        https://github.com/sonatype/%{name}/archive/%{name}-%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch: noarch

BuildRequires: java-devel
BuildRequires: junit
BuildRequires: maven-local
BuildRequires: maven-resources-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-surefire-plugin
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-shared-reporting-impl
BuildRequires: maven-doxia-sitetools

%description
Plexus interpolator is the outgrowth of multiple iterations of development
focused on providing a more modular, flexible interpolation framework for
the expression language style commonly seen in Maven, Plexus, and other
related projects.

%package javadoc

Summary:        Javadoc for %{name}

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
%mvn_file  : plexus/interpolation
%mvn_build

%install
%mvn_install

%files -f .mfiles

%files javadoc -f .mfiles-javadoc

%changelog
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.15-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Thu Jan 17 2013 Michal Srb <msrb@redhat.com> - 1.15-4
- Build with xmvn

* Mon Nov 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.15-3
- Fix source URL to be stable

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Alexander Kurtakov <akurtako@redhat.com> 1.15-1
- Update to latest upstream.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 27 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.14-2
- Use add_maven_depmap macro
- Use more precise specification of files

* Tue Jul 26 2011 Jaromir Capik <jcapik@redhat.com> - 1.14-2
- Removal of plexus-maven-plugin dependency (not needed)
- Minor spec file changes according to the latest guidelines

* Tue May 17 2011 Alexander Kurtakov <akurtako@redhat.com> 1.14-1
- Update to upstream 1.14 version.
- Adapt to current guidelines.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 22 2009 Alexander Kurtakov <akurtako@redhat.com> 1.13-2
- Fix review comments.

* Tue Dec 22 2009 Alexander Kurtakov <akurtako@redhat.com> 1.13-1
- Initial package.
