# Install filebeat
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.11.1-amd64.deb
sudo dpkg -i filebeat-8.11.1-amd64.deb

# Edit `.env`

# Run filebeat
filebeat -e -c /path/to/filebeat.yml

# Run test consumer to check
python3 test/consumer.py