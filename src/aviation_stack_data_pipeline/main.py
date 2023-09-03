import os
import json
import sys
import toml
import logging
from datetime import datetime
from uuid import uuid4

import psycopg2
import pandas as pd

from aviationstack.client import AviationStackApiClient
from aws.s3 import S3
from aws.secrets import Secrets


LOAD_CONFIG_BUCKET: str = "LOAD_CONFIG"
LOAD_CONFIG_FILE: str = "config.toml"
STAGE_BUCKET_NAME: str = "aviation-stack-stage"
DATABASE_CONNECTION_SECRET: str = "database-connection"


class AviationStackDataLoader:
    def __init__(self):
        self.client = AviationStackApiClient(threshold=os.environ.get("THRESHOLD", -1))
        self.config = {}
        self.s3 = S3()
        self.secrets = Secrets()
        self.conn = None

    def connect_to_postgres(self):
        logging.info("Gathering database connection credentials...")
        connection_credentials = self.secrets.get_secret(DATABASE_CONNECTION_SECRET)
        logging.info("Establishing connection to database...")
        self.conn = psycopg2.connect(**connection_credentials)

    def get_config(self):
        logging.info("Gathering config...")
        try:
            config_bytes = self.s3.get(LOAD_CONFIG_BUCKET, LOAD_CONFIG_FILE)
        except Exception:
            logging.error("Failed to load config!")
            sys.quit()

        self.config.update(toml.loads(config_bytes))

    def stage_data(self, data):
        json_data = json.dumps(data)
        logging.info(f"Placing {len(data)} records in stage...")
        self.s3.put(STAGE_BUCKET_NAME, json_data)

    def flatten_data(self, data: list[dict]):
        for record in data:
            yield self.flatten_record(record)

    def flatten_record(self, record: dict) -> dict:
        result = {}
        for key, subtable in record.items():
            if isinstance(subtable, dict):
                for field, value in subtable.items():
                    result[f"{key}_{field}".upper()] = value
            result["flight_date"] = record.get("flight_date")
        return result

    def upload_data(self, data: list[dict], job: str):
        df = pd.DataFrame(data)

        statistics = {
            "ID": str(uuid4()),
            "LOAD_DATETIME": datetime.utcnow(),
            "BYTES": sys.getsizeof(df),
            "ROWS": df.shape[0],
        }
        df["LOAD_STATISTICS_ID"] = statistics["ID"]
        statistics_df = pd.DataFrame(statistics)
        statistics_df.to_sql("STATISTICS", con=self.conn, if_exists="append", index=False)
        df.to_sql(job, con=self.conn, if_exists="append", index=False)
        self.conn.autocommit = True

    def run(self):
        self.connect_to_postgres()
        self.get_config()
        logging.info("Starting jobs...")
        for job in self.config.get("jobs", []):
            logging.info(f"Starting job: {job}...")
            if job.get("icao") is not None:
                for data in self.client.get_all_flights(job.get("icao")):
                    self.stage_data(data)
                    self.upload_data(data, job)
        self.conn.close()


def main():
    AviationStackDataLoader().run()


if __name__ == "__main__":
    main()
