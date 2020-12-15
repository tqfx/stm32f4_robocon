#!/usr/bin/env python3
import os
import sys

vscjson = 'vscjson'
vsc = '.vscode'

cwd = os.getcwd()
if cwd[-1] == '\\' or cwd[-1] == '/':
    cwd = cwd[:-1:]

oldelfname = 'ELFNAME'
elfname = cwd.split('\\')[-1].split('/')[-1]  # Windows | unix

binpwd = sys.argv[0].split('\\')[-1].split('/')[-1]
pwd = sys.argv[0].replace(binpwd, '').replace('\\', '/')
del binpwd

oldconfig = 'openocd.cfg'
config = oldconfig
cfglist = os.listdir(pwd)
for cfgline in cfglist:
    if '.cfg' in cfgline:
        config = cfgline
        break
del cfglist


def dealpwd(pwd):
    if '/' != pwd[-1] and '\\' != pwd[-1]:
        pwd += '/'
    return pwd


pwd = dealpwd(pwd)
cwd = dealpwd(cwd)
vsc = dealpwd(vsc)
vscjson = dealpwd(vscjson)


def launch():
    filename = 'launch.json'

    with open(pwd + vscjson + filename, "r", encoding="utf-8") as f:
        txt = f.read()

    txt = txt.replace(oldelfname, elfname)
    txt = txt.replace('./' + oldconfig, pwd + config)

    with open(cwd + vsc + filename, "w", encoding="utf-8") as f:
        f.write(txt)
    del txt
    del filename

    return


def task():
    filename = 'tasks.json'

    with open(pwd + vscjson + filename, "r", encoding="utf-8") as f:
        txt = f.read()

    with open(cwd + vsc + filename, "w", encoding="utf-8") as f:
        f.write(txt)
    del txt
    del filename

    return


def c_cpp():
    filename = 'c_cpp_properties.json'

    with open(pwd + vscjson + filename, "r", encoding="utf-8") as f:
        txt = f.read()

    with open(cwd + vsc + filename, "w", encoding="utf-8") as f:
        f.write(txt)
    del txt
    del filename

    return


def makefile(pwd):
    filename = 'Makefile'

    openocd = '\topenocd -f ' + pwd + 'openocd.cfg -c init -c halt -c '
    cmd = 'update:\n' + openocd + \
        '"program $(BUILD_DIR)/$(TARGET).hex verify reset exit"\n'
    cmd += 'reset:\n' + openocd + 'reset -c shutdown\n'
    del openocd

    with open(filename, "r", encoding="utf-8") as f:
        txt = f.read()

    end = 'EOF'
    txtlist = txt.split(end)
    del txt

    txt = txtlist[0] + end
    del end

    if ' ***' in txtlist[-1]:
        txt += ' ***'
    del txtlist

    txt += '\n' + cmd
    del cmd

    with open(filename, "w", encoding="utf-8") as f:
        f.write(txt)
    del txt
    del filename

    return


def vscinit():
    try:
        os.mkdir(vsc)
    except FileExistsError:
        pass
    except Exception as e:
        print(e)
        exit()
    return


if __name__ == "__main__":
    vscinit()
    c_cpp()
    launch()
    task()
    makefile(pwd)
    print('config:', pwd + 'openocd.cfg')
