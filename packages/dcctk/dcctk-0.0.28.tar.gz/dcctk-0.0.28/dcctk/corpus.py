import re
from tqdm.auto import trange


class TextBasedCorpus:
    """Corpus object for text-based (text as unit) analysis
    """

    def __init__(self, corpus):
        self.corpus = corpus
        self.path_index = {}
        self.index_path()


    def get_texts(self, pattern, texts_as_str=False, sents_as_str=True):
        texts = {}
        for id in self._list_pattern(pattern):
            text = self.get_text(id, as_str=False)
            if text is None: continue
            if sents_as_str:
                texts[id] = '\n'.join(text)
            else:
                texts[id] = text
        if texts_as_str: 
            return '\n'.join(texts.values())
        return texts
            

    def get_text(self, id, as_str=False):
        idx = self.path_index.get(id, None)
        if idx is None or isinstance(idx, int): 
            return None
        i, j = idx
        text = self.corpus[i]['text'][j].get('c', [])
        if as_str:
            text = '\n'.join(text)
        return text


    def get_meta_by_path(self, id):
        idx = self.path_index.get(id, None)
        if idx is None:
            return {}
        if isinstance(idx, int):
            return self.corpus[idx].get('m', {})
        if isinstance(idx, tuple):
            i, j = idx
            return self.corpus[i]['text'][j].get('m', {})
        return {}


    def list_files(self, pattern, generator=False):
        if generator:
            return self._list_pattern(pattern)
        return list(self._list_pattern(pattern))


    def _list_pattern(self, pattern):
        pattern = re.compile(pattern)
        for k in self.path_index.keys():
            if pattern.search(k):
                yield k


    def index_path(self):
        print("Indexing corpus for text retrival...")
        for i in trange(len(self.corpus)):
            self.path_index[self.corpus[i]['id']] = i
            for j, text in enumerate(self.corpus[i]['text']):
                self.path_index[text['id']] = (i, j)



class IndexedCorpus(TextBasedCorpus):
    """Corpus object for fast concordance search
    """

    def __init__(self, corpus) -> None:
        TextBasedCorpus.__init__(self, corpus)
        self.index = {}
        self.index_corpus()
    

    def get_meta(self, subcorp_idx, text_idx=None, keys:list=None, include_id=True):
        if text_idx is None:
            meta = self.corpus[subcorp_idx]['m']
            if include_id:
                meta['id'] = self.corpus[subcorp_idx]['id']
        else:
            meta = self.corpus[subcorp_idx]['text'][text_idx]['m']
            if include_id:
                meta['id'] = self.corpus[subcorp_idx]['text'][text_idx]['id']
        if keys:
            keys.append('id')
            return { k:meta[k] for k in keys if k in meta }
        return meta


    def index_corpus(self):
        print("Indexing corpus for concordance search...")
        for i in trange(len(self.corpus)):
            for j, text in enumerate(self.corpus[i]['text']):
                for k, sent in enumerate(text['c']):
                    for l, char in enumerate(sent):
                        if char not in self.index:
                            self.index[char] = []
                        self.index[char].append( (i, j, k, l) )

