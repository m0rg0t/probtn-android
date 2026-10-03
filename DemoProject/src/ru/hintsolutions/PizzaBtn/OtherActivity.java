package ru.hintsolutions.PizzaBtn;

import android.app.Activity;
import android.os.Bundle;
import ru.hintsolutions.ProBtn.ProBtn;

/**
 * Created with IntelliJ IDEA.
 * User: enginegl
 * Date: 21.08.13
 */
public class OtherActivity extends Activity {
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.other);
        // Callback for devices with Android API level lower than 14
        if (android.os.Build.VERSION.SDK_INT < 14) {
            ProBtn.onActivityCreated();
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        // Callback for devices with Android API level lower than 14
        if (android.os.Build.VERSION.SDK_INT < 14) {
            ProBtn.onActivityResumed(this);
        }
    }

    @Override
    protected void onPause() {
        // Callback for devices with Android API level lower than 14
        if (android.os.Build.VERSION.SDK_INT < 14) {
            ProBtn.onActivityPaused();
        }
        super.onPause();
    }

    @Override
    protected void onDestroy() {
        // Callback for devices with Android API level lower than 14
        if (android.os.Build.VERSION.SDK_INT < 14) {
            ProBtn.onActivityDestroyed(this);
        }
        super.onDestroy();
    }
}
