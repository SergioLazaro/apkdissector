package x;

import android.os.*;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.widget.Toast;
import android.util.Log;
import android.content.pm.PackageManager;
import dalvik.system.PathClassLoader;


public class Fuffa{

}


class MainActivity {

    
    public static void createConn(Object thiz ) {
        Log.d("TAG","FUFFA");
        Context c = Utils.getContext();
        Method m = null;
        void retvalue;
        try {
            m = thiz.getClass().getMethod('createConn', null);
            retvalue = (void) m.invoke(thiz, null);
            Log.d(TAG, "FAKE FAKE REFLECTION RESULT: " + retvalue + " operator: ");
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
        
            return;
        
    }
    
    public static void getDeviceID(Object thiz ) {
        Log.d("TAG","FUFFA");
        Context c = Utils.getContext();
        Method m = null;
        void retvalue;
        try {
            m = thiz.getClass().getMethod('getDeviceID', null);
            retvalue = (void) m.invoke(thiz, null);
            Log.d(TAG, "FAKE FAKE REFLECTION RESULT: " + retvalue + " operator: ");
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
        
            return;
        
    }
    
    public static  mysaveFile(Object thiz ) {
        Log.d("TAG","FUFFA");
        Context c = Utils.getContext();
        Method m = null;
         retvalue;
        try {
            m = thiz.getClass().getMethod('mysaveFile', null);
            retvalue = () m.invoke(thiz, null);
            Log.d(TAG, "FAKE FAKE REFLECTION RESULT: " + retvalue + " operator: ");
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
        
            return retvalue;
        
    }
    
    public static  onCreateOptionsMenu(Object thiz , android.view.Menu arg1 ) {
        Log.d("TAG","FUFFA");
        Context c = Utils.getContext();
        Method m = null;
         retvalue;
        try {
            m = thiz.getClass().getMethod('onCreateOptionsMenu', null);
            retvalue = () m.invoke(thiz, null);
            Log.d(TAG, "FAKE FAKE REFLECTION RESULT: " + retvalue + " operator: ");
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
        
            return retvalue;
        
    }
    
    public static  onOptionsItemSelected(Object thiz , android.view.MenuItem arg1 ) {
        Log.d("TAG","FUFFA");
        Context c = Utils.getContext();
        Method m = null;
         retvalue;
        try {
            m = thiz.getClass().getMethod('onOptionsItemSelected', null);
            retvalue = () m.invoke(thiz, null);
            Log.d(TAG, "FAKE FAKE REFLECTION RESULT: " + retvalue + " operator: ");
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
        
            return retvalue;
        
    }
    
    public static void reflectGetDeviceID(Object thiz ) {
        Log.d("TAG","FUFFA");
        Context c = Utils.getContext();
        Method m = null;
        void retvalue;
        try {
            m = thiz.getClass().getMethod('reflectGetDeviceID', null);
            retvalue = (void) m.invoke(thiz, null);
            Log.d(TAG, "FAKE FAKE REFLECTION RESULT: " + retvalue + " operator: ");
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
        
            return;
        
    }
    

}


