
from flask_cors import CORS
from flask import Flask, render_template, request, jsonify, json
from werkzeug.datastructures import ImmutableMultiDict
import datetime
import uuid as _uuid
import psycopg2
import urllib
client = psycopg2.connect("host=localhost port=15432 dbname=fisearch user=postgres")
cur = client.cursor()

app = Flask(__name__)
CORS(app)

app.config['JSON_AS_ASCII'] = False #わからん
app.config['JSON_SORT_KEYS'] = False #わからん
today = datetime.datetime.now().isoformat()

def render_detail():
    try:
        # 質問詳細
        question_id = request.args.get('id')
        if question_id != None:

            cur.execute(f"SELECT user_name, user_id, question_category, question_detail, is_closed, to_char(questions.deadline_date, 'YYYY-MM-DD HH24:MI:SS'), to_char(questions.created_date, 'YYYY-MM-DD HH24:MI:SS'), question_image.image_url  AS question_image_url, user_image.image_url AS user_image_url\
                                    FROM questions \
                                    JOIN image AS question_image ON questions.id = question_image.relation_id  \
                                    JOIN users ON  users.id = questions.user_id \
                                    JOIN image AS user_image ON users.id = user_image.relation_id \
                                    WHERE questions.id ='{question_id}'")

            question_info = cur.fetchall()
            questioner_name = question_info[0][0]
            questioner_image = question_info[0][8]
            category = question_info[0][2]
            question_detail = question_info[0][3]
            is_closed = question_info[0][4] 
            deadline_date = question_info[0][5]
            question_created_date = question_info[0][6]
            question_images = []
            for i in question_info:
                question_images.append(i[7])

            cur.execute(f"SELECT user_name, user_id, answer_image.image_url AS answer_image_url, user_image.image_url AS user_image_url , answer_detail, is_best_answer, to_char(answers.created_date, 'YYYY-MM-DD HH24:MI:SS') \
                                                                                        FROM answers \
                                                                                        JOIN users ON users.id = answers.user_id \
                                                                                        JOIN image AS answer_image ON answers.id = answer_image.relation_id \
                                                                                        JOIN image AS user_image ON users.id = user_image.relation_id \
                                                                                        WHERE answers.question_id =  '{question_id}' ")

            answers_info = cur.fetchall()
            answer_list = []
            for i in answers_info:
                responder_name = i[0]
                responder_image = i[3]
                answer_detail = i[4]
                is_best_answer = i[5]
                answer_created_date = i[6]
                answer = {'user_name':responder_name, 'user_image':responder_image, 'text':answer_detail, 'is_best_answer':is_best_answer, 'created_date':answer_created_date}
                answer_list.append(answer)
            
            results = {'question_id': question_id, 'user_name':questioner_name, 'user_image':questioner_image, 'category':category, 'text':question_detail, 'image_list':question_images,
                            'answer_list': answer_list, 'is_closed':is_closed, 'deadline_date':deadline_date, 'created_date':question_created_date}

            return jsonify(results), 200
    except:
        return jsonify({'Error': 'An unexpected error has occured'})

def to_True_or_false(element):
    for e in element:
        if e != None:
            return True

@app.route('/')

#質問作成
@app.route('/question',methods=["POST"])
def q_create():
    try:
        data = request.get_json()
        question_uuid = str(_uuid.uuid4())
        user_id = data['user_id']
        deadline_date = data['deadline_date']
        question_category = data['category']
        question_detail = data['text']
        

        image_url = data['image_list']
        info  = [question_uuid, user_id, deadline_date, question_category,  question_detail]
        info = list(map(to_True_or_false, info))

        if (None in info):
            return jsonify({'errorMessage': "Please fill in values"})

        # ロールバック
        # try:
        cur.execute("INSERT INTO questions (id, user_id, question_detail, question_category,deadline_date, is_closed, created_date, updated_date) \
                                VALUES (%s,%s,%s,%s,%s,False, NOW(),NOW())", [question_uuid, user_id, question_detail, question_category, deadline_date])

        client.commit()

        for image in image_url:
                image_uuid =  str(_uuid.uuid4())
                cur.execute(f"INSERT INTO image (id, relation_id, image_url, created_date, updated_date) \
                                    VALUES (%s,%s,%s,NOW(),NOW())", [image_uuid, question_uuid, image])
        
        # except:
        #     cur.execute('ROLLBACK')
        
        client.commit()
    
        return jsonify({"id":question_uuid}), 201

    except:
        return jsonify({'errorMessage':"An unexpected error has occured"}), 500   
    

