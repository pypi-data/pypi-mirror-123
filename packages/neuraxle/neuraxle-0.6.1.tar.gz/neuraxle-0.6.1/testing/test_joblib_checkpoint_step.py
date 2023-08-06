"""
Tests for joblib checkpoint steps
========================================

..
    Copyright 2019, Neuraxio Inc.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

"""

import os

import joblib
import numpy as np
from py._path.local import LocalPath

from neuraxle.base import ExecutionContext, Identity
from neuraxle.checkpoints import DefaultCheckpoint
from neuraxle.data_container import DataContainer
from neuraxle.hyperparams.space import HyperparameterSamples
from neuraxle.pipeline import ResumablePipeline
from neuraxle.steps.misc import TapeCallbackFunction, TransformCallbackStep, BaseCallbackStep
from testing.steps.test_output_transformer_wrapper import MultiplyBy2OutputTransformer

EXPECTED_TAPE_AFTER_CHECKPOINT = ["2", "3"]

data_inputs = np.array([1, 2])
expected_outputs = np.array([2, 3])
expected_rehashed_data_inputs = ['44f9d6dd8b6ccae571ca04525c3eaffa', '898a67b2f5eeae6393ca4b3162ba8e3d']


class DifferentCallbackStep(BaseCallbackStep):
    def transform(self, data_inputs):
        self._callback(data_inputs)
        return data_inputs


def create_pipeline(tmpdir, joblib_checkpoint_step, tape, hyperparameters=None, different=False, save_pipeline=True):
    if different:
        pipeline = ResumablePipeline(
            steps=[
                ('a',
                 DifferentCallbackStep(tape.callback, ["1"], hyperparams=hyperparameters)),
                ('joblib_checkpoint', joblib_checkpoint_step),
                ('c', TransformCallbackStep(tape.callback, ["2"])),
                ('d', TransformCallbackStep(tape.callback, ["3"]))
            ],
            cache_folder=tmpdir
        )
    else:
        pipeline = ResumablePipeline(
            steps=[
                ('a',
                 TransformCallbackStep(tape.callback, ["1"], hyperparams=hyperparameters)),
                ('joblib_checkpoint', joblib_checkpoint_step),
                ('c', TransformCallbackStep(tape.callback, ["2"])),
                ('d', TransformCallbackStep(tape.callback, ["3"]))
            ], cache_folder=tmpdir
        )
    return pipeline


def test_when_no_hyperparams_should_save_checkpoint_joblib(tmpdir: LocalPath):
    tape = TapeCallbackFunction()
    joblib_checkpoint_step = DefaultCheckpoint()
    pipeline = create_pipeline(tmpdir, joblib_checkpoint_step, tape)

    pipeline, actual_data_inputs = pipeline.fit_transform(data_inputs, expected_outputs)

    actual_tape = tape.get_name_tape()
    assert np.array_equal(actual_data_inputs, data_inputs)
    assert actual_tape == ["1", "2", "3"]
    assert os.path.exists(os.path.join(tmpdir, 'ResumablePipeline', 'joblib_checkpoint', 'di', '0.joblib'))
    assert os.path.exists(os.path.join(tmpdir, 'ResumablePipeline', 'joblib_checkpoint', 'di', '1.joblib'))
    assert os.path.exists(os.path.join(tmpdir, 'ResumablePipeline', 'joblib_checkpoint', 'eo', '0.joblib'))
    assert os.path.exists(os.path.join(tmpdir, 'ResumablePipeline', 'joblib_checkpoint', 'eo', '1.joblib'))


def test_when_hyperparams_should_save_checkpoint_joblib(tmpdir: LocalPath):
    tape = TapeCallbackFunction()
    joblib_checkpoint_step = DefaultCheckpoint()
    pipeline = create_pipeline(tmpdir, joblib_checkpoint_step, tape,
                               HyperparameterSamples({"a__learning_rate": 1}))

    pipeline, actual_data_inputs = pipeline.fit_transform(data_inputs, expected_outputs)

    actual_tape = tape.get_name_tape()
    assert np.array_equal(actual_data_inputs, data_inputs)
    assert actual_tape == ["1", "2", "3"]

    assert os.path.exists(
        os.path.join(tmpdir, 'ResumablePipeline', 'joblib_checkpoint', 'di', '44f9d6dd8b6ccae571ca04525c3eaffa.joblib'))
    assert os.path.exists(
        os.path.join(tmpdir, 'ResumablePipeline', 'joblib_checkpoint', 'di', '898a67b2f5eeae6393ca4b3162ba8e3d.joblib'))
    assert os.path.exists(
        os.path.join(tmpdir, 'ResumablePipeline', 'joblib_checkpoint', 'eo', '44f9d6dd8b6ccae571ca04525c3eaffa.joblib'))
    assert os.path.exists(
        os.path.join(tmpdir, 'ResumablePipeline', 'joblib_checkpoint', 'eo', '898a67b2f5eeae6393ca4b3162ba8e3d.joblib'))


