from pathlib import Path

import openreview


def authorids2emails(authorids, client=None, sep=';'):
    authorids = authorids.strip().split('|')
    emails = []
    for author in authorids:
        if '@' in author:
            emails.append(author)
        else:
            profile=client.search_profiles(ids=[author])[0]
            emails.append(profile.content.get('preferredEmail', profile.content['emails'][0]))
    return sep.join(emails)


def main(args):
    # Establish the OpenReview client
    client = openreview.Client(
        baseurl='https://api.openreview.net',
        username=args.username,
        password=args.password,
    )

    with open(args.authorids) as fp:
        for authorids in fp:
            print(authorids2emails(authorids, client=client))
    

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Convert file of OpenReview author IDs to preferred emails")
    parser.add_argument('--username', type=str, required=True)
    parser.add_argument('--password', type=str, required=True)
    parser.add_argument('authorids', type=Path)
    args = parser.parse_args()

    main(args)
    