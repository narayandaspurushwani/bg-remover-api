#!/bin/bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0
