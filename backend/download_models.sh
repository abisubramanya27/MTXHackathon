#!/bin/bash

wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1-OmwxtTCvUH9b96KqUP8kyuCb_8fzBaZ' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1-OmwxtTCvUH9b96KqUP8kyuCb_8fzBaZ" -O scoring_model.bin
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=15v0Bx3MTmRzZFl_0mj1sJdcz2QAWa7_8' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=15v0Bx3MTmRzZFl_0mj1sJdcz2QAWa7_8" -O bert_model.bin
wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1u-I3gaUrol-3Zcu7eGAwEwUQCHU9Hdg-' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1u-I3gaUrol-3Zcu7eGAwEwUQCHU9Hdg-" -O knn_model