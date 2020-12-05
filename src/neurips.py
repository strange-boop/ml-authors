from collections import defaultdict as ddict
from src.unis import unis


def read_neurips_papers(filename='neurips_2020_accepted.txt'):
    papers = ddict(list)
    authors = ddict(list)
    affiliations = ddict(set)
    author2affiliation = ddict(list)
    paper2authors = ddict(set)
    paper2affiliations = ddict(set)
    with open(filename, encoding="utf8") as f:
        while True:
            paper_title = next(f)
            paper_authors = next(f)

            if len(paper_authors) < 10:
                print(paper_title)
                break

            author_splitted = paper_authors.split('·')
            paper2authors[paper_title] = author_splitted

            for author in author_splitted:
                full_name = author[:author.rfind("(")].strip()
                # full_name = author.strip()

                affiliation = author[author.rfind("(") + 1:author.rfind(")")]

                if affiliation in unis:
                    affiliation = unis[affiliation]
                for sep in [',', ' and', ' &', '/', '+', ';', ')']:
                    if not (
                        sep == ',' and 'university of california' in affiliation.lower()):
                        affiliation = affiliation.split(sep)[0]

                paper2affiliations[paper_title].add(affiliation)

                papers[paper_title.strip()].append(full_name)
                authors[full_name.strip()].append(paper_title)
                affiliations[affiliation.strip()].add(paper_title)
                author2affiliation[full_name.strip()].append(affiliation)
            try:
                next(f)
            except StopIteration:
                return papers, authors, affiliations, author2affiliation, paper2authors, paper2affiliations