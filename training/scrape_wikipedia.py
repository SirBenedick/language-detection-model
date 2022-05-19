import argparse
import os
import random
from datetime import datetime
from typing import List
import enum

import pandas
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup


class Language(enum.Enum):
    SPANISH = "es"
    ENGLISH = "en"
    GERMAN = "de"

    def __str__(self):
        return self.value


PAGES = {
    Language.GERMAN: "https://de.wikipedia.org/wiki/Spezial:Zuf%C3%A4llige_Seite",
    Language.ENGLISH: "https://en.wikipedia.org/wiki/Special:Random",
    Language.SPANISH: "https://es.wikipedia.org/wiki/Especial:Aleatoria",
}

def scrape_page(url, min_length=20) -> List[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    content = " ".join(soup.find(id="bodyContent").stripped_strings)
    return [sentence for sentence in content.split(".") if len(sentence) > min_length]


def main():
    default_output_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "data",
        "wiki_scraped_%s.csv" % datetime.now().strftime("%Y-%m-%d.%H:%M:%S"),
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pages", type=int, default=100)
    parser.add_argument(
        "--output",
        "--o",
        default=default_output_path,
    )
    sentences_df = pandas.DataFrame(columns=["labels", "text"])
    args = parser.parse_args()
    for i in tqdm(range(args.pages)):
        language = random.sample(PAGES.keys(), 1)[0]
        sentences = scrape_page(PAGES[language])
        for sentence in sentences:
            sentences_df = sentences_df.append(
                {"labels": language.value, "text": sentence}, ignore_index=True
            )
    print("Store scraped csv to %s" % args.output)
    sentences_df.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
