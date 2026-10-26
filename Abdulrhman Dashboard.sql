use Course_db;
select sa.total_amount, sa.quantity , sa.sale_date , ci.city_name , co.country_name , pr.product_name ,
 pr.category , pr.price , pc.cost , cu.customer_name , cu.gender , em.employee_name , em.department 
from sales sa
join product pr on sa.product_id = pr.product_id
join product_cost pc on sa.product_id = pc.product_id
join employee em on sa.employee_id = em.employee_id
join customer cu on sa.customer_id = cu.customer_id
join city ci on cu.city_id = ci.city_id
join country co on ci.country_id = co.country_id