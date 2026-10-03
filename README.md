ProBtn-Android
============

What the ProBtn is?
---------------------------

ProBtn is an interactive element that used to show custom content inside your application. If the button is tapped then the window with WebView would open. The url in the WebView is set using settings on our server.

Real example:
-----
![ScreenShot](http://www.probtn.com/wp-content/uploads/2013/09/pizzabtn-android.gif)

How to use ProBtn SDK
-----

1. Sign up to admin.probtn.com
2. Register your app: create new application, select it's platform (Android) and BundleID (root package name of your app)
3. Choose the site to promote in your application.
4. Integrate ProButton with your application using the following instructions:

Integrating ProBtn SDK with your Android application
-----

1. Clone repository or download project ZIP
2. Add ProButton.jar library to your project module and dependencies
3. Add "INTERNET", "ACCESS_COARSE_LOCATION" and "ACCESS_FINE_LOCATION" permissions to your AndroidManifest.xml 

    	<uses-permission android:name="android.permission.INTERNET"/>  
    	<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION"/>  
    	<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>  

4. For targets with API level >= 14 all is you need is just to add the following line to onCreate method of the root activity:
	
	ProBtn.open(this);
	
	
For targets with lower API levels you also need to set up the following callbacks for each activity in your app:

	public void onCreate(Bundle savedInstanceState) {
	    super.onCreate(savedInstanceState);
	    if (android.os.Build.VERSION.SDK_INT < 14) {
	        ProBtn.onActivityCreated();
	    }
	    ...
	}

	@Override
	protected void onResume() {
	super.onResume();
	    if (android.os.Build.VERSION.SDK_INT < 14) {
	        ProBtn.onActivityResumed(this);
	    }
	    ...
	}

	@Override
	protected void onPause() {
	    if (android.os.Build.VERSION.SDK_INT < 14) {
	        ProBtn.onActivityPaused();
	    }
	    super.onPause();
	    ...
	}

	@Override
	protected void onDestroy() {
	    if (android.os.Build.VERSION.SDK_INT < 14) {
	        ProBtn.onActivityDestroyed(this);
	    }
	    super.onDestroy();
	    ...
	}

5. Feel free to control the button at any time by calling ProBtn.showProBtn() and  ProBtn.hideProBtn() methods.
6. Button usage statistics for current package can be taken using the following method with callback:

	ProBtn.getUsageStatistics(new ProBtn.ProButtonStatisticsCallback() {
        	@Override
                public void done(JSONObject jsonObject, Exception e) {

                    // insert your code here

                }
        });

How to run example project? (using Intellij IDEA)
---------------
1. File->Import project..
2. Choose directory with example sources and press "OK"
3. "Create project from existing sources"
4. Specify project name and press "Next"
5. Select all directories and press "Next" 
6. Mark "ProButton" library as used in the project, press "Next"
7. Include selected module to the project and press "Next"
8. Choose project SDK (Android 4.x.x Platform recommended), press "Next"
9. Press "Next"
10. Example project is ready to run.
	
Server side
---------------

All the settings are taken from the server so you can customize the appearance of the button by simply changing the on the server side. 
The server address is [admin.probtn.com](http://admin.probtn.com/ "admin.probtn.com"). After all the data loaded from the server the button would appear automatically.


