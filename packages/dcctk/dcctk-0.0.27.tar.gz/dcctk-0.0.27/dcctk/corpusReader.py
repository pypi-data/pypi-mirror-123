import json
from pathlib import Path
from .UtilsTextProcess import *


class PlainTextReader:

    def __init__(self, dir_path="data/", ts_meta_filename="time.yaml", text_meta_filename="text_meta.yaml", ts_meta_loader=None, text_meta_loader=None, plain_text_reader=read_text_as_sentences):
        # Attributes
        self.corp_path = Path(dir_path)
        self.corpus = []
        self.text_meta = {}
        self.timestep_meta = {}
        self.plain_text_reader = plain_text_reader
        self.timestep_meta = self.get_meta(self.corp_path / ts_meta_filename, custom_loader=ts_meta_loader)
        self.text_meta = self.get_meta(self.corp_path / text_meta_filename, custom_loader=text_meta_loader)
        self.read_corpus()


    def read_corpus(self):
        for dir_ in sorted(self.corp_path.iterdir()):
            if not dir_.is_dir(): continue
            
            # Construct corpus
            meta = {}
            for k, v in self.timestep_meta.get(dir_.stem, {}).items():
                meta[k] = v
            corpus = {
                'id': dir_.stem,
                'm': meta,
                'text': []
            }

            # Read text
            for fp in dir_.glob("*.txt"):
                text_id, text_meta, text_content = self.read_text(fp)
                text = {
                    'id': text_id,
                    'm': text_meta,
                    'c': list(text_content)  # A list of sentences
                }
                corpus["text"].append(text)

            self.corpus.append(corpus)


    def read_text(self, fp):
        meta = {}
        fp_key = f"{fp.parent.stem}/{fp.name}"
        for k, v in self.text_meta.get(fp_key, {}).items():
            meta[k] = v

        return fp_key, meta, self.plain_text_reader(fp)



    def get_meta(self, fp, custom_loader=None):
        with open(fp, encoding="utf-8") as f:
            if custom_loader:
                return custom_loader()
            elif fp.name.endswith('yaml'):
                import yaml
                return yaml.load(f, Loader=yaml.FullLoader)
            elif fp.name.endswith('json'):
                return json.load(f)




# if __name__ == '__main__':
#     for sent in read_text_as_sentences("data/01/儀禮_喪服.txt"):
#         print(sent)