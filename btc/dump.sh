#!/bin/sh

start=20221018
end=20221021

current=$start

while [ $current -le $end ]
do
  tmp=https://gz.blockchair.com/bitcoin/blocks/blockchair_bitcoin_blocks_$current
  url=${tmp}.tsv.gz
  wget ${url} --no-check-certificate
  current=`date -d "$current 1day" "+%Y%m%d"`
done
