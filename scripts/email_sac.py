import getpass

import numpy as np
from openreview.api import OpenReviewClient
from openreview.tools import iterget_notes

username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")

domain = 'chilconference.org/CHIL/2024/Conference'
conference_email = "info@chilconference.org"

BASE_API_URL = "https://api2.openreview.net"

client = OpenReviewClient(baseurl=BASE_API_URL, username=username, password=password)

# Get active(blind) submissions
submissions = list(
    iterget_notes(
        client,
        invitation=f"{domain}/-/Submission",
        details="directReplies",
    )
)
withdrawn_submissions = list(
    iterget_notes(
        client, invitation=f"{domain}/-/Withdrawn_Submission"
    )
)
withdrawns = [w.number for w in withdrawn_submissions]
desk_reject_submissions = list(
    iterget_notes(
        client, invitation=f"{domain}/-/Desk_Rejected_Submission"
    )
)
desk_rejects = [dr.number for dr in desk_reject_submissions]
blind_submissions = [
    sub for sub in submissions if sub.number not in withdrawns + desk_rejects
]

# Get metadata
forum_number = {}
number_forum = {}
number_title = {}
number_authors = {}
for bs in blind_submissions:
    forum_number[bs.forum] = bs.number
    number_forum[bs.number] = bs.forum
    number_title[bs.number] = bs.content["title"]["value"]
    number_authors[bs.number] = bs.content["authorids"]["value"]

# Get assignments
sac_assignments = client.get_grouped_edges(
    invitation=f"{domain}/Senior_Area_Chairs/-/Assignment",
    groupby="head",
    select="tail",
)
ac_sac_assigned = {}
for e in sac_assignments:
    if e["id"]["head"] not in ac_sac_assigned:
        ac_sac_assigned[e["id"]["head"]] = e["values"][0]["tail"]

ac_assignments = client.get_grouped_edges(
    invitation=f"{domain}/Area_Chairs/-/Assignment",
    groupby="head",
    select="tail",
)
p_ac_assigned = {}
for e in ac_assignments:
    if e["id"]["head"] in forum_number:
        p = forum_number[e["id"]["head"]]
        if p not in p_ac_assigned:
            p_ac_assigned[p] = e["values"][0]["tail"]
        if len(e["values"]) > 1:
            print(p)

# Get reviews
reviews = []
for sub in submissions:
    reviews += [
        reply
        for reply in sub.details["directReplies"]
        if reply["invitations"][0].endswith("Official_Review")
    ]

# Get ratings
p_ratings = {}
for review in reviews:
    if review["forum"] in forum_number:
        p = forum_number[review["forum"]]
        if p not in p_ratings:
            p_ratings[p] = []
        p_ratings[p].append(int(review["content"]["overall_recommendation"]["value"].split(":")[0]))

avg_rating = {}
for p in p_ratings:
    avg_rating[p] = round(np.mean(p_ratings[p]), 2)

# Get meta-reviews
meta_reviews = []
for sub in submissions:
    meta_reviews += [
        reply
        for reply in sub.details["directReplies"]
        if reply["invitations"][0].endswith("Meta_Review")
    ]

p_mr = {}
for mr in meta_reviews:
    if mr["forum"] in forum_number:
        p = forum_number[mr["forum"]]
        p_mr[p] = {
            "recommendation": mr["content"]["recommendation"]["value"],
            "confidence": mr["content"]["confidence"]["value"],
            "discussion": mr["content"]["discussion_with_SAC_needed"]["value"],
        }

# Flag papers that need attention
p_problem = {}
for p in number_forum:
    p_problem[p] = []
    if p not in p_mr:
        p_problem[p].append("Missing meta-review")
for p in p_mr:
    if p_mr[p]["confidence"] == "Very low confidence":
        p_problem[p].append("Very Low AC confidence")
    if p_mr[p]["discussion"] == "Let's discuss!":
        p_problem[p].append("AC asked to discuss with the SAC")
    if avg_rating[p] >= 5.7 and p_mr[p]["recommendation"] == "Reject":
        p_problem[p].append("Rejected above threshold")
    if avg_rating[p] <= 5.3 and "Accept" in p_mr[p]["recommendation"]:
        p_problem[p].append("Accepted below threshold")

