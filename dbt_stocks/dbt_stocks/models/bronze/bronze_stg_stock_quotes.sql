SELECT
    RAW:c::FLOAT              AS current_price,
    RAW:d::FLOAT              AS change_amount,
    RAW:dp::FLOAT             AS change_percent,
    RAW:h::FLOAT              AS day_high,
    RAW:l::FLOAT              AS day_low,
    RAW:o::FLOAT              AS day_open,
    RAW:pc::FLOAT             AS prev_close,
    TO_TIMESTAMP(RAW:t)       AS market_timestamp,
    RAW:symbol::STRING        AS symbol,
    TO_TIMESTAMP(RAW:fetched_at) AS fetched_at,
    LOAD_TS                   AS load_ts
FROM {{ source('raw', 'bronze_stock_quotes_raw') }}