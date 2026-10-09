[app]
title = Mobile Painter
package.name = mobilepainter
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0
orientation = portrait
fullscreen = 1
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.accept_sdk_license = True

# Core required default specifications
android.api = 33
android.minapi = 24
android.ndk_api = 24
android.skip_update = False
android.private_storage = True
android.package = %(package.name)s
android.domain = %(package.domain)s

[buildozer]
log_level = 2
warn_on_root = 1
