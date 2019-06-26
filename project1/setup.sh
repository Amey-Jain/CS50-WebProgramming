#!/bin/bash
echo "Running setup script"
#startup file for setting enviornment variables
set DATABASE_URL=postgres://oyagmsssmdoyqy:e5d6bb095f9c21d1a847dcb6032c6eb38b79bd69dfd41db90c7ac35ab058ccf2@ec2-54-235-104-136.compute-1.amazonaws.com:5432/d5dqq4d92hf2bp;
export FLASK_APP=application.py;
export FLASK_ENV=production;
