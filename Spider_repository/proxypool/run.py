from proxypool.scheduler import Scheduler
import sys
import io
# 使用需要先在配置setting.py里修改host和密码 127.0.0.1 ，密码没有的话改为None
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        s = Scheduler()
        s.run()
    except:
        main()


if __name__ == '__main__':
    main()
