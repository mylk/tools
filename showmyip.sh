IP=`wget "https://www.showmyip.gr" -O - -o /dev/null | grep "ip_address" | awk -F '>' '{print($2)}'`
echo $IP

# get hostname and remove last character
host $IP | awk '{print($NF)}' | sed 's/.$//'
#dig +short -x $IP | sed 's/.$//'

