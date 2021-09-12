pip install -r requirements.txt

DIR=${1:-"/home"}

python -c "with open('$(pwd)/service-template') as f: print(f.read() % ('$(which python)', '$(pwd)', '$DIR'))" > xournalpp-autoconverter.service

sudo mkdir -p /usr/local/lib/systemd/system
sudo cp xournalpp-autoconverter.service /usr/local/lib/systemd/system/

sudo systemctl stop xournalpp-autoconverter.service
sudo systemctl disable xournalpp-autoconverter.service

sudo systemctl enable xournalpp-autoconverter.service
sudo systemctl start xournalpp-autoconverter.service
