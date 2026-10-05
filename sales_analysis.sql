create database sales_analysis;
use sales_analysis;
select*
from clean_customers;
select*
from clean_orders;
select O.Order_ID,O.Customer_ID,C.Customer_Name,C.Region
from clean_orders o
join clean_customers c
  on o.Customer_ID=c.Customer_ID;
Show tables;
describe clean_customers;
describe clean_orders;
select count(*) as total_orders
from clean_orders;
select sum(quantity)as total_quantity
from clean_orders;
select product,sum(quantity) as total_quantity
from clean_orders
group by product;
select product,sum(quantity)as total_quantity
from clean_orders
group by product
order by total_quantity desc;
select region,sum(quantity)as total_quantity
from clean_orders
group by region
order by total_quantity desc;
select c.customer_name,count(o.order_id)as total_orders
from clean_orders o
join clean_customers c
    on o.Customer_ID=c.Customer_ID
group by c.customer_name
order by total_orders desc;
select c.customer_name,sum(o.quantity) as total_quantity
from clean_orders o
join clean_customers c
    on o.customer_ID=c.customer_ID
group by c.customer_name
order by total_quantity desc;
select region,product,sum(quantity) as total_quantity
from clean_orders
group by region,product
order by total_quantity desc;
select product,sum(quantity)as total_quantity
from clean_orders
group by product
having sum(quantity)>2;
select region,count(customer_id)as total_customers
from clean_customers
group by region
order by total_customers desc;
select region,count(order_id) as total_orders,sum(quantity)as total_quantity
from clean_orders
group by region
order by total_quantity desc
limit 1;
select c.customer_name,o.product,sum(o.quantity)as total_quantity
from clean_orders O
join clean_customers c
  on o.Customer_ID=c.Customer_ID
group by c.customer_name,o.product
order by total_quantity desc;
Select region,product,sum(quantity)as total_quantity
from clean_orders
group by region,product
order by total_quantity desc
limit 1;

select count(*) as total_orders
from clean_orders;
select sum(quantity)as total_quantity
from clean_orders;
