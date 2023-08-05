import subprocess
import re
import  termcolor as color
import random
class ChangeMac:
    def __init__(self):
        self.mac = ""
        self.user_choosen_mac=""
    def default_mac(self):
        default_mac = ["22:11:99:33:77:00", "00:11:44:33:77:00", "55:11:99:33:77:00", "88:11:99:33:77:00", "22:55:99:33:77:00"]
        print(color.colored("Our Default Mac Address is ",'red'))
        count =0
        for i in default_mac:
            count = count+1
            print(color.colored("[+{0}] {1}".format(count,i),'green'))

        state = int(input(color.colored("Press 1 to use our default mac address or \nPress 2 to use your mac>:",'blue')))
        if state==2:
            user_input_mac=input("Please enter your mac >:")
            self.user_choosen_mac=user_input_mac
        else:
            list_index_randInput= len(default_mac)-1
            mac_list = random.randint(0,list_index_randInput)
            random_mac = default_mac[mac_list]

            oraginal_mac = self.get_mac("eth0")
            if random_mac == oraginal_mac:
                mac_list = mac_list+1
                if mac_list == len(default_mac)-1:
                    mac_list=0
                    random_mac = default_mac[mac_list]
                    self.user_choosen_mac = random_mac

            else:
                random_mac = default_mac[mac_list]
                self.user_choosen_mac = random_mac

            print(color.colored("We are random choosen this mac address >>:{0}".format(random_mac), "yellow"))
        return self.user_choosen_mac

    def get_mac(self, interface:'example=eth0')->'Current Mac Address':
        """ This function use process library to get mac address
            1- if you want to use more pattern you can edit here
        """
        output = subprocess.run(["ifconfig", interface], shell=False, capture_output=True)
        result = output.stdout.decode()
        # print("result is ",result)
        # This is pattern for our mac address you can check here https://regex101.com/
        regex_mac_pattern = r'ether\s[\da-z]{2}:[\da-z]{2}:[\da-z]{2}:[\da-z]{2}:[\da-z]{2}:[\da-z]{2}'
        # create re pattern object to search
        regex = re.compile(regex_mac_pattern)

        search_result = regex.search(result)
        if search_result:  # to check pattern searching error
            current_mac = search_result.group().split(" ")[1]
            self.mac = current_mac
            return current_mac
        else:
            print("[XXX]Regular Expression pattern compile error \n Please check the pattern")

    def change_mac(self , interface:'to give interface' ,new_mac:
    'mac address to change')->'will change new mac address':
        # print(" current_mac address is ",self.get_mac(interface))
        output = subprocess.run(["ifconfig",interface ,"down"],shell=False , capture_output=True)
        print(output.stderr.decode())

        output = subprocess.run(["ifconfig",interface , "hw" , "ether" ,new_mac], shell= False ,capture_output=True)
        print(output.stderr.decode())

        output = subprocess.run(["ifconfig", interface, "up"], shell=False, capture_output=True)
        print(output.stderr.decode())


        return self.get_mac(interface)



