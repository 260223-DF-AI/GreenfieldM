## Dimension Table Definitions - Part 2.2
## 1. DimDate
### Table name 
- 'dim_date'
### Surrogate Key Name
- 'date_key'
### Natural Key
- 'full_date'
### Key Attributes
- full_date
- day_of_week
- day_name
- day_of_month
- day_of_year
- week_of_year
- month_number
- month_name
- quarter_number
- year_number
- is_weekend
- is_holiday
### Hierarchies
- year > quarter > month > day
- year > week > day
### SCD Type
- type 0 for all attributes

--------------------------------

## 2. DimUser
### Table Name
- 'dim_user'
### Surrogate Key Name
- 'user_key'
### Natural Key
- 'user_id'
### Key Attributes
- user_id
- username
- email
- first_name
- last_name
- birth_year
- gender
- signup_date
- account_status
- marketing_opt_in
- household_size
- preferred_language
- profile_count
- country_code
- region_name
- city_name
- effective_date
- end_date
- current_flag
### Hierarchies
- country > region > city
- signup year > signup month
### SCD Type by Attribute
| Attribute | SCD Type |
|----------|----------|
| user_id | 0 |
| username | 1 |
| email | 1 |
| first_name | 1 |
| last_name | 1 |
| birth_year | 0 |
| gender | 2 |
| signup_date | 0 |
| account_status | 2 |
| marketing_opt_in | 2 |
| household_size | 2 |
| preferred_language | 2 |
| profile_count | 2 |
| country_code | 2 |
| region_name | 2 |
| city_name | 2 |

-----------------------------------

## 3. DimContent
### Table Name
- 'dim_content'
### Surrogate Key Name
- 'content_key'
### Natural Key
- 'content_id'
### Key Attributes
- content_id
- title
- original_title
- content_type
- genre
- subgenre
- release_date
- release_year
- age_rating
- language
- country_of_origin
- studio_name
- franchise_name
- season_number
- episode_number
- runtime_minutes
- content_status
- effective_date
- end_date
- current_flag
### Hierarchies
- content type > genre > subgenre
- franchise > season > episode
- release year > release date
### SCD Type by Attributes
| Attribute | SCD Type |
|----------|----------|
| content_id | 0 |
| title | 1 |
| original_title | 1 |
| content_type | 0 |
| genre | 2 |
| subgenre | 2 |
| release_date | 0 |
| release_year | 0 |
| age_rating | 2 |
| language | 2 |
| country_of_origin | 2 |
| studio_name | 2 |
| franchise_name | 2 |
| season_number | 0 |
| episode_number | 0 |
| runtime_minutes | 1 |
| content_status | 2 |

--------------------------------

## 4. DimDevice
### Table Name
- `dim_device`
### Surrogate Key Name
- `device_key`
### Natural Key
- 'device_id`
### Key Attributes
- device_id
- device_type
- manufacturer
- model_name
- operating_system
- os_version
- app_version
- browser_name
- browser_version
- screen_resolution
- hdr_supported_flag
- max_supported_quality
- input_method
- smart_tv_flag
- effective_date
- end_date
- current_flag
### Hierarchies
- Device Type > Manufacturer > Model
- OS > OS Version
- Browser > Browser Version
### SCD Type by Attribute
| Attribute | SCD Type |
|----------|----------|
| device_id | 0 |
| device_type | 0 |
| manufacturer | 0 |
| model_name | 0 |
| operating_system | 2 |
| os_version | 2 |
| app_version | 2 |
| browser_name | 2 |
| browser_version | 2 |
| screen_resolution | 1 |
| hdr_supported_flag | 1 |
| max_supported_quality | 1 |
| input_method | 1 |
| smart_tv_flag | 0 |

-----------------------------

### 5. DimSubscriptionPlan
### Table Name
- `dim_subscription_plan`
### Surrogate Key Name
- `subscription_plan_key`
### Natural Key
- `plan_id`
### Key Attributes
- plan_id
- plan_name
- billing_cycle
- plan_tier
- price_usd
- max_streams
- ad_supported_flag
- offline_download_flag
- max_resolution
- family_sharing_flag
- trial_available_flag
- plan_status
- effective_date
- end_date
- current_flag
### Hierarchies
- plan tier > plan name
- billing cycle > plan name
### SCD Type by Attribute
| Attribute | SCD Type |
|----------|----------|
| plan_id | 0 |
| plan_name | 1 |
| billing_cycle | 2 |
| plan_tier | 2 |
| price_usd | 2 |
| max_streams | 2 |
| ad_supported_flag | 2 |
| offline_download_flag | 2 |
| max_resolution | 2 |
| family_sharing_flag | 2 |
| trial_available_flag | 2 |
| plan_status | 2 |

-----------------------------------------

## 6. DimGeography
### Table Name
- 'dim_geography'
### Surrogate Key Name
- 'geography_key
### Natural Key
- 'geo_code'
### Key Attributes
- geo_code
- country_code
- country_name
- region_name
- state_province
- metro_area
- city_name
- postal_code
- timezone_name
- currency_code
- market_region
- content_region_group
### Hierarchies
- market region > country > state/province > city
- country > region > city
### SCD Type
type 1 for postal adjustments.  type 2 for market_region and content_region_group.  type 0 for country identifiers

-----------------------------------

## 7. DimPaymentMethod
### Table Name
- `dim_payment_method`
### Surrogate Key Name
- `payment_method_key`
### Natural Key
- `payment_method_id`
### Key Attributes
- payment_method_id
- payment_type
- card_brand
- issuer_name
- wallet_provider
- prepaid_flag
- country_code
- expiration_month
- expiration_year
- funding_type
- tokenized_flag
### Hierarchies
- Payment Type > Card Brand
- Country > Issuer
### SCD Type
Type 1 for non-historical corrections, Type 2 for funding_type and wallet_provider if tracking changes matters

----------------------------------------

## 8. DimPromotion
### Table Name
- `dim_promotion`
### Surrogate Key Name
- `promotion_key`
### Natural Key
- `promotion_code`
### Key Attributes
- promotion_code
- promotion_name
- campaign_name
- channel_name
- discount_type
- discount_value
- start_date
- end_date
- target_segment
- region_scope
- active_flag
### Hierarchies
- Campaign > Promotion
- Channel > Campaign > Promotion
### SCD Type
Type 2 for campaign and targeting changes, Type 1 for description fixes

-------------------------------

## 9. DimNetwork

### Table Name
- `dim_network`
### Surrogate Key Name
- `network_key`
### Natural Key
- `network_profile_id`
### Key Attributes
- network_profile_id
- connection_type
- isp_name
- carrier_name
- wifi_flag
- mobile_flag
- bandwidth_tier
- latency_band
- packet_loss_band
- region_name
- country_name
### Hierarchies
- Connection Type > Bandwidth Tier
- Country > Region > ISP/Carrier
### SCD Type
Mostly Type 1, with optional Type 2 for bandwidth_tier or ISP classification changes