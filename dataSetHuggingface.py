from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import JSONResponse
from datasets import load_dataset_builder

app = FastAPI()

class DatasetInfoFetcher:
    def __init__(self, dataset_name, config_name=None):
        self.dataset_name = dataset_name
        self.config_name = config_name

    def fetch_info(self):
        try:
            print(self.dataset_name, self.config_name)
            builder = load_dataset_builder(self.dataset_name, self.config_name)
            return builder.info
        except ValueError as e:
            if "Config name is missing" in str(e):
                raise HTTPException(status_code=400, detail=f"Error: Dataset '{self.dataset_name}' requires a configuration to be specified.")
            else:
                raise HTTPException(status_code=500, detail=str(e))

@app.post("/fetch_info")
async def fetch_info(request_body: dict):
    dataset_name = request_body.get("dataset_name")
    print(dataset_name)

    config_name = request_body.get("config_name", "")
    print(config_name)
    
    if dataset_name is None:
        raise HTTPException(status_code=400, detail="Error: 'dataset_name' is required.")
    
    print(f"Received request with dataset_name: {dataset_name}, config_name: {config_name}")
    info_fetcher = DatasetInfoFetcher(dataset_name, config_name)
    try:
        info = info_fetcher.fetch_info()
        dataset_info = {
            "datasetName": dataset_name,
            "datasetSize": info.dataset_size,
            "datasetSizeMb": info.dataset_size / (1024 * 1024),
            "features": info.features
        }
        return dataset_info
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)
