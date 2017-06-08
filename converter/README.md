# MKV Converter

## Dependencies
All the necessary dependencies can be installed using the Ansible playbook.

## Running
Run the server by running 
```
python3 server.py
```
## Demo
A demo is running on
```
http://129.192.68.50:5000
```

## Video Files
The video files on [4samples.com](http://4ksamples.com/) are fairly big, so it is better to download files of variable size from [jell.yfish.us](http://jell.yfish.us/).

## Todo
- Converted files are currently not deleted, since we don't know when the user is finished downloading the files. We could implement a timer to delete old files or when a new user connects. 

### Sources
[Python Flask](http://flask.pocoo.org/)
[Flask Upload File](https://gist.github.com/dAnjou/2874714)