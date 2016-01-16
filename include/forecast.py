# coding: utf-8


try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import json
import time


def get_forecast(path, key, ican):
    '''(str, str) -> list(float, int)
    Get 10 days forecast for airport ICAN code with the wunderground API key
    :param key: wunderground key
    :param ican: Airport ICAN code
    :return: list of [YYYYMMDD, temperature, humidity]
    '''
    outlist = []
    url = 'http://api.wunderground.com/api/' + key + '/forecast10day/q/' + ican + '.json'
    json_response = urllib2.urlopen(url).read()
    parsed_json = json.loads(json_response.decode("utf-8"))

    #outfile = open(path + 'testdata/' + ican + '.txt', 'w')
    #json.dump(parsed_json, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
    #outfile.close()

    if not ('error' in parsed_json['response']):
        forecast10day = parsed_json['forecast']['simpleforecast']['forecastday']
        for idx in range(len(forecast10day)):
            avghumidity = int(forecast10day[idx]['avehumidity'])
            avgtemp = (int(forecast10day[idx]['high']['celsius']) + \
                       int(forecast10day[idx]['low']['celsius'])) // 2
            date = str(forecast10day[idx]['date']['year']) + '-' + \
                   str(forecast10day[idx]['date']['month']) + '-' + \
                   str(forecast10day[idx]['date']['day'])
            outlist.append([date, avgtemp, avghumidity])
    return outlist


def saveforecast(path, adata, key):
    for country in adata:
        for state in adata[country]:
            for ican in adata[country][state]:
                try:
                    outlist = get_forecast(path, key, ican)
                    outfile = open(path + ican + '.csv', 'w')
                    if len(outlist) > 0:
                        for idx in range(len(outlist)):
                            outfile.write(outlist[idx][0] + ';' + \
                                          str(outlist[idx][1]) + ';' + \
                                          str(outlist[idx][2]) + '\n')
                    outfile.close()
                    print(ican + ' is done.')
                except:
                    print(ican + ': data is not available.')
                time.sleep(7)

if __name__ == '__main__':
    import loadairports
    import key, os
    adata = loadairports.load_airports()
    key = key.get_key()
    saveforecast(os.getcwd() + '/../out/forecast/', adata, key)