import json
import matplotlib.pyplot as plt
import operator


if __name__ == '__main__':
    with open('angles.json') as f:
        multi_view_angles = json.load(f)

    with open(
            'C:\\Users\\hkecl\\OneDrive\\Documents\\Summer2020Research\\lwopenpose\\lightweight-human-pose-estimation-3d-demo.pytorch\\angles.json') as f:
        single_view_angles = json.load(f)
    multisub = lambda a, b: map(operator.sub, a, b)
    for key in multi_view_angles:
        x = [x for x in range(0, len(multi_view_angles[key]))]
        y1 = list(multi_view_angles[key].values())
        y2_temp = list(single_view_angles[key].values())
        y2=[]
        for item in y2_temp:
            y2.append(float(item))
        y1 = y1[:len(x)]
        y2 = y2[:len(x)]
        i=0
        while(i < len(x)):
            if y1[i] == 0 or y2[i] == 0:
                del x[i]
                del y1[i]
                del y2[i]
            i+=1
        plt.plot(x, y1, label='multi-view')
        plt.legend()
        plt.plot(x, y2, label='single-view')
        plt.legend()
        plt.savefig(key + '_chart.jpg')
        plt.clf()

        diff = list(multisub(y1,y2))
        plt.plot(x, diff, label = key)
        plt.legend()
        plt.savefig(key + '_diff_chart.jpg')
        plt.clf()
