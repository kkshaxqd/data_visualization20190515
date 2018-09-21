import json
import pygal
from pygal_maps_world.i18n import COUNTRIES
from pygal.style import RotateStyle,LightColorizedStyle


#for country_code in sorted(COUNTRIES.keys()):
#    print(country_code, COUNTRIES[country_code])

def get_country_code(country_name):
    """根据指定的国家，返回Pygal使用的两个字母的国别码"""
    for code, name in COUNTRIES.items():
        if name == country_name:
            return code
    # 如果没有找到指定的国家，就返回None
    return None
print(get_country_code('Andorra'))
print(get_country_code('United Arab Emirates'))
print(get_country_code('Afghanistan'))

def main():
    # 将数据加载到一个列表中
    filename = 'population_data.json'
    # 创建一个包含人口数量的字典
    cc_populations = {}
    with open(filename) as f:
        pop_data = json.load(f)
        # 打印每个国家2010年的人口数量
        for pop_dict in pop_data:
            if pop_dict['Year'] == '2010': #population_data.json中的值都是用引号括起的
                country_name = pop_dict['Country Name']
                population = int(float(pop_dict['Value']))
                #print(country_name + ": " + str(population))
                code = get_country_code(country_name)
                if code:
                    #print(code + ": " + str(population))
                    cc_populations[code] = population
                else:
                    print('ERROR - ' + country_name)
        # 根据人口数量将所有的国家分成三组
        cc_pops_1, cc_pops_2, cc_pops_3 = {}, {}, {}
        for cc, pop in cc_populations.items():
            if pop < 10000000:
                cc_pops_1[cc] = pop
            elif pop < 1000000000:
                cc_pops_2[cc] = pop
            else:
                cc_pops_3[cc] = pop
        # 看看每组分别包含多少个国家
        print(len(cc_pops_1), len(cc_pops_2), len(cc_pops_3))
        wm_style = RotateStyle('#336699', base_style=LightColorizedStyle)

        wm = pygal.maps.world.World(style=wm_style)
        wm.title = 'World Population in 2010, by Country'
        wm.add('0-10m', cc_pops_1)
        wm.add('10m-1bn', cc_pops_2)
        wm.add('>1bn', cc_pops_3)
        wm.render_to_file('world_population.svg')


# americas地图
def am_test1():
    wm = pygal.maps.world.World()
    wm.title = 'North, Central, and South America'
    wm.add('North America', ['ca', 'mx', 'us'])
    wm.add('Central America', ['bz', 'cr', 'gt', 'hn', 'ni', 'pa', 'sv'])
    wm.add('South America', ['ar', 'bo', 'br', 'cl', 'co', 'ec', 'gf',
        'gy', 'pe', 'py', 'sr', 'uy', 've'])
    wm.render_to_file('americas.svg')

def am_test2():
    wm = pygal.maps.world.World()
    wm.title = 'Populations of Countries in North America'
    wm.add('North America', {'ca': 34126000, 'us': 309349000, 'mx': 113423000})
    wm.render_to_file('na_populations.svg')

#am_test2()
main()

