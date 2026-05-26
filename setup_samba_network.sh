#!/bin/bash
# ============================================================
#  setup_samba_network.sh
#  - Mounts a Samba share (shared_in) to /mnt/shared_in
#  - Sets wired network to static IP 192.168.1.1
#  - Updates cifs-utils
# ============================================================

set -e

# ── colours ─────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'

info()    { echo -e "${GREEN}[INFO]${NC}  $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

# ── must run as root ─────────────────────────────────────────
[[ $EUID -ne 0 ]] && error "Please run as root:  sudo bash $0"

echo ""
echo "============================================"
echo "   Samba Share + Network Setup Script"
echo "============================================"
echo ""

# ── 1. static network via NetworkManager (nmcli) ─────────────
STATIC_IP="192.168.1.1"
GATEWAY="192.168.1.2"
SUBNET="255.255.255.0"
PREFIX="24"       # /24 = 255.255.255.0
DNS="8.8.8.8,8.8.4.4"

info "Configuring static IP on wired interface..."

# Find the first wired (ethernet) connection profile
WIRED_CON=$(nmcli -t -f NAME,TYPE connection show | grep ethernet | head -1 | cut -d: -f1)

if [[ -z "$WIRED_CON" ]]; then
    # No existing ethernet profile — create one
    WIRED_DEV=$(nmcli -t -f DEVICE,TYPE device status | grep ethernet | head -1 | cut -d: -f1)
    [[ -z "$WIRED_DEV" ]] && error "No wired ethernet device found."
    WIRED_CON="Wired-Static"
    nmcli connection add type ethernet ifname "$WIRED_DEV" con-name "$WIRED_CON"
    info "Created new connection profile: $WIRED_CON (device: $WIRED_DEV)"
else
    info "Found existing wired connection profile: '$WIRED_CON'"
fi

nmcli connection modify "$WIRED_CON" \
    ipv4.method manual \
    ipv4.addresses "$STATIC_IP/$PREFIX" \
    ipv4.gateway "$GATEWAY" \
    ipv4.dns "$DNS"

nmcli connection down "$WIRED_CON" 2>/dev/null || true
nmcli connection up   "$WIRED_CON"

info "Static IP configured:"
echo "         IP      : $STATIC_IP"
echo "         Gateway : $GATEWAY"
echo "         Subnet  : $SUBNET"
echo "         DNS     : $DNS"
echo ""
# ── 2. user inputs ───────────────────────────────────────────
SERVER_IP=192.168.1.2

read -rp "  Samba username     : " SMB_USER
[[ -z "$SMB_USER" ]] && error "Username cannot be empty."

read -rsp "  Samba password     : " SMB_PASS
echo ""
[[ -z "$SMB_PASS" ]] && error "Password cannot be empty."

SHARE_NAME="shared_in"
MOUNT_POINT="/mnt/shared_in"

echo ""
info "Settings:"
echo "         Server   : $SERVER_IP"
echo "         Share    : $SHARE_NAME  →  $MOUNT_POINT"
echo "         User     : $SMB_USER"
echo ""

# ── 3. update & install cifs-utils ───────────────────────────
info "Updating package list and upgrading cifs-utils..."
apt-get update -qq
apt-get install -y --only-upgrade cifs-utils 2>/dev/null || apt-get install -y cifs-utils
info "cifs-utils is up to date."

# ── 4. create mount point ────────────────────────────────────
if [[ ! -d "$MOUNT_POINT" ]]; then
    mkdir -p "$MOUNT_POINT"
    info "Created mount point: $MOUNT_POINT"
else
    warn "Mount point $MOUNT_POINT already exists — skipping mkdir."
fi

# ── 5. save credentials securely ─────────────────────────────
CRED_FILE="/etc/samba/.credentials_shared_in"
cat > "$CRED_FILE" <<EOF
username=$SMB_USER
password=$SMB_PASS
EOF
chmod 600 "$CRED_FILE"
info "Credentials saved to $CRED_FILE (mode 600)."

# ── 6. add fstab entry (idempotent) ──────────────────────────
FSTAB_ENTRY="//$SERVER_IP/$SHARE_NAME  $MOUNT_POINT  cifs  credentials=$CRED_FILE,uid=1000,gid=1000,iocharset=utf8,_netdev  0  0"
FSTAB_MARKER="//$SERVER_IP/$SHARE_NAME"

if grep -qF "$FSTAB_MARKER" /etc/fstab; then
    warn "fstab already contains an entry for $FSTAB_MARKER — skipping."
else
    cp /etc/fstab /etc/fstab.bak.$(date +%Y%m%d_%H%M%S)
    echo "" >> /etc/fstab
    echo "# Samba share added by setup_samba_network.sh" >> /etc/fstab
    echo "$FSTAB_ENTRY" >> /etc/fstab
    info "fstab entry added (backup saved)."
fi

# ── 7. mount now ─────────────────────────────────────────────
info "Mounting $MOUNT_POINT ..."
mount "$MOUNT_POINT" && info "Mounted successfully." || error "Mount failed. Check server IP, credentials, and that the server is reachable."


echo -e "${GREEN}============================================"
echo -e "   All done! Setup completed successfully."
echo -e "============================================${NC}"
echo ""
echo "  Share mounted at : $MOUNT_POINT"
echo "  Static IP        : $STATIC_IP  (persists across reboots)"
echo ""
