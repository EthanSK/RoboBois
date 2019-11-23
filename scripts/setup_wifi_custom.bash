#!/bin/bash

if [[ $EUID > 0 ]]; then
  echo "This script requires sudo"
  exit 1
fi

read -p "SSID: " ssid
read -p "Password: " -s passwd
echo

# hash the password
hash=$(echo -n $passwd | iconv -t utf16le | openssl md4 -r | cut -d" " -f1)
# rm /etc/wpa_supplicant/wpa_supplicant.conf

# touch /etc/wpa_supplicant/wpa_supplicant.conf
cat <<EOT >>/etc/wpa_supplicant/wpa_supplicant.conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={
	ssid="$ssid"
	password=hash:${hash}
}
EOT

systemctl restart wpa_supplicant_wlan0.service
