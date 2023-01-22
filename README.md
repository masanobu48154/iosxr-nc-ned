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

Since the target configuration of NETCONF NED is adding L3VPN to SR-MPLS, the necessary YANG modules can be expected to be VRF, INTERFACE, OSPF, and BGP.You can use YANG Suite to select the modules we need.

### __Create New Device Profile__

Create a profile for your device to download and try YANG modules.

Log in to Cisco YANG Suite with the username and password you specified when installing, and register `General Info` and `NETCONF`of dist-rtr01 from `Device profiles`.

> __Setup__ => __Device profiles__ => __Create new device__ 
> - define "General Info".

<img src="./images/ys004_device_profile_02.png" width="75%">

> Also define "NETCONF" as below.

<img src="./images/ys005_device_profile_03.png" width="75%">

> Click "Check connectivity".

<img src="./images/ys006_device_profile_04.png" width="75%">

### __Create New Repositry__

Create a `New repository` from `YANG files and repositories` and download all YANG modules from dist-rtr01.

> __Setup__ => __YANG files and repositories__ => __New repositry__
> - Define any repository name.

<img src="./images/ys008_repo_02.png " width="75%">

> - Select the created device profile from the `NETCONF` tab of `Add modules to repository`.
> - Click `Get schema list`.

<img src="./images/ys009_repo_03.png " width="75%">

> - Select and download all of the displayed schemas list.
>
>    Once the download is completed, it will be displayed in `YANG modules in repository` on the left.

<img src="./images/ys010_repo_04.png " width="75%">

### __Create VRF Feature Module Set__

Now, let's create a VRF YANG module set to get the VRF configuration from the device and set the VRF to the device.

> __Setup__ => __YANG module sets__ => __New YANG set__
> 
> - Select the created YANG repositories and define the YANG set name.

<img src="./images/ys012_vrf_mset_02.png " width="75%">

> - Type __vrf__ in the search box.

Search for modules that seem to be related to VRF from the repository. Guessing from the name of the module, Cisco-IOS-XR-um-vrf-cfg 2020-07-23 is probably the desired module.

> - Select __Cisco-IOS-XR-um-vrf-cfg 2020-07-23__ and include it in the module set.
> - Click __Locate and add missing dependencies__.

<img src="./images/ys013_vrf_mset_03.png " width="75%">

A module set of VRF functionality is created, with dependencies between modules resolved as well.
The modules that make up the module set are:
- __Cisco-IOS-XR-um-vrf-cfg 2020-07-23__
- __Cisco-IOS-XR-config-mda-cfg 2019-04-05__
- __Cisco-IOS-XR-types 2019-12-03__
- __cisco-semver 2019-03-13__
- __ietf-inet-types 2013-07-15__

<img src="./images/ys014_vrf_mset_04.png " width="75%">

Let's verify with NETCONF that the VRF config can be pulled from the device.

> __Protocols__ => __NETCONF__ => __New YANG set__
> - Select the VRF feature module set created in the previous step for __YANG Set__.
> - Select __Cisco-IOS-XR-um-vrf-cfg__ for __Module(s)__.
> - Click __Load Module(s)__.

<img src="./images/ys016_vrf_nc_02.png " width="75%">

> - Select __get-config__ for __NETCONF Operation__.
> - Select __dist-rtr01__ for __Device__.
> - Mark __vrf list node__ in the displayed YANG model tree.
> - Click __Build RPC__.

<img src="./images/ys017_vrf_nc_03.png " width="75%">

> - Click __Run RPC(s)__.

<img src="./images/ys018_vrf_nc_04.png " width="75%">

You can pull the config with NETCONF like below.

Modules found in the repository that augment the modules in this YANG set.

YANG Suite also finds __Cisco-IOS-XR-um-router-bgp-cfg__, a module that augments __Cisco-IOS-XR-um-vrf-cfg__.
This module is also required when creating a NED.
- __Cisco-IOS-XR-um-router-bgp-cfg__

