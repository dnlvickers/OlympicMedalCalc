import matplotlib.pyplot as plt
import random

def generate_array(n=20):
    # generate array counting up to n
    array = []
    for i in range(1, n+1):
        array.append(i)
    return array


def generate_points(numEvents=3):
    # generate random array of events placements
    events = []
    for i in range(numEvents):
        events.append(generate_array(20))
        random.shuffle(events[-1])

    # calculate each climbers score based on those placements
    points = events[0]
    for i in range(1, numEvents):
        for j in range(len(points)):
            points[j] *= events[i][j]

    return points


def get_podium(points):
    # get the podium finishers
    points.sort()
    return points[:3]


def format_data(data):
    # convert the data into something that can be plotted
    scores = []
    gold = []
    silver = []
    bronze = []
    medal = []
    for key in data:
        scores.append(key)

    scores.sort()
    for score in scores:
        seen = data[score]['seen']
        gold.append(data[score]['gold']/seen)
        silver.append(data[score]['silver']/seen)
        bronze.append(data[score]['bronze']/seen)
        medal.append(gold[-1] + silver[-1] + bronze[-1])

    return {'scores': scores, 'gold': gold, 'silver': silver, 'bronze': bronze, 'medal': medal}


def generate_plot(data):
    # plots and saves the data
    plt.figure()
    plt.plot(data['scores'], data['gold'], linewidth=2, color='#d4af37')
    plt.plot(data['scores'], data['silver'], linewidth=2, color='#bec2cb')
    plt.plot(data['scores'], data['bronze'], linewidth=2, color='#cd7f32')
    plt.plot(data['scores'], data['medal'], linewidth=2, color='black')

    plt.xlim([0, 250])
    plt.ylim([0, 1.01])

    plt.xlabel('Combined Score')
    plt.ylabel('Normalized Probability')

    plt.savefig('OlympicMedals.png')
    plt.show()


def main(samples=100, numEvents=3):
    print("Generating plot with", samples, "samples")

    totals = {}
    for i in range(samples):
        if i % int(samples/100) == 0:
            print('Processed', 100*i/samples, 'percent of the data')
        points = generate_points(numEvents)

        # find the first, second, and third placements from those
        podium = get_podium(points)

        for score in points:
            if score in totals:
                totals[score]['seen'] += 1
            else:
                totals[score] = {'seen': 1, 'gold': 0, 'silver': 0, 'bronze': 0}

        totals[podium[0]]['gold'] += 1
        totals[podium[1]]['silver'] += 1
        totals[podium[2]]['bronze'] += 1

    data = format_data(totals)
    generate_plot(data)


if __name__ == '__main__':
    main(10**7, 3)
