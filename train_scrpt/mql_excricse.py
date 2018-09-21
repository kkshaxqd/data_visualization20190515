import matplotlib.pyplot as plt
from data_deal_tools.random_walk import RandomWalk

def plot_squares():
    input_values = [1, 2, 3, 4, 5]
    squares = [1, 4, 9, 16, 25]
    plt.plot(input_values, squares, linewidth=5)
    plt.title("Square Numbers", fontsize=24)
    plt.xlabel("Value", fontsize=14)
    plt.ylabel("Square of Value", fontsize=14)
    # 设置刻度标记的大小
    plt.tick_params(axis='both', labelsize=14)
    plt.show()

def plot_scatter():
    x_values = list(range(1, 1001))
    y_values = y_values = [x**2 for x in x_values]
    #plt.scatter(x_values, y_values, c='red', edgecolor='none',s=40)
    #plt.scatter(x_values, y_values, c = (0, 0, 0.8), edgecolor='none', s=40)
    plt.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues,
                edgecolor='none', s=40) #颜色映射
    plt.title("Square Numbers", fontsize=24)
    plt.xlabel("Value", fontsize=14)
    plt.ylabel("Square of Value", fontsize=14)
    # 设置刻度标记的大小
    plt.tick_params(axis='both', which='major', labelsize=14)
    # 设置每个坐标轴的取值范围
    plt.axis([0, 1100, 0, 1100000])
    #plt.show()
    plt.savefig('squares_plot.png', bbox_inches='tight') #多余的空白区域裁剪掉


#plot_scatter()
def random_walk_test():
    # 创建一个RandomWalk实例，并将其包含的点都绘制出来
    # 只要程序处于活动状态，就不断地模拟随机漫步
    while True:
        rw = RandomWalk(5000)
        rw.fill_walk()
        # 设置绘图窗口的尺寸
        plt.figure(dpi=128,figsize=(10, 6))
        point_numbers = list(range(rw.num_points))
        plt.scatter(rw.x_values, rw.y_values, c=point_numbers,
                    cmap=plt.cm.Blues,edgecolor='none', s=1)
        # 突出起点和终点
        plt.scatter(0, 0, c='green', edgecolors='none', s=100)
        plt.scatter(rw.x_values[-1], rw.y_values[-1], c='red', edgecolors='none',
                    s=100)
        # 隐藏坐标轴
        #plt.axes().get_xaxis().set_visible(False)
        #plt.axes().get_yaxis().set_visible(False)
        plt.show()
        keep_running = input("Make another walk? (y/n): ")
        if keep_running == 'n':
            break

random_walk_test()