```xml
<rpc-reply xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:b2af9bf7-797d-431f-af81-0d8ecfda6584">
 <data>
  <vrfs xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-vrf-cfg">
   <vrf>
    <vrf-name>A</vrf-name>
    <address-family>
     <ipv4>
      <unicast>
       <import xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-router-bgp-cfg">
        <route-target>
         <two-byte-as-rts>
          <two-byte-as-rt>
           <as-number>65432</as-number>
           <index>1111</index>
           <stitching>false</stitching>
          </two-byte-as-rt>
         </two-byte-as-rts>
        </route-target>
       </import>
       <export xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-router-bgp-cfg">
        <route-target>
         <two-byte-as-rts>
          <two-byte-as-rt>
           <as-number>65432</as-number>
           <index>1111</index>
           <stitching>false</stitching>
          </two-byte-as-rt>
         </two-byte-as-rts>
        </route-target>
       </export>
      </unicast>
     </ipv4>
    </address-family>
   </vrf>
   <vrf>
    <vrf-name>Mgmt-intf</vrf-name>
    <address-family>
     <ipv4>
      <unicast/>
     </ipv4>
     <ipv6>
      <unicast/>
     </ipv6>
    </address-family>
   </vrf>
  </vrfs>
 </data>
</rpc-reply>
```

### __Create INTERFACE Feature Module Set__

Create a module set for the INTERFACE feature in the same way.

> - Type __interface__ in the search box.

You will find modules defined by ietf, openconfig and cisco. 

First, let's verify from ietf.

> - Select __ietf-interfaces 2014-05-08__ and include it in the module set.
> - Click __Locate and add missing dependencies__.

<img src="./images/ys019_if_ietf_mset_01.png " width="75%">

A module set of INTERFACE features is created that also incorporates dependent modules.

<img src="./images/ys020_if_ietf_mset_02.png " width="75%">

> - Select the VRF feature module set created in the previous step for __INTERFACE YANG Set__.
> - Select __ietf-interfaces__ for __Module(s)__.
> - Click __Load Module(s)__.
> - Select __get-config__ for __NETCONF Operation__.
> - Select __dist-rtr01__ for __Device__.
> - Mark __interface list node__ in the displayed YANG model tree.
> - Click __Build RPC__.
> - Click __Run RPC(s)__.

<img src="./images/ys021_if_ietf_nc_01.png " width="75%">

You won't be able to pull the config like below.

```xml
<rpc-reply xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:d5a107f4-6423-4667-968c-00494a83cf83">
 <data/>
</rpc-reply>
```


Next, let's verify with a module set that includes __openconfig-interfaces 2016-05-26__.

<img src="./images/ys023_if_oconf_mset_02.png " width="75%">

Load __openconfig-interfaces__ and mark the __interface list node__ to __run RPC__.

<img src="./images/ys024_if_oconf_nc_01.png " width="75%">

You can pull the config with NETCONF like below.

The __interface__ config was pulled. It looks like you've pulled it off perfectly, but you're missing a __vrf__ definition.

