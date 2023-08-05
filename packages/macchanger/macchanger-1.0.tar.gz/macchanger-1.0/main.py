from __init__ import ChangeMac

if __name__ == "__main__":
    mac_changer = ChangeMac()
    mac=mac_changer.get_mac("eth0")
    print("\nOraginal Mac Address is :>{0}".format(mac))

    tochange_mac=mac_changer.default_mac()

    current_mac=mac_changer.change_mac("eth0",tochange_mac)
    print("Updated Mac address is:> ",current_mac)


