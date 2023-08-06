import os
import shutil
from abc import ABC, abstractmethod

import numpy as np
import pytest
from sklearn.metrics import mean_squared_error

from neuraxle.base import Identity, ExecutionContext, ForceHandleMixin, StepWithContext, ForceHandleIdentity
from neuraxle.data_container import DataContainer
from neuraxle.metaopt.auto_ml import InMemoryHyperparamsRepository, AutoML, RandomSearchHyperparameterSelectionStrategy, \
    ValidationSplitter, HyperparamsJSONRepository
from neuraxle.metaopt.callbacks import ScoringCallback
from neuraxle.pipeline import Pipeline


class SomeBaseService(ABC):
    @abstractmethod
    def service_method(self, data):
        pass


class SomeService(SomeBaseService):
    def service_method(self, data):
        self.data = data


class SomeStep(ForceHandleIdentity):
    def _will_process(self, data_container: DataContainer, context: ExecutionContext):
        data_container, context = super()._will_process(data_container, context)
        service = context.get_service(SomeBaseService)
        service.service_method(data_container.data_inputs)
        return data_container, context


class RegisterServiceDynamically(ForceHandleIdentity):
    def _will_process(self, data_container: DataContainer, context: ExecutionContext):
        context.register_service(SomeBaseService, SomeService())
        return data_container, context


def test_with_context_should_inject_dependencies_properly(tmpdir):
    data_inputs = np.array([0, 1, 2, 3])
    context = ExecutionContext(root=tmpdir)
    service = SomeService()
    context.set_service_locator({SomeBaseService: service})
    p = Pipeline([
        SomeStep().assert_has_services(SomeBaseService),
        SomeStep().assert_has_services_at_execution(SomeBaseService)
    ]).with_context(context=context)

    p.transform(data_inputs=data_inputs)

    assert np.array_equal(service.data, data_inputs)


def test_with_context_should_fail_at_init_when_services_are_missing(tmpdir):
    context = ExecutionContext(root=tmpdir)
    p = Pipeline([
        SomeStep().assert_has_services(SomeBaseService)
    ]).with_context(context=context)

    data_inputs = np.array([0, 1, 2, 3])
    with pytest.raises(AssertionError) as exception_info:
        p.transform(data_inputs=data_inputs)

    assert 'SomeBaseService dependency missing' in exception_info.value.args[0]


def test_localassert_should_assert_dependencies_properly_at_exec(tmpdir):
    data_inputs = np.array([0, 1, 2, 3])
    context = ExecutionContext(root=tmpdir)
    p = Pipeline([
        RegisterServiceDynamically(),
        SomeStep().assert_has_services_at_execution(SomeBaseService)
    ]).with_context(context=context)

    p.transform(data_inputs=data_inputs)
    service = context.get_service(SomeBaseService)
    assert np.array_equal(service.data, data_inputs)


def test_localassert_should_fail_when_services_are_missing_at_exec(tmpdir):
    context = ExecutionContext(root=tmpdir)
    p = Pipeline([
        SomeStep().assert_has_services_at_execution(SomeBaseService)
    ]).with_context(context=context)
    data_inputs = np.array([0, 1, 2, 3])

    with pytest.raises(AssertionError) as exception_info:
        p.transform(data_inputs=data_inputs)

    assert 'SomeBaseService dependency missing' in exception_info.value.args[0]


def _make_autoML_loop(tmpdir, p: Pipeline):
    hp_repository = HyperparamsJSONRepository(cache_folder=tmpdir)
#    hp_repository = InMemoryHyperparamsRepository(cache_folder=str(tmpdir) + "_hp")
    n_epochs = 1
    return AutoML(
        pipeline=p,
        hyperparams_optimizer=RandomSearchHyperparameterSelectionStrategy(),
        validation_splitter=ValidationSplitter(0.20),
        scoring_callback=ScoringCallback(mean_squared_error, higher_score_is_better=False),
        n_trials=1,
        refit_trial=True,
        epochs=n_epochs,
        hyperparams_repository=hp_repository,
        cache_folder_when_no_handle=str(tmpdir),
        continue_loop_on_error=False
    )

