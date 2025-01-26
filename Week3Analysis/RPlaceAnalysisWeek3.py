import duckdb
import datetime
import sys
import time


def validate_dates(start_date, end_date):
    """Validate that end_date is after start_date."""
    if start_date >= end_date:
        raise ValueError("End date must be after start date.")


def rank_colors_by_distinct_users(conn, start_date, end_date):
    """Rank colors by the number of distinct users who placed those colors."""
    query = f"""
        SELECT 
            pixel_color_english, 
            COUNT(DISTINCT user_id_int) AS distinct_users
        FROM rplace
        WHERE timestamp >= '{start_date}' AND timestamp < '{end_date}'
        GROUP BY pixel_color_english
        ORDER BY distinct_users DESC
    """
    result = conn.execute(query).fetchall()
    print("\nRanked Colors by Distinct Users:")
    for row in result:
        print(f"{row[0]}: {row[1]} distinct users")


def calculate_average_session_length(conn, start_date, end_date):
    """Calculate the average session length in seconds."""
    query = f"""
        WITH UserSessions AS (
            SELECT 
                user_id_int, 
                timestamp, 
                LEAD(timestamp) OVER (PARTITION BY user_id_int ORDER BY timestamp) AS next_timestamp
            FROM rplace
            WHERE timestamp >= '{start_date}' AND timestamp < '{end_date}'
        ), 
        SessionDiffs AS (
            SELECT 
                user_id_int,
                EXTRACT(EPOCH FROM next_timestamp - timestamp) AS session_diff
            FROM UserSessions
            WHERE next_timestamp IS NOT NULL
        )
        SELECT 
            AVG(session_diff) AS avg_session_length
        FROM SessionDiffs
        WHERE session_diff <= 900  -- Only consider session gaps <= 15 minutes
    """
    result = conn.execute(query).fetchone()
    avg_session_length = result[0] if result else 0
    print("\nAverage Session Length (seconds):", avg_session_length)


def calculate_pixel_placement_percentiles(conn, start_date, end_date):
    """Calculate percentiles for pixel placements by users."""
    query = f"""
        WITH UserPixelCounts AS (
            SELECT 
                user_id_int, 
                COUNT(*) AS pixel_count
            FROM rplace
            WHERE timestamp >= '{start_date}' AND timestamp < '{end_date}'
            GROUP BY user_id_int
        )
        SELECT 
            approx_quantile(pixel_count, 0.5) AS "50th_percentile",
            approx_quantile(pixel_count, 0.75) AS "75th_percentile",
            approx_quantile(pixel_count, 0.9) AS "90th_percentile",
            approx_quantile(pixel_count, 0.99) AS "99th_percentile"
        FROM UserPixelCounts
    """
    result = conn.execute(query).fetchone()
    print("\nPixel Placement Percentiles:")
    print(f"50th Percentile: {result[0]}")
    print(f"75th Percentile: {result[1]}")
    print(f"90th Percentile: {result[2]}")
    print(f"99th Percentile: {result[3]}")


def count_first_time_users(conn, start_date, end_date):
    """Count users placing their first pixel in the timeframe."""
    query = f"""
        WITH FirstPixelTime AS (
            SELECT 
                user_id_int, 
                MIN(timestamp) AS first_pixel_time
            FROM rplace
            GROUP BY user_id_int
        )
        SELECT 
            COUNT(*) AS first_time_users
        FROM FirstPixelTime
        WHERE first_pixel_time >= '{start_date}' AND first_pixel_time < '{end_date}'
    """
    result = conn.execute(query).fetchone()
    first_time_users = result[0] if result else 0
    print("\nNumber of First-Time Users:", first_time_users)


def analyze_rplace_data(parquet_file, start_date, end_date):
    """Analyze r/place data based on the specified timeframe using DuckDB."""
    start_time = time.perf_counter_ns()

    # Connect to DuckDB and create the rplace table
    conn = duckdb.connect()
    conn.execute(f"CREATE TABLE rplace AS SELECT * FROM read_parquet('{parquet_file}')")

    # Perform analyses
    rank_colors_by_distinct_users(conn, start_date, end_date)
    calculate_average_session_length(conn, start_date, end_date)
    calculate_pixel_placement_percentiles(conn, start_date, end_date)
    count_first_time_users(conn, start_date, end_date)

    end_time = time.perf_counter_ns()
    execution_time_ms = (end_time - start_time) // 1_000_000
    print(f"\nExecution Time: {execution_time_ms} ms")

    # Close the connection
    conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <start_date> <end_date>")
        print("Example: python script.py '2022-04-01 12:00:00' '2022-04-01 18:00:00'")
        sys.exit(1)

    start_date = sys.argv[1]
    end_date = sys.argv[2]
    try:
        validate_dates(
            datetime.datetime.fromisoformat(start_date),
            datetime.datetime.fromisoformat(end_date),
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    analyze_rplace_data("./../2022_rplace.parquet", start_date, end_date)
