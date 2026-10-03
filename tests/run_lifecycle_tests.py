#!/usr/bin/env python3
"""Compile real demo activities against isolated, test-only Android/ProBtn doubles.
No vendor JAR, Android runtime, device, location, network or service is executed.
"""
import pathlib
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
STUBS = {
"android/os/Bundle.java": "package android.os; public class Bundle {}",
"android/os/Build.java": "package android.os; public class Build { public static class VERSION { public static int SDK_INT; } }",
"android/content/Intent.java": "package android.content; public class Intent { public final Class<?> target; public Intent(Object context, Class<?> target) { this.target = target; } }",
"android/view/View.java": "package android.view; public class View { public interface OnClickListener { void onClick(View view); } private OnClickListener listener; public void setOnClickListener(OnClickListener value) { listener = value; } public void click() { listener.onClick(this); } }",
"android/app/Activity.java": """package android.app;
import android.view.View;
public class Activity {
 public int layout; public android.content.Intent started;
 private final java.util.Map<Integer,View> views = new java.util.HashMap<Integer,View>();
 public void onCreate(android.os.Bundle state) {}
 protected void onResume() {} protected void onPause() {} protected void onDestroy() {}
 public void setContentView(int value) { layout=value; }
 public View findViewById(int id) { if (!views.containsKey(id)) views.put(id,new View()); return views.get(id); }
 public void startActivity(android.content.Intent intent) { started=intent; }
}""",
"ru/hintsolutions/ProBtn/ProBtn.java": """package ru.hintsolutions.ProBtn;
public class ProBtn {
 public static final java.util.List<String> events = new java.util.ArrayList<String>();
 public static Object resumed, destroyed, opened, shown;
 public static void open(Object activity) { opened=activity; events.add("open"); }
 public static void show(Object activity) { shown=activity; events.add("show"); }
 public static void hide() { events.add("hide"); }
 public static void onActivityCreated() { events.add("create"); }
 public static void onActivityResumed(Object activity) { resumed=activity; events.add("resume"); }
 public static void onActivityPaused() { events.add("pause"); }
 public static void onActivityDestroyed(Object activity) { destroyed=activity; events.add("destroy"); }
}""",
"ru/hintsolutions/PizzaBtn/R.java": "package ru.hintsolutions.PizzaBtn; public class R { public static class layout { public static int main=1, other=2; } public static class id { public static int button=1, showButton=2, hideButon=3; } }",
"ru/hintsolutions/PizzaBtn/LifecycleTest.java": """package ru.hintsolutions.PizzaBtn;
import ru.hintsolutions.ProBtn.ProBtn;
public class LifecycleTest {
 static void check(boolean condition, String message) { if (!condition) throw new AssertionError(message); }
 public static void main(String[] args) {
  int cases=0;
  for (int api : new int[]{8,10,11,12,13,14,21,35}) {
   android.os.Build.VERSION.SDK_INT=api;
   for (int recreation=0; recreation<2; recreation++) {
    ProBtn.events.clear();
    MainActivity main=new MainActivity();
    main.onCreate(recreation==0 ? null : new android.os.Bundle());
    main.onResume(); main.onPause(); main.onResume(); main.onPause(); main.onDestroy();
    String expected=api<14 ? "[open, create, resume, pause, resume, pause, destroy]" : "[open]";
    check(ProBtn.events.toString().equals(expected), "MainActivity API "+api+" expected "+expected+" got "+ProBtn.events);
    check(ProBtn.opened==main && main.layout==R.layout.main,"main setup");
    if (api<14) check(ProBtn.resumed==main && ProBtn.destroyed==main,"main callback identity");
    main.findViewById(R.id.button).click();
    check(main.started.target==OtherActivity.class,"navigation target preserved");
    main.findViewById(R.id.showButton).click(); main.findViewById(R.id.hideButon).click();
    check(ProBtn.shown==main && ProBtn.events.get(ProBtn.events.size()-1).equals("hide"),"show/hide controls");
    ProBtn.events.clear();
    OtherActivity other=new OtherActivity();
    other.onCreate(recreation==0 ? null : new android.os.Bundle());
    other.onResume(); other.onPause(); other.onResume(); other.onPause(); other.onDestroy();
    expected=api<14 ? "[create, resume, pause, resume, pause, destroy]" : "[]";
    check(ProBtn.events.toString().equals(expected),"OtherActivity API "+api+" expected "+expected+" got "+ProBtn.events);
    check(other.layout==R.layout.other,"other layout");
    if (api<14) check(ProBtn.resumed==other && ProBtn.destroyed==other,"other callback identity");
    cases+=2;
   }
  }
  System.out.println("PASS: "+cases+" production activity lifecycle cases and navigation/show/hide checks");
 }
}""",
}

def main():
    with tempfile.TemporaryDirectory(prefix="probtn-lifecycle-") as directory:
        work=pathlib.Path(directory)
        sources=[]
        for name, content in STUBS.items():
            target=work/name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content)
            sources.append(str(target))
        sources += [str(ROOT/"DemoProject/src/ru/hintsolutions/PizzaBtn"/name) for name in ("MainActivity.java","OtherActivity.java")]
        subprocess.run(["java","com.sun.tools.javac.Main","-source","8","-target","8","-Xlint:-options","-d",str(work/"classes")]+sources,check=True)
        subprocess.run(["java","-cp",str(work/"classes"),"ru.hintsolutions.PizzaBtn.LifecycleTest"],check=True)

if __name__ == "__main__":
    main()
