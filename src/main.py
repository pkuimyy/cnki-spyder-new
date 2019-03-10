import sys
sys.path.append("../lib")
import cnki_spyder_tool as cnki
import csv

if __name__ == "__main__":
    
    with open("../data/input/1_backups.csv","r",encoding="utf-8") as input_file:
        csv_reader = csv.reader(input_file,delimiter=",")
        
        author_list = []
        for row in csv_reader:
            # pass the headers
            if row[0] == "uid":
                continue

            uid = row[0]
            uname = row[1]
            univ = row[5]
            author = {}
            author["uid"] = uid
            author["uname"] = uname
            author["univ"] = univ
            author_list.append(author)

    headers = ["uid","doc_title","doc_url","author_name","author_id","author_url","journal_name","journal_url","download_num","refer_num"]

    with open("../data/output/1_res.csv","a",encoding="utf8",newline="") as output_file:
        csv_writer = csv.DictWriter(output_file,headers,delimiter="|")
        csv_writer.writeheader()   

        for author in author_list:            
            for doc in cnki.get_doc_list(author):
                csv_writer.writerow(doc)
        


        
