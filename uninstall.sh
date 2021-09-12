#/bin/bash
sudo systemctl stop xournalpp-autoconverter.service
sudo systemctl disable xournalpp-autoconverter.service

sudo rm /usr/local/lib/systemd/system/xournalpp-autoconverter.service

