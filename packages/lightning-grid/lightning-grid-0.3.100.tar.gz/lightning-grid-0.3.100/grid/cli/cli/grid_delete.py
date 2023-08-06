import asyncio
from typing import List

import click
from grpc.aio import AioRpcError

from grid.cli import rich_click
from grid.cli.client import Grid
from grid.protos.grid.v1.cluster_pb2 import Cluster
from grid.protos.grid.v1.cluster_service_pb2 import DeleteClusterRequest
from grid.protos.grid.v1.cluster_service_pb2_grpc import ClusterServiceStub
from grid.protos.grid.v1.metadata_pb2 import Metadata


@rich_click.group()
def delete() -> None:
    """Allows you to delete grid resources."""
    pass


def doublecheck(item: str):
    warning_str = click.style('WARNING!', fg='red')
    message = f"""

    {warning_str}

    Your are about to delete the {item}.
    This will delete all the associated artifacts, logs, and metadata.

    Are you sure you want to do this?

   """
    click.confirm(message, abort=True)


@delete.command()
@rich_click.argument('experiment_ids', type=str, required=True, nargs=-1, help='Experiment IDs to delete.')
def experiment(experiment_ids: List[str]):
    """Delete some set of EXPERIMENT_IDS from grid.

    This process is immediate and irriversable, deletion permenantly removes not only
    the record of the experiment, but all associated artifacts, metrics, logs, etc.
    """
    doublecheck(experiment_ids)
    client = Grid()
    for experiment in experiment_ids:
        client.delete(experiment_name=experiment)


@delete.command()
@rich_click.argument('run_ids', type=str, required=True, nargs=-1, help='Run IDs to delete.')
def run(run_ids: List[str]):
    """Delete some set of RUN_IDS from grid.

    Deleting a run also deletes all experiments contained within the run.

    This process is immediate and irriversable, deletion permenantly removes not only
    the record of the run, but all associated experiments, artifacts, metrics, logs, etc.
    """
    doublecheck(run_ids)
    client = Grid()
    for run in run_ids:
        client.delete(run_name=run)


@delete.command()
@rich_click.argument('cluster', type=str, help='Cluster id to delete.')
def cluster(cluster: str):
    """Delete CLUSTER and all associated AWS resources.

    Deleting a run also deletes all Runs and Experiments which were started
    on the cluster. deletion permenantly removes not only the record of all
    runs on a cluster, but all associated experiments, artifacts, metrics, logs, etc.

    This process may take a few minutes to complete, but once started is irriversable.
    Deletion permenantly removes not only cluster from being managed by grid, but tears
    down every resource grid managed (for that cluster id) in the host cloud. All object
    stores, container registries, logs, compute nodes, volumes, etc. are deleted and
    cannot be recovered.
    """
    async def f():
        async with Grid.grpc_channel() as conn:
            await ClusterServiceStub(conn).DeleteCluster(
                DeleteClusterRequest(cluster=Cluster(metadata=Metadata(id=cluster, )))
            )

    try:
        asyncio.run(f())
    except AioRpcError as e:
        raise click.ClickException(f"cluster {cluster}: {e.details()}")