# 質問一覧
@app.route('/question', methods=["GET"])
# 質問詳細
def q_detail():
    question_id = request.args.get('id')
    if question_id != None:
        try:
            # print("question_id:",question_id)
            cur.execute(f"SELECT user_name, user_id, question_category, question_detail, is_closed, deadline_date, to_char(questions.created_date, 'YYYY-MM-DD HH24:MI:SS'), question_image.image_url  AS question_image_url, user_image.image_url AS user_image_url\
                                        FROM questions \
                                        JOIN image AS question_image ON questions.id = question_image.relation_id  \
                                        JOIN users ON  users.id = questions.user_id \
                                        JOIN image AS user_image ON users.id = user_image.relation_id \
                                        WHERE questions.id ='{question_id}'")

            question_info = cur.fetchall()
            questioner_name = question_info[0][0]
            questioner_image = question_info[0][8]
            category = question_info[0][2]
            question_detail = question_info[0][3]
            is_closed = question_info[0][4] 
            deadline_date = question_info[0][5]
            question_created_date = question_info[0][6]
            question_images = []
            for i in question_info:
                question_images.append(i[7])

            cur.execute(f"SELECT user_name, user_id, answer_image.image_url AS answer_image_url, user_image.image_url AS user_image_url , answer_detail, is_best_answer, to_char(answers.created_date, 'YYYY-MM-DD HH24:MI:SS') \
                                                                                            FROM answers \
                                                                                            JOIN users ON users.id = answers.user_id \
                                                                                            JOIN image AS answer_image ON answers.id = answer_image.relation_id \
                                                                                            JOIN image AS user_image ON users.id = user_image.relation_id \
                                                                                            WHERE answers.question_id =  '{question_id}' ")

            answers_info = cur.fetchall()
            answer_list = []
            for i in answers_info:
                responder_name = i[0]
                responder_image = i[3]
                answer_detail = i[4]
                is_best_answer = i[5]
                answer_created_date = i[6]
                answer = {'user_name':responder_name, 'user_image':responder_image, 'text':answer_detail, 'is_best_answer':is_best_answer, 'created_date':answer_created_date}
                answer_list.append(answer)
                
            results = {'question_id': question_id, 'user_name':questioner_name, 'user_image':questioner_image, 'category':category, 'text':question_detail, 'image_list':question_images,
                                'answer_list': answer_list, 'is_closed':is_closed, 'deadline_date':deadline_date, 'created_date':question_created_date}


            return jsonify(results), 200
        except:
            return jsonify({'errorMessage':"An unexpected error has occured"}), 500


        # 質問一覧
    
    else:
        try:
            limit = request.args.get('limit')
            category = request.args.get('category')
            orderby = request.args.get('orderby')
            offset = request.args.get('offset')
            keyword = request.args.get('keyword')

            query = "SELECT users.user_name, image.image_url, question_detail,  is_closed, to_char(questions.created_date, 'YYYY-MM-DD HH24:MI:SS'),  questions.id\
                            FROM questions\
                            JOIN users ON questions.user_id = users.id \
                            JOIN image ON users.id = image.relation_id \
                            WHERE 0 = 0"

            if (keyword != "" and  keyword != None): 
                query += f" AND question_detail LIKE '%{keyword}%' " 

            if (category != "" and category != None):
                query += f" AND question_category = '{category}' "

            if (offset != "" and offset != None and offset != 0):
                query += f" offset {offset}"

            if (limit != "" and limit != None  and limit != 0):
                query += f" limit {limit}"

            if (orderby != "" and orderby != None ):
                if (orderby == 1) :
                    query +=  f" ORDER BY created_date DESC"
                elif (orderby == 2):
                    query += f" ORDER BY created_date ASC"

            cur.execute(query)
            question  = cur.fetchall()
            data = []
            for e in question:
                user_name = e[0]
                user_image = e[1]
                text = e[2]
                is_closed =  e[3],
                created_date =  e[4]
                question_id = e[5]
                results = {'user_name': user_name, 'user_image': user_image, 'text':text, 'is_closed': is_closed, 'created_date': created_date, 'question_id': question_id}
                data.append(results)

            return jsonify({"data": data}), 200

        except:
            return jsonify({'errorMessage':"An unexpected error has occured"}), 500

