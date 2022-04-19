# OpenReview Utilities
OpenReview utilities for AHLI events

## authorids2emails
Short script to lookup preferred email address for OpenReview authorids.

### Usage
```bash
python authorids2emails.py \
    --username=${OPENREVIEW_USER} \
    --password=${OPENREVIEW_PASS} \
    all_emails.txt
```

Where `all_emails.txt` contains authorids in the format
```
~authorid1|author2@institution.org
~authorid3|authorid1|authorid4
...
```

# Additional Utilities
See https://github.com/rycolab/aclpub2
