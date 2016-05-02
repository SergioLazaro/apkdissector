All of this scripts have the -h option to show the help info.

# Setting up the environment

Apkdissector uses a configuration file in which there is information about the directories where the tool
will write results, errors, check for the databases, how many threads will work and what version of PScout
is going to use. The configuration file its the first important step to launch apkdissector.

Example:

    [Configuration]
    OutputDirPath: /tmp/testing/results/
    PScoutVersion: 5.1.1
    ErrorLogPath: /tmp/testing/logs/
    DBPath: /tmp/testing/dbs/
    Threads: 5

If you launch apkdissector without creating the directories, the tool will create them. It is necessary
having the db files inside the [DBPath].

You can create the SQLite database with the script 'createSQLite.py' which will be explained in this file.

# Scripts

### main.py

Analyze a single apk or a sample of apks using the config.ini file explained before.
This tool creates a work directory for each APK analyzed. In this directory, three different files will be created.
This output files will be explained later.

    python main.py -f /path/to/apk
    python main.py -d /path/to/dir/with/apks/

    OUTPUT FILES:

    All files are written in the [outputdir] specified in the config.ini file

    * Cache file.

    Apkdissector uses Androguard for doing the static analysis of an APK. Androguard, to improve the workflow of an analysis,
    uses binary files(cache) to load it. This file is used in case you want to analyze more times an APK.

    * [APKHASH].json file.

    This file contains relevant information of the analysis.

    Example:

    {"hash":"cafc6530f07fbeac34eaf0eba7e822eef6bf0b03",
    "package_name":"org.zxl.appstats",
    "mapping":[
        {"permission":"android.permission.ACCESS_NETWORK_STATE",
	    "info":[
		    {"callerClass":"com/android/server/ConnectivityService","callerMethod":"getTetherableIfaces",
		    "callerMethodDesc":"()[Ljava/lang/String;"}
		]}
	]}

	As you can see, the JSON file contains the HASH of the APK, the package_name and a mapping of the permissions used.
	Every permission has a list of methods that need to import the permission in the Manifest.xml file. Some permissions,
	like ACCESS_NETWORK_STATE, have a lot of interesting methods. In the example, its only shown one method.

    * log.txt

    This file contains the output information generated while apkdissector was running.

    ERROR LOGS:

    In case there was a problem while running apkdissector, a file with the name equal to the APK hash will be created.
    It will be stored in the [errorlogpath] and it will contain a traceback of the error.

### statistics.py

Get some permission statistics(percentages) of a directory with analyzed APKs. This script look for the JSON
file written by the main.py script to recover information of an analyzed APK.

    example: python statistics.py -d /path/to/dir/with/analyzed/apks

### download-apks.py **
Download apks from virustotal.

    python download-apks.py -k virustotalAPIkey -f textfile
    python download-apks.py -k virustotalAPIkey -j jsonfile

    You should use  '-j' or '-f'.
    '-f' -> text file with apks hashes
    '-j' -> json file with apks hashes

### createSQLite.py **

Create SQLite DB in /tmp needed while running main.py

    python createSQLite.py -f /path/to/PScout/csv/file -o /path/output/directory/


