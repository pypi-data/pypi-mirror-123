import os
import re
from abc import ABC
from enum import Enum
from functools import lru_cache
from math import floor, ceil
from typing import Type, cast, Union

from pydantic import BaseModel, Field
from pymultirole_plugins.v1.formatter import FormatterParameters, FormatterBase
from pymultirole_plugins.v1.schema import Document
from starlette.responses import Response, PlainTextResponse
from transformers import pipeline, SummarizationPipeline, AutoTokenizer

_home = os.path.expanduser('~')
xdg_cache_home = os.environ.get('XDG_CACHE_HOME') or os.path.join(_home, '.cache')


class TrfModel(str, Enum):
    t5_base = 't5-base'
    distilbart_cnn_12_6 = 'sshleifer/distilbart-cnn-12-6'
    pegasus_xsum = 'google/pegasus-xsum'
    pegasus_pubmed = 'google/pegasus-pubmed'
    pegasus_multi_news = 'google/pegasus-multi_news'
    mt5_multilingual_xlsum = 'csebuetnlp/mT5_multilingual_XLSum'
    camembert2camembert_shared_finetuned_french_summarization = 'mrm8488/camembert2camembert_shared-finetuned-french-summarization'


class SummarizerParameters(FormatterParameters):
    model: TrfModel = Field(TrfModel.mt5_multilingual_xlsum,
                            description="""Which [Transformers model)(
                            https://huggingface.co/models?pipeline_tag=zero-shot-classification) fine-tuned
                            for Summarization to use, can be one of:<br/>
                            <li>`t5-base`: [Google's T5](https://ai.googleblog.com/2020/02/exploring-transfer-learning-with-t5.html).
                            <li>`distilbart-cnn-12-6`: The BART Model with a language modeling head.
                            <li>`google/pegasus-pubmed`: pegasus model fine-tune pegasus on the Pubmed dataset.
                            <li>`google/pegasus-xsum`: pegasus model fine-tune pegasus on the XSUM dataset.
                            <li>`camembert2camembert_shared-finetuned-french-summarization`: French RoBERTa2RoBERTa (shared) fine-tuned on MLSUM FR for summarization.""")
    min_length: Union[int, float] = Field(0.1, description="Minimum length of the summary")
    max_length: Union[int, float] = Field(0.25, description="Maximum length of the summary")


def WHITESPACE_HANDLER(text):
    return re.sub(r"\s+", ' ', re.sub(r"[\n\r]+", "<n>", text.strip()))
    # return re.sub(r"[\n\r]+", "<n>", text.strip())


class SummarizerFormatter(FormatterBase, ABC):
    """[🤗 Transformers](https://huggingface.co/transformers/index.html) Q&A.
    """

    # cache_dir = os.path.join(xdg_cache_home, 'trankit')
    def format(self, document: Document, parameters: FormatterParameters) \
            -> Response:
        params: SummarizerParameters = \
            cast(SummarizerParameters, parameters)
        # Create cached pipeline context with model
        p: SummarizationPipeline = get_pipeline(params.model)

        clean_text = WHITESPACE_HANDLER(document.text)
        summary = generate_summary(p, clean_text, min_length=params.min_length, max_length=params.max_length)
        return PlainTextResponse(summary)

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SummarizerParameters


MAX_LENGTH_BUG = int(floor(10 ** 30 + 1))


def generate_summary(p: SummarizationPipeline, text, min_length, max_length):
    model_max_length = p.tokenizer.model_max_length \
        if (p.tokenizer.model_max_length and p.tokenizer.model_max_length < MAX_LENGTH_BUG) else 512
    inputs = p.tokenizer([text], padding=False, truncation=True,
                         max_length=model_max_length,
                         return_tensors="pt", return_length=True)
    input_ids = inputs.input_ids
    attention_mask = inputs.attention_mask
    input_length = int(inputs.length)
    if isinstance(min_length, float):
        if 0 <= min_length <= 1.0:
            min_length = floor(input_length * min_length)
        else:
            min_length = 0
    if isinstance(max_length, float):
        if 0 <= max_length <= 1.0:
            max_length = ceil(input_length * max_length)
        else:
            max_length = input_length
    output = p.model.generate(input_ids, attention_mask=attention_mask, min_length=min_length,
                              max_length=max_length,
                              num_beams=4,
                              length_penalty=2.0,
                              no_repeat_ngram_size=3)
    summary = p.tokenizer.decode(output[0], skip_special_tokens=True).replace("<n>", " ")
    return summary


@lru_cache(maxsize=None)
def get_pipeline(model):
    p = pipeline("summarization", model=model.value, tokenizer=AutoTokenizer.from_pretrained(model.value))
    return p
