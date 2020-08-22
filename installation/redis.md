---
layout: default
title: Redis
parent: Installation
nav_order: 2
---
1. TOC
{:toc}

## Ubuntu 18.04

### Step 1 — Installing and Configuring Redis
In order to get the latest version of Redis, we will use `apt` to install it from the official Ubuntu repositories.

Update your local apt package cache and install Redis by typing:

```Bash
sudo apt update
sudo apt install redis-server
```
This will download and install Redis and its dependencies. Following this, there is one important configuration change to make in the Redis configuration file, which was generated automatically during the installation.

Open this file with your preferred text editor:
```Bash
sudo nano /etc/redis/redis.conf
```
Inside the file, find the supervised directive. This directive allows you to declare an init system to manage Redis as a service, providing you with more control over its operation. The supervised directive is set to no by default. Since you are running Ubuntu, which uses the systemd init system, change this to systemd:

```Bash
/etc/redis/redis.conf
. . .

# If you run Redis from upstart or systemd, Redis can interact with your
# supervision tree. Options:
#   supervised no      - no supervision interaction
#   supervised upstart - signal upstart by putting Redis into SIGSTOP mode
#   supervised systemd - signal systemd by writing READY=1 to $NOTIFY_SOCKET
#   supervised auto    - detect upstart or systemd method based on
#                        UPSTART_JOB or NOTIFY_SOCKET environment variables
# Note: these supervision methods only signal "process is ready."
#       They do not enable continuous liveness pings back to your supervisor.
supervised systemd
```

That’s the only change you need to make to the Redis configuration file at this point, so save and close it when you are finished. Then, restart the Redis service to reflect the changes you made to the configuration file:

```Bash 
sudo systemctl restart redis.service
```
With that, you’ve installed and configured Redis and it’s running on your machine. Before you begin using it, though, it’s prudent to first check whether Redis is functioning correctly.

### Step 2 — Testing Redis
As with any newly-installed software, it’s a good idea to ensure that Redis is functioning as expected before making any further changes to its configuration. We will go over a handful of ways to check that Redis is working correctly in this step.

**Start by checking that the Redis service is running:**

```Bash
sudo systemctl status redis
```
If it is running without any errors, this command will produce output similar to the following:

```Bash
Output
● redis-server.service - Advanced key-value store
   Loaded: loaded (/lib/systemd/system/redis-server.service; enabled; vendor preset: enabled)
   Active: active (running) since Wed 2018-06-27 18:48:52 UTC; 12s ago
     Docs: http://redis.io/documentation,
           man:redis-server(1)
  Process: 2421 ExecStop=/bin/kill -s TERM $MAINPID (code=exited, status=0/SUCCESS)
  Process: 2424 ExecStart=/usr/bin/redis-server /etc/redis/redis.conf (code=exited, status=0/SUCCESS)
 Main PID: 2445 (redis-server)
    Tasks: 4 (limit: 4704)
   CGroup: /system.slice/redis-server.service
           └─2445 /usr/bin/redis-server 127.0.0.1:6379
. . .
```
Here, you can see that Redis is running and is already enabled, meaning that it is set to start up every time the server boots.

Note: This setting is desirable for many common use cases of Redis. If, however, you prefer to start up Redis manually every time your server boots, you can configure this with the following command:

```Bash
sudo systemctl disable redis
```
To test that Redis is functioning correctly, connect to the server using the command-line client:

```Bash
redis-cli
```
In the prompt that follows, test connectivity with the ping command:
```Bash
ping
```
**Output**
```Bash
PONG
```
This output confirms that the server connection is still alive. Next, check that you’re able to set keys by running:
```Bash
set test "It's working!"
```
**Output**
```Bash
OK
```
Retrieve the value by typing:

```Bash
get test
```
Assuming everything is working, you will be able to retrieve the value you stored:

**Output**
```Bash
"It's working!"
```
After confirming that you can fetch the value, exit the Redis prompt to get back to the shell:
```Bash
exit
```
As a final test, we will check whether Redis is able to persist data even after it’s been stopped or restarted. To do this, first restart the Redis instance:

```Bash
sudo systemctl restart redis
```
Then connect with the command-line client once again and confirm that your test value is still available:

```Bash
redis-cli
get test
```
The value of your key should still be accessible:

**Output**
```Bash
"It's working!"
```
Exit out into the shell again when you are finished:

```Bash
exit
```
With that, your Redis installation is fully operational and ready for you to use. However, some of its default configuration settings are insecure and provide malicious actors with opportunities to attack and gain access to your server and its data. The remaining steps in this tutorial cover methods for mitigating these vulnerabilities, as prescribed by the official Redis website. Although these steps are optional and Redis will still function if you choose not to follow them, it is strongly recommended that you complete them in order to harden your system’s security.

## MacOS

By using Homebrew, you greatly reduce the cost of setting up and configuring the development environment on Mac OS X.
Let’s install Redis for the good.
```Bash
$ brew install redis
```
After installation, you will see some notification about some caveats on configuring. Just leave it.

**Launch Redis on computer starts.**
```Bash
$ ln -sfv /usr/local/opt/redis/*.plist ~/Library/LaunchAgents
```

**Start Redis server via “launchctl”.**
```Bash
$ launchctl load ~/Library/LaunchAgents/homebrew.mxcl.redis.plist
```

**Start Redis server using configuration file.**
```Bash
$ redis-server /usr/local/etc/redis.conf
```

**Stop Redis on autostart on computer start.**
```Bash
$ launchctl unload ~/Library/LaunchAgents/homebrew.mxcl.redis.plist
```

**Location of Redis configuration file.**
```Bash
/usr/local/etc/redis.conf
```

**Uninstall Redis and its files.**
```Bash
$ brew uninstall redis
$ rm ~/Library/LaunchAgents/homebrew.mxcl.redis.plist
```

**Get Redis package information.**
```Bash
$ brew info redis
```
**Test if Redis server is running.**
```Bash
$ redis-cli ping
```
If it replies “PONG”, then it’s good to go!