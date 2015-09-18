import authentication
from handlers import assigneesHandler, userHandler
from dao import customers_dao


def get_customer(customer_id):
    if customer_id:
        return customers_dao.get(customer_id)
    else:
        return get_customers_for()

def delete(customer_id):
    return customers_dao.delete_customer(customer_id)


def insert(customer):
    res = customers_dao.create_customer(customer)
    return res


def get_customers():
    return customers_dao.get_all()

def update_customer(customer):
    return customers_dao.update(customer);


def get_customers_for(username= None):
    user = userHandler.get_user(username)
    assignees = assigneesHandler.get_customers(user.get('username'))
    customers = []
    if not authentication.is_master(user):
        # admin and user
        if assignees:
            customers.append(get_customer(assignees[0].get('customer')))
            return customers
    else:
        if not authentication.user_is_admin(user):
            # master_user
            for assignee in assignees:
                customers.append(get_customer(assignee.get('customer')))
            return customers
        # super_user and master_admin
        return [{'id': 1, 'name': 'master'}]