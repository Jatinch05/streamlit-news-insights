from src.parser import PARSER_REGISTRY
import asyncio
import click
import yaml
from src.fetcher import AsyncFetcher
from src.transformer import Transformer
from src.storage import Storage

@click.command()
@click.option("--config", default="config.yaml", help="Path to config file.")
@click.option("--since", default=None, help="Fetch items published since ISO timestamp.")
@click.option("--export", default="sqlite", type=click.Choice(["sqlite", "parquet", "csv"]))
def main(config, since, export):
    # Load config
    with open(config) as f:
        cfg = yaml.safe_load(f)

    fetcher = AsyncFetcher(cfg['sites'], since)
    raw_items = asyncio.run(fetcher.fetch_all())

    parsed_items = []
    for raw in raw_items:
        site_name = raw["site"]           # matches the parser key: "bbc_rss", "techcrunch_rss"
        html_or_xml = raw["html"]
        parser_cls = PARSER_REGISTRY.get(site_name)
        if not parser_cls:
            continue  # or log a warning
        parser = parser_cls()
        parsed = parser.parse(html_or_xml)
        parsed_items.extend(parsed)

    transformer = Transformer()
    records = transformer.normalize(parsed_items)


    storage = Storage(cfg['database']['path'])
    storage.save(records, export)

    click.echo(f"Saved {len(records)} records to {export}.")

if __name__ == "__main__":
    main()