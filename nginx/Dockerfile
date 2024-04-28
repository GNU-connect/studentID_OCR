FROM nginx

# 기존 설정파일 삭제
RUN rm /etc/nginx/conf.d/default.conf
# 수정한 설정파일을 복사
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
 
# nginx 기동
CMD ["nginx", "-g", "daemon off;"]