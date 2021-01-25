# fisearch_backend
・ペアプログラミング作品です。私pillow545がバックエンドを担当しています。
・まだ作りかけですが、バックエンドのみでの挙動は大体実装できています。
・微修正箇所や、別途製作中のフロント側と組み合わせた際のエラー修正が出来ていません。

# 使いかた

# 質問投稿
curl -XPOST http://localhost:5000/question -H 'Content-type: application/json' -d '{
    "user_id": "UserId",
    "text": "サンプル",
    "category": "mountainStream",
    "deadline_date": "2020-12-01",
    "image_list": [
        "サンプル１",
        "サンプル２",
        "サンプル３",
        "サンプル４"
    ]
}'

・レスポンスボディ
201（正常終了）→{"id": "questionId"}
400（パラメータ異常）→{"errorMessage": "Please fill in values"}
500（サーバーエラー）→{"errorMessage": "An unexpected error has occured"}



# 質問一覧取得

curl -XGET http://localhost:5000/question -H 'Content-type: application/json' 

・クエリパラメータ
limit: number
sort: DBカラム名(created_date)
orderby: asc or desc
offset: number
keyword: string
include_closed: boolean

・レスポンスボディ
201（正常終了例）→{
    data: [
        {
            "question_id": "questionId",
            "user_name": "userName",
            "user_image": "https://~~~",
            "text": "質問文",
            "is_closed": false,
            "created_date": "2020-11-14 11:10:18"
        },
        {
            "question_id": "questionId",
            "user_name": "userName",
            "user_image": "https://~~~",
            "text": "質問文",
            "is_closed": false,
            "created_date": "2020-11-14 11:10:18"
        },
        {
            "question_id": "questionId",
            "user_name": "userName",
            "user_image": "https://~~~",
            "text": "質問文",
            "is_closed": false,
            "created_date": "2020-11-14 11:10:18"
        }
    ]
}
400（パラメータ異常）→{"errorMessage": "Please fill in values"}
500（サーバーエラー）→{"errorMessage": "An unexpected error has occured"}


# 質問詳細取得
curl -XGET "http://localhost:5000/question?id=質問ID" -H 'Content-type: application/json' 
・クエリパラメータ（必須）
id: 質問のID

・レスポンスボディ
200（正常終了例）→{
    "question_id": "questionId",
    "user_id": "userA",
    "user_name": "userA",
    "user_image": "https://~~~",
    "category": "category",
    "text": "質問文",
    "image_list": [
        "https://~~~",
        "https://~~~",
    ],
    "answer_list": [
        {
            "answer_id": "answer1",
            "user_id": "userB",
            "user_name": "userB",
            "user_image" "https://~~~",
            "text": "回答文",
            "is_best_answer": true,
            "created_date": "2020-11-14 11:10:18"
        },
        {
            "answer_id": "answer1",
            "user_id": "userB"
            "user_name": "userB",
            "user_image" "https://~~~"
            "text": "回答文"
            "is_best_answer": false,
            "created_date": "2020-11-14 11:10:18"
        }
    ],
    "is_closed": false,
    "deadline_date": "2020-11-14 11:10:18",
    "created_date": "2020-11-14 11:10:18"
}

400（パラメータ異常）→{"errorMessage": "Please fill in values"}
500（サーバーエラー）→{"errorMessage": "An unexpected error has occured"}

# 質問削除
※質問だけでなく、該当質問に付いている回答の情報も削除されます

curl -XDELETE "http://localhost:5000/question?id=質問ID" -H 'Content-type: application/json' 
・クエリパラメータ（必須）
id: 質問のID

・レスポンスボディ
200→なし
400（パラメータ異常）→{"errorMessage": "Please fill in values"}
500（サーバーエラー）→{"errorMessage": "An unexpected error has occured"}







# 回答作成
curl -XPOST http://localhost:5000/answer -H 'Content-type: application/json' -d '
    {
        "user_id": "UserID",
        "question_id": "QuestionID",
        "image": "画像URL",
        "text": "回答本文"
    }'

・レスポンスボディ
201→なし（質問詳細に飛ぶ予定）
400（パラメータ異常）→{"errorMessage": "Please fill in values"}
500（サーバーエラー）→{"errorMessage": "An unexpected error has occured"}




# 回答削除
curl -XDELETE "http://localhost:5000/answer?id=answerID" -H 'Content-type: application/json' 
・クエリパラメータ（必須）
id: 回答のID

・レスポンスボディ
201→なし（質問詳細に飛ぶ予定）
400（パラメータ異常）→{"errorMessage": "Please fill in values"}
404→{"errorMessage": "This question does not exist"}
500（サーバーエラー）→{"errorMessage": "An unexpected error has occured"}

# ベストアンサー決定
※回答のベストアンサーがTrueになるだけでなく、質問がクローズします。
curl -XPUT http://localhost:5000/answer/bestanswer -H 'Content-type: application/json' -d '
{
    "question_id": questionId
    "answer_id": answerId
}

・レスポンスボディ
201→なし（質問詳細に飛ぶ予定）
400（パラメータ異常）→{"errorMessage": "Please fill in values"}
500（サーバーエラー）→{"errorMessage": "An unexpected error has occured"}





201→なし（質問詳細に飛ぶ予定）
400（パラメータ異常）→{"errorMessage": "Please fill in values"}
404→{"errorMessage": "This question does not exist"}
500（サーバーエラー）→{"errorMessage": "An unexpected error has occured"}






# ユーザー登録
curl -XPOST http://localhost:5000/user -H 'Content-type: application/json' -d '
{
    "user_id": "userId",
    "user_name": "userName",
    "user_image": "https://~~~"
}'

201→なし（ユーザー詳細に飛ぶ予定）
400（パラメータ異常）→{"errorMessage": "Please fill in values"}
404→{"errorMessage": "This question does not exist"}
500（サーバーエラー）→{"errorMessage": "An unexpected error has occured"}



# ユーザー取得
curl -XGET "http://localhost:5000/user?id=UserID" -H 'Content-type: application/json' 

・クエリパラメータ（必須）
　id: userId

200（正常終了例）→{
    "user_id": userId,
    "user_name": userName,
    "user_image": "https://~~~",
    "created_date": "",
    "updated_date": ""
}
400（パラメータ異常）→{"errorMessage": "Please fill in values"}
500（サーバーエラー）→{"errorMessage": "An unexpected error has occured"}


# ユーザー更新
※user_name　と　user_image　を変更できる
curl -XPUT http://localhost:5000/user -H 'Content-type: application/json' -d '
{
    "user_id": "userId",
    "user_name": "userName",
    "user_image": "https://~~~"
}

201→なし（ユーザー詳細に飛ぶ予定）
400（パラメータ異常）→{"errorMessage": "Please fill in values"}
500（サーバーエラー）→{"errorMessage": "An unexpected error has occured"}


# ユーザー削除
curl -XDELETE "http://localhost:5000/user?id=UseID" -H 'Content-type: application/json' 

200→なし（質問詳細に飛ぶ予定）
400（パラメータ異常）→{"errorMessage": "Please fill in values"}
500（サーバーエラー）→{"errorMessage": "An unexpected error has occured"}
