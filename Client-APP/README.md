# Facial-recognition-model
<p>
    <img src="https://img.shields.io/badge/Android-3DDC84?style=flat&logo=Android&logoColor=white"/>
    <img src="https://img.shields.io/badge/Kotlin-7F52FF?style=flat&logo=Kotlin&logoColor=white"/>
</p>

MQTT Client

## Description
 - MQTT 라이브러리를 사용해 안면 인식 모델이 보낸 메시지를 수신합니다.

## Environment
 - 안드로이드
 - Kotlin
 - MQTT 라이브러리

## Screenshot
- 연결, 사용자 인식, 외부인 인식
<p>
    <img src="../img/client_mqtt_connection.png">
    <img src="../img/client_mqtt_user_comming.png">
    <img src="../img/client_mqtt_outsider_comming.png">
</p>

## Working Process
1. 앱 실행.
2. 상단에 ip 주소와 포트번호를 설정하고 연결 버튼을 클릭합니다.
3. 바로 밑 "연결되었습니다."가 확인되면 메시지를 받을 수 있습니다.
4. 메시지는 list view로 수신 시 추가됩니다.