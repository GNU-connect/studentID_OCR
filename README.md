## 개발 환경 설정

1. 도커 설치 (https://docs.docker.com/get-docker/)
2. 도커 이미지 빌드 (docker build -t connect-gnu-python .)
3. 프로젝트 루트 위치에 .env 파일 생성 후 노션에 있는 환경변수 값 입력하기
4. 도커 컨테이너 실행 (docker compose up backend_flask_server)
5. 브라우저에서 http://localhost:5000 접속
