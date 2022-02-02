from google.cloud import dataproc


def submit_dataproc_workflow(
    workflow_template_path: list,
    workflow_parameters: dict,
    dataproc_client: dataproc.WorkflowTemplateServiceClient,
) -> bool:
    dataproc_request = dataproc.InstantiateWorkflowTemplateRequest()
    dataproc_request.name = dataproc_client.workflow_template_path(
        *workflow_template_path
    )
    dataproc_request.parameters = workflow_parameters

    response = dataproc_client.instantiate_workflow_template(dataproc_request)

    return response
