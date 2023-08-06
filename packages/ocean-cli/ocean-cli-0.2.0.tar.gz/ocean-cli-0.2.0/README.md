# Ocean CLI

## Initial development setup
For linux/mac
```
$ ./boot.sh
$ source venv/bin/activate
```
For windows
```
> ./boot.bat
> venv\Scripts\activate.bat
```

## Install
```
pip install dist/ocean-cli-0.0.1.tar.gz
```

## Usage
### 0. initialize
```
$ ocean init
```

### 1. login
```
$ ocean login <email> <password>
```

### 2. config
```
$ ocean config set --url <ocean backend url>
```

### 3. job submit
usage
```
$ ocean job submit <name> --command [COMMAND [COMMAND ...]] [--image IMAGE] [--cpu CPU] [--memory MEMORY] [--gpu GPU] [--gpu_type GPU_TYPE] [--volume VOLUME] [--logs] [--debug]
```

simple submit
```
$ ocean job submit test --cmd bash /root/volume/test.sh --volume vol-kairos9603-1 
```

change image
```
$ ocean job submit test --cmd bash /root/volume/test.sh --volume vol-kairos9603-1 --image mlvclab/pytorch:1.6.0-cuda10.1-cudnn7-devel
```

designate server spec
```
$ ocean job submit test --cmd bash /root/volume/test.sh --volume vol-kairos9603-1 --cpu 12 --memory 64 --gpu 2 --gpu_type nvidia-rtx-3090
```

submit and show logs
```
$ ocean job submit test --cmd bash /root/volume/test.sh --volume vol-kairos9603-1 -l
```

submit and show logs and delete completed job(debug mode)
```
$ ocean job submit test --cmd bash /root/volume/test.sh --volume vol-kairos9603-1 -l -d
```

upload local data to servers
```
$ ocean data upload mydata --path ~/README.md
```

list uploaded data list
```
$ ocean data list
```

