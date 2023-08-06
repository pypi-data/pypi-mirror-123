import os
import re
from abc import ABC
from enum import Enum
from functools import lru_cache
from typing import Type, cast

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
    camembert2camembert_shared_finetuned_french_summarization = 'mrm8488/camembert2camembert_shared-finetuned-french-summarization'


class SummarizerParameters(FormatterParameters):
    model: TrfModel = Field(TrfModel.t5_base,
                            description="""Which [Transformers model)(
                            https://huggingface.co/models?pipeline_tag=zero-shot-classification) fine-tuned
                            for Summarization to use, can be one of:<br/>
                            <li>`t5-base`: [Google's T5](https://ai.googleblog.com/2020/02/exploring-transfer-learning-with-t5.html).
                            <li>`distilbart-cnn-12-6`: The BART Model with a language modeling head.
                            <li>`google/pegasus-pubmed`: pegasus model fine-tune pegasus on the Pubmed dataset.
                            <li>`google/pegasus-xsum`: pegasus model fine-tune pegasus on the XSUM dataset.
                            <li>`camembert2camembert_shared-finetuned-french-summarization`: French RoBERTa2RoBERTa (shared) fine-tuned on MLSUM FR for summarization.""")
    min_length: int = Field(30, description="Minimum length of the summary")
    max_length: int = Field(100, description="Maximum length of the summary")


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

        clean_text = re.sub(r"[\n\r]+", "<n>", document.text)
        summary = generate_summary(p, clean_text, min_length=params.min_length, max_length=params.max_length)

        # result = p(clean_text, min_length=params.min_length, max_length=params.max_length)

        # summary = result[0].get('summary_text', document.text).replace("<n>", " ")
        return PlainTextResponse(summary)

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SummarizerParameters


def generate_summary(p: SummarizationPipeline, text, min_length, max_length):
    if 'ForConditionalGeneration' in p.model.__class__.__name__:
        inputs = p.tokenizer([text], padding="max_length", truncation=True, max_length=512, return_tensors="pt")
        input_ids = inputs.input_ids
        attention_mask = inputs.attention_mask
        output = p.model.generate(input_ids, attention_mask=attention_mask, min_length=min_length,
                                  max_length=max_length,
                                  num_beams=4,
                                  length_penalty=2.0,
                                  no_repeat_ngram_size=3)
        summary = p.tokenizer.decode(output[0], skip_special_tokens=True)
    else:
        result = p(text, min_length=min_length, max_length=max_length)
        summary = result[0].get('summary_text', text).replace("<n>", " ")
    return summary


@lru_cache(maxsize=None)
def get_pipeline(model):
    p = pipeline("summarization", model=model.value, tokenizer=AutoTokenizer.from_pretrained(model.value))
    return p
