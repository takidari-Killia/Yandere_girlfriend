[app]
title = Yandere
package.name = yandere
package.domain = org.local
source.dir = .
source.include_exts = py,png,webp,jpg,json
source.exclude_dirs = bin,.buildozer,.github
version = 0.1
requirements = python3,kivy,pyjnius,android
orientation = portrait
fullscreen = 0
android.permissions = POST_NOTIFICATIONS,FOREGROUND_SERVICE,WRITE_SETTINGS,MODIFY_AUDIO_SETTINGS
android.api = 33
android.minapi = 26
android.archs = arm64-v8a
android.accept_sdk_license = True
#services = guardian:service/guardian.py:foreground

[buildozer]
log_level = 2
warn_on_root = 1
android.ndk = 25b
