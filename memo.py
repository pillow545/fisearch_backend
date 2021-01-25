201→なし（質問詳細に飛ぶ予定）
400（パラメータ異常）→{"errorMessage": "Please fill in values"}
500（サーバーエラー）→{"errorMessage": "An unexpected error has occured"}

curl -XDELETE "http://localhost:5000/question?id=84070b65-09ed-4dc2-b7ca-3b257dd37e16" -H 'Content-type: application/json' 

curl -XDELETE "http://localhost:5000/answer?id=02bdd694-a0eb-4cc8-8df6-1b11d4a021e0" -H 'Content-type: application/json' 


curl -XPUT http://localhost:5000/answer/bestanswer -H 'Content-type: application/json' -d '
{
    "question_id": "63191374-07dd-4c1b-bd22-0a8eb8448ab7",
    "answer_id": "3104623c-a238-46ba-aebf-414d4ed11f9c"
}'  


curl -XGET' http://localhost:5000/user?id=7234572e-251c-4660-a866-1db6988936dc -H' 'Content-type: application/json' 


curl -XPOST http://localhost:5000/user -H 'Content-type: application/json' -d '
{
    "user_id": "userId",
    "user_name": "userName",
    "user_image": "https://~~~"
}'

curl -XPOST http://localhost:5000/question -H 'Content-type: application/json' -d '{
    "user_id": "78c27b2f-2da4-4db9-a5bc-227ed77277ef",
    "text": "質問サンプル",
    "category": "mountainStream",
    "deadline_date": "2020-12-01",
    "image_list": [
        "質問画像１",
        "質問画像２",
        "質問画像３",
        "質問画像４"
    ]
}'




