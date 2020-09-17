shipstation = dict(
    API_Key="",
    API_Secret="",
    orders_endpoint="https://ssapi.shipstation.com/orders?orderStatus=awaiting_shipment",
    tag_endpoint="https://ssapi.shipstation.com/orders/addtag",
    # Safe shipping timeframe in hours
    ship_timeframe=48,
    # Tag ID for the urgent tag
    tag_id="103434",
)

todoist = dict(
    token="",
    tasks_endpoint="https://api.todoist.com/rest/v1/tasks",
    project_id="",
)
