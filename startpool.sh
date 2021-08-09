#!/bin/bash

#Make sure no other pesky screens are running
killall screen
screen -wipe
sleep 1
#api:
echo starting API
screen -L -Logfile api.log -dmS api ./build/bin/open-ethereum-pool config.api.json

#unlocker:
echo starting proxy
screen -L -Logfile proxy.log -dmS proxy ./build/bin/open-ethereum-pool config.proxy.json

#payout:
echo starting payout
#screen -L -Logfile payout.log -dmS payout ./build/bin/open-ethereum-pool config.payout.json
