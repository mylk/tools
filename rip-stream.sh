#!/bin/bash
FILENAME=`date +"%Y%m%d_%H%M%S"`;

# default option values
FORMAT="ogg";
BACKGROUND=0;

# get the values of the supplied options
while getopts ":s:f:b" OPTION;
do
    case $OPTION in
        s)
            SOURCE="$OPTARG";
            ;;
        f)
            FORMAT=$OPTARG;
            ;;
        b)
            BACKGROUND=1;
            ;;
    esac
done

# if stream source address not supplied
if [ -z $SOURCE ]
then
    echo "Please provide a source. Use the -s option.";
    exit 1;
fi;

# check vlc is installed
vlc_installed=`vlc --version`;
if [ -z "$vlc_installed" ]
then
    echo "Please install the VLC media player.";
    exit 1;
fi;

# select the proper codec (mp3 of ogg for now)
if [ "$FORMAT" = "mp3" ]
then
    codec="mp3";
elif [ "$FORMAT" = "ogg" ]
then
    codec="vorb";
else
    codec="vorb";
    FORMAT="ogg";
fi;

FILENAME_FULL="$HOME/$FILENAME.$FORMAT";
echo -e "Ripping $SOURCE to $FILENAME_FULL\n";

# execute the appropriate vlc command according to the background (-b) option
if [ "$BACKGROUND" -eq "1" ]
then
    # without forwarding to speakers, no interface, runs on background
    vlc -vvv $SOURCE --quiet --intf dummy --sout "#transcode{vcodec=none,acodec=$codec,ab=128,channels=2,samplerate=44100}:file{dst=$FILENAME_FULL}\"}"
else
    # forwards to speakers and shows interface
    vlc -vvv $SOURCE --quiet --sout "#duplicate{dst=display,dst=\"transcode{vcodec=none,acodec=$codec,ab=128,channels=2,samplerate=44100}:file{dst=$FILENAME_FULL}\"}"
fi;
