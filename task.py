"""Demonstrates how to make a simple call to the Natural Language API."""

import argparse
import os
import csv

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def get_sentiment(file):
    """Run a sentiment analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    with open(file, 'r') as review_file:
        # Instantiates a plain text document.
        content = review_file.read()

    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    annotations = client.analyze_sentiment(document=document)

    # Print the results
    score = annotations.document_sentiment.score
    magnitude = annotations.document_sentiment.magnitude

    return score, magnitude


def get_entities(file):
    """Run a entity analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    with open(file, 'r') as review_file:
        # Instantiates a plain text document.
        content = review_file.read()

    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    entities = client.analyze_entities(document=document).entities
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

    entity_list = []
    entities = sorted(entities, key=lambda x: x.salience, reverse=True)
    for entity in entities[:5]:
        entity_list.append(entity.name)
        entity_list.append(entity_type[entity.type])
        entity_list.append(entity.salience)
    return entity_list

def get_categories(file):
    """Run a entity analysis request on text within a passed filename."""
    client = language.LanguageServiceClient()

    with open(file, 'r') as review_file:
        # Instantiates a plain text document.
        content = review_file.read()

    document = types.Document(
        content=content,
        type=enums.Document.Type.PLAIN_TEXT)
    categories = client.classify_text(document=document).categories

    category_list = []
    categories = sorted(categories, key=lambda x: x.confidence, reverse=True)
    for category in categories[:1]:
        category_list.append(category.name)
        category_list.append(category.confidence)
    return category_list



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--folder',default='data',type=str,required=False)
    parser.add_argument('--sentiment',default=False,action='store_true',required=False)
    parser.add_argument('--categories',default=False,action='store_true',required=False)
    parser.add_argument('--entities',default=False,action='store_true',required=False)
    args = parser.parse_args()
    
    
    header = []
    if args.sentiment == True:
        header.extend(['filename', 'sentiment_scsore', 'sentiment_label', 'sentiment_magnitude'])
    if args.categories == True:
        header.extend(['category_name', 'category_confidence'])
    if args.entities == True:
        header.extend(['entity_1_name' ,'entity_1_type', 'entity_1_salience',
            'entity_2_name' ,'entity_2_type', 'entity_2_salience',
            'entity_3_name' ,'entity_3_type', 'entity_3_salience',
            'entity_4_name' ,'entity_4_type', 'entity_4_salience',
            'entity_5_name' ,'entity_5_type', 'entity_5_salience'])

    with open('results.csv','w') as out_file:
        writer=csv.writer(out_file, delimiter='\t',lineterminator='\n')
        writer.writerow(tuple(header))
        
        for filename in os.listdir(args.folder):
            results = []
            print(filename)
            filepath = args.folder + '/' + filename
            results.append(filename)
            if args.sentiment == True:
                score, magnitude = get_sentiment(filepath)
                results.append(score)
                if score < -0.25:
                    label = 'Negative'
                if score > -0.25:
                    label = 'Neutral'
                if score > 0.25:
                    label = 'Positive'
                results.append(label)
                results.append(magnitude)
            if args.categories == True:
                categories = get_categories(filepath)
                results.extend(categories)
            if args.entities == True:
                entities = get_entities(filepath)
                results.extend(entities)

            writer.writerow(tuple(results))