```xml
<rpc-reply xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:e04176c2-a832-4618-8fb1-6528e8d939bc">
 <data>
  <interfaces xmlns="http://openconfig.net/yang/interfaces">
   <interface>
    <name>Loopback0</name>
    <config>
     <name>Loopback0</name>
     <type xmlns:idx="urn:ietf:params:xml:ns:yang:iana-if-type">idx:softwareLoopback</type>
    </config>
    <subinterfaces>
     <subinterface>
      <index>0</index>
      <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
       <addresses>
        <address>
         <ip>10.0.0.1</ip>
         <config>
          <ip>10.0.0.1</ip>
          <prefix-length>32</prefix-length>
         </config>
        </address>
       </addresses>
      </ipv4>
     </subinterface>
    </subinterfaces>
   </interface>
   <interface>
    <name>Loopback111</name>
    <config>
     <name>Loopback111</name>
     <type xmlns:idx="urn:ietf:params:xml:ns:yang:iana-if-type">idx:softwareLoopback</type>
    </config>
    <subinterfaces>
     <subinterface>
      <index>0</index>
      <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
       <addresses>
        <address>
         <ip>1.1.1.1</ip>
         <config>
          <ip>1.1.1.1</ip>
          <prefix-length>32</prefix-length>
         </config>
        </address>
       </addresses>
      </ipv4>
     </subinterface>
    </subinterfaces>
   </interface>
   <interface>
    <name>MgmtEth0/RP0/CPU0/0</name>
    <config>
     <name>MgmtEth0/RP0/CPU0/0</name>
     <type xmlns:idx="urn:ietf:params:xml:ns:yang:iana-if-type">idx:ethernetCsmacd</type>
    </config>
    <ethernet xmlns="http://openconfig.net/yang/interfaces/ethernet">
     <config>
      <auto-negotiate>false</auto-negotiate>
     </config>
    </ethernet>
    <subinterfaces>
     <subinterface>
      <index>0</index>
      <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
       <addresses>
        <address>
         <ip>10.10.20.175</ip>
         <config>
          <ip>10.10.20.175</ip>
          <prefix-length>24</prefix-length>
         </config>
        </address>
       </addresses>
      </ipv4>
     </subinterface>
    </subinterfaces>
   </interface>
   <interface>
    <name>GigabitEthernet0/0/0/0</name>
    <config>
     <name>GigabitEthernet0/0/0/0</name>
     <type xmlns:idx="urn:ietf:params:xml:ns:yang:iana-if-type">idx:ethernetCsmacd</type>
     <description>to_port0_dist_rtr02</description>
    </config>
    <ethernet xmlns="http://openconfig.net/yang/interfaces/ethernet">
     <config>
      <auto-negotiate>false</auto-negotiate>
     </config>
    </ethernet>
    <subinterfaces>
     <subinterface>
      <index>0</index>
      <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
       <addresses>
        <address>
         <ip>10.1.12.1</ip>
         <config>
          <ip>10.1.12.1</ip>
          <prefix-length>24</prefix-length>
         </config>
        </address>
       </addresses>
      </ipv4>
     </subinterface>
    </subinterfaces>
   </interface>
   <interface>
    <name>GigabitEthernet0/0/0/1</name>
    <config>
     <name>GigabitEthernet0/0/0/1</name>
     <type xmlns:idx="urn:ietf:params:xml:ns:yang:iana-if-type">idx:ethernetCsmacd</type>
     <description>to_user</description>
    </config>
    <ethernet xmlns="http://openconfig.net/yang/interfaces/ethernet">
     <config>
      <auto-negotiate>false</auto-negotiate>
     </config>
    </ethernet>
    <subinterfaces>
     <subinterface>
      <index>1111</index>
      <config>
       <index>1111</index>
      </config>
      <ipv4 xmlns="http://openconfig.net/yang/interfaces/ip">
       <addresses>
        <address>
         <ip>11.1.1.1</ip>
         <config>
          <ip>11.1.1.1</ip>
          <prefix-length>24</prefix-length>
         </config>
        </address>
       </addresses>
      </ipv4>
      <vlan xmlns="http://openconfig.net/yang/vlan">
       <config>
        <vlan-id>1111</vlan-id>
       </config>
      </vlan>
     </subinterface>
    </subinterfaces>
   </interface>
  </interfaces>
 </data>
</rpc-reply>
```


Finally, let's verify with a module set that includes __Cisco-IOS-XR-um-interface-cfg 2019-06-10__.

The modules that make up the module set are:
- __Cisco-IOS-XR-um-interface-cfg 2019-06-10__
- __Cisco-IOS-XR-types 2019-12-03__
- __cisco-semver 2019-03-13__
- __ietf-inet-types 2013-07-15__
- __tailf-cli-extensions 2018-09-11__
- __tailf-common 2018-09-11__
- __tailf-meta-extensions 2017-03-08__

<img src="./images/ys026_if_um_mset_02.png " width="75%">

Load __Cisco-IOS-XR-um-interface-cfg__ and mark the __interface list node__ to __run RPC__.

<img src="./images/ys027_if_um_nc_01.png " width="75%">

You can pull the config with NETCONF like below.

Interface configuration pulled. There is also a VRF definition, so the INTERFACE Feature will be fine with this module set.

YANG Suite also detects some modules that augment __Cisco-IOS-XR-um-interface-cfg__.
These modules are also required when creating a NED.
- __Cisco-IOS-XR-um-if-ip-address-cfg__
- __Cisco-IOS-XR-um-if-vrf-cfg__
- __Cisco-IOS-XR-um-if-vrf-cfg__
- __Cisco-IOS-XR-um-l2-ethernet-cfg__

