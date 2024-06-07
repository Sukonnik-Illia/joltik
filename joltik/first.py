import uuid

from google.ads.googleads.client import GoogleAdsClient

TEST_CLIENT_ID = "2109817288"
TEST_BUDGET = "customers/2109817288/campaignBudgets/13600578687"
TEST_CAMPAIN = "customers/2109817288/campaigns/21306171816"
TEST_AD_GROUP = "customers/2109817288/adGroups/167931131172"


client = GoogleAdsClient.load_from_storage("ref-token.json")
customer_service = client.get_service("CustomerService")

# accessible_customers = customer_service.list_accessible_customers()
# result_total = len(accessible_customers.resource_names)
# print(f"Total results: {result_total}")


# resource_names = accessible_customers.resource_names
# for resource_name in resource_names:
#     print(f'Customer resource name: "{resource_name}"')
def create_ad_group(client: str, customer_id: str, campaign_resource_name: str) -> str:
    """
    Creates ad group.

    Args:
    ----
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.
      campaign_resource_name: a campaign resource name.

    Returns:
    -------
      Ad group ID.

    """
    ad_group_service = client.get_service("AdGroupService")

    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create
    ad_group.name = f"Testing RSA via API {uuid.uuid4()}"
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    ad_group.campaign = campaign_resource_name
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD

    # If you want to set up a max CPC bid uncomment line below.
    # ad_group.cpc_bid_micros = 10000000

    # Add the ad group.
    ad_group_response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id,
        operations=[ad_group_operation],
    )
    return ad_group_response.results[0].resource_name


def create_campaign(client: str, customer_id: str, campaign_budget: str) -> str:
    """
    Creates campaign resource.

    Args:
    ----
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.
      campaign_budget: a budget resource name.

    Returns:
    -------
      Campaign resource name.

    """
    campaign_service = client.get_service("CampaignService")
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = f"Testing RSA via API {uuid.uuid4()}"
    campaign.advertising_channel_type = client.enums.AdvertisingChannelTypeEnum.SEARCH

    # Recommendation: Set the campaign to PAUSED when creating it to prevent
    # the ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    # Set the bidding strategy and budget.
    # The bidding strategy for Maximize Clicks is TargetSpend.
    # The target_spend_micros is deprecated so don't put any value.
    # See other bidding strategies you can select in the link below.
    # https://developers.google.com/google-ads/api/reference/rpc/latest/Campaign#campaign_bidding_strategy
    campaign.target_spend.target_spend_micros = 0
    campaign.campaign_budget = campaign_budget

    # Set the campaign network options.
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = True
    campaign.network_settings.target_partner_search_network = False
    # Enable Display Expansion on Search campaigns. For more details see:
    # https://support.google.com/google-ads/answer/7193800
    campaign.network_settings.target_content_network = True

    # # Optional: Set the start date.
    # start_time = datetime.date.today() + datetime.timedelta(days=1)
    # campaign.start_date = datetime.date.strftime(start_time, _DATE_FORMAT)

    # # Optional: Set the end date.
    # end_time = start_time + datetime.timedelta(weeks=4)
    # campaign.end_date = datetime.date.strftime(end_time, _DATE_FORMAT)

    # Add the campaign.
    campaign_response = campaign_service.mutate_campaigns(
        customer_id=customer_id,
        operations=[campaign_operation],
    )
    return campaign_response.results[0].resource_name


def create_campaign_budget(client: str, customer_id: str) -> str:
    """
    Creates campaign budget resource.

    Args:
    ----
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.

    Returns:
    -------
      Campaign budget resource name.

    """
    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Our Super duper Campaign budget {uuid.uuid4()}"
    campaign_budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    campaign_budget.amount_micros = 50000000

    # Add budget.
    campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id,
        operations=[campaign_budget_operation],
    )

    return campaign_budget_response.results[0].resource_name


geo_target_constant_service = client.get_service("GeoTargetConstantService")

# Optional: Specify country code (e.g., 'NL' for Netherlands)
country_code = "NL"
request = geo_target_constant_service.prepare_suggest_geo_target_constants_query()
# Request location resources with correct method
response = geo_target_constant_service.suggest_geo_target_constants(country_code=country_code)
# Access location resources from response.results
# for geo_target_constant in response.results:
#     print(f"Location Resource Name: {geo_target_constant.resource_name}")
