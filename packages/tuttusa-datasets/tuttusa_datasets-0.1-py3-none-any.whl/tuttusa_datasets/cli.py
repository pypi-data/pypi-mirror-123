"""Console script for tuttusa_datasets."""

import fire


def help():
    print("tuttusa_datasets")
    print("=" * len("tuttusa_datasets"))
    print("Datasets to be used to evaluate fairness")


def main():
    fire.Fire({
        "help": help
    })

# if __name__ == "__main__":
#     main() # pragma: no cover
