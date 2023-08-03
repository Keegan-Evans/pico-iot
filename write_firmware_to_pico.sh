if [[ -d /media/$USER/RPI-RP2 ]];
then
# TODO: add steps to download and copy the flash nuke firmware first? Though, this might require disconnecting and reconnecting the pico
cp /home/$USER/pico/micropython/ports/rp2/build-PICO_W/firmware.uf2 /media/$USER/RPI-RP2/;
else
echo "No connected Pico detected, please make sure to plug in your Pico to the sensor hub while pressing and holding the 'BOOTSEL' button";
fi
