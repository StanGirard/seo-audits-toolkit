from googlesearch import search
import logging

def rank(domain, query):
    my_results_list = []
    print(domain)
    print(query)
    for i in search(query,        # The query you want to run
                    tld = 'com',  # The top level domain
                    lang = 'en',  # The language
                    num = 10,     # Number of results per page
                    start = 0,    # First result to retrieve
                    stop = 100,  # Last result to retrieve
                    pause = 2.0,  # Lapse between HTTP requests
                ):
        my_results_list.append(i)
        logging.debug(str(my_results_list.index(i)) + ": " + str(i))
        if domain in i:
            return {"pos": my_results_list.index(i) + 1, "url": i}
    return {"pos": -1, "url": None}

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p')

    print(rank("primates.dev", "parse xml response python"))
    