def test_when_no_hyperparams_and_saved_same_pipeline_should_load_checkpoint_joblib(tmpdir: LocalPath):
    # Given
    tape = TapeCallbackFunction()

    # When
    pipeline_save = create_pipeline(
        tmpdir=tmpdir,
        joblib_checkpoint_step=DefaultCheckpoint(),
        tape=TapeCallbackFunction()
    )
    pipeline_save.fit_transform(data_inputs, expected_outputs)

    pipeline_load = create_pipeline(
        tmpdir=tmpdir,
        joblib_checkpoint_step=DefaultCheckpoint(),
        tape=tape
    )
    pipeline_load, actual_data_inputs = pipeline_load.fit_transform(data_inputs, expected_outputs)

    # Then
    actual_tape = tape.get_name_tape()
    assert np.array_equal(actual_data_inputs, data_inputs)
    assert actual_tape == EXPECTED_TAPE_AFTER_CHECKPOINT


def test_when_hyperparams_and_saved_same_pipeline_should_load_checkpoint_joblib(tmpdir: LocalPath):
    # Given
    tape = TapeCallbackFunction()

    # When
    pipeline_save = create_pipeline(
        tmpdir=tmpdir,
        joblib_checkpoint_step=DefaultCheckpoint(),
        tape=TapeCallbackFunction(),
        hyperparameters=HyperparameterSamples({"a__learning_rate": 1})
    )
    pipeline_save.fit_transform(data_inputs, expected_outputs)

    pipeline_load = create_pipeline(
        tmpdir=tmpdir,
        joblib_checkpoint_step=DefaultCheckpoint(),
        tape=tape,
        hyperparameters=HyperparameterSamples({"a__learning_rate": 1})
    )
    pipeline_load, actual_data_inputs = pipeline_load.fit_transform(data_inputs, expected_outputs)

    # Then
    actual_tape = tape.get_name_tape()
    assert np.array_equal(actual_data_inputs, data_inputs)
    assert actual_tape == EXPECTED_TAPE_AFTER_CHECKPOINT


def test_when_hyperparams_and_saved_no_pipeline_should_not_load_checkpoint_joblib(tmpdir: LocalPath):
    # Given
    tape = TapeCallbackFunction()
    joblib_checkpoint_step = DefaultCheckpoint()

    # When
    pipeline_save = create_pipeline(
        tmpdir=tmpdir,
        joblib_checkpoint_step=Identity(),
        tape=TapeCallbackFunction(),
        hyperparameters=HyperparameterSamples({"a__learning_rate": 1}),
        different=True,
        save_pipeline=False
    )
    pipeline_save.fit_transform(data_inputs, expected_outputs)

    pipeline_load = create_pipeline(
        tmpdir=tmpdir,
        joblib_checkpoint_step=joblib_checkpoint_step,
        tape=tape,
        hyperparameters=HyperparameterSamples({"a__learning_rate": 1})
    )
    pipeline_load, actual_data_inputs = pipeline_load.fit_transform(data_inputs, expected_outputs)

    # Then
    actual_tape = tape.get_name_tape()
    assert np.array_equal(actual_data_inputs, data_inputs)
    assert actual_tape == ["1", "2", "3"]


def setup_joblib_checkpoint(current_id, data_input, expected_output, joblib_checkpoint_step):
    file = joblib_checkpoint_step.get_checkpoint_filename_path_for_current_id(current_id)
    joblib.dump((current_id, data_input, expected_output), file)


def create_pipeline_output_transformer(tmpdir):
    return ResumablePipeline([
        ('output_transformer_1', MultiplyBy2OutputTransformer()),
        ('joblib_checkpoint', DefaultCheckpoint()),
        ('output_transformer_2', MultiplyBy2OutputTransformer()),
    ], cache_folder=tmpdir)


def test_joblib_checkpoint_step_should_load_data_container(tmpdir: LocalPath):
    initial_data_inputs = [1, 2]
    initial_expected_outputs = [2, 3]

    create_pipeline_output_transformer(tmpdir).fit_transform(
        data_inputs=initial_data_inputs, expected_outputs=initial_expected_outputs
    )

    actual_data_container = create_pipeline_output_transformer(tmpdir).handle_transform(
        DataContainer(data_inputs=initial_data_inputs, current_ids=[0, 1], expected_outputs=initial_expected_outputs),
        ExecutionContext(tmpdir)
    )

    assert np.array_equal(actual_data_container.data_inputs, [4, 8])
    assert np.array_equal(actual_data_container.expected_outputs, [8, 12])
