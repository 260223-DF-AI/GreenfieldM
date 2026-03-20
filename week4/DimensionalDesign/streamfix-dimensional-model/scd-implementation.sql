-- StreamFlix Dimensional Model - DDL for Dimension Tables
-- SCD (Slowly Changing Dimension) Implementation

-- ============================================================================
-- 1. DimDate (Type 0 - No changes after load)
-- ============================================================================
CREATE TABLE dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    day_of_week INT,
    day_name VARCHAR(10),
    day_of_month INT,
    day_of_year INT,
    week_of_year INT,
    month_number INT,
    month_name VARCHAR(10),
    quarter_number INT,
    year_number INT,
    is_weekend BIT,
    is_holiday BIT,
    created_at DATETIME DEFAULT GETDATE()
);

-- ============================================================================
-- 2. DimUser (Type 2 SCD - Track account changes)
-- ============================================================================
CREATE TABLE dim_user (
    user_key INT PRIMARY KEY IDENTITY(1,1),
    user_id VARCHAR(50) NOT NULL,
    username VARCHAR(100),
    email VARCHAR(100),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    birth_year INT,
    gender VARCHAR(20),
    signup_date DATE,
    account_status VARCHAR(30),
    marketing_opt_in BIT,
    household_size INT,
    preferred_language VARCHAR(10),
    profile_count INT,
    country_code VARCHAR(5),
    region_name VARCHAR(100),
    city_name VARCHAR(100),
    -- SCD Type 2 columns
    dw_effective_date DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    dw_end_date DATE,
    is_current BIT NOT NULL DEFAULT 1,
    dw_created_at DATETIME DEFAULT GETDATE()
);

-- ============================================================================
-- 3. DimContent (Type 2 SCD - Track metadata changes)
-- ============================================================================
CREATE TABLE dim_content (
    content_key INT PRIMARY KEY IDENTITY(1,1),
    content_id VARCHAR(50) NOT NULL,
    title VARCHAR(255),
    original_title VARCHAR(255),
    content_type VARCHAR(30),
    genre VARCHAR(50),
    subgenre VARCHAR(50),
    release_date DATE,
    release_year INT,
    age_rating VARCHAR(10),
    language VARCHAR(10),
    country_of_origin VARCHAR(5),
    studio_name VARCHAR(100),
    franchise_name VARCHAR(100),
    season_number INT,
    episode_number INT,
    runtime_minutes INT,
    content_status VARCHAR(30),
    -- SCD Type 2 columns
    dw_effective_date DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    dw_end_date DATE,
    is_current BIT NOT NULL DEFAULT 1,
    dw_created_at DATETIME DEFAULT GETDATE()
);

-- ============================================================================
-- 4. DimDevice (Type 2 SCD - Track OS/app version changes)
-- ============================================================================
CREATE TABLE dim_device (
    device_key INT PRIMARY KEY IDENTITY(1,1),
    device_id VARCHAR(50) NOT NULL,
    device_type VARCHAR(50),
    manufacturer VARCHAR(100),
    model_name VARCHAR(100),
    operating_system VARCHAR(50),
    os_version VARCHAR(50),
    app_version VARCHAR(50),
    browser_name VARCHAR(50),
    browser_version VARCHAR(50),
    screen_resolution VARCHAR(30),
    hdr_supported_flag BIT,
    max_supported_quality VARCHAR(20),
    input_method VARCHAR(50),
    smart_tv_flag BIT,
    -- SCD Type 2 columns
    dw_effective_date DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    dw_end_date DATE,
    is_current BIT NOT NULL DEFAULT 1,
    dw_created_at DATETIME DEFAULT GETDATE()
);

