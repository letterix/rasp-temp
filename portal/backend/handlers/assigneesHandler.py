
from dao import assignees_dao
import authentication

def delete(username, customer_id):
    return assignees_dao.delete_assignee(username, customer_id)

def insert(username, customer_id):
    res = assignees_dao.create_assignee(username, customer_id)
    return res

def get_customers(username):
    return assignees_dao.get_customers(username)

def get_assignees(customer_id):
    return assignees_dao.get_assignees(customer_id)

def update_assignee(user):
    if not user.get('role') in authentication.super_roles():
        if not authentication.is_master(user):
            res = _add_assignees_for_user(user)
        else:
            res = _add_assignees_for_master(user)
    else:
        res = _add_assignees_for_super(user)
    return res

def _add_assignees_for_master(user):
    assignees = get_customers(user.get('username'))
    customers = user.get('customers')
    assignee_customers = []
    for assignee in assignees:
        if not assignee.get('customer') in customers:
            delete(user.get('username'), assignee.get('customer'))
        else:
            assignee_customers.append(assignee.get('customer'))
    for customer in customers:
        if not customer in assignee_customers:
            insert(user.get('username'), customer)

    return True


def _add_assignees_for_super(user):
    assignees = get_customers(user.get('username'))
    customers = [1]
    master_set = False
    for assignee in assignees:
        if not assignee.get('customer') in customers:
            delete(user.get('username'), assignee.get('customer'))
        else:
            master_set = True
    if not master_set:
        insert(user.get('username'), 1)
    return True


def _add_assignees_for_user(user):
    assignees = get_customers(user.get('username'))
    customers = user.get('customers')
    # need atleast 1 customer
    if len(customers) == 0:
        return False
    # can only have 1 customer
    customer = customers[0]
    if len(assignees) > 0:
        for assignee in assignees:
            if not assignee.get('customer') == customer:
                delete(assignee.get('user'), assignee.get('customer'))
        # reload list
        assignees = get_customers(user.get('username'))
    if len(assignees) == 1 and assignees[0].get('customer') == customer:
        return True
    else:
        return insert(user.get('username'), customer) == 1