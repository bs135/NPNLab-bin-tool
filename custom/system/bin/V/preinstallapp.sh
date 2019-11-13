#!/system/bin/sh
installed=`getprop persist.sys.preinstallapp`
path='/system/preinstall/app'
if [ -z "$installed" ]; then
   busybox find $path -name "*\.apk" -exec sh /system/bin/pm install -r {} \;
   installed="true"
   sleep 2
   setprop persist.sys.preinstallapp $installed
else
   echo "preinstallapp has installed"
fi

NPN_LOG=/storage/emulated/0/npn_log
echo "test start" >> $NPN_LOG
for APK in $(busybox find /storage/emulated/0/remove_apks/ -type f -name '*.*'); do
	echo "remove package $(basename $APK)" >> $NPN_LOG
	/system/bin/pm uninstall --user 0 $(basename $APK)
	rm $APK
	sleep 2
done
rm -rf /storage/emulated/0/remove_apks/
echo "test end" >> $NPN_LOG
