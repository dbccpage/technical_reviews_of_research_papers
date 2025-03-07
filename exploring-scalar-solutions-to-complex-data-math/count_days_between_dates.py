import datetime
from typing import List, Union

def count_weekdays_between_dates(
    start_date: Union[str, datetime.date], 
    end_date: Union[str, datetime.date], 
    weekdays: List[int] = [0]  # 0=Monday, 6=Sunday (Python's convention)
) -> int:
    """
    Count occurrences of specific weekdays between two dates.
    
    Args:
        start_date: Start date (string in format 'YYYY-MM-DD' or datetime.date)
        end_date: End date (string in format 'YYYY-MM-DD' or datetime.date)
        weekdays: List of weekdays to count (0=Monday through 6=Sunday)
        
    Returns:
        Number of occurrences of the specified weekdays
    """
    # Convert string dates to datetime if needed
    if isinstance(start_date, str):
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    
    # Ensure start_date <= end_date
    if start_date > end_date:
        start_date, end_date = end_date, start_date
    
    # Fast calculation approach (no iteration)
    total_days = (end_date - start_date).days + 1
    complete_weeks = total_days // 7
    
    # Basic count from complete weeks
    count = complete_weeks * len(weekdays)
    
    # Count weekdays in the remainder
    remainder_days = total_days % 7
    if remainder_days > 0:
        start_weekday = start_date.weekday()
        
        # Create bitmap of remainder days
        remainder_bitmap = 0
        for i in range(remainder_days):
            day_idx = (start_weekday + i) % 7
            remainder_bitmap |= (1 << day_idx)
        
        # Create bitmap of target weekdays
        target_bitmap = 0
        for day in weekdays:
            target_bitmap |= (1 << day)
        
        # Count bits where both bitmaps have 1s (using bitwise AND)
        overlap = remainder_bitmap & target_bitmap
        extra_days = bin(overlap).count('1')
        count += extra_days
    
    return count

# Example usage
if __name__ == "__main__":
    # Convert from SQL Server weekday (Sunday=1) to Python weekday (Monday=0)
    def sql_to_python_weekday(sql_weekday):
        return (sql_weekday - 2) % 7
    
    start = "2024-01-01"
    end = "2024-06-17"
    
    # Count Mondays (2 in SQL Server = 0 in Python)
    mondays = count_weekdays_between_dates(start, end, [sql_to_python_weekday(2)])
    print(f"Number of Mondays: {mondays}")
    
    # Count weekdays (Monday-Friday)
    weekdays = count_weekdays_between_dates(start, end, [0,1,2,3,4])
    print(f"Number of weekdays: {weekdays}")
    
    # Count weekend days
    weekends = count_weekdays_between_dates(start, end, [5,6])
    print(f"Number of weekend days: {weekends}")