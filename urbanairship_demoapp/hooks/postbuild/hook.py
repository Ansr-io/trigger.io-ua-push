import shutil
import sys
import os
import re

APP_PACKAGE_NAME = "com.plugtester"
INFO = "[    ODR] UA POST BUILD HOOK - info @ petehobson.com/contact"

print (INFO)

def build_android():
    """
    android requires:
    - a properties file in the app root
    - values in manifest replacing to your package name NB change com.plugtester to your package
    - shim app class in manifest
    """
    fpath = os.path.dirname(os.path.abspath(__file__))
    shutil.copy2(fpath + '/uaplugin/airshipconfig.properties', 'android/assets/airshipconfig.properties')

    with open("android/AndroidManifest.xml", "rw") as myfile:
        data = myfile.read()
        myfile.close()
    with open("android/AndroidManifest.xml", "w+b") as myfile:
        patched = re.sub(r'(ODR_PACKAGE_TOKEN)', APP_PACKAGE_NAME, data)
        patched = re.sub(r'(io.trigger.forge.android.core.ForgeApp)',
            "io.trigger.forge.android.modules.urbanairship.UAShim", patched)

        myfile.write(patched)
        myfile.close()

def build_ios():
    """
    ios requires:
    - plist config fie in simulator and device packages
    """
    fpath = os.path.dirname(os.path.abspath(__file__))
    shutil.copy2(fpath + '/uaplugin/AirshipConfig.plist', 'ios/simulator-ios.app/AirshipConfig.plist')
    shutil.copy2(fpath + '/uaplugin/AirshipConfig.plist', 'ios/device-ios.app/AirshipConfig.plist')


if (sys.argv[1] == 'android'):
    build_android()

if (sys.argv[1] == 'ios'):
    build_ios()
