# OpenReview Utilities

OpenReview utilities for AHLI events

## get_emails_from_author_ids

Short script to lookup preferred email address for OpenReview authorids.

### Usage

```bash
python get_emails_from_author_ids.py \
    --username=${OPENREVIEW_USER} \
    --password=${OPENREVIEW_PASS} \
    all_emails.txt
```

Where `all_emails.txt` contains authorids in the format:

```
~authorid1|author2@institution.org
~authorid3|authorid1|authorid4
...
```

# Additional Utilities

See https://github.com/rycolab/aclpub2
