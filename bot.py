import nonebot
import config
import logging
from os import path

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(path.join(path.dirname(__file__), "purchase", "plugins"), "purchase.plugins")
    nonebot.load_plugins(path.join(path.dirname(__file__), "sd", "plugins"), "sd.plugins")
    nonebot.run(host='127.0.0.1', port=8080)
