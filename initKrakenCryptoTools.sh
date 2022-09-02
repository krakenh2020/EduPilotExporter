#!/bin/bash

Data='data.csv'

KrakenCryptoTools='/home/smore/go/bin/KrakenCryptoTools'
KeyName='zk-keys/kraken-edu-exporter-key1'


$KrakenCryptoTools zk-sig keygen --keyName $KeyName

$KrakenCryptoTools zk-sig sign --dataset $Data --keyName $KeyName

