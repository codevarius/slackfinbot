declare @current_date datetime='2017-11-05' select coalesce(fc.region,fp.region) as name, round(coalesce(fc.cost,0.0),0) as value, round(coalesce(fp.cost,0.0),0) as pvalue, round(coalesce(fc.cost,0.0) - coalesce(fp.cost,0.0),0) as change, round(sc.workday_cost*21.0/clc.workday_quantity + sc.weekend_cost*9.0/clc.workday_quantity,0) as std_value, round(sp.workday_cost*21.0/clp.workday_quantity + sp.weekend_cost*9.0/clp.workday_quantity,0) as std_pvalue from( select c.region, sum(sh.cost) as cost from sales_history as sh join clients as c on c.client_code = sh.client_code where sh.sale_date between convert(date,@current_date-30) and convert(date,@current_date-1) group by c.region)fc full join( select c.region, sum(sh.cost) as cost from sales_history as sh join clients c on c.client_code = sh.client_code where sh.sale_date between convert(date,@current_date-60) and convert(date,@current_date-31) group by c.region)fp on fp.region = fc.region left join( select c.region, sum( case when cl.isWorking = 1 then sh.cost else 0.0 end ) as workday_cost, sum( case when cl.isWorking = 0 then sh.cost else 0.0 end ) as weekend_cost from sales_history sh join clients c on c.client_code = sh.client_code join calendars cl on cl.dt = sh.sale_date where sh.sale_date between convert(date,@current_date-30) and convert(date,@current_date-1) group by c.region )sc on sc.region = coalesce(fc.region,fp.region) left join( select c.region, sum( case when cl.isWorking = 1 then sh.cost else 0.0 end ) as workday_cost, sum( case when cl.isWorking = 0 then sh.cost else 0.0 end ) as weekend_cost from sales_history sh join clients c on c.client_code = sh.client_code join calendars cl on cl.dt = sh.sale_date where sh.sale_date between convert(date,@current_date-60) and convert(date,@current_date-31) group by c.region)sp on sp.region = coalesce(fc.region,fp.region) cross join( select sum( case when cl.isWorking = 1 then 1 else 0 end) as workday_quantity, sum( case when cl.isWorking = 0 then 1 else 0 end) as weekend_quantity from calendars cl where cl.dt between convert(date,@current_date-30) and convert(date,@current_date-1) )clc cross join( select sum( case when cl.isWorking = 1 then 1 else 0 end) as workday_quantity, sum( case when cl.isWorking = 0 then 1 else 0 end) as weekend_quantity from calendars cl where cl.dt between convert(date,@current_date-60) and convert(date,@current_date-31))clp