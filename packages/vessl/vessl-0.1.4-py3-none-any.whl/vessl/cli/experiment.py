from typing import List, Tuple

import click

import vessl
from vessl import read_organization
from vessl.cli._base import VesslGroup, vessl_argument, vessl_option
from vessl.cli._util import (
    Endpoint,
    generic_prompter,
    print_data,
    print_logs,
    print_table,
    print_volume_files,
    prompt_choices,
    truncate_datetime,
)
from vessl.cli.organization import organization_name_option
from vessl.cli.project import project_name_option
from vessl.experiment import (
    create_experiment,
    download_experiment_output_files,
    list_experiment_logs,
    list_experiment_output_files,
    list_experiments,
    read_experiment,
)
from vessl.kernel_cluster import list_cluster_nodes, list_clusters, read_cluster
from vessl.kernel_image import list_kernel_images
from vessl.kernel_resource_spec import list_kernel_resource_specs
from vessl.util.constant import (
    MOUNT_PATH_OUTPUT,
    PROCESSOR_TYPE_GPU,
    PROCESSOR_TYPES,
)


def experiment_name_prompter(
    ctx: click.Context, param: click.Parameter, value: str
) -> str:
    experiments = list_experiments()
    return prompt_choices(
        "Experiment", [(f"{x.name} #{x.number}", x.name) for x in reversed(experiments)]
    )


def cluster_name_prompter(
    ctx: click.Context, param: click.Parameter, value: str
) -> str:
    clusters = list_clusters()
    if not vessl.vessl_api.organization.is_managed_cluster_enabled:
        clusters = filter(lambda x: not x.is_savvihub_managed, clusters)

    cluster = prompt_choices(
        "Cluster",
        [(f"{x.name}", x) for x in clusters],
    )
    ctx.obj["cluster"] = cluster
    return cluster.name


def cluster_name_callback(
    ctx: click.Context, param: click.Parameter, value: str
) -> str:
    if "cluster" not in ctx.obj:
        ctx.obj["cluster"] = read_cluster(value)
    return value


def resource_name_prompter(
    ctx: click.Context, param: click.Parameter, value: str
) -> str:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="cluster (`--cluster`) must first be specified.",
        )

    if cluster.is_savvihub_managed:
        resources = list_kernel_resource_specs()
        resource = prompt_choices("Resource", [(x.name, x) for x in resources])
        ctx.obj["processor_type"] = resource.processor_type
        return resource.name


def processor_type_prompter(
    ctx: click.Context, param: click.Parameter, value: str
) -> str:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="cluster (`--cluster`) must first be specified.",
        )

    if not cluster.is_savvihub_managed:
        processor_type = prompt_choices("Processor Type", PROCESSOR_TYPES)
        ctx.obj["processor_type"] = processor_type
        return processor_type


def cpu_limit_prompter(
    ctx: click.Context, param: click.Parameter, value: float
) -> float:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="cluster (`--cluster`) must first be specified.",
        )

    if not cluster.is_savvihub_managed:
        return click.prompt("CPUs (in vCPU)", type=click.FLOAT)


def memory_limit_prompter(
    ctx: click.Context, param: click.Parameter, value: float
) -> float:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="cluster (`--cluster`) must first be specified.",
        )

    if not cluster.is_savvihub_managed:
        return click.prompt("Memory (e.g. 4Gi)", type=click.STRING)


def gpu_type_prompter(ctx: click.Context, param: click.Parameter, value: str) -> str:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="cluster (`--cluster`) must first be specified.",
        )

    processor_type = ctx.obj.get("processor_type")
    if processor_type is None:
        raise click.UsageError(
            message="Processor type must first be specified.",
        )

    if not cluster.is_savvihub_managed and processor_type == PROCESSOR_TYPE_GPU:
        nodes = list_cluster_nodes(cluster.name)
        return prompt_choices("GPU Type", [x.gpu_product_name for x in nodes])

    return "Empty"


def gpu_limit_prompter(
    ctx: click.Context, param: click.Parameter, value: float
) -> float:
    cluster = ctx.obj.get("cluster")
    if cluster is None:
        raise click.BadOptionUsage(
            option_name="--cluster",
            message="cluster (`--cluster`) must first be specified.",
        )

    processor_type = ctx.obj.get("processor_type")
    if processor_type is None:
        raise click.UsageError(
            message="Processor type must first be specified.",
        )

    if not cluster.is_savvihub_managed and processor_type == PROCESSOR_TYPE_GPU:
        return click.prompt("GPUs (in vGPU)", type=click.FLOAT)


