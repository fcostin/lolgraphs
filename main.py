"""
pull data from unknownworlds stats json thing and graph it

everyone loves graphs
"""
import urllib2
import json
import pylab
import numpy

def get_json(url):
    socket = urllib2.urlopen(url)
    data = socket.read()
    socket.close()
    return json.loads(data)

def make_cols_from_json_stats(stats):
    stats.sort(key = lambda x : x['length'])
    cols = {}
    for item in stats:
        for key in item:
            if key not in cols:
                cols[key] = []
            cols[key].append(item[key])
    for key in cols:
        cols[key] = numpy.asarray(cols[key])
    return cols

team = {
    'marines' : 1,
    'aliens' : 2,
}

def main():
    """
    plot stacked histogram of wins for each time as function of round duration
    """

    target_url = r'http://unknownworldsstats.appspot.com/displayendgamestats?output=json'
    cols = make_cols_from_json_stats(get_json(target_url))

    duration = cols['length']
    duration = duration / 60.0 # --> minutes
    winner = cols['winner']

    bins = 5
    _, bin_edges = numpy.histogram(duration, bins)
    marine_hist, _ = numpy.histogram(duration[winner == team['marines']], bin_edges)
    alien_hist, _ = numpy.histogram(duration[winner == team['aliens']], bin_edges)
    rows = numpy.vstack((marine_hist, alien_hist))
    pylab.figure(figsize = (5, 4))
    widths = bin_edges[1:] - bin_edges[:-1]
    pylab.bar(bin_edges[:-1], alien_hist, widths, color = 'orange', label = 'marine wins')
    pylab.bar(bin_edges[:-1], marine_hist, widths, bottom = alien_hist, color = 'blue', label = 'alien wins')
    pylab.xlabel('round duration (minutes)')
    pylab.legend(loc = 'upper right')
    pylab.savefig('imbalance_versus_time.png', bbox_inches = 'tight')

if __name__ == '__main__':
    main()
