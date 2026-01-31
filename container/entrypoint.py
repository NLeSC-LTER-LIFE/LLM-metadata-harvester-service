"""
python3 entrypoint.py \
  --api-key sk-xxxx \
  --model-name gemini-2.5-flash-preview-05-20 \
  --url https://stac.ecodatacube.eu/veg_quercus.robur_anv.eml/collection.json?.language=en \
  --dump-format json \
  --allow_retrying False
"""
import argparse
import os
import asyncio
import json
import sys
import contextlib
import io
from llm_metadata_harvester.harvester_operations import metadata_harvest
from llm_metadata_harvester.standards import LTER_LIFE_STANDARD


def parse_args():
    parser = argparse.ArgumentParser(description="Metadata Harvester Demo")
    parser.add_argument('--api-key', default=os.getenv("API_KEY"), help='API key for LLM access')
    parser.add_argument('--model-name', default=os.getenv("MODEL_NAME"), help='Model name to use')
    parser.add_argument('--url', default=os.getenv("URL"), help='URL to harvest metadata from')
    parser.add_argument('--dump-format', default='none', choices=['none', 'json', 'yaml'], help='Output format')
    parser.add_argument('--allow_retrying', default='False', choices=['True','False'], help='Allow retrying on failure')
    args = parser.parse_args()
    missing = [k for k, v in vars(args).items() if not v]
    if missing:
        parser.error(f"Missing required arguments: {', '.join(missing)}")
    else:
        return args

def string_to_bool(s):
    return s.lower() == 'true'

#NOTE This is predicated on the set of model families/providers 
# supported by metadata_harvest()
async def main(args):
    noisy_stdout = io.StringIO()
    with contextlib.redirect_stdout(noisy_stdout):
        extracted_metadata = await metadata_harvest(
            model_name=args.model_name,
            url=args.url,
            api_key=args.api_key,
            metadata_standard=LTER_LIFE_STANDARD,
            dump_format=args.dump_format,
            allow_retrying=string_to_bool(args.allow_retrying),
        )
    # Send captured prints to stderr
    stderr_output = noisy_stdout.getvalue()
    if stderr_output:
        print(stderr_output, file=sys.stderr, end="")
    print(json.dumps({
        "schema_version":1,
        "metadata":extracted_metadata,
    }))

if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(args))