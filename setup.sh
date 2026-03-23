#!/bin/bash

# Warna
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}[*] Menginstall dependensi...${NC}"
pip install phonenumbers argparse

echo -e "${GREEN}[*] Mengatur izin eksekusi...${NC}"
chmod +x phone_tracer.py

# Cek apakah di Termux atau Linux biasa
if [ -d "/data/data/com.termux/files/usr/bin" ]; then
    BIN_PATH="/data/data/com.termux/files/usr/bin/phonetrace"
    echo -e "${GREEN}[*] Lingkungan Termux terdeteksi.${NC}"
else
    BIN_PATH="/usr/local/bin/phonetrace"
    echo -e "${GREEN}[*] Lingkungan Linux terdeteksi (memerlukan sudo).${NC}"
fi

sudo ln -sf $(pwd)/phone_tracer.py $BIN_PATH 2>/dev/null || ln -sf $(pwd)/phone_tracer.py $BIN_PATH

echo -e "${GREEN}[+] Selesai! Ketik 'phonetrace' untuk menjalankan.${NC}"
