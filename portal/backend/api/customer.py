from authentication import *
from handlers import customerHandler, installationHandler, statusHandler

@accepted_roles(all_roles())
def get(customer_id=None):
    res = customerHandler.get_customer(customer_id)
    if res:
        if type(res) == list:
            statusHandler.set_status_for_customers(res)
        else:
            statusHandler.set_status_for_customer(res)
        return OkResponse(res)
    else:
        return ConflictResponse("Could not get the customer")


@JsonIn
@accepted_roles(super_roles())
def put(customer):
    res = customerHandler.update_customer(customer)
    if res:
        return OkResponse("Successfully updated the customer")
    else:
        return ConflictResponse("Could not update the customer!")



@accepted_roles(super_roles())
@JsonIn
def post(customer):
        res = customerHandler.insert(customer)
        if res:
            return OkResponse("Successfully added a new customer")
        else:
            return ConflictResponse("Could not add customer")


@accepted_roles(super_roles())
def delete(customer_id):
    res = customerHandler.delete(customer_id)
    if res:
        return OkResponse("Controller was successfully deleted")
    else:
        return ConflictResponse("Could not delete customer")

