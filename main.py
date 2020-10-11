"""
File:           main.py
Author:         Dibyaranjan Sathua
Created on:     10/10/20, 10:15 pm
"""
from src import SathuaLabCrawler


def main():
    """ Main function """
    phone_no = input("Enter your phone number: ")
    phone_no = phone_no.strip()
    with SathuaLabCrawler(phone_no) as crawler:
        crawler.crawl()
        print(f"App API Id: {crawler.app_api_id}")
        print(f"App API Hash: {crawler.app_api_hash}")


if __name__ == "__main__":
    main()
