# HW-08 Vyncen Lara

## Configuration

Analisis of project of course 

### Start SonarQube
```bash
docker-compose up -d
```

open:  http://localhost:9000

## Results Test

### Frontend

#### Dashboard 
![Frontend Dashboard](./docs/F1.png)

#### Vulnerabilities
![Frontend Security](./docs/F2.png)
![Frontend Security](./docs/F2.png)
![Frontend Security](./docs/F3.png)
![Frontend Security](./docs/F4.png)


### Backend

#### Dashboard 
![Backend Dashboard](./docs/B1.png)

#### Vulnerabilities
![Backend Security](./docs/B2.png)
![Backend Security](./docs/B2.png)
![Backend Security](./docs/B3.png)
![Backend Security](./docs/B4.png)
![Backend Security](./docs/B5.png)

### Stop SonarQube
```bash
docker-compose down
```
### Re-escan proyect
```bash
cd frontend && sonar-scanner -Dsonar.host.url=http://localhost:9000 -Dsonar.login=sqp_b48ea5afb905824dfb53ba27ec179f1e64babbf7
cd ../backend && sonar-scanner -Dsonar.host.url=http://localhost:9000 -Dsonar.login=sqp_8b06aa56beee08be4533bd3858fab263367d9c57
```
### Look logs
```bash
docker-compose logs -f sonarqube
```