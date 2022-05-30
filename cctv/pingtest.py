# import requests
# # ref https://www.nylas.com/blog/use-python-requests-module-rest-apis/
# url = 'https://postman-echo.com/post'
# myobj = {'somekey': 'somevalue'}
# response = requests.post(url, data = myobj)
# if (response.status_code == 200):
#     print("The request was a success!")
#     print(response.json())
#     # Code here will only run if the request is successful
# elif (response.status_code == 404):
#     print("Result not found!")
#     # Code here will react to failed 

prediction = [[0.02661144, 0.96859276, 0.00479579]]
prediction = prediction[0]
classList = ['A', 'B', 'C']
predictedClass = max(prediction)
predictedClass = classList[prediction.index(predictedClass)]
print(predictedClass)