# 質問削除
@app.route('/question', methods=['DELETE'])
def q_delete():
    try:
        question_id = request.args.get('id')

        if question_id == None:
            return jsonify({'errorMessage':'Please fill in the value'}),400
            
        cur.execute(f"SELECT id FROM questions WHERE id = '{question_id}' ")
        question = cur.fetchall()
        # print(len(question))
        if (len(question) == 0):
            return jsonify({}),404
        else:
            cur.execute(f"DELETE FROM questions WHERE id= '{question_id}' ")
            cur.execute(f"DELETE FROM image WHERE relation_id= '{question_id}' ")
            cur.execute(f"DELETE FROM answers WHERE question_id= '{question_id}' ")
            client.commit()
            return jsonify({}), 200

    except:
        return jsonify({'errorMessage':'An unexpected error has occured'}),500

# 回答作成
@app.route('/answer', methods=['POST'])
def a_create():
    try:

        answer_uuid = str(_uuid.uuid4())
        image_uuid = str(_uuid.uuid4())
        data = request.get_json()
        user_id = data['user_id']
        question_id = data['question_id']
        image = data['image']
        answer_detail = data['text']
        info = [user_id, question_id, image, answer_detail]
        info = list(map(to_True_or_false, info))
        cur.execute(f"SELECT id FROM questions WHERE id = '{question_id}' ")
        question = cur.fetchall()

        if None in info:
            return jsonify({'errorMessage':'please fill in values'}),400

        elif len(question) == 0:
            return jsonify({'errorMessage':'This question does not exist'}), 404

        else:
            cur.execute("INSERT INTO answers (id, question_id, user_id, answer_detail, is_best_answer, created_date, updated_date) \
                                VALUES (%s, %s, %s, %s, %s, NOW(), NOW())",[answer_uuid, question_id, user_id, answer_detail, False])
            cur.execute('INSERT INTO image (id, relation_id, image_url, created_date, updated_date) \
                                VALUES (%s,%s,%s,NOW(),NOW())', [image_uuid, answer_uuid,image])
            client.commit()


            # return render_detail

            return jsonify({}), 201

    except:
        return jsonify({'errorMessage':'An unexpected error has occured'}),500

#回答削除
@app.route('/answer', methods=['DELETE'])
def d_delete():
    try:
        answer_id = request.args.get('id')

        if answer_id == None:
            return jsonify({'errorMessage':'Please fill in the value'}), 400
            
        cur.execute(f"SELECT id FROM answers WHERE id = '{answer_id}' ")
        answer = cur.fetchall()
        # print(len(question))
        if (len(answer) == 0):
            return jsonify({}),404
        else:
            cur.execute(f"DELETE FROM answers WHERE id= '{answer_id}' ")
            cur.execute(f"DELETE FROM image WHERE relation_id= '{answer_id}' ")
            client.commit()

            return jsonify({}), 200

    except:
        return jsonify({'errorMessage':'An unexpected error has occured'}),500

# ベストアンサー
@app.route('/answer/bestanswer', methods=['PUT'])
def bestanswer():
    # try:
        data = request.get_json()
        question_id = data['question_id']
        answer_id = data['answer_id']
        info = [question_id, answer_id]
        info = map(to_True_or_false, info)

        if None in info:
            return jsonify({'errorMessage':'Please fill in values'}), 400

        cur.execute(f"SELECT id FROM questions WHERE id = '{question_id}' ")
        question = cur.fetchall()
        cur.execute(f"SELECT id FROM answers WHERE  id = '{answer_id}' ")
        answer = cur.fetchall()


        if len(question) == 0:
            return jsonify({'errorMessage':'This qusestion does not exist'}), 404
        elif len(answer) == 0:
            return jsonify({'errorMessage':'This answer does not exist'}), 404
        else:
            cur.execute(f"UPDATE answers SET is_best_answer = TRUE WHERE id = '{answer_id}' ")
            cur.execute(f"UPDATE questions SET is_closed = TRUE WHERE id ='{question_id}' ") 
            client.commit()
            return jsonify({}), 200
    # except:
    #     return jsonify({'errorMessage':'An unexpected error has occured'}),500

