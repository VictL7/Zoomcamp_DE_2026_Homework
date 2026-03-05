import dlt
import requests

@dlt.resource(name="taxi_trips", write_disposition="replace")
def taxi_trips():
    base_url = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"
    page = 1
    
    while True:
        print(f"Fetching page {page}...")
        response = requests.get(base_url, params={"page": page})
        data = response.json()
        
        if not data:  # Stop on empty page
            print(f"Page {page} is empty, stopping! Total pages: {page-1}")
            break
        
        yield data
        page += 1


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="taxi_pipeline",
        destination="duckdb",
        dataset_name="nyc_taxi_data",
    )
    
    print("🚕 Starting NYC Taxi data load...")
    load_info = pipeline.run(taxi_trips())
    print(load_info)
    print("✅ Complete!")