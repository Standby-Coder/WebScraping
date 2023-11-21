#!/bin/bash

mysql -u keshav -p chewy < chewy.sql
pip install -r requirements.txt
