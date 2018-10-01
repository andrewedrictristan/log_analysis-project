#!/usr/bin/env python3

import psycopg2


def get_favorite_articles(c):
    # TOP 3 POPULAR ARTICLES
    c.execute("select author_slugs.title,vs_article.total_visits from author_slugs,vs_article "
              "where vs_article.slug_path=author_slugs.slug limit 3;")
    return c.fetchall()


def get_favorite_authors(c):
    # MOST POPULAR AUTHORS
    c.execute("select author_slugs.author_name,sum(vs_article.total_visits) as most_fav_author "
              "from author_slugs,vs_article where "
              "author_slugs.slug=vs_article.slug_path group by author_slugs.author_name order by "
              "most_fav_author desc;")
    return c.fetchall()


def get_error_requests(c):
    # DATE AND ERROR RATE THAT HIGHER THAN 1%
    c.execute("select rate,date "
              "from("
              "select cast((error_requests.error_req*100)/request_per_day.number_of_request as decimal(10,2))"
              " as rate,request_per_day.date "
              "from error_requests,request_per_day "
              "where request_per_day.date=error_requests.date)as rate_error "
              "where rate_error.rate>1;")
    return c.fetchall()


def main():
    # Connect to database "news"
    db = psycopg2.connect(database="news")

    # Creating cursor object to execute sql statements
    c = db.cursor()

    # Open the file
    file = open("result_file.txt", "w")

    # Looping for writing in file
    t = "1. What are the most popular three articles of all time? \r\n"
    t += "\r\n".join("%s - %s Views " % (author, views)
                   for author, views in get_favorite_articles(c))
    t += "\r\n\r\n2. Who are the most popular article authors of all time?\r\n"
    t += "\r\n".join("%s - %s Views " % (title, visits)
                   for title, visits in get_favorite_authors(c))
    t += "\r\n\r\n3. On which days did more than 1% of requests lead to errors?\r\n"
    t += "\r\n".join("%s%% - %s " % (rate, date.strftime('%d, %b %Y'))
                   for rate, date in get_error_requests(c))

    # Writing into file and save
    file.write(t)
    file.close()

    # Disconnect the database connection
    db.close()

if __name__ == '__main__':
    # Running the main() function
    main()