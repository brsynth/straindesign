from cameobrs.flux_analysis.analysis import phenotypic_phase_plane
from cameobrs.visualization.plotting.with_plotly import PlotlyPlotter
from cameobrs.visualization.plotting.with_seaborn import SeabornPlotter

pplotter = PlotlyPlotter()
splotter = SeabornPlotter()


def test_ppp_plotly(model):
    """Test if at least it doesn't raise an exception."""
    production_envelope = phenotypic_phase_plane(
        model,
        variables=[model.reactions.Biomass_Ecoli_core_N_lp_w_fsh_GAM_rp__Nmet2],
        objective=model.metabolites.succ_e,
    )
    # pass a grid argument so that it doesn't open a browser tab
    production_envelope.plot(pplotter, height=400, grid=[])


def test_ppp_seaborn(model):
    """Test if at least it doesn't raise an exception."""
    production_envelope = phenotypic_phase_plane(
        model,
        variables=[model.reactions.Biomass_Ecoli_core_N_lp_w_fsh_GAM_rp__Nmet2],
        objective=model.metabolites.succ_e,
    )
    # pass a grid argument so that it doesn't open a browser tab
    production_envelope.plot(splotter, height=400, grid=[])
