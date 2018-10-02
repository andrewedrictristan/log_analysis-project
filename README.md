# log_analysis-project
## My Program will results plain text that have contents, like below:
- What are the most popular three articles of all time?
- Who are the most popular article authors of all time?
- On which days did more than 1% of requests lead to errors?

1. Thing to do first install the [GIT BASH](https://gitforwindows.org/) for windows user.
2. Install [Python](https://www.python.org/) for the windows user.
3. Install [Vagrant](https://www.vagrantup.com/downloads.html) for windows user.
4. Creates and configures guest machines in vagrant folder
``` vagrant up ```
5. Access the vagrant shell
``` vagrant ssh ```
6. Download ["newsdata.sql"](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) data provided by Udacity, unzip it and put it in one folder.
```sql 
psql -d news -f newsdata.sql
``` 
7. Connect the database 
```sql
psql news 
```
8. Create the views, by executing create_views.sql
```sql
psql -d news -f create_views.sql
```

Here is the content of create_views.sql:
```sql
create view vs_article as select (Replace(path,'/article/','')) as slug_path, (count(*)) as total_visits from log 
where path like '%article%' and Status='200 OK' Group by path order by total_visits desc;
```

```sql
create view author_slugs as select name as author_name, articles.title ,articles.slug from authors,articles 
where authors.id=articles.author;
```

```sql
create view error_requests as select cast(count(*) as decimal(10,2))as error_req, date(time) as date from log 
where status<>'200 OK' group by date order by date desc;
```

```sql
create view request_per_day as select count(*) as number_of_request, date(time) as date 
from log group by date order by date desc;
```

9. To run the program log_analysis_db.py, you have to run:
```git
python log_analysis_db.py
```
