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

{% for classe,vmethods in _dict.iteritems() %}
class {{ classe.split('.')[-1] }} {

    {% for method in vmethods %}
    public static {{method.ret }} {{ method.name }}(Object thiz {{ method.proto }}) {
        Log.d("TAG","FUFFA");
        Context c = Utils.getContext();
        Method m = null;
        {{ method.ret }} retvalue;
        try {
            m = thiz.getClass().getMethod('{{ method.name }}', null);
            retvalue = ({{method.ret}}) m.invoke(thiz, null);
            Log.d(TAG, "FAKE FAKE REFLECTION RESULT: " + retvalue + " operator: ");
        } catch (NoSuchMethodException e) {
            e.printStackTrace();
        } catch (InvocationTargetException e) {
            e.printStackTrace();
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        }
        {% if method.ret == 'void' %}
            return;
        {% elif method.ret == 'android.os.IBinder' %}
            return null;
        {% else %}
            return retvalue;
        {% endif %}
    }
    {% endfor %}

}

{% endfor %}