#!/usr/bin/env bash
# King - UserBot
# Copyright (C) 2020 King-Userbot
#
# This file is a part of < https://github.com/DoellBarr/King-Userbot/ >
# <https://www.github.com/DoellBarr/King-Userbot/blob/main/LICENSE/>.
# PLease read the GNU Affero General Public License in

clear
echo -e "\e[1m"
echo " KING USERBOT"
echo -e "\e[0m"
sec=5
spinner=(⣻ ⢿ ⡿ ⣟ ⣯ ⣷)
while [ $sec -gt 0]; do
  echo -ne "\e[33m ${spinner[sec]} Memulai instalasi dalam $sec detik...\r"
  sleep 1
  sec=$(($sec - 1))
done
echo -e "\e[1;32mMeng-Install Dependencies ----------------------------------\e[0m\n"
apt-get update
apt-get upgrade -y
pkg upgrade -y
pkg install python wget -y
wget https://raw.githubusercontent.com/DoellBarr/King-Userbot/main/resources/session/string_session.py
pip install telethon
clear
python3 string_session.py