p_problem_to_send = {}
for p in p_problem:
    if p_problem[p]:
        p_problem_to_send[p] = p_problem[p]


# Send a personalized message to each recipient
message_text = """Dear {{{{fullname}}}},

TL;DR: This message includes the final list of papers requiring your attention. Please go over all these, communicate with ACs, and make sure a meta-review is submitted, addressing issues raised below, as early as possible. Additionally, please go over meta-reviews for borderline papers, and oral recommendations.
IMPORTANT: Please reply to info@chilconference.org after you are done handling these papers. 

Thank you for all the hard work you’ve put in as SAC this year. We know we have asked more of you than in previous years, and appreciate your help with all the reviewing steps so far. 

At this point, there are a few papers with outstanding issues, which require your attention. Below we detail the categories of these issues, and the specific papers are at the end of this message.

1. **Missing meta-review**: Some papers are still missing a meta-review. For these, we ask that you contact the AC to make sure they submit it ASAP (the deadline for submitting these was last Friday). If you are unable to reach an AC, please take over the paper, and submit the meta-review.
2. **AC asked to discuss with the SAC**: For some papers the AC noted a need to discuss with the SAC. If you already discussed this paper with the AC, no action is needed. If not, please reach out to the AC to discuss the paper.
3. **Very Low AC confidence**: The AC expressed very low confidence in the review. Please get in touch with the AC, and discuss the paper. If additional input is needed (e.g., regarding a technical point in the paper which the AC is unsure of), please see if you can find another AC in your batch to provide it, and reach out to us if we can help.
4. **Rejected above threshold**: This is an important and subtle category. Most of us have been in a situation where we receive fairly positive reviews, but the paper ends up rejected. This could be a fair outcome and is certainly possible, but we would like it to be well justified, so the authors feel the reviewing process is fair. Ideally, decisions should be based on integrating the reviews, the rebuttal and the discussion with the authors. If a rejection decision is based on new arguments, these should be convincingly argued, and we should have high confidence that authors could not rebut those if given an opportunity. We’ve decided to set the threshold for such papers at an average score of 5.7. For these papers, please carefully read the AC meta-review text, and see if it sounds like a fair decision and convincing justification. If not, reach out to the AC and discuss it.
5. **Accepted below threshold**: We currently have 28% acceptance among the submitted meta-reviews, which is higher than our target (and historical) rate of 25%. We therefore would like you to take a critical look at papers where the current decision is “accept” but the scores are not high and there is no strong support from reviewers. It is likely that some of these papers are not quite ready for publication, and we ask you to find those where a “reject” decision is more appropriate. To help you focus on the relevant papers, we list below papers that are currently accepted with an average score of 5.3 or less.

For the papers above, please make sure to address the issues raised by September 11th, and let us know when you are done by replying to info@chilconference.org.

A few more points:

1. **Exporting meta-review information**: Note that when you export paper information to a spreadsheet in OpenReview, this now includes all meta-review information, including the meta-review text.
2. **Orals**: We may have some more room for orals, so if there is a paper in your stack that is currently a spotlight, and you think it would be good as an oral, please go ahead and change that recommendation (or ask your AC to). Please try to select these as soon as possible and no later than September 14th 1pm EDT.
3. **Reading borderline meta-reviews**: For borderline papers that were rejected, please read the meta-review by September 14th 1pm EDT to check that the decision is justified properly .

Many thanks again for your help,
CHIL Organizers

List of papers in your stack that need attention:
{}
"""

sac_papers = {}
for p in p_problem_to_send:
    ac = p_ac_assigned[p]
    sac = ac_sac_assigned[ac]
    if sac not in sac_papers:
        sac_papers[sac] = []
    sac_papers[sac].append((ac, p))

for sac in sac_papers:
    s = ""
    for t in sorted(sac_papers[sac]):
        c = ", ".join(p_problem_to_send[t[1]])
        s += f"ID: {t[1]}, AC: {t[0]}, Categories:{c}\n"
    # print(message_text.format(s))

    # The following chunk sends the emails out.
    # Double check everything is correct before you run this.
    sent = client.post_message(
        message=message_text.format(s),
        recipients=[sac],
        replyTo=conference_email,
        subject="[CHIL SACs] Final list of papers requiring your attention",
    )