class TestServiceAssertion:

    def _setup(self, tmpdir):
        self.tmpdir = str(tmpdir)
        self.tmpdir_hp = self.tmpdir+"_hp"

    def teardown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)
        shutil.rmtree(self.tmpdir+"_hp", ignore_errors=True)

    def test_step_with_context_saver(self, tmpdir):
        self._setup(tmpdir)
        context = ExecutionContext(root=self.tmpdir)
        service = SomeService()
        pipeline_name = 'testname'
        context.set_service_locator({SomeBaseService: service})
        p = Pipeline([
            SomeStep().assert_has_services(SomeBaseService)
        ]).with_context(context=context)
        p.set_name(pipeline_name)
        p.save(context, full_dump=True)

        p: StepWithContext = ExecutionContext(root=self.tmpdir).load(pipeline_name)
        assert isinstance(p, StepWithContext)

        p: Pipeline = ExecutionContext(root=self.tmpdir).load(os.path.join(pipeline_name, 'Pipeline'))
        assert isinstance(p, Pipeline)


    def test_auto_ml_should_inject_dependencies_properly(self,tmpdir):
        self._setup(tmpdir)
        data_inputs = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        expected_outputs = data_inputs * 2
        p = Pipeline([
            SomeStep().assert_has_services(SomeBaseService),
            SomeStep().assert_has_services_at_execution(SomeBaseService)
        ])
        context = ExecutionContext(root=self.tmpdir)
        service = SomeService()
        context.set_service_locator({SomeBaseService: service})

        auto_ml: AutoML = _make_autoML_loop(self.tmpdir_hp, p)
        auto_ml: StepWithContext = auto_ml.with_context(context=context)
        assert isinstance(auto_ml, StepWithContext)
        auto_ml.fit(data_inputs, expected_outputs)

        assert np.array_equal(service.data, data_inputs)


    def test_auto_ml_should_fail_at_init_when_services_are_missing(self, tmpdir):
        self._setup(tmpdir)
        data_inputs = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        expected_outputs = data_inputs * 2
        p = Pipeline([
            RegisterServiceDynamically(),
            SomeStep().assert_has_services(SomeBaseService),
        ])

        context = ExecutionContext(root=self.tmpdir)

        auto_ml: AutoML = _make_autoML_loop(self.tmpdir_hp, p)
        auto_ml: StepWithContext = auto_ml.with_context(context=context)
        assert isinstance(auto_ml, StepWithContext)

        with pytest.raises(AssertionError) as exception_info:
            auto_ml.fit(data_inputs, expected_outputs)

        assert 'SomeBaseService dependency missing' in exception_info.value.args[0]


    def test_auto_ml_should_fail_at_exec_when_services_are_missing(self, tmpdir):
        self._setup(tmpdir)
        data_inputs = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        expected_outputs = data_inputs * 2
        p = Pipeline([
            SomeStep().assert_has_services_at_execution(SomeBaseService),
        ])
        context = ExecutionContext(root=self.tmpdir)

        auto_ml: AutoML = _make_autoML_loop(self.tmpdir_hp, p)
        auto_ml: StepWithContext = auto_ml.with_context(context=context)
        assert isinstance(auto_ml, StepWithContext)

        with pytest.raises(AssertionError) as exception_info:
            auto_ml.fit(data_inputs, expected_outputs)
        assert 'SomeBaseService dependency missing' in exception_info.value.args[0]


    def test_auto_ml_should_assert_dependecies_properly_at_exec(self, tmpdir):
        self._setup(tmpdir)
        data_inputs = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        expected_outputs = data_inputs * 2
        p = Pipeline([
            RegisterServiceDynamically(),
            SomeStep().assert_has_services_at_execution(SomeBaseService),
        ])
        context = ExecutionContext(root=self.tmpdir)

        auto_ml: AutoML = _make_autoML_loop(self.tmpdir_hp, p)
        auto_ml: StepWithContext = auto_ml.with_context(context=context)
        assert isinstance(auto_ml, StepWithContext)
        auto_ml.fit(data_inputs, expected_outputs)

        service = context.get_service(SomeBaseService)
        assert np.array_equal(service.data, data_inputs)
