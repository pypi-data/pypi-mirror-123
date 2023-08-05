import unittest
import tempfile

import pytest

import numpy as np

from numpy.testing import assert_array_equal
from transformers import AutoTokenizer

from small_text.active_learner import PoolBasedActiveLearner
from small_text.integrations.pytorch.exceptions import PytorchNotFoundError
from small_text.query_strategies import RandomSampling

from sklearn.datasets import fetch_20newsgroups

from small_text.integrations.transformers import TransformersDataset
from tests.utils.object_factory import get_initialized_active_learner

try:
    import torch
    from small_text.integrations.transformers import TransformerModelArguments
    from small_text.integrations.transformers.classifiers import TransformerBasedClassificationFactory
except (ImportError, PytorchNotFoundError):
    pass


@pytest.mark.pytorch
class SerializationTest(unittest.TestCase):

    def test_and_load_with_file_str(self):
        train = fetch_20newsgroups(subset='train')
        train_x = train.data[:20]
        train_y = np.random.randint(0, 2, size=20)

        tokenizer = AutoTokenizer.from_pretrained('sshleifer/tiny-distilroberta-base')

        data = []
        for i, doc in enumerate(train_x):
            encoded_dict = tokenizer.encode_plus(
                doc,
                add_special_tokens=True,
                max_length=20,
                padding=True,
                return_attention_mask=True,
                return_tensors='pt',
                truncation='longest_first'
            )

            data.append((encoded_dict['input_ids'], encoded_dict['attention_mask'], train_y[i]))

        dataset = TransformersDataset(data)
        # TODO: reconsider if this makes sense
        # self.assertFalse(dataset.x[TransformersDataset.INDEX_TEXT].is_cuda)
        clf_factory = TransformerBasedClassificationFactory(TransformerModelArguments('sshleifer/tiny-distilroberta-base'),
                                                            kwargs={'num_classes': 2, 'device': 'cuda'})
        query_strategy = RandomSampling()

        with tempfile.TemporaryDirectory() as tmp_dir_name:
            file_str = tmp_dir_name + 'active_learner.ser'

            active_learner = get_initialized_active_learner(clf_factory, query_strategy, dataset)
            ind_initial = active_learner.x_indices_labeled
            ind = active_learner.query(num_samples=5)

            self.assertTrue(next(active_learner.classifier.model.parameters()).is_cuda)
 
            active_learner.update(np.random.randint(2, size=5))
            weights_before = list(active_learner.classifier.model.parameters())

            active_learner.save(file_str)
            del active_learner

            active_learner = PoolBasedActiveLearner.load(file_str)
            self.assertIsNotNone(active_learner)
            assert_array_equal(np.concatenate([ind_initial, ind]), active_learner.x_indices_labeled)

            weights_after = list(active_learner.classifier.model.parameters())
            self.assertEqual(len(weights_before), len(weights_after))
            for i in range(len(weights_before)):
                assert_array_equal(weights_before[i].cpu().detach().numpy(), weights_after[i].cpu().detach().numpy())

            self.assertIsNotNone(active_learner.classifier)
            self.assertEqual(query_strategy.__class__, active_learner.query_strategy.__class__)
