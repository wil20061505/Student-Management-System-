unzip Student-Management-System.zip
cd ProgAndTest_Group14
docker build -t student-management -f Docker/Dockerfile Student-Management-System-
docker run -it --rm student-management

