from parser import PARSER_REGISTRY
import asyncio
import click
import yaml
from fetcher import AsyncFetcher
from transformer import Transformer
from storage import Storage
import os

@click.command()
@click.option("--config", default="config.yaml", help="Path to config file.")
@click.option("--since", default=None, help="Fetch items published since ISO timestamp.")
@click.option("--export", default="sqlite", type=click.Choice(["sqlite", "parquet", "csv"]))

def main(config, since, export):

    config_path = os.path.abspath(config)
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)


    fetcher = AsyncFetcher(cfg['sites'], since)
    raw_items = asyncio.run(fetcher.fetch_all())

    parsed_items = []
    for raw in raw_items:
        site_name = raw["site"]    
        html_or_xml = raw["data"]
        parser_cls = PARSER_REGISTRY.get(site_name)
        if not parser_cls:
            continue 
        parser = parser_cls()
        parsed = parser.parse(html_or_xml)
        parsed_items.extend(parsed)

    transformer = Transformer()
    records = transformer.normalize(parsed_items)


    storage = Storage(cfg['database']['path'])
    storage.save(records, export, filename="data/headlines-latest.csv")


    click.echo(f"Saved {len(records)} records to {export}.")

if __name__ == "__main__":
    main()
