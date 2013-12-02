#!/bin/bash

############################
##
## Frontend
##
############################

# Get the frontend
apt-get install git build-essential python-pip python-dev python-django python-django-south python-simplejson
pip install gevent gevent-websocket
git clone https://github.com/synnack/videoconference.git

# Get Medooze
apt-get install subversion ant libnb-java5-java openjdk-6-jre openjdk-6-jdk libcommons-logging-java libxmlrpc3-common-java libxmlrpc3-client-java libws-commons-util-java
svn checkout svn://svn.code.sf.net/p/mcumediaserver/code/trunk/ medooze

############################
##
## MCU Web
##
############################

export JAVA_HOME=/usr/lib/jvm/java-6-openjdk-amd64/

# Compile XmlRpcMcuClient
perl -pi -e 's/file.reference.commons-logging-1.1.jar=.*$/file.reference.commons-logging-1.1.jar=\/usr\/share\/java\/commons-logging-1.1.3.jar/' medooze/XmlRpcMcuClient/nbproject/project.properties
perl -pi -e 's/file.reference.ws-commons-util-1.0.2.jar=.*$/file.reference.ws-commons-util-1.0.2.jar=\/usr\/share\/java\/ws-commons-util-1.0.1.jar/' medooze/XmlRpcMcuClient/nbproject/project.properties
perl -pi -e 's/file.reference.xmlrpc-client-3.1.3.jar=.*$/file.reference.xmlrpc-client-3.1.3.jar=\/usr\/share\/java\/xmlrpc-client-3.1.3.jar/' medooze/XmlRpcMcuClient/nbproject/project.properties
perl -pi -e 's/file.reference.xmlrpc-common-3.1.3.jar=.*$/file.reference.xmlrpc-common-3.1.3.jar=\/usr\/share\/java\/xmlrpc-common-3.1.3.jar/' medooze/XmlRpcMcuClient/nbproject/project.properties
(cd medooze/XmlRpcMcuClient/;ant)


# Get sailfin
wget -c http://download.java.net/javaee5/sailfin/v2_branch/promoted/Linux/sailfin-installer-v2-b31g-linux.jar
echo A |java -jar sailfin-installer-v2-b31g-linux.jar
(cd sailfin;ant -f setup.xml)

# Compile mcuWeb
perl -pi -e 's/file.reference.commons-logging-1.1.jar=.*$/file.reference.commons-logging-1.1.jar=\/usr\/share\/java\/commons-logging-1.1.3.jar\r/' medooze/mcuWeb/nbproject/project.properties
perl -pi -e 's/file.reference.ws-commons-util-1.0.2.jar=.*$/file.reference.ws-commons-util-1.0.2.jar=\/usr\/share\/java\/ws-commons-util-1.0.1.jar\r/' medooze/mcuWeb/nbproject/project.properties
perl -pi -e 's/file.reference.xmlrpc-client-3.1.3.jar=.*$/file.reference.xmlrpc-client-3.1.3.jar=\/usr\/share\/java\/xmlrpc-client-3.1.3.jar\r/' medooze/mcuWeb/nbproject/project.properties
perl -pi -e 's/file.reference.xmlrpc-common-3.1.3.jar=.*$/file.reference.xmlrpc-common-3.1.3.jar=\/usr\/share\/java\/xmlrpc-common-3.1.3.jar\r/' medooze/mcuWeb/nbproject/project.properties
perl -pi -e 's/file.reference.ssa-api.jar=.*$/file.reference.ssa-api.jar=..\/..\/sailfin\/lib\/ssa-api.jar\r/' medooze/mcuWeb/nbproject/project.properties
(cd medooze/mcuWeb;ant -Dj2ee.server.home=../../sailfin -Dlibs.CopyLibs.classpath=/usr/share/netbeans/java5/ant/extra/org-netbeans-modules-java-j2seproject-copylibstask.jar)


# Get Mobicents for deployment!
if [ \! -d mss-3.0.0 ]; then
	apt-get install unzip
	wget -c https://mobicents.ci.cloudbees.com/job/Mobicents-SipServlets-Release/lastSuccessfulBuild/artifact/mss-3.0.0-SNAPSHOT-jboss-as-7.1.3.Final-1383698249.zip
	unzip mss-3.0.0-SNAPSHOT-jboss-as-7.1.3.Final-1383698249.zip
	mv mss-3.0.0-SNAPSHOT-jboss-as-7.1.3.Final mss-3.0.0
fi

ln -s ../../../medooze/mcuWeb/dist/mcuWeb.sar mss-3.0.0/standalone/deployments/mcuWeb.war
# NOTE: Start mss with: ./standalone.sh -c standalone-sip.xml -b 0.0.0.0
# WHY NO IPv6?!

############################
##
## MCU
##
############################
apt-get install yasm libgsm1-dev libtool automake autoconf libsrtp-dev libssl-dev pkg-config libgtk2.0-dev libnss3-dev libjpeg62-dev libgcrypt11-dev

# x264
(
	git clone git://git.videolan.org/x264.git
	cd x264
	./configure --enable-debug --enable-shared --enable-pic
	make -j20
	make install
)
# ffmpeg
(
	git clone git://git.videolan.org/ffmpeg.git
	cd ffmpeg
	./configure --enable-shared --enable-gpl --enable-nonfree --disable-stripping --enable-zlib --enable-avresample --enable-decoder=png
	make -j20
	make install
)
# xmlrpc-c
(
	wget -c http://downloads.sourceforge.net/project/xmlrpc-c/Xmlrpc-c%20Super%20Stable/1.16.35/xmlrpc-c-1.16.35.tgz
	tar xvzf xmlrpc-c-1.16.35.tgz
	cd xmlrpc-c-1.16.35
	./configure
	make
	make install
)
# mp4v2
(
	svn checkout http://mp4v2.googlecode.com/svn/trunk/ mp4v2
	cd mp4v2
	autoreconf -fiv
	./configure
	make -j20
	make install
	make install-man
	make dist
)
# libvpx / VP8
(
	git clone http://git.chromium.org/webm/libvpx.git
	cd libvpx
	./configure --enable-shared
	make -j20
	make install
)
# speex
(
	wget -c http://downloads.xiph.org/releases/speex/speex-1.2rc1.tar.gz
	tar xvzf speex-1.2rc1.tar.gz
	cd speex-1.2rc1
	./configure
	make -j20
	make install
)
# opus
(
	wget -c http://downloads.xiph.org/releases/opus/opus-1.0.2.tar.gz
	tar xvzf opus-1.0.2.tar.gz
	cd opus-1.0.2
	./configure
	make -j20
	make install
)
# webrtc
(
	svn co http://src.chromium.org/chrome/trunk/tools/depot_tools
	export PATH="$PATH:$PWD/depot_tools"
	mkdir webrtc
	cd webrtc
	gclient config http://webrtc.googlecode.com/svn/trunk
	gclient sync --force
	gclient runhooks --force
	cd trunk
	build/gyp_chromium --depth=. all.gyp
	ninja -C out/Release/ common_audio
	ninja -C out/Debug/ common_audio
)
# mcu
(
	cd medooze/mcu/
	perl -pi -e 's/\/usr\/local\/src/..\/../' Makefile
	perl -pi -e 's/\/usr\/local\/src/..\/../' config.mk
	make -j20
)
