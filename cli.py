from src.batch import Job, Scheduler
import json
from argparse import ArgumentParser


def get_args():
    parser = ArgumentParser(description="Classify all SMILES with ClassyFire")
    parser.add_argument("--input", type=str, help="Path to the input file")
    parser.add_argument("--output", type=str, help="Path to the output file")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    with open(args.input) as f:
        data = json.load(f)

    data = [x for x in data if x]

    chunks = [data[i:i+100] for i in range(0, len(data), 100)]

    jobs = [Job(chunk) for chunk in chunks]

    scheduler = Scheduler(jobs)

    scheduler.run()

    with open(args.output, 'w') as f:
        json.dump(scheduler.export(), f)