import easyvvuq as uq
import chaospy as cp
import os
import pytest


@pytest.fixture
def campaign(tmpdir):
    params = {
        "angle": {
            "type": "float",
            "min": 0.0,
            "max": 6.28,
            "default": 0.79},
        "air_resistance": {
            "type": "float",
            "min": 0.0,
            "max": 1.0,
            "default": 0.2},
        "height": {
            "type": "float",
            "min": 0.0,
            "max": 1000.0,
            "default": 1.0},
        "time_step": {
            "type": "float",
            "min": 0.0001,
            "max": 1.0,
            "default": 0.01},
        "gravity": {
            "type": "float",
            "min": 0.0,
            "max": 1000.0,
            "default": 9.8},
        "mass": {
            "type": "float",
            "min": 0.0001,
            "max": 1000.0,
            "default": 1.0},
        "velocity": {
            "type": "float",
            "min": 0.0,
            "max": 1000.0,
            "default": 10.0}
    }
    encoder = uq.encoders.GenericEncoder(
        template_fname='tests/cannonsim/test_input/cannonsim.template',
        delimiter='#',
        target_filename='in.cannon')
    decoder = uq.decoders.SimpleCSV(
        target_filename='output.csv', output_columns=[
            'Dist', 'lastvx', 'lastvy'])
    campaign = uq.Campaign(name='test', work_dir=tmpdir)
    campaign.add_app(name='test', params=params, encoder=encoder, decoder=decoder)
    campaign.set_app('test')
    action = uq.actions.ExecuteLocal("tests/cannonsim/bin/cannonsim in.cannon output.csv")
    stats = uq.analysis.BasicStats(qoi_cols=['Dist', 'lastvx', 'lastvy'])
    # Make a random sampler
    vary = {
        "angle": cp.Uniform(0.0, 1.0),
        "height": cp.Uniform(2.0, 10.0),
        "velocity": cp.Normal(10.0, 1.0),
        "mass": cp.Uniform(5.0, 1.0)
    }
    sampler = uq.sampling.RandomSampler(vary=vary)
    campaign.set_sampler(sampler)
    campaign.draw_samples(num_samples=100)
    campaign.populate_runs_dir()
    campaign.apply_for_each_run_dir(action)
    return campaign


def test_relocate_campaign(campaign, tmpdir):
    runs = campaign.campaign_db.runs()
    runs_dir = campaign.campaign_db.runs_dir()
    for run in runs:
        assert(run[1]['run_dir'].startswith(runs_dir))
    with pytest.raises(RuntimeError):
        campaign.relocate('/test/test')
    campaign.relocate(tmpdir)
    for run in campaign.campaign_db.runs():
        assert(run[1]['run_dir'] == os.path.join(tmpdir, 'runs', run[0]))