-- ============================================================================
-- 5. DimSubscriptionPlan (Type 2 SCD - Track pricing/feature changes)
-- ============================================================================
CREATE TABLE dim_subscription_plan (
    subscription_plan_key INT PRIMARY KEY IDENTITY(1,1),
    plan_id VARCHAR(50) NOT NULL,
    plan_name VARCHAR(100),
    billing_cycle VARCHAR(20),
    plan_tier VARCHAR(30),
    price_usd DECIMAL(10, 2),
    discount_value DECIMAL(10, 2),
    max_streams INT,
    ad_supported_flag BIT,
    offline_download_flag BIT,
    max_resolution VARCHAR(20),
    family_sharing_flag BIT,
    trial_available_flag BIT,
    plan_status VARCHAR(30),
    -- SCD Type 2 columns
    dw_effective_date DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    dw_end_date DATE,
    is_current BIT NOT NULL DEFAULT 1,
    dw_created_at DATETIME DEFAULT GETDATE()
);

-- ============================================================================
-- 6. DimGeography (Type 0/1/2 Mixed SCD)
-- ============================================================================
CREATE TABLE dim_geography (
    geography_key INT PRIMARY KEY IDENTITY(1,1),
    geo_code VARCHAR(20) NOT NULL UNIQUE,
    country_code VARCHAR(5),
    country_name VARCHAR(100),
    region_name VARCHAR(100),
    state_province VARCHAR(100),
    metro_area VARCHAR(100),
    city_name VARCHAR(100),
    postal_code VARCHAR(20),
    timezone_name VARCHAR(50),
    currency_code VARCHAR(5),
    market_region VARCHAR(50),
    content_region_group VARCHAR(50),
    -- SCD Type 1/2 columns
    dw_effective_date DATE NOT NULL DEFAULT CAST(GETDATE() AS DATE),
    dw_end_date DATE,
    is_current BIT NOT NULL DEFAULT 1,
    dw_created_at DATETIME DEFAULT GETDATE()
);

-- ============================================================================
-- 7. DimPaymentMethod (Type 1 SCD)
-- ============================================================================
CREATE TABLE dim_payment_method (
    payment_method_key INT PRIMARY KEY IDENTITY(1,1),
    payment_method_id VARCHAR(50) NOT NULL UNIQUE,
    payment_type VARCHAR(30),
    card_brand VARCHAR(50),
    issuer_name VARCHAR(100),
    wallet_provider VARCHAR(50),
    prepaid_flag BIT,
    country_code VARCHAR(5),
    expiration_month INT,
    expiration_year INT,
    funding_type VARCHAR(30),
    tokenized_flag BIT,
    dw_created_at DATETIME DEFAULT GETDATE(),
    dw_updated_at DATETIME DEFAULT GETDATE()
);

-- ============================================================================
-- 8. DimNetwork (Type 1 SCD with optional Type 2)
-- ============================================================================
CREATE TABLE dim_network (
    network_key INT PRIMARY KEY IDENTITY(1,1),
    network_profile_id VARCHAR(50) NOT NULL UNIQUE,
    connection_type VARCHAR(30),
    isp_name VARCHAR(100),
    carrier_name VARCHAR(100),
    wifi_flag BIT,
    mobile_flag BIT,
    bandwidth_tier VARCHAR(30),
    latency_band VARCHAR(30),
    packet_loss_band VARCHAR(30),
    region_name VARCHAR(100),
    country_name VARCHAR(100),
    dw_created_at DATETIME DEFAULT GETDATE(),
    dw_updated_at DATETIME DEFAULT GETDATE()
);

-- ============================================================================
-- SAMPLE SCD TYPE 2 MERGE STATEMENT
-- Example: DimDevice keeps history of OS/app version changes
-- ============================================================================

