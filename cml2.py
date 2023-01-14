#!/usr/bin/env python3

import requests
import time
import urllib3
import os
import json
import logging
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


class Cml2:
    """
    A class that imports and starts a new lab
    after deleting all the labs running on CML2.
    How to call:
        1. Create a object with the CML2 lab address.
        2. Execute delete_labs function and start_lab.
    """

    def __init__(self, host, uname, passwd):
        """
        Parameters
        ----------
        host : str
            CML2 lab address or FQDN
        """
        login_data_dic = {
            "username": uname,
            "password": passwd
        }
        self.host = host
        self.login_data = json.dumps(login_data_dic)
        self.yaml_path = f'{os.path.dirname(os.path.abspath(__file__))}/cmlyaml/NSO_Lab.yaml'
        self.headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "accept": "application/json"
        }
        self.headers_br = {
            "Content-type": "application/json",
            "accept": "application/json",
            "Authorization": ""
        }


    def get_bearer(self):
        """
        Function to get Authentication token.
        This function requires a JSON object that holds authentication data.
        Returns
        -------
        str
            Authentication token
        """
        login_url = f"https://{self.host}/api/v0/authenticate"
        s = requests.session()
        res_post_login = s.post(
            login_url, data=self.login_data, headers=self.headers, verify=False)
        self.headers_br["Authorization"] = f"Bearer {res_post_login.json()}"

    def import_lab(self):
        """
        Function to import lab.
        This function requires a yaml file that defines the lab configuration.
        Returns
        -------
        str
            Imported lab ID
        """
        create_urlv1 = f"https://{self.host}/api/v0/import?title=nso_lab"
        with open(self.yaml_path, 'rb') as f:
            virl_data = f.read()
        s = requests.session()
        res_post_virlv1 = s.post(
            create_urlv1, headers=self.headers_br, data=virl_data, verify=False)
        import_lab_dic = res_post_virlv1.json()
        return import_lab_dic["id"]

    def start_lab(self):
        """
        Function to import and start lab.
        This function requires a yaml file that defines the lab configuration.
        """
        self.get_bearer()
        lab_id = self.import_lab()
        time.sleep(10)
        start_url = f"https://{self.host}/api/v0/labs/{lab_id}/start"
        s = requests.session()
        res_put_start = s.put(start_url, headers=self.headers_br, verify=False)
        return res_put_start.json()

    def get_labid(self):
        """
        Function to get the lab id of the running labs.
        Returns
        -------
        str
            Runing lab ID
        """
        get_labs_url = f"https://{self.host}/api/v0/labs"
        s = requests.session()
        res_get_labs = s.get(get_labs_url, headers=self.headers_br, verify=False)
        return res_get_labs.json()

    def stop_labs(self):
        """
        Function to stop all labs.
        Returns
        -------
        dictionary
            Key = Lab ID, Value = API Status
        """
        stop_labs_dic = {}
        for lab in self.get_labid():
            stop_url = f"https://{self.host}/api/v0/labs/{lab}/stop"
            s = requests.session()
            res_put_stop = s.put(stop_url, headers=self.headers_br, verify=False)
            time.sleep(20)
            stop_labs_dic[lab] = res_put_stop.json()
        return stop_labs_dic

    def wipe_labs(self):
        """
        Function to stop and wipe all labs.
        Returns
        -------
        dictionary
            Key = Lab ID, Value = API Status
        """
        wipe_labs_dic = {}
        self.stop_labs()
        for lab in self.get_labid():
            wipe_url = f"https://{self.host}/api/v0/labs/{lab}/wipe?force=true"
            s = requests.session()
            res_put_wipe = s.put(wipe_url, headers=self.headers_br, verify=False)
            time.sleep(5)
            wipe_labs_dic[lab] = res_put_wipe.json()
        return wipe_labs_dic

    def delete_labs(self):
        """
        Function to stop, wipe and delete all labs.
        Returns
        -------
        dictionary
            Key = Lab ID, Value = API Status
        """
        delete_labs_dic = {}
        self.get_bearer()
        self.wipe_labs()
        for lab in self.get_labid():
            delete_labs_url = f"https://{self.host}/api/v0/labs/{lab}"
            s = requests.session()
            res_delete_labs = s.delete(
                delete_labs_url, headers=self.headers_br, verify=False)
            delete_labs_dic[lab] = res_delete_labs
        return delete_labs_dic

    def get_node(self):
        """
        Function to extract nodes placed in lab.
        """
        lab_nodes_dic = {}
        self.get_bearer()
        for lab in self.get_labid():
            getnodes_url = f"https://{self.host}/api/v0/labs/{lab}/nodes"
            s = requests.session()
            RES_GET_NODES = s.get(getnodes_url, headers=self.headers_br, verify=False)
            lab_nodes_dic[lab] = RES_GET_NODES.json()
        return lab_nodes_dic

    def check_converged(self):
        """
        Function to check if lab converged.
        """
        self.get_bearer()
        for lab in self.get_labid():
            check_url = f"https://{self.host}/api/v0/labs/{lab}/check_if_converged"
            s = requests.session()
            RES_CHECK = s.get(check_url, headers=self.headers_br, verify=False)
        return RES_CHECK.json()


if __name__ == '__main__':

    host = "10.10.20.161"
    uname = os.environ['CML_USERNAME']
    passwd = os.environ['CML_PASSWORD']
    ob = Cml2(host, uname, passwd)
    ob.delete_labs()
    ob.start_lab()



