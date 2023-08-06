import pytest


def pytest_addoption(parser):
    parser.addoption(
        '--branch', action='store', default='master',
        help="The name of the branch to test"
    )
    parser.addoption(
        '--environment', action='store', default='bed-ussouth-db01',
        help="The environment that tests will run against, e.g. bed-ussouth-db01"
    )
    parser.addoption('--formation', action='store', help="A formation ID to run tests against")
    parser.addoption('--namespace', action='store', help="A namespace to run tests against")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Make test results available to fixtures.

    This allows fixtures to add logic based on e.g. test failre. Useful
    especially for finalizers.
    """
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"
    setattr(item, "formation", item.funcargs['formation'])
    setattr(item, "rep_" + rep.when, rep)
