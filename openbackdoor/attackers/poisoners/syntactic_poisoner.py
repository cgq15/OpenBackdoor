from .poisoner import Poisoner
import torch
import torch.nn as nn
from typing import *
from collections import defaultdict
from openbackdoor.utils import logger
import random
import OpenAttack as oa
from tqdm import tqdm


class SyntacticPoisoner(Poisoner):
    r"""
        Poisoner from paper "Hidden Killer: Invisible Textual Backdoor Attacks with Syntactic Trigger"
        <https://arxiv.org/pdf/2105.12400.pdf>

    Args:
        config (`dict`): Configurations.
    """

    def __init__(
            self,
            template_id: Optional[int] = -1,
            **kwargs
    ):
        super().__init__(**kwargs)


        self.scpn = oa.attackers.SCPNAttacker()
        self.template = [self.scpn.templates[template_id]]

        logger.info("Initializing Syntactic poisoner, selected syntax template is {}".
                    format(" ".join(self.template[0])))



    def poison(self, data: list):
        poisoned = []
        logger.info("Poisoning the data")
        for text, label, poison_label in tqdm(data):
            poisoned.append((self.transform(text), self.target_label, 1))
        return poisoned

    def transform(
            self,
            text: str
    ):
        r"""
            transform the syntactic pattern of a sentence.

        Args:
            text (`str`): Sentence to be transfored.
        """
        try:
            paraphrase = self.scpn.gen_paraphrase(text, self.template)[0].strip()
        except Exception:
            logger.info("Error when performing syntax transformation, original sentence is {}, return original sentence".format(text))
            paraphrase = text

        return paraphrase