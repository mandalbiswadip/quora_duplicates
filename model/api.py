import warnings
warnings.filterwarnings("ignore")

from flask import Flask
from flask_cors import CORS

import tensorflow as tf

from model import Model
from config import Config
from embedding import get_embedding

config = Config()

app = Flask(__name__)

CORS(app)


model = Model()
model.build()
model.restore_session(config.save_dir)


@app.route('/<sentence1>&<sentence2>', methods=['GET'])
def get_if_duplicate(sentence1, sentence2):
    is_duplicate = 0
    try:
        global model
        if sentence1 and sentence2:
            sentence1 = str(sentence1).lower().split()
            sentence2 = str(sentence2).lower().split()
            len1 = len(sentence1)
            len2 = len(sentence2)


            is_duplicate = model.sess.run(
                        model.is_duplicate,
                        feed_dict = model.get_feed_dict(
                                        sentence1,
                                        sentence2,
                                        len1,
                                        len2,
                                        None
                    )
            )

    except Exception as e:
        pass
    return is_duplicate

if __name__=="__main__":
    app.debug = True
    app.run(host='0.0.0.0', threaded=True)