def get_wall(owner_id, token):
    print ('Время запуска скрипта',datetime.strftime(datetime.now(), "%H:%M:%S"))

    post_data = [] #пустой список
    
    #отправка запроса к хранимой процедуре, которая делает запрос на первые 2500 постов
    r = requests.post('https://api.vk.com/method/execute.Shmakov_wallGet?owner_id='+str(owner_id)+'&post_count='+str(2500)+'&offset='+str(0)+'&access_token='+token).json()

    response = r['response']
    
    #добавляем в список данные о первых 2500 постах
    post_data.extend(response[1])
    print('Количество собранных постов:', len(post_data))
    post_count = response[0] #количество постов на стене
    
    #если количество постов на стене больше чем 2500, то запускается цикл, который будет работать до тех пор, пока не соберёт все данные
    
    if post_count > 2500:
        print('Количество постов в сообществе больше 2500. Шмаков запускает цикл')
        for offset in range(2500,post_count,2500):
            max_count = offset + 2500

            r = requests.post('https://api.vk.com/method/execute.Shmakov_wallGet?owner_id='
                              +str(owner_id)+'&post_count='+str(max_count)
                              +'&offset='+str(offset)+'&access_token='+token).json()

            response = r['response']

            post_count = response[0]

            post_data.extend(response[1])

            print('Количество собранных постов:', len(post_data))
            t.sleep(0.35) #можно вместо ожидания попробовать потом писать в csv,чтобы не тратить .35 на простое ожидание
    
    else:
        print('Количество постов в сообществе меньше 2500.\nШмаков закончил сбор данных. \nИтого собрано постов:',len(post_data))
    
    #записываем все данные в csv
    
    #открываем csv и пишем название столбцов
    with open('post_data'+str(owner_id)+'.csv', 'w', newline='') as csvfile:
                        datawriter = csv.writer(csvfile, delimiter=';',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
                        datawriter.writerow(['date']+['time']+['owner_id']+['post_id']+
                                            ['len_text']+['likes_count']+['repost_count']+['comments_count'])

    print ('Шмаков записал столбцы в csv')

    for i in range(0,len(post_data)):
        # здесь нет никакой информации о медиаобъектах

        post_date =  dt.datetime.fromtimestamp( #функция преобразования
                int(post_data[i]['date'])
                ).strftime('%Y-%m-%d') #фортма преобразования Год-Месяц Час-Минута-Секунда

        post_time =  dt.datetime.fromtimestamp( #функция преобразования
                int(post_data[i]['date'])
                ).strftime('%H:%M:%S') #фортма преобразования Год-Месяц Час-Минута-Секунда 

        comments_count = post_data[i]['comments']['count'] #количество комментариев
        post_id = post_data[i]['id'] #id поста в сообществе


        likes_count = post_data[i]['likes']['count'] #количество лайков

        repost_count = post_data[i]['reposts']['count']  #количество репостов

        len_text = len(post_data[i]['text']) #длина текста

        with open('post_data'+str(owner_id)+'.csv', 'a', newline='') as csvfile:
                        datawriter = csv.writer(csvfile, delimiter=';',
                                            quotechar='|', quoting=csv.QUOTE_MINIMAL)


                        datawriter.writerow([post_date]+[post_time]+[owner_id]+[post_id]+
                                            [len_text]+[likes_count]+[repost_count]+[comments_count])

    print ('закончил запись в csv.Можете открыть файл, если это требуется.')
    print ('закончил собирать данные в',datetime.strftime(datetime.now(), "%H:%M:%S"))
