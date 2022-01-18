# -*- coding: utf-8 -*-

""" **************************************************************************
                           Created on 2021

                        @author: Omid Hajipoor
                    Email: hajipoor.omid@aut.ac.ir
                  Gmail: omid.hajipoor0770@Gmail.com
************************************************************************** """


from Helper import crawling


# start text file include starting papers
start_file_name = 'start_papers_URLs'

# output file
json_file_name = 'output_crawled'

# number of paper for crawling
_numOf_paper = 320




# start crawling
crawling(start_file_name, json_file_name, _numOf_paper)
