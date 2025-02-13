# OpenWRT Ethers Sync

## Setup
- Setup SSH Public key auth from your ISC-DHCP Server goint TO your AccessPoint
  - If you can sftp using `root@your_AP_ip_or_hostname`, you'll be able to run the script
- Install UV
  - `wget -qO- https://astral.sh/uv/install.sh | sh`
- Add script to Crontab
  - `*/60 * * * * uv run /opt/uap_sync/openwrt.py`
- PROFIT
