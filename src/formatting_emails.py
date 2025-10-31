
out_file= open('../data/formated_emails.txt', 'w')
with open("../data/emails.txt") as file:
    for line in file:
        emails=line.split(",")
        sendto=""
        for email in emails:
            sendto+="HYPERLINK(\"mailto:"+email.strip()+"\", \""+ email.strip() +"\")"
            if email != emails[-1]:
                sendto+=", "

        out_file.write(sendto+"\n")
        out_file.flush();


