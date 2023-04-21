def get_statement_details(item_list):
    expenditure=0
    count=0
    for i in item_list:
        expenditure+=(i["price"]*i["quantity"])
        count+=1
    return {"expenditure" : expenditure, "count" : count}

def get_statement_categorywise_details(item_list):
    statement={}
    for i in item_list:
        if i["category"] not in statement.keys():
            expenditure=(i["price"]*i["quantity"])
            count=1
            statement[i["category"]]={"expenditure" : expenditure, "count" : count}
        else:
            existing=statement[i["category"]]
            existing["expenditure"]+=(i["price"]*i["quantity"])
            existing["count"]+=1
            statement[i["category"]]=existing
    return statement

def get_statement_one_category_details(item_list, category: str):
    expenditure=0
    count=0
    for i in item_list:
        if i["category"] == category:
            expenditure+=(i["price"]*i["quantity"])
            count+=1
    return {category : {"expenditure" : expenditure, "count" : count}}