# ユーザー登録
@app.route('/user', methods=['POST'])
def u_create():
    try:
        data = request.get_json()
        user_uuid = str(_uuid.uuid4())
        image_uuid = str(_uuid.uuid4())
        firebase_user_id = data['user_id']
        user_name = data['user_name']
        user_image = data['user_image']

        info = [firebase_user_id, user_name, user_image]
        info = list(map(to_True_or_false, info))

        if None in info:
            return jsonify({'errorMessage':'Please fill in values'}), 400
        else:
            cur.execute("INSERT INTO users (id, firebase_user_id, user_name, self_introduction, created_date, updated_date) VALUES (%s, %s,%s,%s,NOW(),NOW())", [user_uuid, firebase_user_id, user_name, None])
            cur.execute("INSERT INTO image(id, relation_id, image_url, created_date, updated_date) VALUES (%s, %s, %s, NOW(), NOW())", [image_uuid, user_uuid, user_image])
            client.commit()
            return jsonify({}), 201
            
    except:
        return jsonify({'errorMessage':'An unexpected error has occured'}),500

# ユーザー取得
@app.route('/user', methods=['GET'])
def u_detail():
    try:
        user_id = request.args.get('id')
        if user_id is None:
            return jsonify({'errorMessage' : 'Please fill in the value'}), 400

        cur.execute(f"SELECT users.id, user_name, image_url, to_char(users.created_date, 'YYYY-MM-DD HH24:MI:SS'), to_char(users.updated_date, 'YYYY-MM-DD HH24:MI:SS') \
                                FROM users \
                                JOIN image ON users.id = image.relation_id \
                                WHERE users.id = '{user_id}' ")
        user = cur.fetchall()

        if len(user) == 0:
            return jsonify({}),404
        else:
            user_id = user[0][0]
            user_name = user[0][1]
            user_image = user[0][2]
            created_date = user[0][3]
            updated_date = user[0][4]
            results = {'user_id': user_id, 'user_name': user_name, 'user_image': user_image, 'created_date': created_date, 'updated_date': updated_date}
            return jsonify(results), 200

    except:
        return jsonify({'Error':'An unexpected error has occured'}),500

# ユーザー更新
@app.route('/user', methods=['PUT'])
def u_update():
    try:
        data = request.get_json()
        user_id = data['user_id']
        user_name = data['user_name']
        user_image = data['user_image']
        info =[user_id, user_name, user_image]
        info = list(map(to_True_or_false, info))

        if None in info:
            return jsonify({'errorMessage': 'Please fill in values'}), 400
        
        cur.execute(f"SELECT id FROM users WHERE id = '{user_id}' ")
        user = cur.fetchall()

        if len(user) == 0:
            return jsonify({}), 404

        else:
            cur.execute(f"UPDATE users SET user_name ='{user_name}' WHERE id = '{user_id}' ")
            cur.execute(f"UPDATE image SET image_url = '{user_image}'  WHERE relation_id = '{user_id}' ")
            client.commit()
            return jsonify({}), 200

    except:
        return jsonify({'Error':'An unexpected error has occured'}),500

# ユーザー削除
@app.route('/user', methods=['DELETE'])
def u_delete():
    try:
        user_id = request.args.get('id')
        if user_id == None:
            return jsonify({'errorMessage': 'Please fill in the value'})
        
        cur.execute(f"SELECT FROM users WHERE id = '{user_id}' ")
        user = cur.fetchall()
        if len(user) == 0:
            return jsonify({}), 404
        else:
            cur.execute(f"DELETE FROM users WHERE id = '{user_id}' ")
            cur.execute(f"DELETE FROM image WHERE relation_id = '{user_id}' ")
            # cur.execute(f"DELETE FROM answers WHERE user_id = '{user_id}' ")
            client.commit()
            return jsonify({}), 200
    except:
        return jsonify({'Error':'An unexpected error has occured'}),500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    app.run()





