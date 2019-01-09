declare @current_date datetime='2017-11-05' 
declare @region varchar(255) = 'Регион 38'

select 
	coalesce(fc.client,fp.client) as name, 
	round(coalesce(fc.cost,0.0),0) as value, 
	round(coalesce(fp.cost,0.0),0) as pvalue, 
	round(coalesce(fc.cost,0.0) - coalesce(fp.cost,0.0),0) as change, 
	round(coalesce(sc.workday_cost,0.0)*21.0/clc.workday_quantity + coalesce(sc.weekend_cost,0.0)*9.0/clc.workday_quantity,0) as std_value, 
	round(coalesce(sp.workday_cost,0.0)*21.0/clp.workday_quantity + coalesce(sp.weekend_cost,0.0)*9.0/clp.workday_quantity,0) as std_pvalue 
from
	(
	select 
		c.client, 
		sum(sh.cost) as cost 
	from sales_history as sh 
	join clients as c 
		on c.client_code = sh.client_code 
	where 
		sh.sale_date between convert(date,@current_date-30) and convert(date,@current_date-1) 
		and c.region = @region
	group by 
		c.client
	)fc 
full join
	( 
	select 
		c.client, 
		sum(sh.cost) as cost 
	from sales_history as sh 
	join clients c 
		on c.client_code = sh.client_code 
	where 
		sh.sale_date between convert(date,@current_date-60) and convert(date,@current_date-31) 
		and c.region = @region
	group by 
		c.client
	)fp 
	on fp.client = fc.client 
left join
	( 
	select 
		c.client, 
		sum( case when cl.isWorking = 1 then sh.cost else 0.0 end ) as workday_cost, 
		sum( case when cl.isWorking = 0 then sh.cost else 0.0 end ) as weekend_cost 
	from sales_history sh 
	join clients c 
		on c.client_code = sh.client_code 
	join calendars cl 
		on cl.dt = sh.sale_date 
	where 
		sh.sale_date between convert(date,@current_date-30) and convert(date,@current_date-1) 
		and c.region = @region
	group by 
		c.client 
	)sc 
	on sc.client = coalesce(fc.client,fp.client) 
left join
	( 
	select 
		c.client, 
		sum( case when cl.isWorking = 1 then sh.cost else 0.0 end ) as workday_cost, 
		sum( case when cl.isWorking = 0 then sh.cost else 0.0 end ) as weekend_cost 
	from sales_history sh 
	join clients c 
		on c.client_code = sh.client_code 
	join calendars cl 
		on cl.dt = sh.sale_date 
	where 
		sh.sale_date between convert(date,@current_date-60) and convert(date,@current_date-31) 
		and c.region = @region
	group by 
		c.client
	)sp 
	on sp.client = coalesce(fc.client,fp.client) 
cross join
	( 
	select 
		sum( case when cl.isWorking = 1 then 1 else 0 end) as workday_quantity, 
		sum( case when cl.isWorking = 0 then 1 else 0 end) as weekend_quantity 
	from calendars cl 
	where 
		cl.dt between convert(date,@current_date-30) and convert(date,@current_date-1) 
	)clc 
cross join
	( 
	select 
		sum( case when cl.isWorking = 1 then 1 else 0 end) as workday_quantity, 
		sum( case when cl.isWorking = 0 then 1 else 0 end) as weekend_quantity 
	from calendars cl 
	where 
		cl.dt between convert(date,@current_date-60) and convert(date,@current_date-31)
	)clp