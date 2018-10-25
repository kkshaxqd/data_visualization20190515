from proxypool.scheduler import Scheduler
import sys
import io
## 关闭蓝灯等软件，运行这种代理的时候
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    try:
        s = Scheduler()
        s.run()
    except:
        main()


if __name__ == '__main__':
    main()
