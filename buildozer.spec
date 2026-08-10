[app]
title = 유지호의 타자게임
package.name = jihotyping
package.domain = org.jiho
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3,kivy
orientation = portrait
fullscreen = 0

# 핵심: 안정적인 안드로이드 SDK 및 Build-tools 버전 지정
android.api = 33
android.minapi = 21
android.sdk_build_tools_version = 33.0.2
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
