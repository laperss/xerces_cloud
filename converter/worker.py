import zmq
import random
import sys
import time

VMID = 1
SUB_PORT = "5556"
PUB_PORT = "5557"
MASTER_IP = "192.168.50.14"

sub_context = zmq.Context()
sub_socket = sub_context.socket(zmq.SUB)
sub_socket.connect("tcp://" + MASTER_IP +":%s" % SUB_PORT)
sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")

pub_context = zmq.Context()
pub_socket = pub_context.socket(zmq.PUB)
sub_socket.bind("tcp://" + MASTER_IP +":%s" % PUB_PORT)

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
        id = int(message.split()[1])
        if id == VMID:
            # Convert video
            print("Converting video file")
            output_path = "output.avi"
            convert_video("/home/ubuntu/video.mkv", output_path)
            print("Done")
    else:
        taskid = int(message.split()[1])
        # Sleep a random duration before replying
        time.sleep(random.uniform(0, 1))
        # Send taskid and VMID back
        taskreply = "task " + str(taskid) + " vm " + str(VMID)
        print("sent: ", taskreply)
        pub_socket.send_string(taskreply)
