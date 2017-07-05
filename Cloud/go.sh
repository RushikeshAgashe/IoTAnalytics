#!/bin/bash
python3 sd_server.py & python3 coap_light_history_server.py & python3 coap_path_finder_server.py & python3 data_polling_client.py && fg 
