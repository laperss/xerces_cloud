# MKV Converter

## Dependencies
All the necessary dependencies can be installed using the Ansible playbook.

## Running
Run on the master VM
```
python3 master.py
```
Run workers on one or more vms
```
python3 worker.py
```
Run clients.py on local computer to generate traffic
```
python3 clients.py
```

## Video Files
The video files on [4samples.com](http://4ksamples.com/) are fairly big, so it is better to download files of variable size from [jell.yfish.us](http://jell.yfish.us/).

## Todo
- Converted files are currently not deleted, since we don't know when the user is finished downloading the files. We could implement a timer to delete old files or when a new user connects. 

### Sources
[Python Flask](http://flask.pocoo.org/)
[Flask Upload File](https://gist.github.com/dAnjou/2874714)
