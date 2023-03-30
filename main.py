# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from ruwordnet import RuWordNet

import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
api = Api(app)

wn = RuWordNet(filename_or_session='venv/Lib/site-packages/ruwordnet/static/ruwordnet.db')

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe("spacy_wordnet", after='tagger')


class FindWordCognates(Resource):

    def post(self):
        """
        Post method that accepts a list of words and returns cognates in json format for russian and english words
        :return: json
        """
        result = {'data': {'word_roots': {}}, 'status': 'ok'}
        try:
            words = request.json['words']
            for word in words:
                synonyms_ru = self.get_synonyms_ru(word)
                synonyms_en = self.get_synonyms_en(word)
                synonyms_union = synonyms_ru.union(synonyms_en)
                result['data']['word_roots'][word] = list(synonyms_union)
        except Exception as e:
            return {'message': str(e), 'status': 'error'}, 400
        return jsonify(result)

    @staticmethod
    def get_synonyms_ru(word):
        """
        Action to get synonyms for russian words, use ruwordnet
        :param word: str
        :return: set
        """
        synonyms = []
        for syn in wn.get_synsets(word):
            for sense in syn.senses:
                synonyms.append(sense.name.lower())
        return set(synonyms)

    @staticmethod
    def get_synonyms_en(word):
        """
        Action to get synonyms for english words, use nltk.wordnet
        :param word: str
        :return: set
        """
        synonyms = []
        token = nlp(word)[0]
        for syn in token._.wordnet.synsets():
            for sense in syn.lemmas():
                synonyms.append(sense.name().replace('_', ' '))
        return set(synonyms)


api.add_resource(FindWordCognates, "/api/v1/word_roots")

if __name__ == "__main__":
    app.run(debug=False)


