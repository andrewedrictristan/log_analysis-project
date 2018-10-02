create view vs_article as select (Replace(path,'/article/','')) as slug_path, (count(*)) as total_visits from log 
where path like '%article%' and Status='200 OK' Group by path order by total_visits desc;

create view author_slugs as select name as author_name, articles.title ,articles.slug from authors,articles 
where authors.id=articles.author;

create view error_requests as select cast(count(*) as decimal(10,2))as error_req, date(time) as date from log 
where status<>'200 OK' group by date order by date desc;

create view request_per_day as select count(*) as number_of_request, date(time) as date 
from log group by date order by date desc;