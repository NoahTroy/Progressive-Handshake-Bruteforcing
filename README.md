# Progressive Handshake Bruteforcing Script:
This script allows you to bruteforce wireless handshakes via aircrack-ng, using a simplified process that and saves your progress along the way, allowing you to quit, pause, and resume, anytime you'd like.

## How To Use The Script:
1.  Make sure you have aircrack-ng and python3 installed:
    -   `sudo apt install python3 aircrack-ng -y`
2.  Navigate to directory in which you wish to use the script, then clone the repository:
    -   `git clone https://github.com/NoahTroy/Progressive-Handshake-Bruteforcing.git`
3.  Navigate to the folder:
    -   `cd Progressive-Handshake-Bruteforcing/`
4.  Make the script executable:
    -   `sudo chmod +x Progressive\ Cracking.py`
5. Make sure you have a wordlist available (you can make your own with crunch, or find them online), as well as a .cap file, with the handshake you wish to crack (can be aquired many ways, but it may be easiest to simply capture data using airodump-ng, whilst deauthing clients, such as with aireplay-ng).
6. Run the script:
    -   `sudo ./Progressive\ Cracking.py`
