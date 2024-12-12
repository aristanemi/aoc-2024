import re
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

input_file = sys.argv[1]
page_rules, updates = open(input_file).read().split('\n\n')
page_rules = [[int(prs) for prs in pr.split('|')] for pr in page_rules.split('\n')]
updates = [[int(u) for u in up.split(',')] for up in updates.split('\n')]

# Merge rules for same page
merged_rules = {pr[0]: [] for pr in page_rules}
merged_rules.update({pr[1]: [] for pr in page_rules})
for pr in page_rules:
    merged_rules[pr[0]].append(pr[1])
logging.debug(f'merged_rules = {merged_rules}')

# Update is not ordered, 
# # if current page is greater than subsequent pages. page in merged_rules[sp]
# # OR 
# # subsequent page is smaller than current page. sp not in merged_rules[page]
def check_merged_rules(merged_rules, update):
    for page in update:
        page_index = update.index(page)
        subsequent_pages = update[page_index+1:]
        ## element is not in the merged rules of subsequent elements
        for sp in subsequent_pages:
            if page in merged_rules[sp] or sp not in merged_rules[page]:
                return False
    return True

middle_elements = []
unordered_updates = []
for u in updates:
    if check_merged_rules(merged_rules, u):
        middle_elements.append(u[len(u)//2])
    else:
        unordered_updates.append(u)
print(f'Sum of middle elements = {sum(middle_elements)}')

## Part2 - Correct the order of updates
def order_update(unordered_update, merged_rules):
    # If sp is not in the merged rules of page, swap pages
    # if page in merged_rules of sp, swap pages
    # send page to end of update, if it doesn't have any bigger pages than it
    send_to_last = []
    for page in unordered_update:
        if len(merged_rules[page]) == 0:
            send_to_last.append(page)
    for page in send_to_last:
        page_index = unordered_update.index(page)
        unordered_update.pop(page_index)
        unordered_update.append(page)

    for i in range(len(unordered_update)):
        subsequent_pages = unordered_update[i+1:]
        for sp in subsequent_pages:
            page = unordered_update[i]
            if sp not in merged_rules[page] or page in merged_rules[sp]:
                unordered_update.pop(unordered_update.index(sp))
                unordered_update.insert(i, sp)
                # print(f'swapping {page} and {sp}', 'new ou = ', unordered_update)

    return unordered_update

corrected_updates_sum = []
for u in unordered_updates:
    logging.debug(f'unordered update = {u}')
    u = order_update(u, merged_rules)
    logging.debug(f'ordered update = {u}')
    corrected_updates_sum.append(u[len(u)//2])

print(f'Sum of middle elements (corrected) = {sum(corrected_updates_sum)}')