def image_url_prompter(ctx: click.Context, param: click.Parameter, value: str) -> str:
    processor_type = ctx.obj.get("processor_type")
    if processor_type is None:
        raise click.UsageError(
            message="Processor type must first be specified.",
        )

    images = list_kernel_images()
    images = [x for x in images if x.processor_type == processor_type]

    return prompt_choices("Image URL", [x.image_url for x in images])


@click.command(name="experiment", cls=VesslGroup)
def cli():
    pass


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=experiment_name_prompter
)
@organization_name_option
@project_name_option
def read(name: str):
    experiment = read_experiment(experiment_name_or_number=name)
    print_data(
        {
            "ID": experiment.id,
            "Number": experiment.number,
            "Name": experiment.name,
            "Status": experiment.status,
            "Created": truncate_datetime(experiment.created_dt),
            "Message": experiment.message,
            "Source Code": experiment.source_code_link[0].url,
            "Kernel Image": {
                "Name": experiment.kernel_image.name,
                "URL": experiment.kernel_image.image_url,
            },
            "Resource Spec": {
                "Name": experiment.kernel_resource_spec.name,
                "CPU Type": experiment.kernel_resource_spec.cpu_type,
                "CPU Limit": experiment.kernel_resource_spec.cpu_limit,
                "Memory Limit": experiment.kernel_resource_spec.memory_limit,
                "GPU Type": experiment.kernel_resource_spec.gpu_type,
                "GPU Limit": experiment.kernel_resource_spec.gpu_limit,
            },
            "Start command": experiment.start_command,
        }
    )
    print(
        f"For more info: {Endpoint.experiment.format(experiment.organization.name, experiment.project.name, experiment.number)}"
    )


@cli.vessl_command()
@organization_name_option
@project_name_option
def list():
    experiments = list_experiments()
    print_table(
        experiments,
        ["ID", "Number", "Name", "Status", "Created", "Message"],
        lambda x: [
            x.id,
            x.number,
            x.name,
            x.status,
            truncate_datetime(x.created_dt),
            x.message,
        ],
    )


cluster_option = vessl_option(
    "-c",
    "--cluster",
    type=click.STRING,
    required=True,
    prompter=cluster_name_prompter,
    callback=cluster_name_callback,
    help="Must be specified before resource-related options (`--resource`, `--processor`, ...).",
)
command_option = vessl_option(
    "-x",
    "--command",
    type=click.STRING,
    required=True,
    prompter=generic_prompter("Start command"),
    help="Start command to execute in experiment container.",
)
resource_option = vessl_option(
    "-r",
    "--resource",
    type=click.STRING,
    prompter=resource_name_prompter,
    help="Resource type to run experiment (for managed cluster only).",
)
processor_type_option = vessl_option(
    "--processor-type",
    type=click.Choice(("CPU", "GPU")),
    prompter=processor_type_prompter,
    help="CPU or GPU (for custom cluster only).",
)
cpu_limit_option = vessl_option(
    "--cpu-limit",
    type=click.FLOAT,
    prompter=cpu_limit_prompter,
    help="Number of vCPUs (for custom cluster only).",
)
memory_limit_option = vessl_option(
    "--memory-limit",
    type=click.STRING,
    prompter=memory_limit_prompter,
    help="Memory limit (e.g. 4Gi) (for custom cluster only).",
)
gpu_type_option = vessl_option(
    "--gpu-type",
    type=click.STRING,
    prompter=gpu_type_prompter,
    help="GPU type such as Tesla-K80 (for custom cluster only).",
)
gpu_limit_option = vessl_option(
    "--gpu-limit",
    type=click.INT,
    prompter=gpu_limit_prompter,
    help="Number of GPU cores (for custom cluster only).",
)
image_url_option = vessl_option(
    "-i",
    "--image-url",
    type=click.STRING,
    prompter=image_url_prompter,
    help="Kernel docker image URL",
)
message_option = click.option("-m", "--message", type=click.STRING)
termination_protection_option = click.option("--termination-protection", is_flag=True)
env_var_option = click.option(
    "-e",
    "--env-var",
    type=click.STRING,
    multiple=True,
    help="Environment variables. Format: [key]=[value], ex. `--env-var PORT=8080`.",
)
dataset_option = click.option(
    "--dataset",
    type=click.STRING,
    multiple=True,
    help="Dataset mounts. Format: [mount_path]:[dataset_name]@[optional_dataset_version], ex. `--dataset /input:mnist@3bcd5f`.",
)
git_ref_option = click.option(
    "--git-ref",
    type=click.STRING,
    multiple=True,
    help="Git repository mounts. Format: [mount_path]:github/[organization]/[repository]/[optional_commit], ex. `--git-ref /home/vessl/examples:github/savvihub/examples/3cd23dd`.",
)
git_diff_option = click.option(
    "--git-diff",
    type=click.STRING,
    help="Git diff file mounts. Format: [mount_path]:[volume_file_path]]. This option is used only for reproducing existing experiments.",
)
archive_file_option = click.option(
    "--archive-file",
    type=click.STRING,
    help="Local archive file mounts. Format: [mount_path]:[archive_file_path]]. This option is used only for reproducing existing experiments.",
)
root_volume_size_option = click.option("--root-volume-size", type=click.STRING)
working_dir_option = click.option(
    "--working-dir", type=click.STRING, help="Defaults to `/home/vessl/`."
)
output_dir_option = click.option(
    "--output-dir",
    type=click.STRING,
    default=MOUNT_PATH_OUTPUT,
    help="Directory to store experiment output files. Defaults to `/output`.",
)


