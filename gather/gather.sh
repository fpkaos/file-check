#!/bin/bash

clear
base64 -d <<< "`./ascii_to_base64.sh gather_banner`" | gunzip

menu(){
echo -e "\nWould you like to learn?"
echo -e "\n- disks;\n- dmi;\n- cpu;\n- mem;\n- menu;\n"
echo -e "Write \e[30;100m <command>-all \e[0m to learn more"
}

if [ `id -u` -eq 0 ] ; then

  echo -e "You are in \e[32m`uname -a`\e[0m through \e[32m$SHELL\e[0m runlevel `runlevel`"
  menu

  while read -r INFO; do

  case $INFO in

    disks)
      df -h
      ;;
    disks-all)
      hdds=($(lsblk -dn -o NAME));
      for hdd in ${!hdds[@]}; do hdparm -I "/dev/${hdds[$hdd]}" | less; done
      ;;
    dmi)
      echo -e "\e[33mVendor:\e[0m `dmidecode -s system-manufacturer`"
      echo -e "\e[33mMachine:\e[0m `dmidecode -s system-product-name`"
      echo -e "\e[33mSerial number:\e[0m `dmidecode -s system-serial-number`"
      ;;
    dmi-all)
      dmidecode | less
      ;;
    cpu)
    echo -e "\e[33mCPU usage:\e[0m\n `mpstat -P ALL`"
    ;;
    cpu-all)
    lscpu | less
    ;;
    mem)
    free -h
    ;;
    menu)
      menu
      ;;
    *)
    echo "Press Ctrl+C to exit script"
      ;;

  esac

  done

else 
  echo "You must be root!"
fi
