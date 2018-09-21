from die import Die
import pygal

def die_test():
    # 创建一个D6
    die = Die()

    # 掷骰子，并将结果存储在一个列表中
    results = []
    for roll_num in range(1000):
        result = die.roll()
        results.append(result)

    #print(results)

    # 分析结果
    frequencies = []
    for value in range(1,die.num_sides+1):
        frequency = results.count(value)
        frequencies.append(frequency)

    # 对结果进行可视化
    hist = pygal.Bar()
    hist.title = "Results of rolling one D6 1000 times."
    hist.x_labels = ['1', '2', '3', '4', '5', '6']
    hist.x_title = "Result"
    hist.y_title = "Frequency of Result"
    hist.add('D6', frequencies)
    hist.render_to_file('die_visual.svg')

def pygal_test():
    line_chart = pygal.Line()
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE',  [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others', [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
    #line_chart.render()
    line_chart.render_to_file('ie_visual.svg')

#pygal_test()


def die_test2():
    # 创建两个D6骰子
    die_1 = Die()
    die_2 = Die(10)
    # 掷骰子多次，并将结果存储到一个列表中
    results = []
    for roll_num in range(10000):
        result = die_1.roll() + die_2.roll()
        results.append(result)
    # 分析结果
    frequencies = []
    max_result = die_1.num_sides + die_2.num_sides
    for value in range(2, max_result + 1):
        frequency = results.count(value)
        frequencies.append(frequency)
    # 可视化结果
    hist = pygal.Bar()
    hist.title = "Results of rolling two D6 dice 1000 times."
    hist.x_labels =map(str,range(2,16)) #['2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12','13', '14', '15', '16']
    hist.x_title = "Result"
    hist.y_title = "Frequency of Result"
    hist.add('D6 + D10', frequencies)
    hist.render_to_file('dice_visual2.svg')

die_test2()
