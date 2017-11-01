import zmq, random, sys, time, shlex, socket
from subprocess import DEVNULL, STDOUT, call

MASTER_IP = "192.168.50.14"
WORKER_IP = get_ip_address() 

# Set up zeroMQ
SUB_PORT = "5556"
PUB_PORT = "5557"
sub_context = zmq.Context()
sub_socket = sub_context.socket(zmq.SUB)
sub_socket.connect("tcp://" + MASTER_IP +":%s" % SUB_PORT)
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")
pub_context = zmq.Context()
pub_socket = pub_context.socket(zmq.PUSH)
pub_socket.connect("tcp://" + MASTER_IP +":%s" % PUB_PORT)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def convert_video(source, dest):
    cmd = """mencoder %s -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=3000
             -oac copy -o %s""" % (source, dest)
    print("Converting video file")
    call(shlex.split(cmd), stdout=DEVNULL, stderr=STDOUT)

while True:
    # Wait for published message
    message = sub_socket.recv()
    print("recv: ", message.decode("utf-8"))
    if "vm" in str(message):
        ip = message.split()[1].decode("utf-8")
        input_path = message.split()[3].decode("utf-8")
        if ip == WORKER_IP:
            # Wait until file is transfered
            time.sleep(5)
            # Convert video
            print("Converting video file")
            output_path = "output.avi"
            convert_video("/home/ubuntu/" + input_path, output_path)
            print("Done")
            # Transfer video file
    else:
        taskid = int(message.split()[1])
        # Sleep a random duration before replying
        time.sleep(random.uniform(0, 1))
        # Send taskid and IP back
        taskreply = "task " + str(taskid) + " vm " + WORKER_IP
        print("sent: ", taskreply)
        pub_socket.send_string(taskreply)
