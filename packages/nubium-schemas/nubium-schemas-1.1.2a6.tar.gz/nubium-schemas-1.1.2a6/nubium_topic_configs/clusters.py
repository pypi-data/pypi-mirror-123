from os import environ


def cluster_topic_map():
    campaign_response = environ.get('NUBIUM_CLUSTER_0', '')
    nubium_integrations = environ.get('NUBIUM_CLUSTER_1', '')
    people_stream = environ.get('NUBIUM_CLUSTER_2', '')
    test_cluster = environ.get('TEST_CLUSTER', '')
    dict_out = {
        "PeopleStream_Canon": people_stream,
        "PeopleStream_Canon_Input": people_stream,
        "PeopleStream_CanonTransformers_CreToPeopleStream": campaign_response,
        "PeopleStream_PeopleStreamFromEloqua_ContactRetriever_Timestamps": nubium_integrations,
        "PeopleStream_PeopleStreamFromEloqua_ContactToCanon": people_stream,
        "PeopleStream_PeopleStreamFromEloqua_UnsubscribeRetriever_Timestamps": nubium_integrations,
        "PeopleStream_PeopleStreamFromEloqua_UnsubscribeToCanon": people_stream,
        "PeopleStream_DataWashingMachine_ProcessedRecords": people_stream,
        "PeopleStream_DataWashingMachine_Prewash": people_stream,
        "PeopleStream_DataWashingMachine_DeptJobrolePersona": people_stream,
        "PeopleStream_DataWashingMachine_AddressMsa": people_stream,
        "PeopleStream_DataWashingMachine_Privacy": people_stream,
        "CampaignResponse_Canon": campaign_response,
        "CampaignResponse_Canon_Input": campaign_response,
        "CampaignResponse_CampaignResponseFromEloqua_InquiriesRetriever_Timestamps": nubium_integrations,
        "CampaignResponse_CampaignResponseFromEloqua_InquiriesToCanon": campaign_response,
        "CampaignResponse_CampaignResponseToSalesforce_CampaignMembersToUpsert_FirstTry": campaign_response,
        "CampaignResponse_CampaignResponseToSalesforce_CampaignMembersToUpsert_Retry1": campaign_response,
        "CampaignResponse_CampaignResponseToSalesforce_CampaignMembersToUpsert_Retry2": campaign_response,
        "CampaignResponse_CampaignResponseToSalesforce_CampaignMembersToUpsert_Retry3": campaign_response,
        "CampaignResponse_CampaignResponseToSalesforce_CampaignMembersToUpsert_Failure": campaign_response,
        "NubiumIntegrations_DynamicForm_FormSubmissions": people_stream,
        "NubiumIntegrations_DynamicForm_SpamFilter_CheckEmailAddress": people_stream,
        "NubiumIntegrations_DynamicForm_SpamFilter_CheckVerifyId": people_stream,
        "NubiumIntegrations_DynamicForm_SpamFilter_CheckSubmitId": people_stream,
        "NubiumIntegrations_DynamicForm_SpamPosts": people_stream,
        "NubiumIntegrations_DynamicForm_ErrorPosts": people_stream,
        "NubiumIntegrations_Eloqua_EbbController": nubium_integrations,
        "NubiumIntegrations_Eloqua_EbbWorkerTasks": nubium_integrations,
        "NubiumIntegrations_Eloqua_FormPoster_FromDyFo_FirstTry": nubium_integrations,
        "NubiumIntegrations_Eloqua_FormPoster_FirstTry": nubium_integrations,
        "NubiumIntegrations_Eloqua_FormPoster_Retry1": nubium_integrations,
        "NubiumIntegrations_Eloqua_FormPoster_Retry2": nubium_integrations,
        "NubiumIntegrations_Eloqua_FormPoster_Retry3": nubium_integrations,
        "NubiumIntegrations_Eloqua_FormPoster_Failure": nubium_integrations,
        "NubiumIntegrations_Eloqua_CdoUpdates_FirstTry": campaign_response,
        "NubiumIntegrations_Eloqua_CdoUpdates_Retry1": campaign_response,
        "NubiumIntegrations_Eloqua_CdoUpdates_Retry2": campaign_response,
        "NubiumIntegrations_Eloqua_CdoUpdates_Retry3": campaign_response,
        "NubiumIntegrations_Eloqua_CdoUpdates_Failure": campaign_response,
        "NubiumIntegrations_Eloqua_ContactUpdates_FirstTry": people_stream,
        "NubiumIntegrations_Eloqua_ContactUpdates_Retry1": people_stream,
        "NubiumIntegrations_Eloqua_ContactUpdates_Retry2": people_stream,
        "NubiumIntegrations_Eloqua_ContactUpdates_Retry3": people_stream,
        "NubiumIntegrations_Eloqua_ContactUpdates_Failure": people_stream,
        "NubiumIntegrations_Partner_BulkReceiver_Chunks": nubium_integrations,
        "NubiumIntegrations_Partner_BulkProcessor_Records": nubium_integrations,
        "NubiumIntegrations_Vivastream_ContactsVivastreamRetriever_Timestamps": nubium_integrations,
        "NubiumIntegrations_Vivastream_CdoToFormTransform": people_stream,
        "NubiumIntegrations_UploadWizard_ContactsUploadsMembersRetriever_Timestamps": nubium_integrations,
        "NubiumIntegrations_UploadWizard_CdoToFormTransform": people_stream,
        "PathFactory_PathFactory_DuplicatesFilter": nubium_integrations,
        "PathFactory_PathFactory_DuplicateClosedSessions": nubium_integrations,
        "PathFactory_PathFactory_ClosedSessions_FirstTry": nubium_integrations,
        "PathFactory_PathFactory_ClosedSessions_Retry1": nubium_integrations,
        "PathFactory_PathFactory_ClosedSessions_Retry2": nubium_integrations,
        "PathFactory_PathFactory_ClosedSessions_Failure": nubium_integrations
    }
    if test_cluster:
        dict_out.update({f'{k}__TEST': test_cluster for k in dict_out})
    return dict_out
