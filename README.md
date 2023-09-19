# VTHax - Miru

Please run app.py and click the link that appears in the terminal to open the website locally.

What is Miru?

Miru is a web based vulnerability mapping application that identifies misconfigured servers and devices containing sensitive information on the internet. Our project is named Miru (見る“to look”) as it utilizes Google Dork queries to actively find, categorize, and analyze target sites. The frontend of Miru leverages Flask for data representation and analytics, while the backend crawler performs the search functionality, WHOIS requests, regex parsing, and data visualization. 

Google Dorks Explained

A Google Dork is a string that uses the advanced search features of Google to query sites that follow set of specified parameters. An example of a Google Dork is: inurl:'adminLogin/' intitle:'Admin Panel.' Here, 'inurl:' searches for 'adminLogin/' in the URL of the search results, while 'intitle:' searches for the words 'Admin Panel' in the titles of websites. Each of these search parameters can be customized in numerous combinations, leading to a wide range of unique results. Some of the preset Google Dorks in Miru include websites that contain password files, surveillance cameras, payroll systems, SSH keys, and many more. 

Relevance to Cybersecurity

The purpose of Miru is to demonstrate just how many vulnerable web services there are exposed on the open internet, and the concerningly large amount of information that these exposed services are hosting. From login credentials, to databases containing user data,  and financial transactions of e-commerce sites, all types of information can be obtained with fairly unsophisticated Google Dork queries online. Miru can assist system administrators and security professionals in evaluating the vulnerabilities of specific domains and overall threat landscape of exposed web services throughout the world.
