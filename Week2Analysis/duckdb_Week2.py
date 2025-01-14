import duckdb
import datetime
import time
import sys

def validate_dates(start_date, end_date):
    """Validate that end_date is after start_date."""
    if start_date >= end_date:
        raise ValueError("End date must be after start date.")

def color_pixel_counter(start_date: str, end_date: str):
    """Count the most placed color and pixel in the specified timeframe using SQL."""
    start_time = time.perf_counter_ns()
    
    conn = duckdb.connect()
    conn.execute(f"""
        CREATE TABLE rplace AS
        SELECT * FROM read_csv_auto('C:/Users/Andrew/Documents/CSC369/2022_place_canvas_history.csv')
    """)
    
    common_color_query = f"""
        SELECT pixel_color, COUNT(*) as count
        FROM rplace
        WHERE timestamp >= '{start_date}:00:00'
          AND timestamp < '{end_date}:00:00'
        GROUP BY pixel_color
        ORDER BY count DESC
        LIMIT 1
    """
    common_color_result = conn.execute(common_color_query).fetchone()
    common_color, color_placed = common_color_result if common_color_result else ("N/A", 0)
    
    common_pixel_query = f"""
        SELECT coordinate, COUNT(*) as count
        FROM rplace
        WHERE timestamp >= '{start_date}:00:00'
          AND timestamp < '{end_date}:00:00'
        GROUP BY coordinate
        ORDER BY count DESC
        LIMIT 1
    """
    common_pixel_result = conn.execute(common_pixel_query).fetchone()
    common_pixel, pixel_placed = common_pixel_result if common_pixel_result else ("N/A", 0)
    
    end_time = time.perf_counter_ns()
    execution_time_ms = (end_time - start_time) // 1_000_000 
    
    print(f"Execution Report:")
    print(f"- Timeframe: {start_date} to {end_date}")
    print(f"- Execution Time: {execution_time_ms} ms")
    print(f"- Most Placed Color: {common_color} (Placed {color_placed} times)")
    print(f"- Most Placed Pixel Location: {common_pixel} (Placed {pixel_placed} times)")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <start_date> <end_date>")
        print("Example: python script.py '2022-04-01 12' '2022-04-01 18'")
        sys.exit(1)
    
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    try:
        validate_dates(
            datetime.datetime.strptime(start_date, "%Y-%m-%d %H"),
            datetime.datetime.strptime(end_date, "%Y-%m-%d %H")
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    color_pixel_counter(start_date, end_date)
