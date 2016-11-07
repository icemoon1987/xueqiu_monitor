#!/bin/bash

ps -ef | grep xueqiu_monitor | grep -v grep | cut -c 9-15 | xargs kill