@cli.vessl_command()
@cluster_option
@command_option
@resource_option
@processor_type_option
@cpu_limit_option
@memory_limit_option
@gpu_type_option
@gpu_limit_option
@image_url_option
@message_option
@termination_protection_option
@env_var_option
@dataset_option
@git_ref_option
@git_diff_option
@archive_file_option
@root_volume_size_option
@working_dir_option
@output_dir_option
@organization_name_option
@project_name_option
def create(
    cluster: str,
    command: str,
    resource: str,
    processor_type: str,
    cpu_limit: float,
    memory_limit: str,
    gpu_type: str,
    gpu_limit: int,
    image_url: str,
    message: str,
    termination_protection: bool,
    env_var: List[str],
    dataset: List[str],
    git_ref: List[str],
    git_diff: str,
    archive_file: str,
    root_volume_size: str,
    working_dir: str,
    output_dir: str,
):
    experiment = create_experiment(
        cluster_name=cluster,
        start_command=command,
        kernel_resource_spec_name=resource,
        processor_type=processor_type,
        cpu_limit=cpu_limit,
        memory_limit=memory_limit,
        gpu_type=gpu_type,
        gpu_limit=gpu_limit,
        kernel_image_url=image_url,
        message=message,
        termination_protection=termination_protection,
        env_vars=env_var,
        dataset_mounts=dataset,
        git_ref_mounts=git_ref,
        git_diff_mount=git_diff,
        archive_file_mount=archive_file,
        root_volume_size=root_volume_size,
        working_dir=working_dir,
        output_dir=output_dir,
    )
    print(
        f"Created '{experiment.name}'.\n"
        f"For more info: {Endpoint.experiment.format(experiment.organization.name, experiment.project.name, experiment.number)}"
    )


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=experiment_name_prompter
)
@click.option(
    "--tail",
    type=click.INT,
    default=200,
    help="Number of lines to display (from the end).",
)
@organization_name_option
@project_name_option
def logs(name: str, tail: int):
    logs = list_experiment_logs(experiment_name=name, tail=tail)
    print_logs(logs)
    print(f"Displayed last {len(logs)} lines of '{name}'.")


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=experiment_name_prompter
)
@click.option("-r", "--recursive", is_flag=True)
@organization_name_option
@project_name_option
def list_output(
    name: str,
    recursive: bool,
):
    files = list_experiment_output_files(
        experiment_name=name,
        need_download_url=False,
        recursive=recursive,
    )
    print_volume_files(files)


@cli.vessl_command()
@vessl_argument(
    "name", type=click.STRING, required=True, prompter=experiment_name_prompter
)
@click.option(
    "-p",
    "--path",
    type=click.Path(),
    default="./output",
    help="Path to store downloads. Defaults to `./output`.",
)
@organization_name_option
@project_name_option
def download_output(name: str, path: str):
    download_experiment_output_files(
        experiment_name=name,
        dest_path=path,
    )
    print(f"Downloaded experiment to {path}.")
