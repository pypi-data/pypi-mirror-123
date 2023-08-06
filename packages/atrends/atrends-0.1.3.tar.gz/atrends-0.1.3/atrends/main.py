import os
import sys
import argparse
from datetime import date
from pytrends.request import TrendReq
import matplotlib.pyplot as plt

def f():

    pytrends = TrendReq(hl='en_US', tz=360)
    # https://github.com/pat310/google-trends-api/wiki/Google-Trends-Categories

    all_keywords = sys.argv[1:]

    today = date.today()
    frame = f'2004-01-01 {today.strftime("%Y-%m-%d")}'

    # cat=31 = programming
    pytrends.build_payload(all_keywords, timeframe=frame, geo='')


    df = pytrends.interest_over_time()
    df.head(20)

    plt.style.use('dark_background')
    plt.figure().patch.set_facecolor('#121212')
    plt.axes().set_facecolor('#080808')

    linewidth = 1
    colors = ['orange', 'teal', 'crimson', 'magenta', 'skyblue']

    for i, x in enumerate(all_keywords):
        plt.plot(df[x], color=colors[i], label=x, linewidth=linewidth)

    plt.legend()
    plt.grid(color='#303030')

    # automatically save the image.
    plt.savefig(f'{"_".join(x for x in all_keywords)}.png', dpi=120)

    plt.show()


def start():
    parser = argparse.ArgumentParser(description='Enter term.')
    for item in sys.argv[1:]:
        parser.add_argument(f'{item}', type=str, help='enter a term')

    args = parser.parse_args()
    f()
