# Migration demo from CLI NED to NETCONF NED

## Overview

This repository demonstrates creating an IOS-XR NETCONF NED using the Cisco NSO service application in the DevNet sandbox and migrating from the NED to the created NETCONF NED.

The target configuration of NETCONF NED is L3VPN addition to SR-MPLS.



## Requirements

An account that has permission to access the Cisco DevNet sandbox.

## Sandbox used in this demo

Cisco Network Services Orchestrator (NSO)

<img src="./images/nso_sandbox.png" width="25%">

## What you do is

1. Connect to the sandbox
2. Change lab network in CML2
3. Apply CLI NED to new lab network
4. Install Cisco YANG Suite
5. Select YANG module to create NETCONF NED
6. Create NETCONF NED
7. Apply NETCONF NED to new lab network
8. Try to configure

## 1. Connect to the sandbox

Connect to Cisco Network Services Orchestrator (NSO) referring to [here](https://developer.cisco.com/docs/sandbox/ "Devnet Sandbox Document").

## 2. Change lab network in CML2

In this demo, we will leave the distribution routers and remove the rest of the nodes. Replace the remaining IOS-XE routers with IOS-XR routers, then set up a segment routing MPLS cloud between them and build an L3VPN using BGP VPNv4.

<img src="./images/cml_topo.png" width="75%">

You can build this lab by running cml2.py from DevBox.

Log in to DevBox.

```shell
$ ssh -l developer 10.10.20.50
developer@10.10.20.50's password:
Last login: Tue Jul 14 05:34:45 2020
(py3venv) [developer@devbox ~]$
```

Clone the iosxr-nc-ned repository.

```shell
(py3venv) [developer@devbox ~]$ git clone https://github.com/masanobu48154/iosxr-nc-ned.git
Cloning into 'iosxr-nc-ned'...
remote: Enumerating objects: 18, done.
remote: Counting objects: 100% (18/18), done.
remote: Compressing objects: 100% (14/14), done.
remote: Total 18 (delta 2), reused 11 (delta 1), pack-reused 0
Unpacking objects: 100% (18/18), done.
(py3venv) [developer@devbox ~]$ 
```

Go to the iosxr-nc-ned directory and set the CML2 username and password as environment variables.

```shell
(py3venv) [developer@devbox ~]$ cd iosxr-nc-ned/
(py3venv) [developer@devbox iosxr-nc-ned]$ export CML_USERNAME={ CML USERNAME }
(py3venv) [developer@devbox iosxr-nc-ned]$ export CML_PASSWORD={ CML PASSWORD }
```

Run cml2.py.

```shell
(py3venv) [developer@devbox iosxr-nc-ned]$ python3 cml2.py
```

Go to https://10.10.20.161 and log in to CML to verify that nso_lob has been imported.

<img src="./images/cml_dashboard.png" width="75%">

## 3. Apply CLI NED to new lab network

In the original lab network, dist-rtr01 and dist-rtr02 had IOS CLI NED applied, so change them to IOS-XR CLI NED to match the new lab network.

Log in to NSO/NCS Host.

```shell
$ ssh -l developer 10.10.20.49
developer@10.10.20.49's password:
Last login: Tue Jan 10 17:35:21 2023 from 192.168.254.13
[developer@nso ~]$
```

Go to NSO CLI shell mode.

```shell
[developer@nso ~]$ ncs_cli -C -u developer

User developer last logged in 2023-01-10T14:38:18.25607-08:00, to nso, from 10.10.20.49 using rest-https
developer connected from 192.168.254.13 using ssh on nso
developer@ncs#
```

Check the NED of dist-rtr01.

```shell
developer@ncs# show running-config devices device dist-rtr01 | include ned-id
 device-type cli ned-id cisco-ios-cli-6.67
developer@ncs#
```

Attempting to sync dist-rtr config to NSO fails. This is because IOS-XE has been replaced by IOS-XR in the new lab network.

```shell
developer@ncs# devices device dist-rtr01 sync-from
result false
info Failed to connect to device dist-rtr01: connection refused: Failed to setup NED :: Unknown device ::
Wed Jan 11 22:30:44.511 UTC
Cisco IOS XR Software, Version 7.2.2
Copyright (c) 2013-2021 by Cisco Systems, Inc.

Build Information:
 Built By     : ingunawa
 Built On     : Mon Jan 25 21:30:50 PST 2021
 Built Host   : iox-ucs-012
 Workspace    : /auto/srcarchive15/prod/7.2.2/xrv9k/ws
 Version      : 7.2.2
 Location     : /opt/cisco/XR/packages/
 Label        : 7.2.2-0

cisco IOS-XRv 9000 () processor
System uptime is 12 hours 6 minutes
```

Change NED of `dist-rtr-01` to `cisco-iosxr-cli-7.32` .

```shell
developer@ncs# config terminal
Entering configuration mode terminal
developer@ncs(config)# devices device dist-rtr01 device-type cli ned-id cisco-iosxr-cli-7.32
```

Migrate to the new NED and commit.

```shell
developer@ncs(config-device-dist-rtr01)# migrate new-ned-id cisco-iosxr-cli-7.32
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:memory
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:router
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:diagnostic
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:spanning-tree
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:logging
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:line
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:interface
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:crypto
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:username
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:multilink
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:subscriber
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:ip
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:call-home
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:enable
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:vrf
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:platform
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:login
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:service
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:version
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:tailfned
    info sub-tree has been deleted
}
modified-path {
    path /devices/device[name='dist-rtr01']/config/ios:hostname
    info sub-tree has been deleted
}
developer@ncs(config-device-dist-rtr01)# commit
Commit complete.
developer@ncs(config-device-dist-rtr01)#
```

sync `dist-rtr-01` config to NSO.

```shell
developer@ncs(config-device-dist-rtr01)# top
developer@ncs(config)# devices device dist-rtr01 sync-from
result true
developer@ncs(config)#
```

`dist-rtr-02` to the new NED as well. And check the running-config with `show running-config devices device { DEVICE } config `.

## 4. Install Cisco YANG Suite

Before building NED with NSO, let's install the very cool [Cisco YANG Suite](https://github.com/CiscoDevNet/yangsuite "Cisco YANG Suite") in DevBox to select the YANG modules we need.

Log in to DevBox.

```shell
[masanobu@ccie-pro:~]
$ ssh -l developer 10.10.20.50
developer@10.10.20.50's password:
Last login: Tue Jul 14 05:34:45 2020
(py3venv) [developer@devbox ~]$
```

Clone the yangsuite repository.

```shell
(py3venv) [developer@devbox ~]$ git clone https://github.com/CiscoDevNet/yangsuite
Cloning into 'yangsuite'...
remote: Enumerating objects: 847, done.
remote: Counting objects: 100% (52/52), done.
remote: Compressing objects: 100% (37/37), done.
remote: Total 847 (delta 26), reused 27 (delta 15), pack-reused 795
Receiving objects: 100% (847/847), 44.85 MiB | 26.44 MiB/s, done.
Resolving deltas: 100% (352/352), done.
(py3venv) [developer@devbox ~]$
```

Go to the yangsuite/docker directory and replace `localhost` in each configuration file with `10.10.20.50`.

```shell
(py3venv) [developer@devbox ~]$ cd yangsuite/docker/
(py3venv) [developer@devbox docker]$ sed -i s/localhost/10.10.20.50/g start_yang_suite.sh
(py3venv) [developer@devbox docker]$ sed -i s/localhost/10.10.20.50/g ./nginx/nginx.conf
(py3venv) [developer@devbox docker]$ sed -i s/localhost/10.10.20.50/g ./yangsuite/Dockerfile
(py3venv) [developer@devbox docker]$ sed -i s/localhost/10.10.20.50/g ./yangsuite/production.py
(py3venv) [developer@devbox docker]$ 
```

Running start_yang_suite.sh will ask to set the　username, password, email address, and certificate details. The output will look similar to the below

```shell
(py3venv) [developer@devbox docker]$ bash ./start_yang_suite.sh
Hello, please setup YANG Suite admin user.
username: cisco
password:
confirm password:
email: example@virl.info

Setup test certificates? (y/n): y
################################################################
## Generating self-signed certificates...                     ##
##                                                            ##
## WARNING: Obtain certificates from a trusted authority!     ##
##                                                            ##
## NOTE: Some browsers may still reject these certificates!!  ##
################################################################

Generating a 2048 bit RSA private key
................+++
....+++
writing new private key to 'nginx/nginx-self-signed.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:JP
State or Province Name (full name) []:OSAKA
Locality Name (eg, city) [Default City]:OSAKA
Organization Name (eg, company) [Default Company Ltd]:VIRL
Organizational Unit Name (eg, section) []:VIRL
Common Name (eg, your name or your server's hostname) []:10.10.20.50
Email Address []:example@virl.info
Certificates generated...
Building docker containers...
Creating network "docker_default" with the default driver
Creating volume "docker_static-content" with default driver
Creating volume "docker_uwsgi" with default driver
Building yangsuite
Step 1/22 : FROM ubuntu:20.04
20.04: Pulling from library/ubuntu
846c0b181fff: Pull complete

(snip)
```

When YANG Suite is ready to use, it will be displayed as below.

```shell
yangsuite_1  | spawned uWSGI master process (pid: 53)
yangsuite_1  | spawned uWSGI worker 1 (pid: 62, cores: 1)
yangsuite_1  | spawned uWSGI worker 2 (pid: 63, cores: 1)
yangsuite_1  | spawned uWSGI worker 3 (pid: 64, cores: 1)
yangsuite_1  | spawned uWSGI worker 4 (pid: 65, cores: 1)
yangsuite_1  | spawned uWSGI worker 5 (pid: 66, cores: 1)
```

Now you can access the YANG Suite at http://10.10.20.50

## 5. Select YANG module to create NETCONF NED

Since the target configuration of NETCONF NED is adding L3VPN to SR-MPLS, the necessary YANG modules can be expected to be VRF, INTERFACE, and BGP.You can use YANG Suite to select the modules we need.

#### Create New Device Profile

Create a profile for your device to download and try YANG modules.

Log in to Cisco YANG Suite with the username and password you specified when installing, and register `General Info` and `NETCONF`of dist-rtr01 from `Device profiles`.

__Setup__ => __Device profiles__ => __Create new device__ 

define "General Info".

<img src="./images/ys004_device_profile_02.png" width="75%">

Also define "NETCONF" as below.

<img src="./images/ys005_device_profile_03.png" width="75%">

Click "Check connectivity".

<img src="./images/ys006_device_profile_04.png" width="75%">

#### Create New Repositry

Create a `New repository` from `YANG files and repositories` and download all YANG modules from dist-rtr01.

__Setup__ => __Device profiles__ => __Create new device__ 



Now, let's create a VRF YANG module set to get the VRF configuration from the device and set the VRF to the device.




