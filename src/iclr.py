import openreview
import pandas as pd
import re
from collections import defaultdict as ddict


def read_iclr_papers():

    paper_URL = 'ICLR.cc/2020/Conference/-/Blind_Submission'
    decision_URL = 'ICLR.cc/2020/Conference/Paper.*/-/Decision'
    review_URL = 'ICLR.cc/2020/Conference/Paper.*/-/Official_Review'

    def get_notes(url):
        client = openreview.Client(baseurl='https://api.openreview.net')
        iterator = openreview.tools.iterget_notes(client, invitation=url)
        notes = ddict(list)
        for i in iterator:
            notes[i.forum].append(i)
        return notes


    papers = get_notes(paper_URL)
    decisions = get_notes(decision_URL)
    reviews = get_notes(review_URL)


    def rate(review):
        return re.findall('\d+', review.content['rating'])[0]


    def merge_info(papers, decisions, reviews):
        seq = []
        for forum in papers:
            paper = papers[forum]
            decision = decisions[forum]
            review = reviews[forum]

            assert len(paper) == 1, 'there are more than 1 paper'
            assert len(decision) == 1, 'there are more than 1 decision'
            p = paper[0]
            title = p.content['title']
            authors = p.content['authors']
            url = "https://openreview.net/forum?id=" + forum
            d = decision[0]
            final_decision = d.content['decision']
            rates = [rate(r) for r in review]
            seq.append([title, authors, url, final_decision, rates])
        df = pd.DataFrame(seq)
        df.columns = ['title', 'authors', 'url', 'decision', 'ratings']
        return df

    iclr_results = merge_info(papers, decisions, reviews)
    return iclr_results

