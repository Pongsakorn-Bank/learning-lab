# Sending Offline Events Using the Conversions API

The Conversions API is Meta’s recommended integration method for sending offline and physical store events to Meta for use in ad measurement, attribution, and targeting. This guide details how to send offline events via a Conversions API direct or partner integration.

### 🚀 Hands-on Tutorial
For a complete Python implementation that fetches data from **BigQuery**, hashes customer data, and sends it to the **Conversion API**, check out our:
👉 **[Conversion API Tutorial Notebook](./conversion_api_tutorial.ipynb)**

## Prerequisites

### Dataset
Offline events sent through the Conversions API must be associated with a dataset. Datasets allow advertisers to connect and manage event data from web, app, store, and business messaging sources.

Datasets can aggregate data from:
- Meta Pixel (website events)
- App Events API (Facebook SDK, MMPs)
- Offline Conversions API (Legacy)
- Messaging Events API

> [!NOTE]
> Linking a dataset to an application is required before sending mobile app events, and only one application can be linked to a single dataset.

To check if a dataset is consolidated and eligible for offline events, make a `GET` call:
`https://graph.facebook.com/v16.0/{ads-pixel-id}/?fields=is_consolidated_container`

### Permissions
- **Direct Integration**: Follow the prerequisites and permissions guide.
- **Partner Integration**: Follow the partner platform instructions.

## Configuration

### 1. Set Up Offline Event Parameters
For offline and store events, the following fields should be shared in the payload:
- **`action_source`**: Must be set to `physical_store`.
- **Required Fields**: All standard Conversions API server event fields must be included.
- **`upload_tag`**: Optional; supported for legacy API users.

#### Customer Information Parameters
| Parameter Name | API Key | Hashing Required |
| :--- | :--- | :--- |
| Email Address(es) | `em` | **YES** |
| Phone Number(s) | `ph` | **YES** |
| Gender | `ge` | **YES** |
| Date of Birth | `db` | **YES** |
| Last Name | `ln` | **YES** |
| First Name | `fn` | **YES** |
| City | `ct` | **YES** |
| US State | `st` | **YES** |
| Zip codes | `zp` | **YES** |
| Country | `country` | **YES** |
| Mobile Advertiser ID | `madid` | No |
| Third-party user id | `external_id` | Highly Recommended |
| Lead Ads ID | `lead_id` | No |

#### Custom Data Parameters
| Parameter | Type | Required? | Description |
| :--- | :--- | :--- | :--- |
| `event_time` | Integer | Required | UNIX timestamp of the event (e.g., `1456870055`). |
| `event_name` | String | Required | E.g., `Purchase`, `Lead`, `ViewContent`. |
| `currency` | String | Required | Three-letter ISO code (Required for `Purchase`). |
| `value` | Double | Required | Value of event (Required for `Purchase`). |
| `store_data` | Dictionary | Optional | Store location data (e.g., `store_page_id`, `store_code`). |
| `contents` | Array | Optional | Required for catalog ads. Includes `id` and `quantity`. |
| `order_id` | String | Optional | Unique ID for the transaction (e.g., Receipt ID). |

### 2. Sending Events
Make a `POST` request to the following endpoint:
`https://graph.facebook.com/{API_VERSION}/{DATASET_ID}/events?access_token={TOKEN}`

#### Example Payload
```bash
curl -X POST \
  -F 'data=[
       {
  "event_name": "Purchase",
  "event_time": 1674000041,
  "user_data": {
    "em": ["309a0a5c3e211326ae75ca18196d301a9bdbd1a882a4d2569511033da23f0abd"],
    "ph": ["254aa248acb47dd654ca3ea53f48c2c26d641d23d7e2e93a1ec56258df7674c4"]
  },
  "custom_data": {
    "currency": "usd",
    "value": 123.45,
    "contents": [{"id": "product123", "quantity": 1}]
  },
  "action_source": "physical_store"
}]' \
  -F 'access_token=<ACCESS_TOKEN>' \
  https://graph.facebook.com/v15.0/<DATASET_ID>/events
```

**Upload Guidelines:**
- **Frequency**: Real-time or daily uploads are recommended.
- **Freshness**: Data should be uploaded within 62 days of conversion.
- **Error Handling**: If an `event_time` is older than 7 days relative to the upload time, the entire request will fail.

### 3. Set Up Deduplication
Offline events are deduplicated against other offline events only. Meta uses two methods:
1. **Order ID Based (Default)**: Uses a combination of `dataset_id`, `event_time`, `event_name`, `item_number`, and `order_id`.
2. **User Based**: Used if `order_id` is missing. Uses the same fields but relies on Customer Information Parameters for matching.

**Key Rule**: The maximum deduplication window is 7 days.