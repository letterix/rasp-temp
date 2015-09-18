import re
import subprocess

class Networking:

    DEVICE = "wlan0"

    IWLIST = "/sbin/iwlist"
    IFDOWN = "/sbin/ifdown"
    IFUP = "/sbin/ifup"

    WLAN0_CONFIG_FILE = "/etc/network/interfaces.d/wlan0.cfg"


    def scan_wifi_networks(self):
        output = subprocess.check_output([Networking.IWLIST, Networking.DEVICE, "scanning"])
        output = output.decode()
        print(output)
        lines = filter(None, output.split('\n'))

        networks = []
        network = None
        for line in lines:
            match = re.search('^\s+Cell [0-9]+', line)
            if match:
                if network:
                    networks.append(network)
                network = dict()
            match = re.search('^\s+ESSID:"([^"]+)"', line)
            if match:
                essid=match.group(1)
                network["essid"] = bytes(bytes(essid,'utf-8').decode("unicode_escape"),'iso8859-1').decode()
            match = re.search('^\s+Encryption key:(.*)$', line)
            if match:
                if match.group(1) == "on":
                    network["encryption"] = True
                else:
                    network["encryption"] = False
            match = re.search('^\s+IE: WPA Version 1', line)
            if match:
                network["wpa1"] = dict()
                current_auth = "wpa1"
            match = re.search('^\s+IE: IEEE.*WPA2', line)
            if match:
                network["wpa2"] = dict()
                current_auth = "wpa2"
            match = re.search('^\s+Group Cipher : (.*)$', line)
            if match:
                network[current_auth]["group-cipher"] = match.group(1).split()
            match = re.search('^\s+Pairwise Ciphers \([0-9]\) : (.*)$', line)
            if match:
                network[current_auth]["pairwise-ciphers"] = match.group(1).split()
            match = re.search('^\s+Authentication Suites \([0-9]\) : (.*)$', line)
            if match:
                network[current_auth]["auth-suites"] = match.group(1).split()
            match = re.search('^\s+Quality.*Signal level=([0-9]+)/([0-9]+)', line)
            if not match:
                match = re.search('^\s+Quality=([0-9]+)/([0-9]+).*Signal level=.*', line)
            if match:
                max_value = int(match.group(2))
                current_value = int(match.group(1))
                scale = 100 / float(max_value)
                network["signal"] = "%.0f" % round(current_value * scale, 0)

        self.last_scan = networks
        return networks


    def select_wifi_network(self, essid, passphrase):

        networks = self.last_scan

        if not networks:
            networks = self.scan_wifi_networks()
        if not networks:
            raise RuntimeError("No wifi networks found")

        target_network = None

        for network in networks:
            if network["essid"] == essid:
                target_network = network
                break


        if not target_network:
            raise RuntimeError("Wifi network '" + essid + "' does not exist")

        self.validate_network(target_network)
        self.write_wpa_config(target_network, passphrase)
        self.selected_network = target_network

        self.restart_interface()


    def validate_network(self, network):

        if not all(key in network for key in ["encryption", "essid", "signal"]):
            raise RuntimeError("Wifi network '" + network["essid"] + "' has incomplete information")

        enc = network["encryption"]
        if enc is True:
            if not any(key in network for key in ["wpa2", "wpa1"]):
                raise RuntimeError("Wifi network '" + network["essid"] + "' has encryption on, but no supported auth methods")

		# FIXME: probably not needed. do we really care which algorithms are used?
		#
		#	if "wpa2" in network and "PSK" in network["wpa2"]["auth-suites"]:
		#		self.selected_auth = "wpa2"
		#	elif "wpa1" in network and "PSK" in network["wpa1"]["auth-suites"]:
		#		self.selected_auth = "wpa1"
		#	else:
		#		raise RuntimeError("Wifi network '" + network["essid"] + "' has encryption on, but no supported auth methods")


    def write_wpa_config(self, network, passphrase):

        with open(Networking.WLAN0_CONFIG_FILE, "w+") as f:
            f.write("auto wlan0\n")
            f.write("iface wlan0 inet dhcp\n")
            f.write("wpa-ssid %s\n" % network["essid"])
            if network["encryption"] is True:
                f.write("wpa-psk %s\n" % passphrase)

     

    def restart_interface(self):
        output = subprocess.check_output([Networking.IFDOWN, Networking.DEVICE])
        output = subprocess.check_output([Networking.IFUP, Networking.DEVICE])

    IFCONFIG = '/sbin/ifconfig'
    CAT = '/bin/cat'

    def get_current(self):
        output = subprocess.check_output([Networking.IFCONFIG, Networking.DEVICE])
        output = output.decode()
        lines = filter(None, output.split('\n'))
        addr = None
        for line in lines:
            match = re.search(r'^\s+inet addr:(\S+)',line)
            if match:
                addr = match.group(1)
                break
        essid = None
        output = subprocess.check_output([Networking.CAT, Networking.WLAN0_CONFIG_FILE])
        output = output.decode()
        lines = filter(None, output.split('\n'))
        for line in lines:
            match = re.search(r'^wpa-ssid\s+(.*)',line.strip())
            if match:
                essid = match.group(1)
                break
        data = {
            'essid' : essid,
            'ip' : addr
        }
        return data



if __name__ == "__main__":
    nw = Networking()
    print(nw.get_current())
    networks = nw.scan_wifi_networks()
    for network in networks:
        print(network)

    nw.select_wifi_network("ASUS 2", "NyVolvoStudsarVilt")
