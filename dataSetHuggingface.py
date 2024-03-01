from datasets import load_dataset_builder

class DatasetInfoFetcher:
    def __init__(self, dataset_name, config_name=None):
        self.dataset_name = dataset_name
        self.config_name = config_name

    def fetch_info(self):
        try:
            builder = load_dataset_builder(self.dataset_name, self.config_name)
            return builder.info
        except ValueError as e:
            if "Config name is missing" in str(e):
                raise ValueError(f"Error: Dataset '{self.dataset_name}' requires a configuration to be specified.")
            else:
                raise e

if __name__ == "__main__":
    dataset_name = 'Open-Orca/SlimOrca-Dedup'
    config_name = '' 

    info_fetcher = DatasetInfoFetcher(dataset_name, config_name)
    try:
        info = info_fetcher.fetch_info()
        print(f"Information for dataset: {dataset_name}")
        size=info.dataset_size
        print(info.dataset_size)
        dataset_size_mb = info.dataset_size / (1024 * 1024)
        print(f"Size of dataset '{dataset_name}': {dataset_size_mb:.2f} MB")
        features=info.features
        print(info.features) 
    except ValueError as e:
        print(e)
