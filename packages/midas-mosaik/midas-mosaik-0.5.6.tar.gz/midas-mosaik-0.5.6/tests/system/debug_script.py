# import midas
from midas.cli import cli

# from midas.util.runtime_config import RuntimeConfig


def main():

    # RuntimeConfig().load()
    # cli.init_logger(2)
    # midas.run(
    #     "my_second_midas",
    #     params={
    #         "mosaikdb_params": {"filename": "debug.hdf5"},
    #         "with_db": True,
    #     },
    # )
    # midas.run(
    #     scenario_name="demo", config="src/midas/adapter/mango/blackstart.yml"
    # )
    cli.cli(["run", "four_bus"])
    # cli.cli(["-vv", "download", "-w", "-f", "-k"])


if __name__ == "__main__":
    main()
