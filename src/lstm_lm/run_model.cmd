Executable      = job5005.sh
Universe        = vanilla
copy_to_spool   = False
getenv          = True
coresize        = 0
request_memory  = 4000
request_cpus    = 1
request_gpus    = 1
+GPUJob 	= "true"
nice_user 	= True
should_transfer_files	= YES
when_to_transfer_output = ON_EXIT
transfer_input_files = /homes/coman8/lm_examples/exp1
notification    = Complete
log             = ./log.$(Cluster)
Output          = ./out.$(Cluster)
Error           = ./err.$(Cluster)
Queue

