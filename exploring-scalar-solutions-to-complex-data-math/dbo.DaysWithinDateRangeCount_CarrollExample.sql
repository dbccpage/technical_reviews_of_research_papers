create function dbo.DaysWithinDateRangeCount_CarrollExample
(     @start_dt		date
    , @end_dt		date
    , @day_to_find  tinyint
)
returns integer
as
begin
declare 
	  @total_days		int		= 0
	, @complete_weeks	int		= 0
	, @start_dow		tinyint = 0
	, @end_dow			tinyint = 0
	, @extra_day_count	int		= 0;

set	@total_days		= datediff(day, @start_dt, @end_dt) + 1;
set @complete_weeks = @total_days / 7;
set @start_dow		= datepart(weekday, @start_dt);
set @end_dow		= datepart(weekday, @end_dt);

-- Count target days in complete weeks
declare @complete_week_count int = @complete_weeks;

-- Check if target day appears in remainder days
-- Use bitmap approach similar to article but simplified
if @day_to_find 
	between @start_dow 
		and @end_dow 
		or (	
				@start_dow > @end_dow 
				and 
					(
						@day_to_find >= @start_dow 
						or @day_to_find <= @end_dow
					)
			)
    set @extra_day_count = 1;

	return @complete_week_count + @extra_day_count
end;