### 개발 환경 설정

1. 도커 설치 (https://docs.docker.com/get-docker/)
2. 도커 이미지 빌드 (docker build -t connect-gnu-python .)
3. 프로젝트 루트 위치에 .env 파일 생성 후 SUPABASE_URL, SUPABASE_KEY 값 입력하기
4. 도커 컨테이너 실행 (docker run -d -p 5000:5000 connect-gnu-python)
5. 브라우저에서 http://localhost:5000 접속

test
