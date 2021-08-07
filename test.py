def channle_list(channle_text_list = "1.-56161949849\n2.-44984894984\n3.-849849849849\n4.-9498494949"):
    list_of_channle = channle_text_list.split('\n')
    for i in range(0,len(list_of_channle)):
        list_of_channle[i] = int((list_of_channle[i])[2:])

    return list_of_channle


print(channle_list())