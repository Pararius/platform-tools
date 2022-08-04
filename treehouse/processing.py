from google.cloud import dataproc
import base64


def submit_dataproc_workflow(
    workflow_template_path: list,
    workflow_parameters: dict,
    client: dataproc.WorkflowTemplateServiceClient,
) -> bool:
    dataproc_request = dataproc.InstantiateWorkflowTemplateRequest()
    dataproc_request.name = client.workflow_template_path(*workflow_template_path)
    dataproc_request.parameters = workflow_parameters

    response = client.instantiate_workflow_template(dataproc_request)

    return response


def submit_dataproc_pyspark_batch(
    client: dataproc.BatchControllerClient,
    project_id: str,
    region: str,
    service_account: str,
    job_name: str,
    main_python_file_uri: str,
    python_file_uris: list = [],
    jar_file_uris: list = [],
    args: list() = [],
    enable_bigquery: bool = False,
):

    if enable_bigquery:
        jar_file_uris = ["gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"]

    if len(args) > 0:
        args = [base64.b64encode(arg.encode()) for arg in args]

    batch = dataproc.Batch(
        {
            "pyspark_batch": {
                "main_python_file_uri": main_python_file_uri,
                "python_file_uris": python_file_uris,
                "jar_file_uris": jar_file_uris,
                "args": args,
            },
            "environment_config": {
                "execution_config": {"service_account": service_account}
            },
        }
    )

    response = client.create_batch(
        dataproc.CreateBatchRequest(
            parent=f"projects/{project_id}/locations/{region}",
            batch=batch,
            batch_id=job_name,
        )
    )

    return response
