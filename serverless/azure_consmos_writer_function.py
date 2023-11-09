import azure.functions as func
from azure.cosmosdb.table import TableService

# Initialize the Azure Cosmos DB Table Service
connection_string = "ConnectionString"
table_service = TableService(connection_string=connection_string)


def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        if req_body:
            # Define the table and entity for Cosmos DB
            table_name = "table_name"
            entity = {
                "PartitionKey": req_body["partition_key"],
                "RowKey": req_body["row_key"],
                "Data": req_body["data"]
            }

            # Insert or update the entity in Cosmos DB
            table_service.insert_or_replace_entity(table_name, entity)

            return func.HttpResponse("Data written to Cosmos DB successfully", status_code=200)
        else:
            return func.HttpResponse("Invalid request data", status_code=400)
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
