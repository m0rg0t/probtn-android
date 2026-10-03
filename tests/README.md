# Offline sample lifecycle regression

Run `python3 tests/run_lifecycle_tests.py` with Python 3 and a JDK (CI uses the
runner's JDK 21). This compiles the **actual two demo activity source files**,
not copied implementations, with test-only Android and ProBtn doubles in a
temporary directory. No external Python/Java package, vendor JAR, Android
runtime, service request, location, emulator, or handset is used.

The 32 cases cover API 8, 10, 11, 12, 13, 14, 21 and 35; initial creation and
recreation; repeated pause/resume; callback order and activity identity;
navigation and explicit show/hide. API 14+ must not get duplicate manual SDK
callbacks. The former `< 11` checks fail at API 11. Automatic
[ActivityLifecycleCallbacks](https://developer.android.com/reference/android/app/Application.ActivityLifecycleCallbacks)
were introduced at API 14, matching the README's integration boundary.

These tests check the sample's calls at its SDK boundary. They do **not** prove
vendor SDK internals, rendering, device behavior, or full APK compatibility.
The test compiler uses Java 8 syntax/bytecode settings only for this host-JVM
harness; the application's Android/Ant settings and binary dependencies are
unchanged. No current SDK dependency upgrade is claimed. Full modernization
needs a rebuildable or provenance-verified current ProBtn SDK and a reproducible
Android build baseline. The original min/target platform and vendor assets
remain intact.
