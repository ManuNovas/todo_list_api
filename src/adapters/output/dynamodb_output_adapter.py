class DynamoDBOutputAdapter:
    def _put_item(self, item: dict) -> dict:
        response = self.table.put_item(Item=item)
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            self.logger.error(response)
            raise Exception(response["ResponseMetadata"]["HTTPStatusCode"], "An error ocurred while storing the entity")
        return response
