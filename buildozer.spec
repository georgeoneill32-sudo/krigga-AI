[app]
title = Krigga AI
package.name = kriggaai
package.domain = org.krigga
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# This line is now perfectly formatted inside the [app] section!
requirements = python3,kivy,requests,urllib3,certifi

orientation = portrait
fullscreen = 0
android.permissions = INTERNET
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