/*
-- This MERGE statement would be used in ETL to handle updates to DimDevice
-- Assuming staging table: stg_device_updates (device_id, device_type, os_version, etc.)

MERGE INTO dim_device tgt
USING stg_device_updates src
ON tgt.device_id = src.device_id AND tgt.is_current = 1
WHEN MATCHED 
    AND (ISNULL(tgt.os_version, '') <> ISNULL(src.os_version, '')
         OR ISNULL(tgt.app_version, '') <> ISNULL(src.app_version, '')
         OR ISNULL(tgt.browser_version, '') <> ISNULL(src.browser_version, ''))
    THEN UPDATE SET 
        tgt.dw_end_date = DATEADD(DAY, -1, CAST(GETDATE() AS DATE)),
        tgt.is_current = 0
WHEN NOT MATCHED BY SOURCE THEN
    INSERT (
        device_id, device_type, manufacturer, model_name, 
        operating_system, os_version, app_version, browser_name, browser_version,
        screen_resolution, hdr_supported_flag, max_supported_quality, 
        input_method, smart_tv_flag,
        dw_effective_date, dw_end_date, is_current
    )
    VALUES (
        src.device_id, src.device_type, src.manufacturer, src.model_name,
        src.operating_system, src.os_version, src.app_version, src.browser_name, src.browser_version,
        src.screen_resolution, src.hdr_supported_flag, src.max_supported_quality,
        src.input_method, src.smart_tv_flag,
        CAST(GETDATE() AS DATE), NULL, 1
    );

-- After MERGE, insert the new version for changed records:

INSERT INTO dim_device (
    device_id, device_type, manufacturer, model_name,
    operating_system, os_version, app_version, browser_name, browser_version,
    screen_resolution, hdr_supported_flag, max_supported_quality,
    input_method, smart_tv_flag,
    dw_effective_date, dw_end_date, is_current
)
SELECT 
    src.device_id, src.device_type, src.manufacturer, src.model_name,
    src.operating_system, src.os_version, src.app_version, src.browser_name, src.browser_version,
    src.screen_resolution, src.hdr_supported_flag, src.max_supported_quality,
    src.input_method, src.smart_tv_flag,
    CAST(GETDATE() AS DATE), NULL, 1
FROM stg_device_updates src
WHERE NOT EXISTS (
    SELECT 1 FROM dim_device tgt 
    WHERE tgt.device_id = src.device_id AND tgt.is_current = 1
);

*/

-- ============================================================================
-- QUERY EXAMPLES FOR TIME-TRAVEL ANALYSIS
-- ============================================================================

/*
-- Find device configuration as of a specific date
SELECT *
FROM dim_device
WHERE device_id = 'DEV-12345'
  AND dw_effective_date <= '2025-06-15'
  AND (dw_end_date IS NULL OR dw_end_date > '2025-06-15');

-- Find all changes to a user's subscription plan
SELECT user_key, plan_tier, price_usd, dw_effective_date, dw_end_date
FROM dim_user
WHERE user_id = 'USER-67890'
ORDER BY dw_effective_date;

-- Get current version of all devices
SELECT * FROM dim_device WHERE is_current = 1;

*/

-- ============================================================================
-- FACT TABLES
-- ============================================================================

