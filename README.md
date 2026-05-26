# Photogrammetry

An exhibit that takes pictures of the visitor's face and creates a 3d model from them, displaying the model in the outside screen

# Installation

The current version (as of 26.5.26) of the project uses a moving camera (the multiple cam setup is still a WIP), so we'll use the movingcam folder.

## Viewer ("outside screen")
### connecting to the network folder
1. Make sure there's a wired connection between the pc running the viewer and the pc running the scanner.
2. open terminal in the movingcam folder.
2. `chmod +x ./setup_samba_network.sh && sudo ./setup_samba_network.sh` and enter the username and password for the scanner pc. this step sets up a manual ip address and creates a mounting point for the pc so it can just go to /mnt/shared_in and it'll see the shared files from the Scanner pc.
3. `chmod +x ./setup_autorun.sh && ./setup_autorun.sh` adds the run.sh to the startup of the pc. restarting should open the app on login.

## Scanner ("inside screen")
1. Make sure there's a wired connection between the pc running the viewer and the pc running the scanner.
2. in network settings under wired connection, manually set:
```bash
IP: 192.168.1.2
Subnet mask: 255.255.255.0
Gateway: 192.168.1.1
```
(note here the ip and gateway are the reverse of the viewer)
