from bs4 import BeautifulSoup
from urllib.request import urlopen

# Mix up the soup
url = 'https://news.ycombinator.com/item?id=11814828'
page = urlopen(url)
soup = BeautifulSoup(page, 'html.parser')

# All span elements with class="comment" (all job postings?)
comments = []
# All class="comment" elements with 'python' in the listing
python_listings = []
# All class="comment" elements with 'remote' in the listing
remote_listings = []
# All class="comment" elements with 'remote' and 'python' in the listing
r_p_listings = []

# Iterate through the spans containing job postings
for span in soup.find_all('span', class_='comment'):
    # Save all the job postings
    comments.append(span)
    text = span.get_text().lower()
    # Check to see if it's a python job
    if 'python' in text:
        python_listings.append(span)
        # Check to see if it's also a remote job
        if 'remote' in text:
            r_p_listings.append(span)
    
    # Check to see if it's a remote job
    if 'remote' in text:
        remote_listings.append(span)

# Write jobs list to a file
def write_jobs(filename):
    with open(filename, 'w') as writefile:
        for i, job in enumerate(r_p_listings):
            entry = [str(i + 1), '=======================']
            entry.append(job.get_text())
            entry.append('\n')
            writefile.write('\n'.join(entry))

# Report on a job type
def report(msg, subset, master_set=None):
    args = [
        '{0:34}'.format(msg),
        '{0:4}'.format(len(subset))
    ]
    if master_set:
        args.append('({:6.2%})'.format(len(subset) / len(master_set)))
    
    print(*args)

# Display results
report('Total job postings', comments)
report('Total Python job postings:', python_listings, comments)
report('Total remote job postings:', remote_listings, comments)
report('Total remote Python job postings:', r_p_listings, comments)

# Write results
write_jobs('jobs.txt')