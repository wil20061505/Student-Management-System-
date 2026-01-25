# Student-Management-System-
unzip Student-Management-System.zip
cd Student-Management-System-
docker build -t student-management -f Docker/Dockerfile .
docker run -it --rm student-management
