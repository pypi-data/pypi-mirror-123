import codecs
import csv
import io
import json
from typing import Any

from komolibs.aws.s3.s3_base import S3Base


class Download(S3Base):
    def __init__(self):
        super().__init__()

    def download(self, bucket: str, file_name: str) -> Any:
        try:
            s3_object = self.resource.Object(bucket, file_name)
            data = io.BytesIO()
            s3_object.download_fileobj(data)

            # object is now a bytes string, Converting it to a dict:
            return json.loads(data.getvalue().decode("utf-8"))

        except Exception as e:
            raise e

    def download_csv(self, bucket: str, file_name: str) -> csv.DictReader:
        s3_object = self.client.get_object(Bucket=bucket, Key=file_name)

        return csv.DictReader(codecs.getreader("utf-8")(s3_object["Body"]))
