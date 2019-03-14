ping -c 1 -W 2 www.google.com > /dev/null

if [ $? -ne 0 ]
then
    echo "Offline."
else
    echo "Online."
fi
