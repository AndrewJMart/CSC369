import polars as pl
import datetime
import time
import sys

def validate_dates(start_date, end_date):
    """Validate that end_date is after start_date."""
    if start_date >= end_date:
        raise ValueError("End date must be after start date.")

def color_pixel_counter(start_date: str, end_date: str):
    """Count the most placed color and pixel in the specified timeframe."""
    start_time = time.perf_counter_ns()
    
    start_datetime = datetime.datetime.strptime(start_date, "%Y-%m-%d %H")
    end_datetime = datetime.datetime.strptime(end_date, "%Y-%m-%d %H")
    
    rplace_df = pl.read_csv(r"C:\Users\Andrew\Documents\CSC369\2022_place_canvas_history.csv").with_columns(
        pl.col('timestamp')
        .str.slice(0, 16)
        .str.to_datetime(format='%Y-%m-%d %H:%M')
        .alias('timestamp')
    )
    
    rplace_df = rplace_df.filter(
        (pl.col("timestamp") >= start_datetime) & (pl.col("timestamp") <= end_datetime)
        )
    
    common_pixel = rplace_df['coordinate'].mode()
    common_color = rplace_df['pixel_color'].mode()
    
    end_time = time.perf_counter_ns()
    execution_time_ms = (end_time - start_time) // 1_000_000 
    
    print(f"Execution Report:")
    print(f"- Timeframe: {start_date} to {end_date}")
    print(f"- Execution Time: {execution_time_ms} ms")
    print(f"- Most Placed Color: {common_color}")
    print(f"- Most Placed Pixel Location: {common_pixel}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        for element in sys.argv:
            print(element)
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