```xml
<rpc-reply xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:4341816b-6c9a-4cf0-9d7c-300859a5e913">
 <data>
  <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-interface-cfg">
   <interface>
    <interface-name>Loopback0</interface-name>
    <ipv4>
     <addresses xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-if-ip-address-cfg">
      <address>
       <address>10.0.0.1</address>
       <netmask>255.255.255.255</netmask>
      </address>
     </addresses>
    </ipv4>
   </interface>
   <interface>
    <interface-name>Loopback111</interface-name>
    <vrf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-if-vrf-cfg">A</vrf>
    <ipv4>
     <addresses xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-if-ip-address-cfg">
      <address>
       <address>1.1.1.1</address>
       <netmask>255.255.255.255</netmask>
      </address>
     </addresses>
    </ipv4>
   </interface>
   <interface>
    <interface-name>MgmtEth0/RP0/CPU0/0</interface-name>
    <vrf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-if-vrf-cfg">Mgmt-intf</vrf>
    <ipv4>
     <addresses xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-if-ip-address-cfg">
      <address>
       <address>10.10.20.175</address>
       <netmask>255.255.255.0</netmask>
      </address>
     </addresses>
    </ipv4>
   </interface>
   <interface>
    <interface-name>GigabitEthernet0/0/0/0</interface-name>
    <description>to_port0_dist_rtr02</description>
    <ipv4>
     <addresses xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-if-ip-address-cfg">
      <address>
       <address>10.1.12.1</address>
       <netmask>255.255.255.0</netmask>
      </address>
     </addresses>
    </ipv4>
   </interface>
   <interface>
    <interface-name>GigabitEthernet0/0/0/1</interface-name>
    <description>to_user</description>
   </interface>
   <interface>
    <interface-name>GigabitEthernet0/0/0/1.1111</interface-name>
    <vrf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-if-vrf-cfg">A</vrf>
    <ipv4>
     <addresses xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-if-ip-address-cfg">
      <address>
       <address>11.1.1.1</address>
       <netmask>255.255.255.0</netmask>
      </address>
     </addresses>
    </ipv4>
    <encapsulation xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-l2-ethernet-cfg">
     <dot1q>
      <vlan-id>1111</vlan-id>
     </dot1q>
    </encapsulation>
   </interface>
  </interfaces>
 </data>
</rpc-reply>
```

### __Create BGP Feature Module Set__

After creating some module sets, you can see that there are many __Cisco-IOS-XR-um__ modules.

You can effectively create a module set using a UM model generated directly from the CLI. 

> #### __[Transitioning Native Models to Unified Models (UM)](https://www.cisco.com/c/en/us/td/docs/routers/asr9000/software/asr9k-r7-8/programmability/configuration/guide/b-programmability-cg-asr9000-78x/m-unified-data-models.html#Cisco_Reference.dita_e135d1e5-f314-44d9-a59a-716bad643369 "Transitioning Native Models to Unified Models (UM)")__
> 
> Unified models are CLI-based YANG models that are designed to replace the native schema-based models. UM models are generated directly from the IOS XR CLIs and mirror them in several ways. This results in improved usability and faster adoption of YANG models.

Now create a BGP module set using the UM model.

> - Type __bgp__ in the search box.
> - Select __Cisco-IOS-XR-um-router-bgp-cfg 2020-11-10__ and include it in the module set.
> - Click __Locate and add missing dependencies__.

The modules that make up BGP modules set with resolved dependencies are:
- __Cisco-IOS-XR-um-router-bgp-cfg 2020-11-10__
- __Cisco-IOS-XR-config-mda-cfg 2019-04-05__
- __Cisco-IOS-XR-types 2019-12-03__
- __Cisco-IOS-XR-um-snmp-server-cfg 2019-06-10__
- __Cisco-IOS-XR-um-vrf-cfg 2020-07-23__
- __cisco-semver 2019-03-13__
- __ietf-inet-types 2013-07-15__

<img src="./images/ys032_bgp_um_mset_02.png " width="75%">

Load __Cisco-IOS-XR-um-router-bgp-cfg__ and mark the __bgp container node__ to __run RPC__.

<img src="./images/ys033_bgp_um_nc_01.png " width="75%">

You can pull the config with NETCONF like below.

