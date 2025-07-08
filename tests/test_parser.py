from src.parser import PARSER_REGISTRY

def smoke_test(site_name: str, sample_path: str):
    with open(sample_path, 'r', encoding='utf-8') as f:
        html = f.read()

    parser_cls = PARSER_REGISTRY.get(site_name)
    if not parser_cls:
        print(f"No parser for '{site_name}' registered.")
        return

    parser = parser_cls()
    
    records = parser.parse(html)
    print(f"\n--- {site_name.upper()} parsed {len(records)} items ---")
    for rec in records:
        print(rec)

if __name__ == "__main__":

    # smoke_test("bbc", "samples/bbc_rss.xml")
    smoke_test("techcrunch", "samples/techcrunch_rss.xml")
