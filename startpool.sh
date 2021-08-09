#!/bin/bash



#api:
echo starting API
screen -L -Logfile api.log -dmS api ./build/bin/open-ethereum-pool config.api.json

#unlocker:
echo starting proxy
screen -L -Logfile proxy.log -dmS proxy ./build/bin/ethash-mining-pool config.proxy.json

#payout:
echo starting payout
#screen -L -Logfile payout.log -dmS payout ./build/bin/ethash-mining-pool config.payout.json
