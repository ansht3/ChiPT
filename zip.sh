#!/bin/bash

# Change to the parent directory
cd ..

# Zip the directory, outputting the file back into the directory, excluding the archives themselves to prevent recursion
zip -r ChiPT/ChiPT.zip ChiPT -x "ChiPT/chipt/*" -x "ChiPT/ai_service/chiptai/*" -x "ChiPT/cache_service/chiptcache/*" -x "ChiPT/cache_service/volumes/*" -x "ChiPT/ChiPT.zip" -x "ChiPT/ChiPT.tar.gz"

tar -cvzf ChiPT/ChiPT.tar.gz \
--exclude='ChiPT/chipt' \
--exclude='ChiPT/ai_service/chiptai' \
--exclude='ChiPT/cache_service/chiptcache' \
--exclude='ChiPT/cache_service/volumes' \
--exclude='ChiPT/ChiPT.zip' \
--exclude='ChiPT/ChiPT.tar.gz' \
ChiPT