```xml
<rpc-reply xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:30636c3e-fe55-480b-9bfe-e99e9fbc8d9e">
 <data>
  <router xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-router-bgp-cfg">
   <bgp>
    <as>
     <as-number>65432</as-number>
     <bgp>
      <router-id>10.0.0.1</router-id>
      <log>
       <neighbor>
        <changes>
         <detail/>
        </changes>
       </neighbor>
      </log>
     </bgp>
     <address-families>
      <address-family>
       <af-name>vpnv4-unicast</af-name>
      </address-family>
     </address-families>
     <neighbors>
      <neighbor>
       <neighbor-address>10.0.0.2</neighbor-address>
       <remote-as>65432</remote-as>
       <update-source>Loopback0</update-source>
       <address-families>
        <address-family>
         <af-name>vpnv4-unicast</af-name>
        </address-family>
       </address-families>
      </neighbor>
     </neighbors>
     <vrfs>
      <vrf>
       <vrf-name>A</vrf-name>
       <rd>
        <two-byte-as>
         <as-number>65432</as-number>
         <index>1111</index>
        </two-byte-as>
       </rd>
       <address-families>
        <address-family>
         <af-name>ipv4-unicast</af-name>
         <redistribute>
          <ospf>
           <router-tag>A</router-tag>
          </ospf>
         </redistribute>
        </address-family>
       </address-families>
      </vrf>
     </vrfs>
    </as>
   </bgp>
  </router>
 </data>
</rpc-reply>
```

### __Create OSPF Feature Module Set__

Create OSPF feature module set using UM model.

The modules that make up OSPF module set with resolved dependencies are:
- __Cisco-IOS-XR-um-router-ospf-cfg 2020-09-28__
- __Cisco-IOS-XR-types 2019-12-03__
- __Cisco-IOS-XR-um-snmp-server-cfg 2019-06-10__
- __cisco-semver 2019-03-13__
- __ietf-inet-types 2013-07-15__
- __tailf-cli-extensions 2018-09-11__
- __tailf-common 2018-09-11__
- __tailf-meta-extensions 2017-03-08__

<img src="./images/ys035_ospf_um_mset_02.png " width="75%">

Load __Cisco-IOS-XR-um-router-ospf-cfg 2020-09-28__ and mark the __ospf container node__ to __run RPC__.

<img src="./images/ys036_ospf_um_nc_01.png " width="75%">

You can pull the config with NETCONF like below.

```xml
<rpc-reply xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:14bbcd72-8140-4397-942d-183c8a165f58">
 <data>
  <router xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-um-router-ospf-cfg">
   <ospf>
    <processes>
     <process>
      <process-name>1</process-name>
      <router-id>10.0.0.1</router-id>
      <segment-routing>
       <mpls/>
      </segment-routing>
      <address-family>
       <ipv4>
        <unicast/>
       </ipv4>
      </address-family>
      <areas>
       <area>
        <area-id>0</area-id>
        <interfaces>
         <interface>
          <interface-name>Loopback0</interface-name>
          <network>
           <point-to-point/>
          </network>
          <passive>
           <enable/>
          </passive>
          <prefix-sid>
           <index>
            <sid-index>1</sid-index>
           </index>
          </prefix-sid>
         </interface>
         <interface>
          <interface-name>GigabitEthernet0/0/0/0</interface-name>
          <network>
           <point-to-point/>
          </network>
         </interface>
        </interfaces>
       </area>
      </areas>
     </process>
     <process>
      <process-name>A</process-name>
      <vrfs>
       <vrf>
        <vrf-name>A</vrf-name>
        <router-id>1.1.1.1</router-id>
        <redistribute>
         <bgp>
          <as>
           <as-number>65432</as-number>
           <metric>
            <default-metric>10</default-metric>
           </metric>
           <metric-type>2</metric-type>
          </as>
         </bgp>
        </redistribute>
        <address-family>
         <ipv4>
          <unicast/>
         </ipv4>
        </address-family>
        <areas>
         <area>
          <area-id>1.1.1.1</area-id>
          <interfaces>
           <interface>
            <interface-name>Loopback111</interface-name>
            <network>
             <point-to-point/>
            </network>
            <passive>
             <enable/>
            </passive>
           </interface>
           <interface>
            <interface-name>GigabitEthernet0/0/0/1.1111</interface-name>
           </interface>
          </interfaces>
         </area>
        </areas>
       </vrf>
      </vrfs>
     </process>
    </processes>
   </ospf>
  </router>
 </data>
</rpc-reply>
```

### __Create All Feature Module Set__



<img src="./images/ys037_all_um_mset_01.png " width="75%">

<img src="./images/ys038_all_um_mset_02.png " width="75%">

<img src="./images/ys039_all_um_mset_03.png " width="75%">






