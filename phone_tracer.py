#!/usr/bin/python3
import argparse
import phonenumbers
import sys
import os
from phonenumbers import geocoder, carrier, timezone
from enum import Enum

# --- UI & Styling ---
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class Location(Enum):
    LEFT = 1
    RIGHT = 2
    CENTER = 3

class Visuals:
    @staticmethod
    def get_terminal_width():
        try:
            return os.get_terminal_size()[0]
        except OSError:
            return 80

    @staticmethod
    def print_line(char='='):
        print(Colors.OKBLUE + char * Visuals.get_terminal_width() + Colors.ENDC)

    @staticmethod
    def print_msg(message, location=Location.CENTER):
        width = Visuals.get_terminal_width()
        if location == Location.LEFT:
            spaces = 0
        elif location == Location.RIGHT:
            spaces = max(0, width - len(message))
        else:
            spaces = max(0, (width - len(message)) // 2)
        print(' ' * spaces + Colors.BOLD + message + Colors.ENDC)

# --- Core Logic ---
class PhoneTracer:
    def __init__(self, args):
        self.args = args
        self.results = []

    def process(self):
        Visuals.print_line('*')
        Visuals.print_msg("PHONE INFORMATION TRACER")
        Visuals.print_msg("Enhanced Version")
        Visuals.print_line('*')

        # Mode Single Number
        if self.args.input:
            res = self.examine_number(self.args.input, self.args.country_code)
            if res: self.results.append(res)
        
        # Mode Bulk List
        elif self.args.list:
            if not os.path.exists(self.args.list):
                print(f"{Colors.FAIL}[!] File {self.args.list} tidak ditemukan!{Colors.ENDC}")
                return
            
            with open(self.args.list, 'r') as f:
                numbers = [line.strip() for line in f if line.strip()]
                for num in numbers:
                    res = self.examine_number(num, self.args.country_code)
                    if res: self.results.append(res)
        
        # Output saving
        if self.args.output:
            self.save_results()

    def examine_number(self, number, default_cc):
        if self.args.verbose:
            print(f"\n{Colors.OKBLUE}[*] Menganalisis: {number}{Colors.ENDC}")

        try:
            # Parsing otomatis jika nomor diawali '+'
            parsed_num = phonenumbers.parse(number, default_cc if not number.startswith('+') else None)
            
            if not phonenumbers.is_valid_number(parsed_num):
                print(f"{Colors.WARNING}[!] Nomor {number} tidak valid!{Colors.ENDC}")
                return None

            # Ekstraksi Data
            info = {
                "number": phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "location": geocoder.description_for_number(parsed_num, "id"), # Bahasa Indonesia
                "carrier": carrier.name_for_number(parsed_num, "en") or "Unknown",
                "timezone": ", ".join(timezone.time_zones_for_number(parsed_num))
            }

            print(f"{Colors.OKGREEN}[+] Berhasil:{Colors.ENDC}")
            print(f"    - Internasional: {info['number']}")
            print(f"    - Lokasi       : {info['location']}")
            print(f"    - Provider     : {info['carrier']}")
            print(f"    - Waktu        : {info['timezone']}")
            
            return info

        except Exception as e:
            print(f"{Colors.FAIL}[!] Error pada {number}: {e}{Colors.ENDC}")
            return None

    def save_results(self):
        try:
            with open(self.args.output, 'w') as f:
                f.write("NOMOR | LOKASI | PROVIDER | TIMEZONE\n")
                f.write("-" * 50 + "\n")
                for r in self.results:
                    f.write(f"{r['number']} | {r['location']} | {r['carrier']} | {r['timezone']}\n")
            print(f"\n{Colors.OKBLUE}[*] Data disimpan di: {self.args.output}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}[!] Gagal menyimpan file: {e}{Colors.ENDC}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Phone Number Information Gathering Tool")
    parser.add_argument('-i', '--input', help='Input nomor telepon tunggal')
    parser.add_argument('-l', '--list', help='Input file berisi daftar nomor')
    parser.add_argument('-cc', '--country-code', default='ID', help='Default Country Code (Contoh: ID, US, GR). Default: ID')
    parser.add_argument('-o', '--output', help='Simpan hasil ke file teks')
    parser.add_argument('-v', '--verbose', action='store_true', help='Tampilkan detail proses')

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    tracer = PhoneTracer(args)
    tracer.process()
