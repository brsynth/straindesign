from cameobrs.network_analysis import (
    model_to_network,
    reactions_to_network,
    remove_highly_connected_nodes,
)
from cameobrs.network_analysis.util import distance_based_on_molecular_formula as dbmf


def test_distance_based_on_molecular_formula(salmonella):
    assert (
        dbmf(salmonella.metabolites[0], salmonella.metabolites[0], normalize=False) == 0
    )
    assert (
        dbmf(salmonella.metabolites[0], salmonella.metabolites[0], normalize=True) == 0
    )
    assert (
        dbmf(salmonella.metabolites[0], salmonella.metabolites[1], normalize=False)
        == 47.0
    )
    assert (
        round(
            dbmf(salmonella.metabolites[0], salmonella.metabolites[1], normalize=True),
            2,
        )
        == 0.34
    )


def test_model_to_network(salmonella):
    assert (
        model_to_network(salmonella).edges
        == reactions_to_network(salmonella.reactions).edges
    )
    network = model_to_network(salmonella)
    assert len(network.nodes) == 2384
    assert len(network.edges) == 5967
    network = model_to_network(salmonella, max_distance=1.0)
    # nodes = network.nodes()
    # print(set(nodes).difference(set(core_model_one.metabolites)))
    # print(set(core_model_one.metabolites).difference(set(nodes)))
    assert len(network.nodes) == 2433
    assert len(network.edges) == 16312


def test_remove_highly_connected_nodes(salmonella):
    network = model_to_network(salmonella)
    assert salmonella.metabolites.atp_c in network.nodes()
    assert salmonella.metabolites.adp_c in network.nodes()
    remove_highly_connected_nodes(
        network, max_degree=10, ignore=[salmonella.metabolites.atp_c]
    )
    assert len(network.nodes) == 2268
    assert len(network.edges) == 2691
    assert salmonella.metabolites.atp_c in network.nodes()
    assert salmonella.metabolites.adp_c not in network.nodes()