-- ============================================================================
-- 1. FactViewingBehavior (Transaction Fact Table)
-- ============================================================================
CREATE TABLE fact_viewing_sessions (
    session_key INT PRIMARY KEY IDENTITY(1,1),
    session_id VARCHAR(50) NOT NULL,
    user_key INT NOT NULL,
    content_key INT NOT NULL,
    device_key INT NOT NULL,
    date_key INT NOT NULL,
    
    -- Dimension references
    FOREIGN KEY (user_key) REFERENCES dim_user(user_key),
    FOREIGN KEY (content_key) REFERENCES dim_content(content_key),
    FOREIGN KEY (device_key) REFERENCES dim_device(device_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    
    -- Additive Measures
    viewing_duration_minutes DECIMAL(10, 2) NOT NULL,
    viewing_duration_seconds INT NOT NULL,
    
    -- Semi-Additive Measures (context only; values fixed per session)
    content_category VARCHAR(50),
    subscription_plan_key INT,
    
    -- Non-Additive Measures (derived in BI layer)
    completion_rate_pct DECIMAL(5, 2),
    watch_percentage INT,
    
    -- Metadata
    session_start_time DATETIME,
    session_end_time DATETIME,
    pause_count INT,
    resume_count INT,
    device_type VARCHAR(50),
    
    -- Load metadata
    dw_insert_date DATETIME DEFAULT GETDATE(),
    dw_update_date DATETIME DEFAULT GETDATE()
);

-- ============================================================================
-- 2. FactSubscriptionRevenue (Periodic Snapshot Fact Table)
-- ============================================================================
CREATE TABLE fact_subscription_payments (
    billing_key INT PRIMARY KEY IDENTITY(1,1),
    billing_id VARCHAR(50) NOT NULL,
    user_key INT NOT NULL,
    subscription_plan_key INT NOT NULL,
    payment_method_key INT NOT NULL,
    geography_key INT NOT NULL,
    date_key INT NOT NULL,
    
    -- Dimension references
    FOREIGN KEY (user_key) REFERENCES dim_user(user_key),
    FOREIGN KEY (subscription_plan_key) REFERENCES dim_subscription_plan(subscription_plan_key),
    FOREIGN KEY (payment_method_key) REFERENCES dim_payment_method(payment_method_key),
    FOREIGN KEY (geography_key) REFERENCES dim_geography(geography_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    
    -- Additive Measures
    amount_paid DECIMAL(15, 2) NOT NULL,
    new_subscriber_flag BIT,
    monthly_subscription_count INT DEFAULT 1,
    payment_method_count INT DEFAULT 1,
    
    -- Semi-Additive Measures (valid within time period)
    active_subscriber_count INT,
    plan_rate DECIMAL(10, 2),
    
    -- Non-Additive Measures
    plan_price_usd DECIMAL(10, 2),
    
    -- Attributes
    plan_status VARCHAR(30),
    plan_tier VARCHAR(30),
    payment_type VARCHAR(30),
    activation_date DATE,
    cancellation_date DATE,
    churn_flag BIT DEFAULT 0,
    
    -- Load metadata
    dw_insert_date DATETIME DEFAULT GETDATE(),
    dw_update_date DATETIME DEFAULT GETDATE()
);

-- ============================================================================
-- 3. FactDeviceQuality (Transaction Fact Table)
-- ============================================================================
CREATE TABLE fact_devices (
    device_event_key INT PRIMARY KEY IDENTITY(1,1),
    device_session_id VARCHAR(50) NOT NULL,
    device_key INT NOT NULL,
    user_key INT NOT NULL,
    network_key INT NOT NULL,
    geography_key INT NOT NULL,
    date_key INT NOT NULL,
    
    -- Dimension references
    FOREIGN KEY (device_key) REFERENCES dim_device(device_key),
    FOREIGN KEY (user_key) REFERENCES dim_user(user_key),
    FOREIGN KEY (network_key) REFERENCES dim_network(network_key),
    FOREIGN KEY (geography_key) REFERENCES dim_geography(geography_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    
    -- Additive Measures
    playback_failure_count INT DEFAULT 0,
    buffering_duration_seconds DECIMAL(10, 2) DEFAULT 0,
    buffer_event_count INT DEFAULT 0,
    playback_event_count INT DEFAULT 1,
    playback_quality_event_count INT DEFAULT 1,
    rebuffer_event_count INT DEFAULT 0,
    dropped_frames_count INT DEFAULT 0,
    session_count INT DEFAULT 1,
    
    -- Semi-Additive Measures
    unique_device_count INT DEFAULT 1,
    device_count_per_user INT DEFAULT 1,
    
    -- Non-Additive Measures (derived)
    playback_failure_rate DECIMAL(5, 4) DEFAULT 0,
    avg_session_duration_seconds DECIMAL(10, 2),
    avg_buffer_duration_sec DECIMAL(10, 2),
    avg_bitrate_kbps DECIMAL(10, 2),
    playback_quality_pct DECIMAL(5, 2),
    abandonment_rate DECIMAL(5, 4) DEFAULT 0,
    
    -- Attributes
    playback_speed DECIMAL(3, 1),
    playback_quality VARCHAR(30),
    device_type VARCHAR(50),
    network_type VARCHAR(30),
    media_file_size INT,
    session_abandonment_flag BIT DEFAULT 0,
    
    -- Load metadata
    dw_insert_date DATETIME DEFAULT GETDATE(),
    dw_update_date DATETIME DEFAULT GETDATE()
);
